import { JOINT_LIMITS, useStore } from "../state/store";

const RAD2DEG = 180 / Math.PI;

export function JointPanel() {
  const q = useStore((s) => s.q);
  const setJoint = useStore((s) => s.setJoint);
  const home = useStore((s) => s.home);
  const ik = useStore((s) => s.ik);

  return (
    <div className="panel">
      <h2>Joints</h2>
      {q.map((value, i) => {
        const [min, max] = JOINT_LIMITS[i];
        return (
          <div className="joint-row" key={i}>
            <label>J{i + 1}</label>
            <input
              type="range"
              min={min}
              max={max}
              step={0.005}
              value={value}
              onChange={(e) => setJoint(i, parseFloat(e.target.value))}
            />
            <span>{(value * RAD2DEG).toFixed(1)}°</span>
          </div>
        );
      })}
      <button onClick={home}>Home</button>

      <h2 className="section-h">TCP control</h2>
      <p className="hint">
        Drag the colored arrows at the tool tip to move the arm. Red = X,
        green = Y, blue = Z.
      </p>
      {ik && (
        <div className={`ik-status ${ik.error ? "err" : ik.ok ? "ok" : "warn"}`}>
          {ik.error ? (
            <>
              <strong>error:</strong> {ik.error}
            </>
          ) : (
            <>
              <strong>{ik.ok ? "ok" : "approx"}</strong>{" "}
              residual {(ik.residual * 1000).toFixed(1)} mm
              {ik.clamped && " · joint clamped"}
            </>
          )}
        </div>
      )}
    </div>
  );
}
