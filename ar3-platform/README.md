# AR3 Platform

Desktop application for simulating, visualizing, and (eventually) carving
sculptures with the Annin AR3 robot arm.

See [`DESIGN.md`](./DESIGN.md) for the architecture and milestone plan.

## Status

**M0 — Scaffold** ✅
**M1 — Viewer + FK** ✅ (URDF + joint sliders driving the 3D arm)
**M2 — Inverse Kinematics** ✅ (drag the TCP, joints solve automatically)
**M3 — Programs** ✅ (record waypoints, save / load, play back smoothly)
**M4 — Transport abstraction** ✅ (Rust `Transport` trait + SimTransport; joint state mirrors at 50 Hz)
**M5 — Polish** ✅ (reach dome, TCP readout, smooth jumps, undo / redo, view toolbar, real AR3 meshes)

**v1 foundation complete.** Next: **M6 — Real hardware** (`SerialTransport` driving an AR3 Teensy over USB).

## Robot description

The 3D model in the viewer comes from
[`ongdexter/ar3_core`](https://github.com/ongdexter/ar3_core)
(MIT licensed). The mesh STLs and the URDF live under
[`public/ar3-meshes/`](public/ar3-meshes/) and
[`public/ar3.urdf`](public/ar3.urdf). The hand-built cylinder
fallback lives at `public/ar3-cylinders.urdf` — change the path in
`src/scene/Viewer.tsx` to swap.

## Prerequisites

| Tool       | Version  | Notes |
| ---------- | -------- | ----- |
| Node.js    | ≥ 18     | tested on 22 |
| pnpm       | ≥ 9      | `npm i -g pnpm` |
| Rust       | ≥ 1.77   | install via [rustup](https://rustup.rs) |
| Python     | ≥ 3.10   | system python is fine for M0 |

### Platform packages

- **Linux**: `webkit2gtk-4.1`, `libgtk-3-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, `libssl-dev`, `build-essential`
- **macOS**: Xcode command-line tools (`xcode-select --install`)
- **Windows**: Microsoft C++ Build Tools + WebView2 (preinstalled on Win11)

See the [Tauri prerequisites](https://tauri.app/start/prerequisites/) page for the latest.

## First-time setup

```bash
cd ar3-platform
pnpm install

# Generate placeholder app icons from any source PNG (one-time)
pnpm tauri icon path/to/source-icon.png

# Python kinematics dependencies (one-time, needed for M2+)
python -m pip install ikpy numpy scipy
```

## Run in dev

```bash
pnpm tauri dev
```

This will:

1. Start Vite on `localhost:1420`
2. Build the Rust shell
3. Open a desktop window
4. Spawn the Python sidecar as a child process
5. Show "✓ Sidecar up — version 0.0.1" if everything wired up

## Test the sidecar standalone

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"health","params":{}}' \
  | python3 sidecar/server.py
```

Expected output:

```
{"jsonrpc":"2.0","id":1,"result":{"ok":true,"version":"0.0.1"}}
```

## Layout

```
ar3-platform/
├── DESIGN.md            architecture + roadmap
├── package.json         frontend deps + tauri scripts
├── src/                 React + Three.js UI
├── src-tauri/           Rust shell (Tauri 2)
│   └── src/
│       ├── lib.rs       app setup + command handlers
│       └── sidecar.rs   JSON-RPC client for the Python child process
├── sidecar/             Python kinematics service
│   ├── server.py        JSON-RPC over stdio loop
│   └── tests/
└── assets/              URDF + meshes (added in M1)
```

## Environment variables

| Var            | Default    | Purpose |
| -------------- | ---------- | ------- |
| `AR3_PYTHON`   | `python3`  | override the python interpreter used for the sidecar |

## Troubleshooting

- **"sidecar/server.py not found"** — `pnpm tauri dev` runs from `src-tauri/`, so the sidecar is found relative to it. If you launched the binary directly, set `AR3_PYTHON` and ensure the script is next to the binary or in a Tauri resource dir.
- **Blank window, sidecar prints "ready"** — open devtools (`Ctrl/Cmd+Shift+I`) and check the invoke error.
- **Webview build errors on Linux** — install the apt packages listed above.
