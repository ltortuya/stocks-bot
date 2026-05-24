"""Smoke test: drive the sidecar over a pipe and check the health response."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SIDECAR = Path(__file__).resolve().parent.parent / "server.py"


def test_health_roundtrip() -> None:
    proc = subprocess.Popen(
        [sys.executable, "-u", str(SIDECAR)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None

    req = {"jsonrpc": "2.0", "id": 1, "method": "health", "params": {}}
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()

    line = proc.stdout.readline()
    proc.stdin.close()
    proc.wait(timeout=5)

    resp = json.loads(line)
    assert resp["id"] == 1
    assert resp["result"]["ok"] is True
    assert isinstance(resp["result"]["version"], str)
