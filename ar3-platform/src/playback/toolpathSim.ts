//! Compile a loaded toolpath into a joint trajectory via batch IK, then
//! play it back at a configurable speed. Compile happens once per
//! (toolpath × workpiece origin) and is cached in module scope; the user
//! can stop and replay without re-compiling.

import { JointVec, useStore } from "../state/store";
import { sampleToolpath } from "../gcode/sample";
import { kin } from "../rpc/kinematics";

interface TrajSample {
  t: number;          // seconds from start of simulation
  q: JointVec;
  ok: boolean;
}

let trajectory: TrajSample[] = [];
let totalDuration_s = 0;
let unreachableCount = 0;

let raf = 0;
let startMs = 0;
let cancelToken = 0;

const CHUNK_SIZE = 256;

export async function runToolpathSimulation(): Promise<void> {
  const state = useStore.getState();
  if (state.sim.status === "compiling" || state.sim.status === "playing") return;
  if (!state.toolpath) return;

  const token = ++cancelToken;
  state.setSimStatus("compiling");
  state.setSimProgress(0);

  try {
    const samples = sampleToolpath(
      state.toolpath,
      state.workpieceOrigin,
      state.tool.length_mm
    );
    if (samples.length === 0) {
      state.setSimStatus("idle");
      return;
    }

    trajectory = [];
    unreachableCount = 0;
    let seed: JointVec = state.q;

    for (let i = 0; i < samples.length; i += CHUNK_SIZE) {
      if (cancelToken !== token) return; // user pressed stop while compiling
      const chunk = samples.slice(i, i + CHUNK_SIZE);
      const points: [number, number, number][] = chunk.map((s) => s.urdf);
      const r = await kin.ikBatch(points, seed);
      for (let j = 0; j < chunk.length; j++) {
        const res = r.results[j];
        trajectory.push({ t: chunk[j].t, q: res.q as JointVec, ok: res.ok });
        if (!res.ok) unreachableCount++;
        seed = res.q as JointVec;
      }
      state.setSimProgress(Math.min(1, (i + chunk.length) / samples.length));
    }

    totalDuration_s = trajectory[trajectory.length - 1]?.t ?? 0;
    state.setSimReachability(unreachableCount, samples.length);

    if (cancelToken !== token) return;
    startMs = performance.now();
    state.setSimStatus("playing");
    state.setSimProgress(0);
    raf = requestAnimationFrame(tick);
  } catch (err) {
    console.error("[toolpathSim] compile failed:", err);
    if (cancelToken === token) {
      state.setSimStatus("error");
      state.setSimError(String(err));
    }
  }
}

export function stopToolpathSimulation(): void {
  cancelToken++;
  if (raf) cancelAnimationFrame(raf);
  raf = 0;
  const state = useStore.getState();
  state.setSimStatus("idle");
  state.setSimProgress(0);
}

function tick(now: number): void {
  const state = useStore.getState();
  if (state.sim.status !== "playing") {
    raf = 0;
    return;
  }
  if (trajectory.length === 0 || totalDuration_s === 0) {
    state.setSimStatus("idle");
    raf = 0;
    return;
  }

  const elapsed = ((now - startMs) / 1000) * state.sim.speed;
  if (elapsed >= totalDuration_s) {
    const last = trajectory[trajectory.length - 1];
    state.setAllJoints(last.q);
    state.setSimProgress(1);
    state.setSimStatus("idle");
    raf = 0;
    return;
  }

  // Binary search for the first sample with t > elapsed.
  let lo = 0;
  let hi = trajectory.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (trajectory[mid].t <= elapsed) lo = mid + 1;
    else hi = mid;
  }
  const idx = lo;

  if (idx === 0) {
    state.setAllJoints(trajectory[0].q);
  } else {
    const a = trajectory[idx - 1];
    const b = trajectory[idx];
    const dt = Math.max(1e-6, b.t - a.t);
    const f = (elapsed - a.t) / dt;
    const q: JointVec = [0, 0, 0, 0, 0, 0];
    for (let i = 0; i < 6; i++) q[i] = a.q[i] + (b.q[i] - a.q[i]) * f;
    state.setAllJoints(q);
  }

  state.setSimProgress(elapsed / totalDuration_s);
  raf = requestAnimationFrame(tick);
}
