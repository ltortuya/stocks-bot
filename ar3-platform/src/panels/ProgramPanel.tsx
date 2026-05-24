import { useState } from "react";
import { useStore } from "../state/store";
import { jumpTo, playProgram, stopProgram } from "../playback/player";

const RAD2DEG = 180 / Math.PI;

export function ProgramPanel() {
  const q = useStore((s) => s.q);
  const program = useStore((s) => s.program);
  const playback = useStore((s) => s.playback);
  const defaultDuration = useStore((s) => s.defaultDuration);
  const setDefaultDuration = useStore((s) => s.setDefaultDuration);
  const addWaypoint = useStore((s) => s.addWaypoint);
  const deleteWaypoint = useStore((s) => s.deleteWaypoint);
  const moveWaypoint = useStore((s) => s.moveWaypoint);
  const updateWaypoint = useStore((s) => s.updateWaypoint);
  const clearProgram = useStore((s) => s.clearProgram);
  const loadProgram = useStore((s) => s.loadProgram);
  const undo = useStore((s) => s.undo);
  const redo = useStore((s) => s.redo);
  const undoLen = useStore((s) => s._undo.length);
  const redoLen = useStore((s) => s._redo.length);

  const [modal, setModal] = useState<"export" | "import" | null>(null);
  const [importText, setImportText] = useState("");

  const exportJson = JSON.stringify(
    { version: 1, waypoints: program.map(({ id: _id, ...rest }) => rest) },
    null,
    2
  );

  const onImport = () => {
    try {
      const parsed = JSON.parse(importText);
      const wps = parsed?.waypoints;
      if (!Array.isArray(wps)) throw new Error("expected { waypoints: [...] }");
      for (const w of wps) {
        if (!Array.isArray(w?.q) || w.q.length !== 6) {
          throw new Error("each waypoint needs a 6-element q array");
        }
      }
      loadProgram(wps);
      setModal(null);
      setImportText("");
    } catch (e) {
      alert("Import failed: " + (e instanceof Error ? e.message : String(e)));
    }
  };

  const copyExport = async () => {
    try {
      await navigator.clipboard.writeText(exportJson);
    } catch {
      // Clipboard may be unavailable in some webviews; user can still select.
    }
  };

  return (
    <div className="panel">
      <div className="section-head">
        <h2 className="section-h">Program</h2>
        <div className="undo-buttons">
          <button
            className="icon"
            onClick={undo}
            disabled={undoLen === 0}
            title="Undo (Ctrl+Z)"
          >
            ↶
          </button>
          <button
            className="icon"
            onClick={redo}
            disabled={redoLen === 0}
            title="Redo (Ctrl+Shift+Z)"
          >
            ↷
          </button>
        </div>
      </div>

      <button className="primary" onClick={() => addWaypoint(q)}>
        + Record current pose
      </button>

      {program.length === 0 && (
        <p className="hint">
          No waypoints yet. Pose the arm with the sliders or by dragging the
          TCP, then click record.
        </p>
      )}

      <div className="program-list">
        {program.map((wp, i) => {
          const active = playback.playing && i === playback.index;
          return (
            <div key={wp.id} className={`wp ${active ? "wp-active" : ""}`}>
              <div className="wp-row">
                <span className="wp-idx">{i + 1}</span>
                <input
                  className="wp-name"
                  placeholder={`waypoint ${i + 1}`}
                  value={wp.name ?? ""}
                  onChange={(e) =>
                    updateWaypoint(wp.id, { name: e.target.value })
                  }
                />
                <button
                  className="icon"
                  title="Jump arm to this pose (animated)"
                  onClick={() => jumpTo(wp.q, Math.min(wp.duration, 0.8))}
                >
                  →
                </button>
                <button
                  className="icon"
                  title="Move up"
                  onClick={() => moveWaypoint(wp.id, -1)}
                  disabled={i === 0}
                >
                  ↑
                </button>
                <button
                  className="icon"
                  title="Move down"
                  onClick={() => moveWaypoint(wp.id, 1)}
                  disabled={i === program.length - 1}
                >
                  ↓
                </button>
                <button
                  className="icon danger"
                  title="Delete"
                  onClick={() => deleteWaypoint(wp.id)}
                >
                  ×
                </button>
              </div>
              <div className="wp-meta">
                <span className="wp-q">
                  {wp.q.map((v) => `${(v * RAD2DEG).toFixed(0)}°`).join(" / ")}
                </span>
                <span className="wp-dur">
                  <input
                    type="number"
                    min="0.1"
                    step="0.1"
                    value={wp.duration}
                    onChange={(e) =>
                      updateWaypoint(wp.id, {
                        duration: parseFloat(e.target.value) || 1,
                      })
                    }
                  />
                  s
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="default-dur">
        <label>New waypoint duration</label>
        <input
          type="number"
          min="0.1"
          step="0.1"
          value={defaultDuration}
          onChange={(e) => setDefaultDuration(parseFloat(e.target.value) || 1)}
        />
        <span>s</span>
      </div>

      <div className="playback-controls">
        {playback.playing ? (
          <button className="play stop" onClick={stopProgram}>
            ■ Stop
          </button>
        ) : (
          <button
            className="play"
            onClick={playProgram}
            disabled={program.length === 0}
          >
            ▶ Play
          </button>
        )}
      </div>

      <div className="program-io">
        <button
          onClick={() => setModal("export")}
          disabled={program.length === 0}
        >
          Export
        </button>
        <button onClick={() => setModal("import")}>Import</button>
        <button
          onClick={() => {
            if (confirm("Delete all waypoints?")) clearProgram();
          }}
          disabled={program.length === 0}
        >
          Clear
        </button>
      </div>

      {modal === "export" && (
        <div className="modal-backdrop" onClick={() => setModal(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Export program</h3>
            <p className="hint">
              Copy this JSON to save your program somewhere. Paste it back via
              Import later.
            </p>
            <textarea readOnly value={exportJson} />
            <div className="modal-actions">
              <button onClick={copyExport}>Copy to clipboard</button>
              <button onClick={() => setModal(null)}>Close</button>
            </div>
          </div>
        </div>
      )}

      {modal === "import" && (
        <div className="modal-backdrop" onClick={() => setModal(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Import program</h3>
            <p className="hint">
              Paste a previously exported program JSON. This replaces the
              current program.
            </p>
            <textarea
              value={importText}
              onChange={(e) => setImportText(e.target.value)}
              placeholder='{ "version": 1, "waypoints": [...] }'
            />
            <div className="modal-actions">
              <button onClick={onImport} disabled={!importText.trim()}>
                Import
              </button>
              <button onClick={() => setModal(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
