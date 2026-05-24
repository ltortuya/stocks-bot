import { invoke } from "@tauri-apps/api/core";
import type { JointVec } from "../state/store";

export type Pose = { xyz: [number, number, number]; rpy: [number, number, number] };

export type IkResult = {
  q: JointVec;
  ok: boolean;
  residual: number;
  clamped: boolean;
};

async function call<T>(method: string, params: Record<string, unknown>): Promise<T> {
  return invoke<T>("sidecar_call", { method, params });
}

export const kin = {
  fk: (q: JointVec) => call<{ pose: Pose }>("fk", { q }),
  ik: (xyz: [number, number, number], qSeed?: JointVec) =>
    call<IkResult>("ik", { pose: { xyz }, q_seed: qSeed }),
  jointLimits: () => call<{ min: number[]; max: number[] }>("joint_limits", {}),
};
