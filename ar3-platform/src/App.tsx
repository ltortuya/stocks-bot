import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { Viewer } from "./scene/Viewer";
import { JointPanel } from "./panels/JointPanel";
import { ProgramPanel } from "./panels/ProgramPanel";
import { TransportPill } from "./panels/TransportPill";
import { useStore } from "./state/store";

type SidecarStatus =
  | { kind: "loading" }
  | { kind: "ok"; version: string }
  | { kind: "error"; message: string };

export default function App() {
  const [status, setStatus] = useState<SidecarStatus>({ kind: "loading" });

  useEffect(() => {
    invoke<{ ok: boolean; version: string }>("sidecar_health")
      .then((h) => setStatus({ kind: "ok", version: h.version }))
      .catch((err) => setStatus({ kind: "error", message: String(err) }));
  }, []);

  // Global keyboard shortcuts (undo / redo on the program).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return; // don't hijack editing
      const mod = e.ctrlKey || e.metaKey;
      if (!mod) return;
      if (e.key === "z" && !e.shiftKey) {
        e.preventDefault();
        useStore.getState().undo();
      } else if ((e.key === "z" && e.shiftKey) || e.key === "y") {
        e.preventDefault();
        useStore.getState().redo();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className="app">
      <header>
        <div>
          <h1>AR3 Platform</h1>
          <p className="subtitle">Milestone 5 — polish</p>
        </div>
        <div className="header-status">
          <span className={`status status-${status.kind}`}>
            {status.kind === "loading" && "connecting…"}
            {status.kind === "ok" && `sidecar v${status.version}`}
            {status.kind === "error" && `sidecar error`}
          </span>
          <TransportPill />
        </div>
      </header>

      <main>
        <Viewer />
        <aside>
          <JointPanel />
          <ProgramPanel />
        </aside>
      </main>
    </div>
  );
}
