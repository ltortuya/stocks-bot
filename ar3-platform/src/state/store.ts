import { create } from "zustand";
import { persist } from "zustand/middleware";
import { parseGcode, type Toolpath } from "../gcode/parser";

export type JointVec = [number, number, number, number, number, number];
export type Vec3 = [number, number, number];

// Joint limits in radians, matching public/ar3.urdf (community AR3 model
// from ongdexter/ar3_core, with our added <limit> elements).
export const JOINT_LIMITS: ReadonlyArray<readonly [number, number]> = [
  [-2.97, 2.97],
  [-1.75, 1.75],
  [-2.4, 2.4],
  [-2.88, 2.88],
  [-1.83, 1.83],
  [-2.71, 2.71],
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
  duration: number;
  name?: string;
}

export interface PlaybackState {
  playing: boolean;
  index: number;
}

export interface ViewerSettings {
  showGrid: boolean;
  showWorkspace: boolean;
  showToolpath: boolean;
  resetViewTick: number; // increment to request a camera reset
}

const UNDO_LIMIT = 50;

interface AppState {
  // ---- live joint state ----
  q: JointVec;
  setJoint: (i: number, v: number) => void;
  setAllJoints: (q: JointVec) => void;
  home: () => void;

  // ---- TCP (URDF-local xyz, updated by Viewer after every FK) ----
  tcp: Vec3 | null;
  setTcp: (tcp: Vec3 | null) => void;

  // ---- IK status ----
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

  // ---- undo / redo ----
  _undo: Waypoint[][];
  _redo: Waypoint[][];
  undo: () => void;
  redo: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;

  // ---- playback ----
  playback: PlaybackState;
  setPlaying: (playing: boolean) => void;
  setPlaybackIndex: (index: number) => void;

  // ---- viewer ----
  viewer: ViewerSettings;
  toggleGrid: () => void;
  toggleWorkspace: () => void;
  toggleToolpath: () => void;
  requestResetView: () => void;

  // ---- toolpath (runtime-only; the source gcode is persisted, see below) ----
  toolpath: Toolpath | null;
  toolpathSource: string | null;
  loadToolpath: (gcode: string) => Toolpath;
  clearToolpath: () => void;

  // Workpiece origin in URDF coords (metres). The toolpath's (0, 0, 0)
  // sits here. Default places it visibly in front of the robot's base.
  workpieceOrigin: Vec3;
  setWorkpieceOrigin: (xyz: Vec3) => void;

  // ---- toolpath simulation ----
  sim: SimState;
  setSimStatus: (s: SimState["status"]) => void;
  setSimProgress: (p: number) => void;
  setSimSpeed: (speed: number) => void;
  setSimReachability: (unreachable: number, total: number) => void;
  setSimError: (err: string | null) => void;
}

export interface SimState {
  status: "idle" | "compiling" | "playing" | "error";
  progress: number; // 0..1
  speed: number;    // playback multiplier vs. real time
  unreachableSamples: number;
  totalSamples: number;
  error: string | null;
}

const newId = () =>
  typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : Math.random().toString(36).slice(2);

// Helper: wrap a program mutator so the prior state is captured for undo.
const withUndo = (
  state: AppState,
  next: Waypoint[]
): Pick<AppState, "program" | "_undo" | "_redo"> => ({
  program: next,
  _undo: [...state._undo, state.program].slice(-UNDO_LIMIT),
  _redo: [],
});

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      q: [0, 0, 0, 0, 0, 0],
      setJoint: (i, v) =>
        set((state) => {
          const q = [...state.q] as JointVec;
          q[i] = v;
          return { q };
        }),
      setAllJoints: (q) => set({ q }),
      home: () => set({ q: [0, 0, 0, 0, 0, 0], ik: null }),

      tcp: null,
      setTcp: (tcp) => set({ tcp }),

      ik: null,
      setIkStatus: (s) => set({ ik: s }),

      program: [],
      defaultDuration: 1.0,
      setDefaultDuration: (d) => set({ defaultDuration: d }),
      addWaypoint: (q) =>
        set((state) =>
          withUndo(state, [
            ...state.program,
            { id: newId(), q, duration: state.defaultDuration },
          ])
        ),
      deleteWaypoint: (id) =>
        set((state) =>
          withUndo(
            state,
            state.program.filter((w) => w.id !== id)
          )
        ),
      moveWaypoint: (id, direction) =>
        set((state) => {
          const i = state.program.findIndex((w) => w.id === id);
          if (i < 0) return state;
          const j = i + direction;
          if (j < 0 || j >= state.program.length) return state;
          const program = [...state.program];
          [program[i], program[j]] = [program[j], program[i]];
          return withUndo(state, program);
        }),
      updateWaypoint: (id, patch) =>
        set((state) =>
          withUndo(
            state,
            state.program.map((w) => (w.id === id ? { ...w, ...patch } : w))
          )
        ),
      clearProgram: () =>
        set((state) => withUndo(state, [])),
      loadProgram: (waypoints) =>
        set((state) =>
          withUndo(
            state,
            waypoints.map((w) => ({
              id: newId(),
              q: w.q,
              duration: typeof w.duration === "number" ? w.duration : 1.0,
              name: w.name,
            }))
          )
        ),

      _undo: [],
      _redo: [],
      undo: () =>
        set((state) => {
          if (state._undo.length === 0) return state;
          const prev = state._undo[state._undo.length - 1];
          return {
            program: prev,
            _undo: state._undo.slice(0, -1),
            _redo: [...state._redo, state.program],
          };
        }),
      redo: () =>
        set((state) => {
          if (state._redo.length === 0) return state;
          const next = state._redo[state._redo.length - 1];
          return {
            program: next,
            _redo: state._redo.slice(0, -1),
            _undo: [...state._undo, state.program],
          };
        }),
      canUndo: () => get()._undo.length > 0,
      canRedo: () => get()._redo.length > 0,

      playback: { playing: false, index: 0 },
      setPlaying: (playing) =>
        set((state) => ({ playback: { ...state.playback, playing } })),
      setPlaybackIndex: (index) =>
        set((state) => ({ playback: { ...state.playback, index } })),

      viewer: {
        showGrid: true,
        showWorkspace: true,
        showToolpath: true,
        resetViewTick: 0,
      },
      toggleGrid: () =>
        set((state) => ({
          viewer: { ...state.viewer, showGrid: !state.viewer.showGrid },
        })),
      toggleWorkspace: () =>
        set((state) => ({
          viewer: {
            ...state.viewer,
            showWorkspace: !state.viewer.showWorkspace,
          },
        })),
      toggleToolpath: () =>
        set((state) => ({
          viewer: {
            ...state.viewer,
            showToolpath: !state.viewer.showToolpath,
          },
        })),
      requestResetView: () =>
        set((state) => ({
          viewer: {
            ...state.viewer,
            resetViewTick: state.viewer.resetViewTick + 1,
          },
        })),

      toolpath: null,
      toolpathSource: null,
      loadToolpath: (gcode) => {
        const parsed = parseGcode(gcode);
        set({ toolpath: parsed, toolpathSource: gcode });
        return parsed;
      },
      clearToolpath: () => set({ toolpath: null, toolpathSource: null }),

      // 30 cm in front of the robot in URDF X, 5 cm above the floor in
      // URDF Z. Far enough from the base mesh that small parts are visible.
      workpieceOrigin: [0.3, 0, 0.05],
      setWorkpieceOrigin: (xyz) => set({ workpieceOrigin: xyz }),

      sim: {
        status: "idle",
        progress: 0,
        speed: 10,
        unreachableSamples: 0,
        totalSamples: 0,
        error: null,
      },
      setSimStatus: (status) =>
        set((s) => ({ sim: { ...s.sim, status, error: status === "error" ? s.sim.error : null } })),
      setSimProgress: (progress) =>
        set((s) => ({ sim: { ...s.sim, progress } })),
      setSimSpeed: (speed) =>
        set((s) => ({ sim: { ...s.sim, speed } })),
      setSimReachability: (unreachable, total) =>
        set((s) => ({
          sim: { ...s.sim, unreachableSamples: unreachable, totalSamples: total },
        })),
      setSimError: (error) =>
        set((s) => ({ sim: { ...s.sim, error } })),
    }),
    {
      name: "ar3-platform",
      partialize: (state: AppState) => ({
        program: state.program,
        defaultDuration: state.defaultDuration,
        viewer: state.viewer,
        toolpathSource: state.toolpathSource,
        workpieceOrigin: state.workpieceOrigin,
      }),
      onRehydrateStorage: () => (state) => {
        // Re-parse the saved gcode so the in-memory Toolpath is rebuilt
        // without persisting the (potentially large) parsed move list.
        if (state?.toolpathSource) {
          try {
            state.toolpath = parseGcode(state.toolpathSource);
          } catch {
            state.toolpath = null;
            state.toolpathSource = null;
          }
        }
      },
    }
  )
);
