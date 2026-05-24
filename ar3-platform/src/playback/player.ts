import { JointVec, useStore } from "../state/store";

// S-curve easing: zero velocity at both endpoints, smooth all the way through.
function smoothStep(t: number): number {
  const x = Math.max(0, Math.min(1, t));
  return x * x * (3 - 2 * x);
}

let raf = 0;
let segmentStartMs = 0;
let segmentStartQ: JointVec = [0, 0, 0, 0, 0, 0];

export function playProgram(): void {
  const state = useStore.getState();
  if (state.playback.playing || state.program.length === 0) return;

  segmentStartQ = [...state.q] as JointVec;
  segmentStartMs = performance.now();
  state.setPlaybackIndex(0);
  state.setPlaying(true);
  raf = requestAnimationFrame(tick);
}

export function stopProgram(): void {
  if (raf) cancelAnimationFrame(raf);
  raf = 0;
  useStore.getState().setPlaying(false);
}

function tick(now: number): void {
  const state = useStore.getState();
  if (!state.playback.playing) {
    raf = 0;
    return;
  }

  const wp = state.program[state.playback.index];
  if (!wp) {
    stopProgram();
    return;
  }

  const elapsed = (now - segmentStartMs) / 1000;
  const dur = Math.max(0.05, wp.duration);
  const u = smoothStep(elapsed / dur);

  if (elapsed >= dur) {
    // Snap to waypoint and advance.
    state.setAllJoints(wp.q);
    const next = state.playback.index + 1;
    if (next >= state.program.length) {
      stopProgram();
      return;
    }
    segmentStartQ = wp.q;
    segmentStartMs = now;
    state.setPlaybackIndex(next);
  } else {
    const q: JointVec = [0, 0, 0, 0, 0, 0];
    for (let i = 0; i < 6; i++) {
      q[i] = segmentStartQ[i] + (wp.q[i] - segmentStartQ[i]) * u;
    }
    state.setAllJoints(q);
  }

  raf = requestAnimationFrame(tick);
}
