"""AR3 Platform — kinematics sidecar.

A JSON-RPC 2.0 server that reads newline-delimited requests on stdin
and writes responses on stdout. Spawned and supervised by the Tauri
shell.

Methods implemented:
    health           — handshake; always available
    joint_limits     — joint limits in radians
    fk               — forward kinematics: joints -> TCP pose
    ik               — inverse kinematics: TCP pose -> joints
"""

from __future__ import annotations

import argparse
import json
import math
import queue
import sys
import threading
import traceback
from typing import Any, Callable

VERSION = "0.1.0"

# ---------------------------------------------------------------------------
# Optional heavy deps (ikpy / numpy). The sidecar still runs without them so
# health/joint_limits remain available; FK/IK return a clean error instead of
# crashing the whole app.
# ---------------------------------------------------------------------------

try:
    import numpy as np
    import ikpy.chain
    KINEMATICS_OK = True
    KINEMATICS_ERR = None
except Exception as e:  # noqa: BLE001 — want the broadest "anything missing"
    np = None  # type: ignore
    ikpy = None  # type: ignore
    KINEMATICS_OK = False
    KINEMATICS_ERR = f"{type(e).__name__}: {e}"

CHAIN = None  # ikpy.chain.Chain, populated in main()
URDF_PATH: str | None = None

# Joint limits in radians, matching public/ar3.urdf.
JOINT_LIMITS: list[tuple[float, float]] = [
    (-2.97, 2.97),
    (-2.25, 2.25),
    (-2.50, 2.50),
    (-2.88, 2.88),
    (-1.83, 1.83),
    (-2.70, 2.70),
]

# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------

Handler = Callable[[dict[str, Any]], dict[str, Any]]
METHODS: dict[str, Handler] = {}


def method(name: str) -> Callable[[Handler], Handler]:
    def deco(fn: Handler) -> Handler:
        METHODS[name] = fn
        return fn

    return deco


def _need_kinematics() -> None:
    if not KINEMATICS_OK or CHAIN is None:
        raise RuntimeError(
            "kinematics unavailable — install Python deps with: "
            "python -m pip install ikpy numpy scipy "
            f"(import error: {KINEMATICS_ERR})"
        )


# ---------------------------------------------------------------------------
# ikpy helpers — map between 6 active joints and the chain's joint vector.
# ---------------------------------------------------------------------------


def _to_chain_q(q_active: list[float]) -> list[float]:
    """Pad a 6-element joint vector into the chain's full joint array."""
    mask = CHAIN.active_links_mask  # type: ignore[union-attr]
    full = [0.0] * len(mask)
    j = 0
    for i, active in enumerate(mask):
        if active:
            if j < len(q_active):
                full[i] = float(q_active[j])
            j += 1
    return full


def _from_chain_q(q_full: list[float]) -> list[float]:
    mask = CHAIN.active_links_mask  # type: ignore[union-attr]
    return [float(q_full[i]) for i, active in enumerate(mask) if active]


def _matrix_to_rpy(m) -> tuple[float, float, float]:
    """Extract roll, pitch, yaw (XYZ convention) from a 3x3 rotation matrix."""
    # Standard URDF rpy = R = Rz(yaw) * Ry(pitch) * Rx(roll)
    sy = math.sqrt(m[0, 0] ** 2 + m[1, 0] ** 2)
    if sy > 1e-6:
        roll = math.atan2(m[2, 1], m[2, 2])
        pitch = math.atan2(-m[2, 0], sy)
        yaw = math.atan2(m[1, 0], m[0, 0])
    else:
        roll = math.atan2(-m[1, 2], m[1, 1])
        pitch = math.atan2(-m[2, 0], sy)
        yaw = 0.0
    return roll, pitch, yaw


# ---------------------------------------------------------------------------
# Methods
# ---------------------------------------------------------------------------


@method("health")
def _health(_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "version": VERSION,
        "kinematics": KINEMATICS_OK,
        "urdf": URDF_PATH,
    }


@method("joint_limits")
def _joint_limits(_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "min": [lo for lo, _ in JOINT_LIMITS],
        "max": [hi for _, hi in JOINT_LIMITS],
    }


@method("fk")
def _fk(params: dict[str, Any]) -> dict[str, Any]:
    _need_kinematics()
    q = params.get("q") or [0.0] * 6
    if len(q) != 6:
        raise ValueError("q must have 6 elements")
    full = _to_chain_q(list(q))
    T = CHAIN.forward_kinematics(full)  # type: ignore[union-attr]
    xyz = [float(T[0, 3]), float(T[1, 3]), float(T[2, 3])]
    rpy = list(_matrix_to_rpy(T[:3, :3]))
    return {"pose": {"xyz": xyz, "rpy": rpy}}


@method("ik")
def _ik(params: dict[str, Any]) -> dict[str, Any]:
    _need_kinematics()
    pose = params.get("pose") or {}
    xyz = pose.get("xyz")
    if not xyz or len(xyz) != 3:
        raise ValueError("pose.xyz must be [x, y, z]")

    q_seed = params.get("q_seed") or [0.0] * 6
    seed_full = _to_chain_q(list(q_seed))

    # Run ikpy in a worker thread with a hard timeout. ikpy's Levenberg-
    # Marquardt solver can take very long (or effectively forever) on
    # unreachable targets; without this bound, one bad call jams the entire
    # IK pipeline because the host has no way to know we hung.
    result_q: queue.Queue = queue.Queue(maxsize=1)

    def _worker() -> None:
        try:
            sol = CHAIN.inverse_kinematics(  # type: ignore[union-attr]
                target_position=xyz,
                initial_position=seed_full,
            )
            result_q.put(("ok", sol))
        except BaseException as e:  # noqa: BLE001
            result_q.put(("err", e))

    threading.Thread(target=_worker, daemon=True).start()
    try:
        kind, value = result_q.get(timeout=0.4)
    except queue.Empty:
        raise TimeoutError(
            "IK solver exceeded 400ms — target likely unreachable"
        )
    if kind == "err":
        raise value  # type: ignore[misc]
    sol = value

    q_active = _from_chain_q(list(sol))

    # Clamp to declared limits and report whether we ended up at a limit.
    clamped = False
    for i, (lo, hi) in enumerate(JOINT_LIMITS):
        if q_active[i] < lo:
            q_active[i] = lo
            clamped = True
        elif q_active[i] > hi:
            q_active[i] = hi
            clamped = True

    # Residual = how far off the achieved TCP is from the requested point.
    achieved = CHAIN.forward_kinematics(_to_chain_q(q_active))  # type: ignore[union-attr]
    err = float(
        (achieved[0, 3] - xyz[0]) ** 2
        + (achieved[1, 3] - xyz[1]) ** 2
        + (achieved[2, 3] - xyz[2]) ** 2
    ) ** 0.5

    # Cast every comparison through `bool()` — numpy comparisons return
    # numpy.bool_ which the stdlib json encoder cannot serialize. A previous
    # build of this code crashed the sidecar whenever the residual exceeded
    # the tolerance, jamming the frontend's in-flight IK request forever.
    return {
        "q": [float(v) for v in q_active],
        "ok": bool(err < 0.01 and not clamped),
        "residual": err,
        "clamped": bool(clamped),
    }


# ---------------------------------------------------------------------------
# JSON-RPC loop
# ---------------------------------------------------------------------------


def _json_safe(o: Any) -> Any:
    """Fallback for objects the default json encoder can't handle.

    numpy scalars (numpy.bool_, numpy.float64, etc.) and numpy arrays leak
    into responses easily. Without this default the encoder raises
    TypeError, which kills the sidecar and freezes the frontend.
    """
    if hasattr(o, "item"):
        return o.item()
    if hasattr(o, "tolist"):
        return o.tolist()
    raise TypeError(f"not JSON-serializable: {type(o).__name__}")


def _write(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, separators=(",", ":"), default=_json_safe) + "\n")
    sys.stdout.flush()


def _error(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def _result(req_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def handle(line: str) -> dict[str, Any] | None:
    try:
        req = json.loads(line)
    except json.JSONDecodeError as e:
        return _error(None, -32700, f"parse error: {e}")

    req_id = req.get("id")
    method_name = req.get("method")
    params = req.get("params") or {}

    if not isinstance(method_name, str):
        return _error(req_id, -32600, "missing method")
    handler = METHODS.get(method_name)
    if handler is None:
        return _error(req_id, -32601, f"unknown method: {method_name}")

    try:
        return _result(req_id, handler(params))
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return _error(req_id, -32000, f"{type(e).__name__}: {e}")


def _load_chain(urdf_path: str) -> None:
    """Build the ikpy chain from the AR3 URDF. Silent no-op if deps missing."""
    global CHAIN, URDF_PATH
    URDF_PATH = urdf_path
    if not KINEMATICS_OK:
        return
    try:
        CHAIN = ikpy.chain.Chain.from_urdf_file(  # type: ignore[union-attr]
            urdf_path,
            base_elements=["base_link"],
        )
        # ikpy's auto-generated mask marks the fixed base link (index 0) as
        # active, which makes IK return 7 values instead of 6 and shifts the
        # FK mapping by one. Force only the last 6 links (joint1..joint6)
        # to be active.
        n = len(CHAIN.links)  # type: ignore[union-attr]
        nq = len(JOINT_LIMITS)
        mask = [False] * n
        for i in range(max(0, n - nq), n):
            mask[i] = True
        CHAIN.active_links_mask = mask  # type: ignore[union-attr]
        print(
            f"[ar3-sidecar] loaded URDF: {urdf_path} "
            f"({sum(CHAIN.active_links_mask)} active joints of {n})",  # type: ignore[union-attr]
            file=sys.stderr,
            flush=True,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[ar3-sidecar] URDF load FAILED: {e}", file=sys.stderr, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urdf", default=None, help="Path to ar3.urdf")
    args = parser.parse_args()

    if args.urdf:
        _load_chain(args.urdf)
    else:
        print("[ar3-sidecar] no --urdf provided; FK/IK disabled", file=sys.stderr)

    print(f"[ar3-sidecar] v{VERSION} ready (kinematics={KINEMATICS_OK})",
          file=sys.stderr, flush=True)

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        resp = handle(line)
        if resp is not None:
            _write(resp)


if __name__ == "__main__":
    main()
