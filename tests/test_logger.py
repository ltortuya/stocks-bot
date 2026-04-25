"""Tests for bot.logger."""
from __future__ import annotations

import json
from pathlib import Path

from bot.logger import get_logger


def test_get_logger_writes_json_line(tmp_path: Path) -> None:
    log_path = tmp_path / "test.jsonl"
    log = get_logger("scanner", log_dir=tmp_path, filename="test.jsonl")
    log.info("hello", extra={"symbol": "AAPL", "rvol": 2.4})

    for handler in log.handlers:
        handler.flush()

    line = log_path.read_text().strip().splitlines()[-1]
    record = json.loads(line)
    assert record["msg"] == "hello"
    assert record["symbol"] == "AAPL"
    assert record["rvol"] == 2.4
    assert record["level"] == "INFO"
    assert record["component"] == "scanner"


def test_get_logger_is_idempotent(tmp_path: Path) -> None:
    """Calling get_logger twice should not duplicate handlers."""
    log1 = get_logger("scanner", log_dir=tmp_path)
    log2 = get_logger("scanner", log_dir=tmp_path)
    assert log1 is log2
    assert len(log1.handlers) == 1
