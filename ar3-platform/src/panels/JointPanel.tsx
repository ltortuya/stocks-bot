import { JOINT_LIMITS, useStore } from "../state/store";

const RAD2DEG = 180 / Math.PI;

export function JointPanel() {
  const q = useStore((s) => s.q);
  const setJoint = useStore((s) => s.setJoint);
  const home = useStore((s) => s.home);

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
    </div>
  );
}
