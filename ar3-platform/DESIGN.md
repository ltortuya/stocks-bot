# Annin AR3 Platform — Design

A desktop application for **simulating and visualizing** the Annin AR3
6-axis robot arm, with a pluggable transport layer so real hardware can
be wired in later without touching the UI.

> Status: design document. No code yet. Scaffolded inside `stocks-bot/ar3-platform/`
> for now; will migrate to a standalone repo before implementation begins in earnest.

---

## 1. Goals & non-goals

### Goals (v1)
- Load the AR3 mesh + URDF and render it in an interactive 3D scene.
- Drive joints via sliders → forward kinematics → visual update.
- Drive a target TCP pose → inverse kinematics → joint solution → visual update.
- Author and replay simple waypoint programs (record / save / load / play).
- Trajectory generation (trapezoidal, eventually splines) for smooth playback.
- Clean transport abstraction with a default **simulated** backend.

### Non-goals (v1)
- Driving real hardware (transport stub only — real serial / firmware lands in v2).
- Multi-robot scenes, dynamics simulation, collision-mesh authoring.
- ROS integration. (Easy to add later via a transport implementation.)
- Mobile / web deployment.

---

## 2. Stack

| Layer            | Choice                                  | Why |
| ---------------- | --------------------------------------- | --- |
| Desktop shell    | **Tauri** (Rust)                        | ~10 MB binary vs. ~150 MB Electron; native FS / dialog APIs; a sensible home for the hardware transport trait. |
| UI framework     | **React** + Vite + TypeScript           | Mature; trivial Three.js integration; familiar to most. |
| 3D rendering     | **Three.js** + `urdf-loader`            | Loads AR3 URDF/STL directly; well-documented; manipulating joints is just scene-graph transforms. |
| Kinematics       | **Python sidecar** using `roboticstoolbox-python` (fallback `ikpy`) | AR3 community DH parameters already live in Python; mature IK/FK/Jacobian implementations; numpy-fast. |
| IPC              | **JSON-RPC over stdio**                 | Tauri spawns the Python sidecar as a child process and pipes JSON-RPC; no network port to clash. |
| Packaging        | Tauri bundler + PyInstaller for sidecar | One-binary install per OS (mac, linux, windows). |

**Main tradeoff:** two languages instead of one. Python's robotics
ecosystem (DH parameters, IK solvers, trajectory tooling) is worth the
extra IPC moving piece. If Rust becomes a blocker, swap Tauri for
Electron with a Node host — same architecture, larger binary.

---

## 3. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  Tauri Shell  (Rust)                                             │
│  ─ window / menu / file dialogs                                  │
│  ─ spawns + supervises Python sidecar                            │
│  ─ owns the Transport trait (sim today, serial/ROS later)        │
└──────────────────────────────────────────────────────────────────┘
              ▲                                       ▲
              │  Tauri commands (JS ⇄ Rust)           │  JSON-RPC stdio
              ▼                                       ▼
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  Frontend  (React + Three.js + TS)   │  │  Kinematics Sidecar (Py) │
│                                      │  │                          │
│  ─ Scene: URDF, TCP frame, workspace │  │  ─ FK / IK               │
│  ─ Joint sliders, TCP pose inputs    │  │  ─ Jacobian, singularity │
│  ─ Program editor (waypoint list)    │  │  ─ Trajectory generation │
│  ─ Timeline / playback controls      │  │  ─ Reachability check    │
│  ─ State store (Zustand)             │  │                          │
└──────────────────────────────────────┘  └──────────────────────────┘
                                                       │
                                          ┌────────────┴────────────┐
                                          │ AR3 model: DH params,   │
                                          │ joint limits, URDF link │
                                          └─────────────────────────┘
```

### Why a Python sidecar (vs. WASM-compile or all-TS)?
- AR3 DH parameters live in Python in the community.
- `roboticstoolbox` IK is battle-tested; no JS equivalent at the same quality.
- Sidecar isolates GIL / heavy numpy from the UI thread.
- Trade: one extra process and IPC layer. Acceptable.

### Transport trait (Rust)

```rust
trait Transport: Send + Sync {
    fn connect(&mut self) -> Result<()>;
    fn disconnect(&mut self) -> Result<()>;
    fn send_joint_state(&mut self, q: [f64; 6]) -> Result<()>;
    fn read_joint_state(&mut self) -> Result<[f64; 6]>;
    fn estop(&mut self) -> Result<()>;
}
```

v1 implementations:
- `SimTransport` — echoes commanded state back; default.

v2+ (out of scope, but the trait must accommodate them):
- `SerialTransport` — talks to stock AR3 Teensy firmware over USB.
- `Ros2Transport` — publishes JointTrajectory to ros2_control.
- `CustomFirmwareTransport` — if we ever replace the Teensy.

---

## 4. File layout

```
ar3-platform/
├── DESIGN.md                   ← this file
├── README.md                   ← quickstart, build instructions (later)
├── src-tauri/                  ← Rust shell
│   ├── src/
│   │   ├── main.rs
│   │   ├── commands.rs         ← Tauri commands exposed to JS
│   │   ├── sidecar.rs          ← spawns + RPCs the Python process
│   │   └── transport/
│   │       ├── mod.rs          ← Transport trait
│   │       └── sim.rs          ← SimTransport (default)
│   ├── Cargo.toml
│   └── tauri.conf.json
├── src/                        ← React frontend
│   ├── main.tsx
│   ├── App.tsx
│   ├── scene/
│   │   ├── Viewer.tsx          ← Three.js canvas
│   │   ├── urdf.ts             ← URDF loader wrapper
│   │   └── tcpGizmo.ts         ← drag-target gizmo for IK
│   ├── panels/
│   │   ├── JointPanel.tsx      ← per-joint sliders
│   │   ├── TcpPanel.tsx        ← XYZ + RPY inputs
│   │   ├── ProgramPanel.tsx    ← waypoint list, save/load, play
│   │   └── StatusBar.tsx
│   ├── state/
│   │   └── store.ts            ← Zustand store: joints, tcp, program, mode
│   └── rpc/
│       └── kinematics.ts       ← typed client for Python sidecar
├── sidecar/                    ← Python kinematics service
│   ├── ar3/
│   │   ├── __init__.py
│   │   ├── model.py            ← DH params, joint limits, link masses
│   │   ├── kinematics.py       ← FK / IK / Jacobian
│   │   └── trajectory.py       ← trapezoidal & cubic splines
│   ├── server.py               ← JSON-RPC over stdio loop
│   ├── pyproject.toml
│   └── tests/
├── assets/
│   ├── ar3.urdf
│   └── meshes/                 ← STL files for links
└── docs/
    ├── PROTOCOL.md             ← JSON-RPC method list
    └── ROADMAP.md              ← milestone tracker
```

---

## 5. Sidecar protocol (JSON-RPC over stdio)

Each line on stdin/stdout is one JSON-RPC 2.0 message. Methods:

| Method                | Params                                     | Returns                                |
| --------------------- | ------------------------------------------ | -------------------------------------- |
| `fk`                  | `{ q: number[6] }`                         | `{ pose: { xyz, rpy }, T_links }`     |
| `ik`                  | `{ pose, q_seed?, max_iters? }`            | `{ q: number[6], ok, residual }`      |
| `jacobian`            | `{ q }`                                    | `{ J: number[6][6] }`                  |
| `reachable`           | `{ pose }`                                 | `{ ok, reason? }`                      |
| `plan_trajectory`     | `{ waypoints, max_vel, max_acc, dt }`      | `{ samples: { t, q, qd, qdd }[] }`    |
| `joint_limits`        | `{}`                                       | `{ min[6], max[6], vmax[6] }`         |
| `health`              | `{}`                                       | `{ ok, version }`                      |

Errors follow JSON-RPC error codes; UI shows the message in StatusBar.

---

## 6. State model (frontend)

```ts
type Mode = "jog" | "ik-drag" | "program-edit" | "program-play";

interface AppState {
  mode: Mode;
  q: [number, number, number, number, number, number];   // current joints
  qTarget: [number, ...] | null;                          // commanded
  tcp: { xyz: Vec3; rpy: Vec3 };                          // derived from q
  program: Waypoint[];                                    // ordered
  playback: { idx: number; t: number; playing: boolean };
  transport: "sim" | "serial" | "disconnected";
  warnings: string[];                                     // singularity, limits, etc.
}
```

Joints are the single source of truth. TCP is derived via FK on every
update. IK runs only when the user drags the gizmo or edits TCP inputs
directly — never in a render loop.

---

## 7. Milestones

| #   | Name                       | Deliverable                                                                                          |
| --- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| M0  | Scaffold                   | Tauri app boots, blank React UI, Python sidecar handshake (`health`).                                |
| M1  | Viewer + FK                | URDF loads, 6 joint sliders drive the arm, TCP frame visible.                                        |
| M2  | IK                         | Drag-gizmo on TCP → sidecar IK → joints update. Limits + singularity warnings in StatusBar.          |
| M3  | Programs                   | Record waypoints, save/load `.ar3prog` JSON, play back with trapezoidal trajectories.                |
| M4  | Transport abstraction      | Rust `Transport` trait + `SimTransport`; UI shows "Sim" vs "Disconnected"; ready for v2 hardware.    |
| M5  | Polish                     | Workspace volume display, reachability shading, undo/redo for program edits.                        |

v2 (separate design pass): `SerialTransport` to real AR3 Teensy.

---

## 8. Risks & open questions

- **URDF accuracy.** Community URDFs exist but joint axes / signs vary
  between forks. Need to pick one and validate against the physical
  arm's joint zero conventions before M1 lands.
- **IK solver choice.** `roboticstoolbox` uses Levenberg-Marquardt by
  default; we'll need a seed strategy that prefers the current pose to
  avoid solution jumps when dragging.
- **Sidecar packaging.** PyInstaller + numpy can be finicky across OSes;
  may need to ship a small portable Python via `python-build-standalone`.
- **Rust learning curve.** Tauri commands are simple; the Transport
  trait is small. If this proves friction-y, fall back to Electron.

---

## 9. Out of scope (deliberately)

- Dynamics, force control, contact simulation.
- ROS 2 integration (kept as a future Transport implementation).
- Multi-robot scenes.
- Cloud sync of programs (local files only for v1).
- Vision / camera integration.
