//! Sample a parsed Toolpath into a sequence of (TCP target, time-from-start)
//! points for simulation. Long moves are subdivided so arcs and rapids look
//! smooth in playback; very short segments collapse to one sample.

import type { Toolpath, Vec3 } from "./parser";

const STEP_MM = 5;
const ASSUMED_RAPID_MM_PER_MIN = 5000;

export interface SamplePoint {
  urdf: [number, number, number]; // TCP position in URDF metres
  t: number;                       // seconds from program start
  type: "rapid" | "feed";
  spindleOn: boolean;
}

/**
 * Convert workpiece (mm) → URDF (m) given the workpiece origin in URDF m
 * and the tool length offset. The flange (link_6 origin) sits `toolLength`
 * above where the G-code says the tip should go — we assume the spindle
 * points along workpiece -Z, which is the typical CNC mount.
 */
function toUrdf(
  pt_mm: Vec3,
  origin_m: readonly [number, number, number],
  toolLength_mm: number
): [number, number, number] {
  return [
    pt_mm[0] / 1000 + origin_m[0],
    pt_mm[1] / 1000 + origin_m[1],
    (pt_mm[2] + toolLength_mm) / 1000 + origin_m[2],
  ];
}

export function sampleToolpath(
  toolpath: Toolpath,
  workpieceOrigin: readonly [number, number, number],
  toolLength_mm: number
): SamplePoint[] {
  const samples: SamplePoint[] = [];
  let t = 0;

  if (toolpath.moves.length > 0) {
    const first = toolpath.moves[0];
    samples.push({
      urdf: toUrdf(first.from, workpieceOrigin, toolLength_mm),
      t,
      type: first.type,
      spindleOn: first.spindleOn,
    });
  }

  for (const move of toolpath.moves) {
    const dx = move.to[0] - move.from[0];
    const dy = move.to[1] - move.from[1];
    const dz = move.to[2] - move.from[2];
    const len_mm = Math.sqrt(dx * dx + dy * dy + dz * dz);
    if (len_mm === 0) continue;

    const speed_mm_per_min =
      move.type === "rapid"
        ? ASSUMED_RAPID_MM_PER_MIN
        : Math.max(1, move.feed_mm_per_min);
    const move_sec = (len_mm / speed_mm_per_min) * 60;

    const nSteps = Math.max(1, Math.ceil(len_mm / STEP_MM));
    for (let i = 1; i <= nSteps; i++) {
      const f = i / nSteps;
      const pt: Vec3 = [
        move.from[0] + dx * f,
        move.from[1] + dy * f,
        move.from[2] + dz * f,
      ];
      samples.push({
        urdf: toUrdf(pt, workpieceOrigin, toolLength_mm),
        t: t + move_sec * f,
        type: move.type,
        spindleOn: move.spindleOn,
      });
    }
    t += move_sec;
  }

  return samples;
}
