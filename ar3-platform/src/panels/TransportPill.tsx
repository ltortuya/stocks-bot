import { useEffect, useState } from "react";
import { transport, TransportStatus } from "../rpc/transport";
import { useStore } from "../state/store";

// Mirror commanded joint state to the transport. M4 just sends it to the
// SimTransport; M6+ this is what drives real motors. Throttle to ~50 Hz
// so dragging the IK gizmo doesn't flood the channel.
const SEND_INTERVAL_MS = 20;

export function TransportPill() {
  const [status, setStatus] = useState<TransportStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Poll status periodically so estop / spindle / connection changes from
  // anywhere stay visible.
  useEffect(() => {
    let alive = true;
    const refresh = () =>
      transport
        .status()
        .then((s) => alive && setStatus(s))
        .catch(() => alive && setStatus(null));

    refresh();
    const t = setInterval(refresh, 750);
    return () => {
      alive = false;
      clearInterval(t);
    };
  }, []);

  // Mirror live joint state to the transport.
  useEffect(() => {
    let lastSent = 0;
    let pending: number | null = null;
    let stopped = false;

    const sendIfNeeded = (q: ReturnType<typeof useStore.getState>["q"]) => {
      if (stopped) return;
      const now = performance.now();
      if (now - lastSent < SEND_INTERVAL_MS) {
        if (pending != null) return;
        pending = window.setTimeout(() => {
          pending = null;
          sendIfNeeded(useStore.getState().q);
        }, SEND_INTERVAL_MS - (now - lastSent));
        return;
      }
      lastSent = now;
      transport.sendJoints(q).catch((e) => setError(String(e)));
    };

    const unsub = useStore.subscribe((state) => sendIfNeeded(state.q));
    sendIfNeeded(useStore.getState().q);

    return () => {
      stopped = true;
      if (pending != null) clearTimeout(pending);
      unsub();
    };
  }, []);

  const toggle = async () => {
    setError(null);
    try {
      const s = status?.connected
        ? await transport.disconnect()
        : await transport.connect();
      setStatus(s);
    } catch (e) {
      setError(String(e));
    }
  };

  const estop = async () => {
    setError(null);
    try {
      setStatus(await transport.estop());
    } catch (e) {
      setError(String(e));
    }
  };

  const label = (() => {
    if (!status) return "transport ?";
    if (status.estopped) return "E-STOPPED";
    if (!status.connected) return "disconnected";
    return status.kind === "sim" ? "sim ✓" : status.kind;
  })();

  const variant = (() => {
    if (!status) return "loading";
    if (status.estopped) return "error";
    if (!status.connected) return "warn";
    return "ok";
  })();

  return (
    <div className="transport-pill-group">
      {error && (
        <span className="status status-error" title={error}>
          transport err
        </span>
      )}
      <button
        className={`status-btn status-${variant}`}
        onClick={toggle}
        title={
          status?.connected
            ? "Click to disconnect from sim transport"
            : "Click to connect to sim transport"
        }
      >
        {label}
      </button>
      <button
        className="status-btn estop"
        onClick={estop}
        disabled={!status?.connected || status?.estopped}
        title="Emergency stop"
      >
        E-STOP
      </button>
    </div>
  );
}
