import { create } from "zustand";

export type JointVec = [number, number, number, number, number, number];

// Joint limits in radians, matching public/ar3.urdf.
export const JOINT_LIMITS: ReadonlyArray<readonly [number, number]> = [
  [-2.97, 2.97],
  [-2.25, 2.25],
  [-2.5, 2.5],
  [-2.88, 2.88],
  [-1.83, 1.83],
  [-2.7, 2.7],
] as const;

export interface IkStatus {
  residual: number;     // distance in meters from requested TCP
  ok: boolean;
  clamped: boolean;     // hit a joint limit
  error?: string;
}

interface AppState {
  q: JointVec;
  setJoint: (i: number, v: number) => void;
  setAllJoints: (q: JointVec) => void;
  home: () => void;

  ik: IkStatus | null;
  setIkStatus: (s: IkStatus | null) => void;
}

export const useStore = create<AppState>((set) => ({
  q: [0, 0, 0, 0, 0, 0],
  setJoint: (i, v) =>
    set((state) => {
      const q = [...state.q] as JointVec;
      q[i] = v;
      return { q };
    }),
  setAllJoints: (q) => set({ q }),
  home: () => set({ q: [0, 0, 0, 0, 0, 0], ik: null }),

  ik: null,
  setIkStatus: (s) => set({ ik: s }),
}));
