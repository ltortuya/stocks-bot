"""Structured JSON logger with daily-rotated file output."""
from __future__ import annotations

import json
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

_LOGGERS: dict[str, logging.Logger] = {}


class _JsonFormatter(logging.Formatter):
    _RESERVED = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "component": record.name,
            "msg": record.getMessage(),
        }
        for key, val in record.__dict__.items():
            if key not in self._RESERVED and not key.startswith("_"):
                payload[key] = val
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def get_logger(
    component: str,
    log_dir: Path | str = Path("data/logs"),
    filename: str | None = None,
) -> logging.Logger:
    """Return a JSON logger that writes to <log_dir>/<filename or component>-YYYY-MM-DD.jsonl."""
    if component in _LOGGERS:
        return _LOGGERS[component]

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    fname = filename or f"{component}.jsonl"

    logger = logging.getLogger(component)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = TimedRotatingFileHandler(
        log_dir / fname, when="midnight", backupCount=30, encoding="utf-8"
    )
    handler.setFormatter(_JsonFormatter())
    logger.addHandler(handler)
    _LOGGERS[component] = logger
    return logger
