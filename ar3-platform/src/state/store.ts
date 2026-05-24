import { create } from "zustand";
import { persist } from "zustand/middleware";

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
  residual: number;
  ok: boolean;
  clamped: boolean;
  error?: string;
}

export interface Waypoint {
  id: string;
  q: JointVec;
  duration: number;  // seconds to reach from the previous waypoint
  name?: string;
}

export interface PlaybackState {
  playing: boolean;
  index: number;     // waypoint currently being interpolated TO
}

interface AppState {
  // ---- live joint state ----
  q: JointVec;
  setJoint: (i: number, v: number) => void;
  setAllJoints: (q: JointVec) => void;
  home: () => void;

  // ---- IK status (not persisted) ----
  ik: IkStatus | null;
  setIkStatus: (s: IkStatus | null) => void;

  // ---- program (persisted) ----
  program: Waypoint[];
  defaultDuration: number;
  setDefaultDuration: (d: number) => void;
  addWaypoint: (q: JointVec) => void;
  deleteWaypoint: (id: string) => void;
  moveWaypoint: (id: string, direction: -1 | 1) => void;
  updateWaypoint: (id: string, patch: Partial<Omit<Waypoint, "id">>) => void;
  clearProgram: () => void;
  loadProgram: (waypoints: Omit<Waypoint, "id">[]) => void;

  // ---- playback ----
  playback: PlaybackState;
  setPlaying: (playing: boolean) => void;
  setPlaybackIndex: (index: number) => void;
}

const newId = () =>
  typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : Math.random().toString(36).slice(2);

export const useStore = create<AppState>()(
  persist(
    (set) => ({
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

      program: [],
      defaultDuration: 1.0,
      setDefaultDuration: (d) => set({ defaultDuration: d }),
      addWaypoint: (q) =>
        set((state) => ({
          program: [
            ...state.program,
            { id: newId(), q, duration: state.defaultDuration },
          ],
        })),
      deleteWaypoint: (id) =>
        set((state) => ({ program: state.program.filter((w) => w.id !== id) })),
      moveWaypoint: (id, direction) =>
        set((state) => {
          const i = state.program.findIndex((w) => w.id === id);
          if (i < 0) return state;
          const j = i + direction;
          if (j < 0 || j >= state.program.length) return state;
          const program = [...state.program];
          [program[i], program[j]] = [program[j], program[i]];
          return { program };
        }),
      updateWaypoint: (id, patch) =>
        set((state) => ({
          program: state.program.map((w) =>
            w.id === id ? { ...w, ...patch } : w
          ),
        })),
      clearProgram: () => set({ program: [] }),
      loadProgram: (waypoints) =>
        set({
          program: waypoints.map((w) => ({
            id: newId(),
            q: w.q,
            duration: typeof w.duration === "number" ? w.duration : 1.0,
            name: w.name,
          })),
        }),

      playback: { playing: false, index: 0 },
      setPlaying: (playing) =>
        set((state) => ({ playback: { ...state.playback, playing } })),
      setPlaybackIndex: (index) =>
        set((state) => ({ playback: { ...state.playback, index } })),
    }),
    {
      name: "ar3-platform",
      // Only persist program-related data. Live joint state and IK status
      // are runtime-only.
      partialize: (state) => ({
        program: state.program,
        defaultDuration: state.defaultDuration,
      }),
    }
  )
);
