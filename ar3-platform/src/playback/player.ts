import { JointVec, useStore } from "../state/store";

// S-curve easing: zero velocity at both endpoints, smooth all the way through.
function smoothStep(t: number): number {
  const x = Math.max(0, Math.min(1, t));
  return x * x * (3 - 2 * x);
}

// ---- program playback ----------------------------------------------------

let programRaf = 0;
let segmentStartMs = 0;
let segmentStartQ: JointVec = [0, 0, 0, 0, 0, 0];

export function playProgram(): void {
  const state = useStore.getState();
  if (state.playback.playing || state.program.length === 0) return;

  cancelAllAnimations();
  segmentStartQ = [...state.q] as JointVec;
  segmentStartMs = performance.now();
  state.setPlaybackIndex(0);
  state.setPlaying(true);
  programRaf = requestAnimationFrame(programTick);
}

export function stopProgram(): void {
  if (programRaf) cancelAnimationFrame(programRaf);
  programRaf = 0;
  useStore.getState().setPlaying(false);
}

function programTick(now: number): void {
  const state = useStore.getState();
  if (!state.playback.playing) {
    programRaf = 0;
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

  programRaf = requestAnimationFrame(programTick);
}

// ---- one-shot jump (smooth animated move to a target pose) ---------------

let jumpRaf = 0;
let jumpStartMs = 0;
let jumpStartQ: JointVec = [0, 0, 0, 0, 0, 0];
let jumpTargetQ: JointVec = [0, 0, 0, 0, 0, 0];
let jumpDuration = 0.5;

export function jumpTo(targetQ: JointVec, duration: number = 0.5): void {
  cancelAllAnimations();
  jumpStartQ = [...useStore.getState().q] as JointVec;
  jumpTargetQ = [...targetQ] as JointVec;
  jumpStartMs = performance.now();
  jumpDuration = Math.max(0.05, duration);
  jumpRaf = requestAnimationFrame(jumpTick);
}

function jumpTick(now: number): void {
  const elapsed = (now - jumpStartMs) / 1000;
  const u = smoothStep(elapsed / jumpDuration);

  if (elapsed >= jumpDuration) {
    useStore.getState().setAllJoints(jumpTargetQ);
    jumpRaf = 0;
    return;
  }

  const q: JointVec = [0, 0, 0, 0, 0, 0];
  for (let i = 0; i < 6; i++) {
    q[i] = jumpStartQ[i] + (jumpTargetQ[i] - jumpStartQ[i]) * u;
  }
  useStore.getState().setAllJoints(q);
  jumpRaf = requestAnimationFrame(jumpTick);
}

function cancelAllAnimations(): void {
  if (programRaf) {
    cancelAnimationFrame(programRaf);
    programRaf = 0;
    useStore.getState().setPlaying(false);
  }
  if (jumpRaf) {
    cancelAnimationFrame(jumpRaf);
    jumpRaf = 0;
  }
}

