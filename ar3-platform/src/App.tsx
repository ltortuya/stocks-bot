import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type Health = { ok: boolean; version: string };
type Status =
  | { kind: "loading" }
  | { kind: "ok"; health: Health }
  | { kind: "error"; message: string };

export default function App() {
  const [status, setStatus] = useState<Status>({ kind: "loading" });

  useEffect(() => {
    invoke<Health>("sidecar_health")
      .then((health) => setStatus({ kind: "ok", health }))
      .catch((err) => setStatus({ kind: "error", message: String(err) }));
  }, []);

  return (
    <div className="app">
      <header>
        <h1>AR3 Platform</h1>
        <p className="subtitle">Milestone 0 — scaffold</p>
      </header>

      <section className="card">
        <h2>Sidecar status</h2>
        {status.kind === "loading" && <p>Pinging Python sidecar…</p>}
        {status.kind === "ok" && (
          <p className="ok">
            ✓ Sidecar up — version <code>{status.health.version}</code>
          </p>
        )}
        {status.kind === "error" && (
          <p className="err">✗ {status.message}</p>
        )}
      </section>

      <footer>
        <span>Tauri + React + Three.js + Python · v0.0.1</span>
      </footer>
    </div>
  );
}
