"""AR3 Platform — kinematics sidecar.

A JSON-RPC 2.0 server that reads newline-delimited requests on stdin
and writes responses on stdout. Spawned and supervised by the Tauri
shell. M0 implements only the `health` method.
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any, Callable

VERSION = "0.0.1"

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


@method("health")
def _health(_params: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "version": VERSION}


# ---------------------------------------------------------------------------
# JSON-RPC loop
# ---------------------------------------------------------------------------


def _write(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
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


def main() -> None:
    # Announce on stderr so the host can see we started.
    print(f"[ar3-sidecar] v{VERSION} ready", file=sys.stderr, flush=True)
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        resp = handle(line)
        if resp is not None:
            _write(resp)


if __name__ == "__main__":
    main()
