import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { Viewer } from "./scene/Viewer";
import { JointPanel } from "./panels/JointPanel";
import { ProgramPanel } from "./panels/ProgramPanel";

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

  return (
    <div className="app">
      <header>
        <div>
          <h1>AR3 Platform</h1>
          <p className="subtitle">Milestone 3 — programs</p>
        </div>
        <span className={`status status-${status.kind}`}>
          {status.kind === "loading" && "connecting…"}
          {status.kind === "ok" && `sidecar v${status.version}`}
          {status.kind === "error" && `sidecar error`}
        </span>
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
