import { useState } from "react";
import { useStore } from "../state/store";

const EXAMPLE_PLACEHOLDER = `; Example: 100mm square pocket pass
G21
G90
G0 Z5
G0 X-50 Y-50
M3 S12000
G1 Z-1 F300
G1 X50 Y-50 F800
G1 X50 Y50
G1 X-50 Y50
G1 X-50 Y-50
G0 Z5
M5
M30`;

function formatLen(mm: number): string {
  return mm >= 1000 ? `${(mm / 1000).toFixed(2)} m` : `${mm.toFixed(0)} mm`;
}

function formatTime(s: number): string {
  if (!isFinite(s) || s <= 0) return "—";
  if (s < 60) return `${Math.round(s)} s`;
  const m = Math.floor(s / 60);
  const r = Math.round(s % 60);
  return r === 0 ? `${m} min` : `${m}m ${r}s`;
}

export function ToolpathPanel() {
  const toolpath = useStore((s) => s.toolpath);
  const loadToolpath = useStore((s) => s.loadToolpath);
  const clearToolpath = useStore((s) => s.clearToolpath);
  const workpieceOrigin = useStore((s) => s.workpieceOrigin);
  const setWorkpieceOrigin = useStore((s) => s.setWorkpieceOrigin);

  const [showImport, setShowImport] = useState(false);
  const [text, setText] = useState("");
  const [parseError, setParseError] = useState<string | null>(null);

  const setOriginAxis = (axis: 0 | 1 | 2, valueMm: number) => {
    const next = [...workpieceOrigin] as [number, number, number];
    next[axis] = valueMm / 1000;
    setWorkpieceOrigin(next);
  };

  const onLoad = () => {
    setParseError(null);
    try {
      loadToolpath(text);
      setShowImport(false);
      setText("");
    } catch (e) {
      setParseError(e instanceof Error ? e.message : String(e));
    }
  };

  return (
    <div className="panel">
      <h2 className="section-h">Toolpath</h2>

      {!toolpath && (
        <>
          <p className="hint">
            Paste G-code from your CAM tool (Fusion 360, FreeCAD Path,
            etc.) to overlay the toolpath in the workspace. Position is
            relative to the robot base for now — workpiece coordinates
            come in a later milestone.
          </p>
          <button
            className="primary"
            onClick={() => {
              setText("");
              setShowImport(true);
            }}
          >
            Load G-code
          </button>
        </>
      )}

      {toolpath && (
        <>
          <div className="wp-origin">
            <div className="row-label">Workpiece origin (mm in robot frame)</div>
            <div className="wp-origin-row">
              {(["X", "Y", "Z"] as const).map((axis, i) => (
                <label key={axis}>
                  <em>{axis}</em>
                  <input
                    type="number"
                    step="10"
                    value={Math.round(workpieceOrigin[i] * 1000)}
                    onChange={(e) =>
                      setOriginAxis(i as 0 | 1 | 2, parseFloat(e.target.value) || 0)
                    }
                  />
                </label>
              ))}
            </div>
          </div>

          <div className="tp-stats">
            <div className="row"><span>Moves</span><span>{toolpath.moves.length}</span></div>
            <div className="row"><span>Feed length</span><span>{formatLen(toolpath.feedLength_mm)}</span></div>
            <div className="row"><span>Rapid length</span><span>{formatLen(toolpath.rapidLength_mm)}</span></div>
            <div className="row">
              <span>Bounding box</span>
              <span>
                {(toolpath.bbox_mm.max[0] - toolpath.bbox_mm.min[0]).toFixed(0)} ×{" "}
                {(toolpath.bbox_mm.max[1] - toolpath.bbox_mm.min[1]).toFixed(0)} ×{" "}
                {(toolpath.bbox_mm.max[2] - toolpath.bbox_mm.min[2]).toFixed(0)} mm
              </span>
            </div>
            <div className="row"><span>Est. time</span><span>{formatTime(toolpath.estimatedTime_s)}</span></div>
          </div>

          {toolpath.warnings.length > 0 && (
            <div className="ik-status warn">
              {toolpath.warnings.length} warning
              {toolpath.warnings.length === 1 ? "" : "s"} — see browser console
            </div>
          )}

          <div className="tp-legend">
            <span><i className="sw sw-rapid" /> rapid</span>
            <span><i className="sw sw-feed" /> feed</span>
            <span><i className="sw sw-cut" /> cutting</span>
          </div>

          <div className="program-io">
            <button
              onClick={() => {
                setText("");
                setShowImport(true);
              }}
            >
              Replace
            </button>
            <button
              onClick={() => {
                if (confirm("Clear the toolpath?")) clearToolpath();
              }}
            >
              Clear
            </button>
          </div>
        </>
      )}

      {showImport && (
        <div className="modal-backdrop" onClick={() => setShowImport(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Load G-code</h3>
            <p className="hint">
              Paste a G-code program. Supports G0/G1/G2/G3, G20/G21,
              G90/G91, M3/M5. Comments using <code>;</code> or
              parentheses are ignored.
            </p>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={EXAMPLE_PLACEHOLDER}
            />
            {parseError && (
              <div className="ik-status err" style={{ marginTop: "0.5rem" }}>
                {parseError}
              </div>
            )}
            <div className="modal-actions">
              <button
                onClick={() => setText(EXAMPLE_PLACEHOLDER)}
              >
                Use example
              </button>
              <button onClick={onLoad} disabled={!text.trim()}>
                Load
              </button>
              <button onClick={() => setShowImport(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
