# Annin AR3 Platform — Design

A desktop application for **simulating, visualizing, and ultimately
driving** the Annin AR3 6-axis robot arm — with the long-term goal of
using it as a 6-axis CNC for **carving 3D sculptures** in soft
materials (foam, wax, soft wood, MDF).

> Status: design document. No code yet. Scaffolded inside
> `stocks-bot/ar3-platform/` for now; will migrate to a standalone repo
> before implementation begins in earnest.

---

## 0. Long-term vision: 3D sculpting

End state: load a 3D model, generate toolpaths in an **external CAM
tool** (RoboDK, Fusion 360, or FreeCAD Path), import the result into
this app, visualize and validate it against the real AR3, then stream
it to the arm while controlling a spindle to carve the part.

**This app does not write its own CAM.** That's a years-long project
and the existing tools are already excellent. This app is the bridge
between "CAM output" and "robot moving with a spindle running."

### Hardware reality check
The AR3 is a hobby-grade arm. Realistic materials:
- ✅ Foam (EPS, EPP, urethane), machinable wax, balsa, pine, MDF (light passes)
- ⚠️ Hardwoods, plywood — possible but expect chatter and slow feeds
- ❌ Aluminum, brass, steel — too much deflection; will ruin parts and break bits

A small trim-router-class spindle (300–800 W) is the sweet spot.
Anything bigger and the arm becomes the weak link.

---

## 1. Goals & non-goals

### Goals (v1 — foundation)
- Load the AR3 mesh + URDF and render it in an interactive 3D scene.
- Drive joints via sliders → forward kinematics → visual update.
- Drive a target TCP pose → inverse kinematics → joint solution → visual update.
- Author and replay simple waypoint programs (record / save / load / play).
- Trajectory generation (trapezoidal, eventually splines) for smooth playback.
- Clean transport abstraction with a default **simulated** backend.

### Goals (v2 — sculpting)
- Import toolpaths from an external CAM tool (G-code and/or RoboDK joint files).
- Overlay the toolpath on the 3D scene; flag unreachable or out-of-limits moves.
- Workpiece coordinate setup (touch-off / probing routine).
- Tool library (bit length, diameter, TCP offset from the flange).
- **High-rate streaming** of joint commands (100–500 Hz) instead of waypoint playback.
- **Spindle control** via the transport layer (on/off, RPM).
- Real-time feed-rate override, pause/resume, e-stop.

### Non-goals
- **Writing our own CAM.** Use RoboDK / Fusion 360 / FreeCAD Path instead.
- Driving anything other than the AR3 (single-robot focus).
- Multi-robot scenes, dynamics simulation, force control.
- ROS integration (kept easy via a future Transport implementation).
- Mobile / web deployment.
- Cloud sync of programs.

---

## 2. Stack

| Layer            | Choice                                  | Why |
| ---------------- | --------------------------------------- | --- |
| Desktop shell    | **Tauri** (Rust)                        | ~10 MB binary vs. ~150 MB Electron; native FS / dialog APIs; a sensible home for the hardware transport trait and high-rate streaming loop. |
| UI framework     | **React** + Vite + TypeScript           | Mature; trivial Three.js integration; familiar to most. |
| 3D rendering     | **Three.js** + `urdf-loader`            | Loads AR3 URDF/STL directly; well-documented; toolpath overlays are just line geometry. |
| Kinematics & G-code | **Python sidecar** using `roboticstoolbox-python` (fallback `ikpy`) + a G-code parser (`pygcode` or hand-rolled subset) | AR3 community DH parameters already live in Python; mature IK/FK/Jacobian; G-code → poses → IK pipeline stays in one place. |
| IPC              | **JSON-RPC over stdio**                 | Tauri spawns the Python sidecar as a child process; no network port to clash. Bulk toolpath data is sent once, then high-rate streaming happens in Rust. |
| Packaging        | Tauri bundler + PyInstaller for sidecar | One-binary install per OS (mac, linux, windows). |

**Main tradeoff:** two languages instead of one. Python's robotics
ecosystem (DH parameters, IK solvers, G-code libraries) is worth the
extra IPC moving piece. The hot streaming loop stays in Rust so we
aren't bottlenecked by Python.

---

## 3. Architecture

```
                  ┌──────────────────────────────────┐
                  │  External CAM tool               │
                  │  • RoboDK  (joint trajectories)  │
                  │  • Fusion 360 + post (G-code)    │
                  │  • FreeCAD Path (G-code)         │
                  └────────────────┬─────────────────┘
                                   │ exports
                                   ▼  *.nc / *.gcode / *.json
┌──────────────────────────────────────────────────────────────────┐
│  Tauri Shell  (Rust)                                             │
│  ─ window / menu / file dialogs                                  │
│  ─ spawns + supervises Python sidecar                            │
│  ─ Transport trait: joint cmds, spindle, digital I/O, e-stop     │
│  ─ HIGH-RATE STREAMING loop (100–500 Hz) for sculpting           │
└──────────────────────────────────────────────────────────────────┘
              ▲                                       ▲
              │  Tauri commands (JS ⇄ Rust)           │  JSON-RPC stdio
              ▼                                       ▼
┌──────────────────────────────────────┐  ┌──────────────────────────┐
│  Frontend  (React + Three.js + TS)   │  │  Kinematics Sidecar (Py) │
│                                      │  │                          │
│  ─ Scene: URDF, TCP frame, workpiece │  │  ─ FK / IK / Jacobian    │
│  ─ Toolpath overlay (lines + colors) │  │  ─ G-code → pose stream  │
│  ─ Joint sliders, TCP pose inputs    │  │  ─ Pose stream → joint   │
│  ─ Program / job editor              │  │    trajectory (with IK   │
│  ─ Tool library, workpiece setup     │  │    continuity)           │
│  ─ Run controls (play/pause/feed %)  │  │  ─ Reachability check    │
│  ─ State store (Zustand)             │  │  ─ Trajectory smoothing  │
└──────────────────────────────────────┘  └──────────────────────────┘
                                                       │
                                          ┌────────────┴────────────┐
                                          │ AR3 model: DH params,   │
                                          │ joint limits, URDF link │
                                          └─────────────────────────┘
```

### How the CAM hand-off works
1. User designs sculpture in their CAM tool of choice.
2. CAM tool exports either:
   - **G-code** (`.nc` / `.gcode`) — universal, but needs IK to map to joints
   - **Pre-solved joint trajectory** (RoboDK can do this) — bypasses IK
3. App loads the file, sidecar parses it into a sampled `(t, q, spindle)` stream.
4. UI overlays the path on the 3D scene, flags problems.
5. User hits "Run." Rust streams commands to the transport at the configured rate.

### Transport trait (Rust)

```rust
trait Transport: Send + Sync {
    fn connect(&mut self) -> Result<()>;
    fn disconnect(&mut self) -> Result<()>;

    // Motion
    fn send_joint_state(&mut self, q: [f64; 6]) -> Result<()>;
    fn read_joint_state(&mut self) -> Result<[f64; 6]>;

    // Sculpting additions
    fn set_spindle(&mut self, on: bool, rpm: Option<u32>) -> Result<()>;
    fn set_digital_out(&mut self, pin: u8, level: bool) -> Result<()>;
    fn read_digital_in(&mut self, pin: u8) -> Result<bool>;   // probes, limit switches
    fn estop(&mut self) -> Result<()>;
}
```

v1 implementations:
- `SimTransport` — echoes commanded state back; default.

v2+:
- `SerialTransport` — talks to stock AR3 Teensy firmware over USB.
- `Ros2Transport` — publishes to ros2_control (optional).

### Why streaming, not waypoint playback
Waypoint playback (M3) sends "go here, then here, then here" and the
robot smooths between. Sculpting requires the TCP to follow a curve
with tight tolerance at controlled feed rate. That means commanding
joint positions at a fixed rate (100–500 Hz typical), with the host
holding the trajectory clock. This is a different control model and
needs to live in Rust for latency reasons.

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
│   │   ├── streamer.rs         ← high-rate streaming loop (v2)
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
│   │   ├── tcpGizmo.ts         ← drag-target gizmo for IK
│   │   ├── toolpath.ts         ← toolpath line overlay (v2)
│   │   └── workpiece.ts        ← workpiece bounding box (v2)
│   ├── panels/
│   │   ├── JointPanel.tsx      ← per-joint sliders
│   │   ├── TcpPanel.tsx        ← XYZ + RPY inputs
│   │   ├── ProgramPanel.tsx    ← waypoint list, save/load, play
│   │   ├── JobPanel.tsx        ← load .nc / .gcode / .json, run job (v2)
│   │   ├── ToolPanel.tsx       ← bit library, TCP offset (v2)
│   │   ├── WorkpiecePanel.tsx  ← origin probing / touch-off (v2)
│   │   └── StatusBar.tsx
│   ├── state/
│   │   └── store.ts            ← Zustand store
│   └── rpc/
│       └── kinematics.ts       ← typed client for Python sidecar
├── sidecar/                    ← Python kinematics service
│   ├── ar3/
│   │   ├── __init__.py
│   │   ├── model.py            ← DH params, joint limits, link masses
│   │   ├── kinematics.py       ← FK / IK / Jacobian
│   │   ├── trajectory.py       ← trapezoidal & cubic splines
│   │   └── gcode.py            ← G-code parser → pose stream (v2)
│   ├── server.py               ← JSON-RPC over stdio loop
│   ├── pyproject.toml
│   └── tests/
├── assets/
│   ├── ar3.urdf
│   └── meshes/                 ← STL files for links
└── docs/
    ├── PROTOCOL.md             ← JSON-RPC method list
    ├── CAM-WORKFLOWS.md        ← how to set up RoboDK / Fusion / FreeCAD
    └── ROADMAP.md              ← milestone tracker
```

---

## 5. Sidecar protocol (JSON-RPC over stdio)

v1 methods:

| Method                | Params                                     | Returns                                |
| --------------------- | ------------------------------------------ | -------------------------------------- |
| `fk`                  | `{ q: number[6] }`                         | `{ pose: { xyz, rpy }, T_links }`     |
| `ik`                  | `{ pose, q_seed?, max_iters? }`            | `{ q: number[6], ok, residual }`      |
| `jacobian`            | `{ q }`                                    | `{ J: number[6][6] }`                  |
| `reachable`           | `{ pose }`                                 | `{ ok, reason? }`                      |
| `plan_trajectory`     | `{ waypoints, max_vel, max_acc, dt }`      | `{ samples: { t, q, qd, qdd }[] }`    |
| `joint_limits`        | `{}`                                       | `{ min[6], max[6], vmax[6] }`         |
| `health`              | `{}`                                       | `{ ok, version }`                      |

v2 additions for sculpting:

| Method                | Params                                     | Returns                                |
| --------------------- | ------------------------------------------ | -------------------------------------- |
| `load_gcode`          | `{ path, tool, workpiece_origin }`         | `{ job_id, n_lines, bbox, est_time }`  |
| `load_joint_program`  | `{ path }` (RoboDK joint export)           | `{ job_id, n_samples, est_time }`      |
| `solve_job`           | `{ job_id, sample_hz }`                    | `{ samples, warnings: [{ line, msg }] }` |
| `set_tcp_offset`      | `{ xyz, rpy }` (bit length / fixture)      | `{ ok }`                               |

Errors follow JSON-RPC error codes; UI shows the message in StatusBar.

---

## 6. State model (frontend)

```ts
type Mode = "jog" | "ik-drag" | "program-edit" | "program-play" | "job-run";

interface AppState {
  mode: Mode;
  q: [number, number, number, number, number, number];   // current joints
  qTarget: [number, ...] | null;                          // commanded
  tcp: { xyz: Vec3; rpy: Vec3 };                          // derived from q
  tcpOffset: { xyz: Vec3; rpy: Vec3 };                    // tool/bit offset (v2)
  program: Waypoint[];                                    // ordered waypoints
  job: Job | null;                                        // loaded CAM job (v2)
  workpiece: { origin: Vec3; size: Vec3 } | null;         // (v2)
  playback: { idx: number; t: number; playing: boolean; feedOverride: number };
  spindle: { on: boolean; rpm: number };                  // (v2)
  transport: "sim" | "serial" | "disconnected";
  warnings: string[];
}
```

---

## 7. Milestones

### Foundation (v1)
| #   | Name                       | Deliverable                                                                                          |
| --- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| M0  | Scaffold                   | Tauri app boots, blank React UI, Python sidecar handshake (`health`).                                |
| M1  | Viewer + FK                | URDF loads, 6 joint sliders drive the arm, TCP frame visible.                                        |
| M2  | IK                         | Drag-gizmo on TCP → sidecar IK → joints update. Limits + singularity warnings in StatusBar.          |
| M3  | Programs                   | Record waypoints, save/load `.ar3prog` JSON, play back with trapezoidal trajectories.                |
| M4  | Transport abstraction      | Rust `Transport` trait + `SimTransport`; UI shows "Sim" vs "Disconnected".                          |
| M5  | Polish                     | Workspace volume display, reachability shading, undo/redo for program edits.                        |

### Sculpting (v2)
| #   | Name                       | Deliverable                                                                                          |
| --- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| M6  | Hardware transport         | `SerialTransport` to AR3 Teensy. Joint commands actually move the real arm.                          |
| M7  | Spindle + I/O              | Extend Transport with spindle on/off + RPM and digital I/O. UI controls + safety interlocks.         |
| M8  | Tool & workpiece setup     | Tool library, TCP offset, workpiece origin probing routine (manual touch-off first).                 |
| M9  | G-code import              | Load `.nc` / `.gcode`, parse, render as line overlay, sanity-check reachability per move.            |
| M10 | RoboDK joint import        | Load pre-solved joint trajectories, bypass IK, render path.                                          |
| M11 | High-rate streaming        | Rust streaming loop at 100–500 Hz; play loaded jobs to SimTransport, then to real hardware.          |
| M12 | Run controls               | Pause/resume, feed-rate override, e-stop, retract-to-safe-Z, mid-job recovery.                       |

---

## 8. Risks & open questions

- **AR3 rigidity.** Hobby arm; deflection under cutting load is the
  biggest unknown. Plan to characterize empirically with a dial
  indicator before trusting any toolpath.
- **URDF accuracy.** Community URDFs vary between forks. Pick one and
  validate against the physical arm's joint zero conventions before
  M1 lands.
- **IK continuity along toolpaths.** Naive per-pose IK can flip
  configurations mid-cut and ruin a part. Need a seeded solver that
  prefers the previous solution and warns near singularities.
- **Streaming latency.** USB serial to the Teensy may not hit 500 Hz
  reliably. Worst case: lower the rate and rely on on-board interpolation,
  or replace firmware later. Defer the decision until M6 testing.
- **Spindle integration.** AR3 has spare digital outputs but no
  built-in spindle driver. Need to spec a relay or VFD interface as
  part of M7.
- **Safety.** Spinning bit + 6-axis arm = real hazard. Need a hard
  e-stop in hardware (button wired to spindle + arm power), not just
  software. Document this clearly before anyone runs a real job.
- **Sidecar packaging.** PyInstaller + numpy can be finicky across OSes.
  May need `python-build-standalone`.

---

## 9. Out of scope (deliberately)

- **Writing our own CAM.** Use external tools.
- Dynamics, force control, contact simulation.
- ROS 2 integration (future Transport implementation).
- Multi-robot scenes.
- Cloud sync of programs.
- Vision / camera integration (could be useful for workpiece
  alignment someday, but not v2).
- Adaptive feed control / load-aware cutting.
