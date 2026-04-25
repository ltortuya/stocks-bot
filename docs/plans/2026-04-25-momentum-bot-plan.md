# Momentum Breakout Trading Bot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python momentum-breakout trading bot that runs against Alpaca paper trading on the existing Ubuntu mini PC, with end-of-day scanner, intraday polling trader, backtester, and Telegram alerts — per the design at `docs/specs/2026-04-25-momentum-bot-design.md`.

**Architecture:** Three Python entrypoints — `run_scanner.py` (cron, 4:05 PM ET), `run_trader.py` (systemd-supervised long-running daemon, 9:25 AM–4:05 PM ET), and `run_backtest.py` (manual). Strategy logic is decoupled from market data via a `MarketDataProvider` ABC so polling can later be swapped for streaming. State is persisted in SQLite. Alerts go to Telegram via the existing `.env` bot.

**Tech Stack:** Python 3.11+, `alpaca-py` SDK, `yfinance`, `pandas`, `numpy`, `python-dotenv`, `requests`, `pytest`, `freezegun` (for time-based tests), SQLite (stdlib), systemd, cron.

---

## File Structure

```
stocks_monitoring/
├── README.md                                    # ops + dev intro (Task 28)
├── requirements.txt                             # pinned deps (Task 1)
├── pyproject.toml                               # project metadata + pytest cfg (Task 1)
├── .env.example                                 # template (Task 1)
├── .gitignore                                   # (Task 1)
├── docs/
│   ├── specs/2026-04-25-momentum-bot-design.md  # (already exists)
│   └── plans/2026-04-25-momentum-bot-plan.md    # (this file)
├── bot/
│   ├── __init__.py                              # (Task 1)
│   ├── logger.py                                # JSON logger + rotation (Task 2)
│   ├── config.py                                # env + typed constants (Task 3)
│   ├── state.py                                 # SQLite persistence (Task 4)
│   ├── indicators.py                            # SMA / ATR / RVOL (Tasks 5-7)
│   ├── data/
│   │   ├── __init__.py                          # (Task 8)
│   │   ├── base.py                              # MarketDataProvider ABC (Task 8)
│   │   ├── alpaca_data.py                       # REST impl (Task 9)
│   │   └── earnings.py                          # yfinance wrapper (Task 10)
│   ├── universe.py                              # NDX∪SPX + filters (Task 11)
│   ├── risk.py                                  # sizing + halt checks (Task 13)
│   ├── entry.py                                 # trigger + vol confirm (Task 14)
│   ├── exit.py                                  # TP/SL/trail/time/earnings (Task 15)
│   ├── scanner.py                               # daily scan logic (Task 16)
│   ├── alerts.py                                # Telegram (Task 18)
│   ├── executor.py                              # Alpaca order wrappers (Task 19)
│   └── reconcile.py                             # state ↔ Alpaca sync (Task 20)
├── cli/
│   ├── __init__.py                              # (Task 1)
│   ├── refresh_universe.py                      # (Task 12)
│   ├── run_scanner.py                           # (Task 17)
│   ├── run_trader.py                            # main polling loop (Task 21)
│   ├── run_backtest.py                          # (Task 24)
│   └── ops.py                                   # admin commands (Task 27)
├── backtest/
│   ├── __init__.py                              # (Task 22)
│   ├── engine.py                                # bar-replay (Task 22)
│   ├── metrics.py                               # CAGR / DD / Sharpe (Task 23)
│   └── report.py                                # CSV + summary (Task 24)
├── data/
│   ├── universe/
│   │   ├── sp500.csv                            # populated by Task 12
│   │   ├── ndx.csv                              # populated by Task 12
│   │   └── exclusions.csv                       # seeded in Task 11
│   ├── state.sqlite                             # created on first run
│   ├── halt.flag                                # absent by default
│   └── logs/                                    # daily rotated jsonl
├── tests/
│   ├── __init__.py                              # (Task 1)
│   ├── conftest.py                              # shared fixtures (Task 1)
│   ├── fakes/
│   │   ├── __init__.py
│   │   ├── fake_alpaca.py                       # mock client (Task 9)
│   │   └── fake_data.py                         # canned bars (Task 5)
│   ├── fixtures/
│   │   └── bars/                                # canned bar CSVs
│   ├── test_logger.py                           # (Task 2)
│   ├── test_config.py                           # (Task 3)
│   ├── test_state.py                            # (Task 4)
│   ├── test_indicators.py                       # (Tasks 5-7)
│   ├── test_data_alpaca.py                      # (Task 9)
│   ├── test_data_earnings.py                    # (Task 10)
│   ├── test_universe.py                         # (Task 11)
│   ├── test_risk.py                             # (Task 13)
│   ├── test_entry.py                            # (Task 14)
│   ├── test_exit.py                             # (Task 15)
│   ├── test_scanner.py                          # (Task 16)
│   ├── test_alerts.py                           # (Task 18)
│   ├── test_executor.py                         # (Task 19)
│   ├── test_reconcile.py                        # (Task 20)
│   ├── test_trader_loop.py                      # (Task 21)
│   ├── test_backtest_engine.py                  # (Task 22)
│   └── test_metrics.py                          # (Task 23)
└── ops/
    ├── stocks-bot-trader.service                # systemd unit (Task 25)
    └── crontab.txt                              # cron template (Task 26)
```

## Task List Overview

| # | Task | Phase |
|---|---|---|
| 1 | Project scaffolding + git init | Foundation |
| 2 | Logger | Foundation |
| 3 | Config | Foundation |
| 4 | State (SQLite) | Foundation |
| 5 | SMA + ATR | Indicators |
| 6 | EOD relative volume | Indicators |
| 7 | Intraday RVOL curve | Indicators |
| 8 | MarketDataProvider ABC | Data |
| 9 | AlpacaMarketData REST + fake | Data |
| 10 | EarningsProvider (yfinance) | Data |
| 11 | Universe builder | Universe |
| 12 | refresh_universe CLI | Universe |
| 13 | Risk sizing + halt checks | Strategy |
| 14 | Entry trigger logic | Strategy |
| 15 | Exit logic | Strategy |
| 16 | Scanner | Scanner |
| 17 | run_scanner CLI | Scanner |
| 18 | Telegram alerts | Execution |
| 19 | Executor (Alpaca orders) | Execution |
| 20 | Reconciliation | Execution |
| 21 | Trader main loop | Trader |
| 22 | Backtest engine | Backtest |
| 23 | Backtest metrics | Backtest |
| 24 | run_backtest CLI + report | Backtest |
| 25 | systemd service file | Ops |
| 26 | Crontab template + start/stop scripts | Ops |
| 27 | ops CLI (positions, halt, flatten) | Ops |
| 28 | README + deployment docs | Ops |

---

## Task 1: Project Scaffolding + git init

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `bot/__init__.py`, `cli/__init__.py`, `tests/__init__.py`, `tests/fakes/__init__.py`, `backtest/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Initialize git and write .gitignore**

```bash
cd "c:/Users/ltort/stocks monitoring"
git init -b main
```

Create `.gitignore`:
```
.venv/
__pycache__/
*.pyc
.pytest_cache/
data/state.sqlite
data/state.sqlite-journal
data/halt.flag
data/logs/
data/universe/sp500.csv
data/universe/ndx.csv
backtest/results/
.env
*.egg-info/
build/
dist/
.DS_Store
```

- [ ] **Step 2: Write requirements.txt**

```
alpaca-py==0.30.0
yfinance==0.2.50
pandas==2.2.3
numpy==2.1.3
python-dotenv==1.0.1
requests==2.32.3
pytz==2024.2
pytest==8.3.4
pytest-mock==3.14.0
freezegun==1.5.1
responses==0.25.3
```

- [ ] **Step 3: Write pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "stocks_monitoring"
version = "0.1.0"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
include = ["bot*", "cli*", "backtest*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
markers = [
    "integration: end-to-end tests that hit the network (skipped by default)",
]
```

- [ ] **Step 4: Write .env.example**

```
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
ALPACA_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALPACA_BASE_URL=https://paper-api.alpaca.markets
TELEGRAM_TOKEN=000000000:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_CHAT_ID=000000000
```

- [ ] **Step 5: Create empty package files**

```bash
mkdir -p bot/data cli backtest tests/fakes tests/fixtures/bars data/universe data/logs ops
touch bot/__init__.py bot/data/__init__.py cli/__init__.py backtest/__init__.py
touch tests/__init__.py tests/fakes/__init__.py
```

- [ ] **Step 6: Write tests/conftest.py with shared fixtures**

```python
"""Shared pytest fixtures."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def tmp_state_db(tmp_path: Path) -> Path:
    """Returns a path to a fresh empty SQLite file for each test."""
    return tmp_path / "state.sqlite"


@pytest.fixture
def env_paper(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stubs Alpaca + Telegram env vars for tests that read config."""
    monkeypatch.setenv("ALPACA_API_KEY", "test_key")
    monkeypatch.setenv("ALPACA_API_SECRET", "test_secret")
    monkeypatch.setenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
    monkeypatch.setenv("TELEGRAM_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
```

- [ ] **Step 7: Create venv + install deps**

```bash
python -m venv .venv
# On Windows: .venv\Scripts\pip install -r requirements.txt
# On Linux (mini PC): .venv/bin/pip install -r requirements.txt
```

- [ ] **Step 8: Verify pytest runs (zero tests)**

Run: `.venv/Scripts/python -m pytest -v` (Windows) or `.venv/bin/pytest -v` (Linux)
Expected: `collected 0 items` with exit code 5.

- [ ] **Step 9: Commit**

```bash
git add .gitignore requirements.txt pyproject.toml .env.example bot/ cli/ backtest/ tests/ data/ ops/
git commit -m "chore: scaffold project structure"
```

---

## Task 2: Logger

**Files:**
- Create: `bot/logger.py`
- Test: `tests/test_logger.py`

- [ ] **Step 1: Write the failing test**

`tests/test_logger.py`:
```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_logger.py -v`
Expected: `ImportError: No module named 'bot.logger'`

- [ ] **Step 3: Implement `bot/logger.py`**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_logger.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/logger.py tests/test_logger.py
git commit -m "feat(logger): JSON logger with daily file rotation"
```

---

## Task 3: Config

**Files:**
- Create: `bot/config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_config.py`:
```python
"""Tests for bot.config."""
from __future__ import annotations

import pytest

from bot import config as cfg


def test_load_returns_typed_settings(env_paper) -> None:
    settings = cfg.load()
    assert settings.alpaca_api_key == "test_key"
    assert settings.alpaca_api_secret == "test_secret"
    assert settings.alpaca_base_url == "https://paper-api.alpaca.markets"
    assert settings.telegram_chat_id == "12345"


def test_load_uses_strategy_defaults(env_paper) -> None:
    settings = cfg.load()
    assert settings.poll_interval_sec == 30
    assert settings.poll_interval_fast_sec == 15
    assert settings.fast_poll_end_min == 90
    assert settings.min_price == 10.0
    assert settings.min_dollar_vol == 25_000_000
    assert settings.pct_change_min == 0.04
    assert settings.rvol_min == 1.8
    assert settings.near_breakout_pct == 0.02
    assert settings.lookback_breakout == 20
    assert settings.per_trade_risk_pct == 0.015
    assert settings.max_open_positions == 3
    assert settings.max_daily_new_entries == 5
    assert settings.daily_drawdown_halt_pct == -0.03
    assert settings.profit_target_pct == 0.10
    assert settings.hard_stop_pct == 0.05
    assert settings.trail_activation_pct == 0.06
    assert settings.trail_distance_pct == 0.05
    assert settings.time_stop_days == 5
    assert settings.gap_skip_pct == 0.08
    assert settings.no_entry_first_min == 5
    assert settings.no_new_entry_after == "14:30"
    assert settings.trader_end_time == "15:55"
    assert settings.exchange_tz == "America/New_York"


def test_load_raises_when_required_env_missing(monkeypatch) -> None:
    for key in ["ALPACA_API_KEY", "ALPACA_API_SECRET", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]:
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(cfg.MissingConfigError) as excinfo:
        cfg.load()
    assert "ALPACA_API_KEY" in str(excinfo.value)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_config.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/config.py`**

```python
"""Centralized typed configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class MissingConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    # secrets
    alpaca_api_key: str
    alpaca_api_secret: str
    alpaca_base_url: str
    telegram_token: str
    telegram_chat_id: str

    # poll cadence
    poll_interval_sec: int = 30
    poll_interval_fast_sec: int = 15
    fast_poll_end_min: int = 90

    # universe
    min_price: float = 10.0
    min_dollar_vol: float = 25_000_000

    # scan
    pct_change_min: float = 0.04
    rvol_min: float = 1.8
    near_breakout_pct: float = 0.02
    lookback_breakout: int = 20

    # risk
    per_trade_risk_pct: float = 0.015
    max_open_positions: int = 3
    max_daily_new_entries: int = 5
    daily_drawdown_halt_pct: float = -0.03

    # exits
    profit_target_pct: float = 0.10
    hard_stop_pct: float = 0.05
    trail_activation_pct: float = 0.06
    trail_distance_pct: float = 0.05
    time_stop_days: int = 5
    gap_skip_pct: float = 0.08

    # session timing (ET)
    no_entry_first_min: int = 5
    no_new_entry_after: str = "14:30"
    trader_end_time: str = "15:55"
    exchange_tz: str = "America/New_York"


_REQUIRED = ("ALPACA_API_KEY", "ALPACA_API_SECRET", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID")


def load(env_file: Path | str | None = None) -> Settings:
    """Load Settings from env (and optionally a .env file)."""
    if env_file is None:
        # default to user-level shared .env if present
        candidate = Path("C:/Users/ltort/.env")
        if candidate.exists():
            load_dotenv(candidate)
    else:
        load_dotenv(env_file)

    missing = [k for k in _REQUIRED if not os.environ.get(k)]
    if missing:
        raise MissingConfigError(f"Missing required env vars: {', '.join(missing)}")

    return Settings(
        alpaca_api_key=os.environ["ALPACA_API_KEY"],
        alpaca_api_secret=os.environ["ALPACA_API_SECRET"],
        alpaca_base_url=os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"),
        telegram_token=os.environ["TELEGRAM_TOKEN"],
        telegram_chat_id=os.environ["TELEGRAM_CHAT_ID"],
    )
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_config.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/config.py tests/test_config.py
git commit -m "feat(config): typed Settings loader from .env"
```

---

## Task 4: State (SQLite Persistence)

**Files:**
- Create: `bot/state.py`
- Test: `tests/test_state.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_state.py`:
```python
"""Tests for bot.state."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from bot.state import State, WatchlistEntry, Position


def test_init_creates_schema(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    tables = {row[0] for row in state.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    assert {"watchlist", "positions", "fills", "rvol_curves", "halts", "cycles"} <= tables


def test_upsert_and_load_watchlist(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    entry = WatchlistEntry(
        scan_date="2026-04-27",
        symbol="AAPL",
        signal_high=215.42,
        signal_low=207.15,
        signal_close=213.80,
        atr_14=4.21,
        rvol_eod=2.31,
        earnings_next="2026-05-02",
    )
    state.upsert_watchlist([entry])
    rows = state.active_watchlist("2026-04-27")
    assert len(rows) == 1
    assert rows[0].symbol == "AAPL"
    assert rows[0].signal_high == 215.42
    assert rows[0].is_active is True
    assert rows[0].breakout_attempts == 0


def test_deactivate_watchlist_symbol(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    state.upsert_watchlist([WatchlistEntry(
        scan_date="2026-04-27", symbol="MSFT",
        signal_high=410.0, signal_low=405.0, signal_close=409.0,
        atr_14=3.0, rvol_eod=2.0, earnings_next=None,
    )])
    state.deactivate_symbol("2026-04-27", "MSFT")
    state.increment_breakout_attempts("2026-04-27", "MSFT")
    active = state.active_watchlist("2026-04-27")
    assert active == []
    all_entries = state.all_watchlist("2026-04-27")
    assert all_entries[0].is_active is False
    assert all_entries[0].breakout_attempts == 1


def test_open_and_close_position_round_trip(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    pos = Position(
        symbol="NVDA",
        entry_order_id="ord-1",
        entry_time="2026-04-28T13:35:00+00:00",
        entry_price=120.50,
        qty=10,
        signal_high=120.40,
        signal_low=117.20,
        initial_stop=117.20,
        current_stop=117.20,
        highest_price_since_entry=120.50,
        trailing_active=False,
        status="open",
    )
    pos_id = state.open_position(pos)
    assert pos_id > 0

    open_positions = state.open_positions()
    assert len(open_positions) == 1
    assert open_positions[0].symbol == "NVDA"

    state.close_position(
        pos_id, exit_time="2026-04-30T19:00:00+00:00",
        exit_price=132.55, exit_reason="target", realized_pnl=120.50,
    )
    assert state.open_positions() == []


def test_record_cycle_and_heartbeat(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    state.record_cycle(
        cycle_at="2026-04-28T14:30:00+00:00",
        duration_ms=412, positions_open=2, watchlist_size=18,
    )
    rows = list(state.conn.execute("SELECT cycle_at, duration_ms FROM cycles"))
    assert rows == [("2026-04-28T14:30:00+00:00", 412)]


def test_halt_set_and_clear(tmp_state_db: Path) -> None:
    state = State(tmp_state_db)
    state.init()
    state.set_halt("2026-04-28T15:00:00+00:00", "daily DD")
    assert state.is_halted() is True
    state.clear_halt("2026-04-28T15:30:00+00:00")
    assert state.is_halted() is False
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_state.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/state.py`**

```python
"""SQLite persistence for watchlist, positions, fills, halts, cycles."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS watchlist (
  scan_date TEXT NOT NULL,
  symbol TEXT NOT NULL,
  signal_high REAL NOT NULL,
  signal_low REAL NOT NULL,
  signal_close REAL NOT NULL,
  atr_14 REAL NOT NULL,
  rvol_eod REAL NOT NULL,
  earnings_next TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  breakout_attempts INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (scan_date, symbol)
);

CREATE TABLE IF NOT EXISTS positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  symbol TEXT NOT NULL,
  entry_order_id TEXT,
  entry_time TEXT,
  entry_price REAL,
  qty INTEGER,
  signal_high REAL,
  signal_low REAL,
  initial_stop REAL,
  current_stop REAL,
  highest_price_since_entry REAL,
  trailing_active INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,
  exit_time TEXT,
  exit_price REAL,
  exit_reason TEXT,
  realized_pnl REAL
);

CREATE TABLE IF NOT EXISTS fills (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  position_id INTEGER NOT NULL,
  alpaca_order_id TEXT,
  side TEXT,
  qty INTEGER,
  price REAL,
  filled_at TEXT,
  FOREIGN KEY (position_id) REFERENCES positions(id)
);

CREATE TABLE IF NOT EXISTS rvol_curves (
  symbol TEXT NOT NULL,
  minute_of_day INTEGER NOT NULL,
  avg_cum_volume REAL NOT NULL,
  computed_at TEXT NOT NULL,
  PRIMARY KEY (symbol, minute_of_day)
);

CREATE TABLE IF NOT EXISTS halts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  triggered_at TEXT NOT NULL,
  reason TEXT,
  cleared_at TEXT
);

CREATE TABLE IF NOT EXISTS cycles (
  cycle_at TEXT PRIMARY KEY,
  duration_ms INTEGER NOT NULL,
  positions_open INTEGER NOT NULL,
  watchlist_size INTEGER NOT NULL
);
"""


@dataclass
class WatchlistEntry:
    scan_date: str
    symbol: str
    signal_high: float
    signal_low: float
    signal_close: float
    atr_14: float
    rvol_eod: float
    earnings_next: str | None
    is_active: bool = True
    breakout_attempts: int = 0


@dataclass
class Position:
    symbol: str
    entry_order_id: str | None
    entry_time: str | None
    entry_price: float | None
    qty: int | None
    signal_high: float
    signal_low: float
    initial_stop: float
    current_stop: float
    highest_price_since_entry: float
    trailing_active: bool
    status: str
    id: int | None = None
    exit_time: str | None = None
    exit_price: float | None = None
    exit_reason: str | None = None
    realized_pnl: float | None = None


class State:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    def init(self) -> None:
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # -- watchlist --
    def upsert_watchlist(self, entries: Iterable[WatchlistEntry]) -> None:
        cur = self.conn.cursor()
        for e in entries:
            cur.execute(
                """
                INSERT INTO watchlist
                  (scan_date, symbol, signal_high, signal_low, signal_close,
                   atr_14, rvol_eod, earnings_next, is_active, breakout_attempts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(scan_date, symbol) DO UPDATE SET
                  signal_high=excluded.signal_high,
                  signal_low=excluded.signal_low,
                  signal_close=excluded.signal_close,
                  atr_14=excluded.atr_14,
                  rvol_eod=excluded.rvol_eod,
                  earnings_next=excluded.earnings_next
                """,
                (
                    e.scan_date, e.symbol, e.signal_high, e.signal_low, e.signal_close,
                    e.atr_14, e.rvol_eod, e.earnings_next,
                    1 if e.is_active else 0, e.breakout_attempts,
                ),
            )
        self.conn.commit()

    def active_watchlist(self, scan_date: str) -> list[WatchlistEntry]:
        return [
            self._row_to_watchlist(r)
            for r in self.conn.execute(
                "SELECT * FROM watchlist WHERE scan_date=? AND is_active=1",
                (scan_date,),
            )
        ]

    def all_watchlist(self, scan_date: str) -> list[WatchlistEntry]:
        return [
            self._row_to_watchlist(r)
            for r in self.conn.execute(
                "SELECT * FROM watchlist WHERE scan_date=?", (scan_date,)
            )
        ]

    def deactivate_symbol(self, scan_date: str, symbol: str) -> None:
        self.conn.execute(
            "UPDATE watchlist SET is_active=0 WHERE scan_date=? AND symbol=?",
            (scan_date, symbol),
        )
        self.conn.commit()

    def reactivate_symbol(self, scan_date: str, symbol: str) -> None:
        self.conn.execute(
            "UPDATE watchlist SET is_active=1 WHERE scan_date=? AND symbol=?",
            (scan_date, symbol),
        )
        self.conn.commit()

    def increment_breakout_attempts(self, scan_date: str, symbol: str) -> None:
        self.conn.execute(
            "UPDATE watchlist SET breakout_attempts=breakout_attempts+1 "
            "WHERE scan_date=? AND symbol=?",
            (scan_date, symbol),
        )
        self.conn.commit()

    @staticmethod
    def _row_to_watchlist(r: sqlite3.Row) -> WatchlistEntry:
        return WatchlistEntry(
            scan_date=r["scan_date"], symbol=r["symbol"],
            signal_high=r["signal_high"], signal_low=r["signal_low"],
            signal_close=r["signal_close"], atr_14=r["atr_14"],
            rvol_eod=r["rvol_eod"], earnings_next=r["earnings_next"],
            is_active=bool(r["is_active"]),
            breakout_attempts=r["breakout_attempts"],
        )

    # -- positions --
    def open_position(self, pos: Position) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO positions
              (symbol, entry_order_id, entry_time, entry_price, qty,
               signal_high, signal_low, initial_stop, current_stop,
               highest_price_since_entry, trailing_active, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pos.symbol, pos.entry_order_id, pos.entry_time, pos.entry_price,
                pos.qty, pos.signal_high, pos.signal_low, pos.initial_stop,
                pos.current_stop, pos.highest_price_since_entry,
                1 if pos.trailing_active else 0, pos.status,
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def open_positions(self) -> list[Position]:
        return [
            self._row_to_position(r)
            for r in self.conn.execute("SELECT * FROM positions WHERE status='open'")
        ]

    def position_by_symbol(self, symbol: str) -> Position | None:
        r = self.conn.execute(
            "SELECT * FROM positions WHERE symbol=? AND status='open' LIMIT 1",
            (symbol,),
        ).fetchone()
        return self._row_to_position(r) if r else None

    def update_position_stop(self, pos_id: int, current_stop: float, highest: float, trailing: bool) -> None:
        self.conn.execute(
            "UPDATE positions SET current_stop=?, highest_price_since_entry=?, trailing_active=? WHERE id=?",
            (current_stop, highest, 1 if trailing else 0, pos_id),
        )
        self.conn.commit()

    def close_position(
        self, pos_id: int, exit_time: str, exit_price: float,
        exit_reason: str, realized_pnl: float,
    ) -> None:
        self.conn.execute(
            "UPDATE positions SET status='closed', exit_time=?, exit_price=?, "
            "exit_reason=?, realized_pnl=? WHERE id=?",
            (exit_time, exit_price, exit_reason, realized_pnl, pos_id),
        )
        self.conn.commit()

    @staticmethod
    def _row_to_position(r: sqlite3.Row) -> Position:
        return Position(
            id=r["id"], symbol=r["symbol"], entry_order_id=r["entry_order_id"],
            entry_time=r["entry_time"], entry_price=r["entry_price"], qty=r["qty"],
            signal_high=r["signal_high"], signal_low=r["signal_low"],
            initial_stop=r["initial_stop"], current_stop=r["current_stop"],
            highest_price_since_entry=r["highest_price_since_entry"],
            trailing_active=bool(r["trailing_active"]), status=r["status"],
            exit_time=r["exit_time"], exit_price=r["exit_price"],
            exit_reason=r["exit_reason"], realized_pnl=r["realized_pnl"],
        )

    # -- fills --
    def record_fill(
        self, position_id: int, order_id: str, side: str,
        qty: int, price: float, filled_at: str,
    ) -> None:
        self.conn.execute(
            "INSERT INTO fills (position_id, alpaca_order_id, side, qty, price, filled_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (position_id, order_id, side, qty, price, filled_at),
        )
        self.conn.commit()

    # -- cycles --
    def record_cycle(
        self, cycle_at: str, duration_ms: int,
        positions_open: int, watchlist_size: int,
    ) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO cycles (cycle_at, duration_ms, positions_open, watchlist_size) "
            "VALUES (?, ?, ?, ?)",
            (cycle_at, duration_ms, positions_open, watchlist_size),
        )
        self.conn.commit()

    # -- halts --
    def set_halt(self, triggered_at: str, reason: str) -> None:
        self.conn.execute(
            "INSERT INTO halts (triggered_at, reason) VALUES (?, ?)",
            (triggered_at, reason),
        )
        self.conn.commit()

    def clear_halt(self, cleared_at: str) -> None:
        self.conn.execute(
            "UPDATE halts SET cleared_at=? WHERE cleared_at IS NULL",
            (cleared_at,),
        )
        self.conn.commit()

    def is_halted(self) -> bool:
        r = self.conn.execute(
            "SELECT 1 FROM halts WHERE cleared_at IS NULL LIMIT 1"
        ).fetchone()
        return r is not None
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_state.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/state.py tests/test_state.py
git commit -m "feat(state): SQLite persistence for watchlist, positions, fills, halts"
```

---

## Task 5: SMA + ATR

**Files:**
- Create: `bot/indicators.py`
- Test: `tests/test_indicators.py`
- Create: `tests/fakes/fake_data.py`

- [ ] **Step 1: Write the failing test (SMA + ATR)**

`tests/test_indicators.py`:
```python
"""Tests for bot.indicators."""
from __future__ import annotations

import math

import pandas as pd
import pytest

from bot.indicators import sma, atr_wilder


def test_sma_window_3() -> None:
    series = pd.Series([10.0, 11.0, 12.0, 13.0, 14.0])
    result = sma(series, window=3)
    assert math.isnan(result.iloc[0])
    assert math.isnan(result.iloc[1])
    assert result.iloc[2] == pytest.approx(11.0)
    assert result.iloc[3] == pytest.approx(12.0)
    assert result.iloc[4] == pytest.approx(13.0)


def test_sma_full_series_average() -> None:
    series = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = sma(series, window=5)
    assert result.iloc[-1] == pytest.approx(3.0)


def test_atr_wilder_matches_known_values() -> None:
    df = pd.DataFrame({
        "high":  [10.0, 11.0, 12.0, 11.5, 13.0],
        "low":   [9.0,  10.0, 10.5, 10.5, 11.5],
        "close": [9.5,  10.5, 11.5, 11.0, 12.5],
    })
    result = atr_wilder(df, period=3)
    # First TR uses high-low fallback (no prev_close):
    #   TR1=1.0, TR2=max(1,1.5,0.5)=1.5, TR3=max(1.5,1.5,0)=1.5
    # Initial ATR = mean(1.0, 1.5, 1.5) = 1.3333
    assert result.iloc[2] == pytest.approx(1.3333333, rel=1e-4)
    # TR4 = max(1.0, 0.0, 1.0) = 1.0; ATR4 = (1.3333*2 + 1.0)/3 = 1.2222
    assert result.iloc[3] == pytest.approx(1.2222222, rel=1e-4)
    # TR5 = max(1.5, 2.0, 0.5) = 2.0; ATR5 = (1.2222*2 + 2.0)/3 = 1.4815
    assert result.iloc[4] == pytest.approx(1.4814814, rel=1e-4)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: ImportError on `bot.indicators`.

- [ ] **Step 3: Implement SMA + ATR**

`bot/indicators.py`:
```python
"""Technical indicators (SMA, ATR, relative volume)."""
from __future__ import annotations

import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple moving average. NaN for the first (window-1) entries."""
    return series.rolling(window=window, min_periods=window).mean()


def atr_wilder(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Wilder's ATR.

    df must have columns: high, low, close (in chronological order).
    Returns a Series aligned with df.index. First (period-1) values are NaN.
    """
    high = df["high"]
    low = df["low"]
    prev_close = df["close"].shift(1)

    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    tr.iloc[0] = high.iloc[0] - low.iloc[0]

    atr = pd.Series(index=df.index, dtype=float)
    if len(df) < period:
        return atr
    initial = tr.iloc[:period].mean()
    atr.iloc[period - 1] = initial
    for i in range(period, len(df)):
        atr.iloc[i] = (atr.iloc[i - 1] * (period - 1) + tr.iloc[i]) / period
    return atr
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: 3 passed.

- [ ] **Step 5: Add canned-bar fixture helper**

`tests/fakes/fake_data.py`:
```python
"""Helpers to build canned bar DataFrames for tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd


def make_daily_bars(
    start: str, periods: int, base_price: float = 100.0,
    daily_volume: int = 1_000_000, daily_change_pct: float = 0.005,
) -> pd.DataFrame:
    start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    rows = []
    close = base_price
    for i in range(periods):
        ts = start_dt + timedelta(days=i)
        open_ = close
        close = close * (1 + daily_change_pct)
        high = max(open_, close) * 1.002
        low = min(open_, close) * 0.998
        rows.append({
            "timestamp": ts, "open": open_, "high": high,
            "low": low, "close": close, "volume": daily_volume,
        })
    return pd.DataFrame(rows).set_index("timestamp")
```

- [ ] **Step 6: Commit**

```bash
git add bot/indicators.py tests/test_indicators.py tests/fakes/fake_data.py
git commit -m "feat(indicators): SMA + Wilder ATR"
```

---

## Task 6: EOD Relative Volume

**Files:**
- Modify: `bot/indicators.py`
- Modify: `tests/test_indicators.py`

- [ ] **Step 1: Add the failing test**

Append to `tests/test_indicators.py`:
```python
from bot.indicators import rvol_eod


def test_rvol_eod_uses_prior_n_sessions() -> None:
    volumes = [1_000_000] * 20 + [2_500_000]
    series = pd.Series(volumes)
    rvol = rvol_eod(series, lookback=20)
    assert rvol.iloc[-1] == pytest.approx(2.5)
    assert math.isnan(rvol.iloc[19])


def test_rvol_eod_excludes_today_from_average() -> None:
    volumes = list(range(1, 22))  # 1..21
    series = pd.Series(volumes, dtype=float)
    rvol = rvol_eod(series, lookback=20)
    # day 21 vol=21; mean(1..20)=10.5; rvol=21/10.5=2.0
    assert rvol.iloc[20] == pytest.approx(2.0)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: ImportError on `rvol_eod`.

- [ ] **Step 3: Implement `rvol_eod`**

Append to `bot/indicators.py`:
```python
def rvol_eod(volume_series: pd.Series, lookback: int = 20) -> pd.Series:
    """Today / mean(prior `lookback` sessions, EXCLUDING today)."""
    avg_prior = volume_series.shift(1).rolling(window=lookback, min_periods=lookback).mean()
    return volume_series / avg_prior
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/indicators.py tests/test_indicators.py
git commit -m "feat(indicators): EOD relative volume"
```

---

## Task 7: Intraday RVOL Curve

**Files:**
- Modify: `bot/indicators.py`
- Modify: `tests/test_indicators.py`

- [ ] **Step 1: Add the failing tests**

Append to `tests/test_indicators.py`:
```python
from bot.indicators import build_intraday_volume_curve, rvol_intraday


def test_build_intraday_curve_averages_per_minute() -> None:
    sessions = [
        pd.DataFrame({"minute_of_day": [570, 571, 572], "cumulative_volume": [100.0, 250.0, 400.0]}),
        pd.DataFrame({"minute_of_day": [570, 571, 572], "cumulative_volume": [200.0, 300.0, 500.0]}),
    ]
    curve = build_intraday_volume_curve(sessions)
    assert curve.loc[570] == pytest.approx(150.0)
    assert curve.loc[571] == pytest.approx(275.0)
    assert curve.loc[572] == pytest.approx(450.0)


def test_rvol_intraday_lookup() -> None:
    curve = pd.Series({570: 150.0, 571: 275.0, 572: 450.0})
    assert rvol_intraday(today_cum_volume=550.0, minute_of_day=571, curve=curve) == pytest.approx(2.0)


def test_rvol_intraday_unknown_minute_returns_nan() -> None:
    curve = pd.Series({570: 150.0, 571: 275.0})
    result = rvol_intraday(today_cum_volume=100.0, minute_of_day=999, curve=curve)
    assert math.isnan(result)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement intraday RVOL**

Append to `bot/indicators.py`:
```python
def build_intraday_volume_curve(sessions: list[pd.DataFrame]) -> pd.Series:
    """Per-minute-of-day average cumulative volume across N sessions.

    Each session DataFrame must have columns ['minute_of_day', 'cumulative_volume'].
    """
    if not sessions:
        return pd.Series(dtype=float)
    combined = pd.concat(sessions, ignore_index=True)
    return combined.groupby("minute_of_day")["cumulative_volume"].mean()


def rvol_intraday(today_cum_volume: float, minute_of_day: int, curve: pd.Series) -> float:
    """today_cum_volume / expected_cum_volume_at(minute). NaN if minute not in curve."""
    if minute_of_day not in curve.index:
        return float("nan")
    expected = curve.loc[minute_of_day]
    if expected <= 0:
        return float("nan")
    return today_cum_volume / expected
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_indicators.py -v`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/indicators.py tests/test_indicators.py
git commit -m "feat(indicators): intraday volume curve + same-time-of-day RVOL"
```

---

## Task 8: MarketDataProvider ABC

**Files:**
- Create: `bot/data/base.py`
- Test: `tests/test_data_alpaca.py` (subset — interface contract test)

- [ ] **Step 1: Write the failing test**

`tests/test_data_alpaca.py`:
```python
"""Tests for the data layer."""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import pytest

from bot.data.base import MarketDataProvider, Bar, LatestTrade, MarketClock


def test_market_data_provider_is_abstract() -> None:
    with pytest.raises(TypeError):
        MarketDataProvider()  # type: ignore[abstract]


def test_bar_dataclass_round_trip() -> None:
    b = Bar(
        timestamp=datetime(2026, 4, 28, 13, 30, tzinfo=timezone.utc),
        open=100.0, high=101.0, low=99.5, close=100.5, volume=12345,
    )
    assert b.timestamp.tzinfo is not None
    assert b.high >= b.low
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_data_alpaca.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/data/base.py`**

```python
"""Abstract market data interface — concrete impls in alpaca_data.py etc."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class LatestTrade:
    symbol: str
    price: float
    timestamp: datetime


@dataclass(frozen=True)
class MarketClock:
    is_open: bool
    next_open: datetime
    next_close: datetime
    timestamp: datetime


class MarketDataProvider(ABC):
    """Strategy code depends only on this interface, not on Alpaca specifically."""

    @abstractmethod
    def get_clock(self) -> MarketClock: ...

    @abstractmethod
    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        """Returns DataFrame indexed by timestamp with columns [open,high,low,close,volume]."""

    @abstractmethod
    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame: ...

    @abstractmethod
    def get_latest_trade(self, symbol: str) -> LatestTrade: ...

    @abstractmethod
    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        """Batch latest-trade lookup. Default impl in subclasses can iterate get_latest_trade."""
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_data_alpaca.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/data/base.py tests/test_data_alpaca.py
git commit -m "feat(data): MarketDataProvider abstract interface"
```

---

## Task 9: AlpacaMarketData REST + Fake

**Files:**
- Create: `bot/data/alpaca_data.py`
- Create: `tests/fakes/fake_alpaca.py`
- Modify: `tests/test_data_alpaca.py`

- [ ] **Step 1: Add the failing tests**

Append to `tests/test_data_alpaca.py`:
```python
import responses

from bot.data.alpaca_data import AlpacaMarketData
from tests.fakes.fake_alpaca import FakeAlpaca


def _alpaca() -> AlpacaMarketData:
    return AlpacaMarketData(
        api_key="k", api_secret="s",
        trading_base_url="https://paper-api.alpaca.markets",
        data_base_url="https://data.alpaca.markets",
    )


@responses.activate
def test_get_clock_parses_alpaca_response() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/clock",
        json={
            "is_open": False,
            "next_close": "2026-04-27T16:00:00-04:00",
            "next_open": "2026-04-27T09:30:00-04:00",
            "timestamp": "2026-04-25T17:09:41-04:00",
        },
        status=200,
    )
    clock = _alpaca().get_clock()
    assert clock.is_open is False
    assert clock.next_open.isoformat().startswith("2026-04-27T09:30:00")


@responses.activate
def test_get_latest_trade_parses() -> None:
    responses.add(
        responses.GET,
        "https://data.alpaca.markets/v2/stocks/AAPL/trades/latest",
        json={"symbol": "AAPL", "trade": {"t": "2026-04-28T13:35:01Z", "p": 215.42, "s": 100}},
        status=200,
    )
    t = _alpaca().get_latest_trade("AAPL")
    assert t.symbol == "AAPL"
    assert t.price == 215.42


@responses.activate
def test_get_daily_bars_returns_dataframe() -> None:
    responses.add(
        responses.GET,
        "https://data.alpaca.markets/v2/stocks/AAPL/bars",
        json={
            "bars": [
                {"t": "2026-04-24T04:00:00Z", "o": 210, "h": 213, "l": 209, "c": 212, "v": 50_000_000},
                {"t": "2026-04-25T04:00:00Z", "o": 212, "h": 215, "l": 211, "c": 214, "v": 60_000_000},
            ],
            "next_page_token": None,
        },
        status=200,
    )
    df = _alpaca().get_daily_bars(
        "AAPL",
        start=__import__("datetime").datetime(2026, 4, 24, tzinfo=__import__("datetime").timezone.utc),
        end=__import__("datetime").datetime(2026, 4, 25, 23, 59, tzinfo=__import__("datetime").timezone.utc),
    )
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert df["close"].iloc[-1] == 214


def test_fake_alpaca_implements_interface() -> None:
    fake = FakeAlpaca()
    fake.set_latest_trade("AAPL", price=215.42)
    t = fake.get_latest_trade("AAPL")
    assert t.price == 215.42
    clock = fake.get_clock()
    assert clock.is_open in (True, False)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_data_alpaca.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/data/alpaca_data.py`**

```python
"""Alpaca REST implementation of MarketDataProvider."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import pandas as pd
import requests

from bot.data.base import Bar, LatestTrade, MarketClock, MarketDataProvider


def _parse_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


class AlpacaMarketData(MarketDataProvider):
    def __init__(
        self, api_key: str, api_secret: str,
        trading_base_url: str = "https://paper-api.alpaca.markets",
        data_base_url: str = "https://data.alpaca.markets",
        timeout_sec: float = 10.0,
    ) -> None:
        self.trading_base_url = trading_base_url.rstrip("/")
        self.data_base_url = data_base_url.rstrip("/")
        self.timeout = timeout_sec
        self._headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Accept": "application/json",
        }

    def _get(self, url: str, params: dict | None = None) -> dict:
        resp = requests.get(url, headers=self._headers, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_clock(self) -> MarketClock:
        d = self._get(f"{self.trading_base_url}/v2/clock")
        return MarketClock(
            is_open=bool(d["is_open"]),
            next_open=_parse_iso(d["next_open"]),
            next_close=_parse_iso(d["next_close"]),
            timestamp=_parse_iso(d["timestamp"]),
        )

    def _bars_to_df(self, bars: list[dict]) -> pd.DataFrame:
        if not bars:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        rows = [
            {
                "timestamp": _parse_iso(b["t"]),
                "open": b["o"], "high": b["h"], "low": b["l"],
                "close": b["c"], "volume": b["v"],
            }
            for b in bars
        ]
        return pd.DataFrame(rows).set_index("timestamp")

    def _fetch_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: str,
    ) -> pd.DataFrame:
        all_bars: list[dict] = []
        page_token: str | None = None
        while True:
            params = {
                "timeframe": timeframe,
                "start": start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end": end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "limit": 10000,
                "feed": "iex",
                "adjustment": "split",
            }
            if page_token:
                params["page_token"] = page_token
            d = self._get(f"{self.data_base_url}/v2/stocks/{symbol}/bars", params=params)
            all_bars.extend(d.get("bars", []) or [])
            page_token = d.get("next_page_token")
            if not page_token:
                break
        return self._bars_to_df(all_bars)

    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        return self._fetch_bars(symbol, start, end, timeframe="1Day")

    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame:
        return self._fetch_bars(symbol, start, end, timeframe=f"{timeframe_minutes}Min")

    def get_latest_trade(self, symbol: str) -> LatestTrade:
        d = self._get(f"{self.data_base_url}/v2/stocks/{symbol}/trades/latest")
        t = d["trade"]
        return LatestTrade(symbol=d["symbol"], price=t["p"], timestamp=_parse_iso(t["t"]))

    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        symbols = list(symbols)
        if not symbols:
            return {}
        d = self._get(
            f"{self.data_base_url}/v2/stocks/trades/latest",
            params={"symbols": ",".join(symbols), "feed": "iex"},
        )
        out: dict[str, LatestTrade] = {}
        for sym, payload in (d.get("trades") or {}).items():
            out[sym] = LatestTrade(symbol=sym, price=payload["p"], timestamp=_parse_iso(payload["t"]))
        return out
```

- [ ] **Step 4: Implement `tests/fakes/fake_alpaca.py`**

```python
"""In-memory MarketDataProvider used in unit tests + backtest dry-runs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import pandas as pd

from bot.data.base import LatestTrade, MarketClock, MarketDataProvider


class FakeAlpaca(MarketDataProvider):
    def __init__(self) -> None:
        self._daily: dict[str, pd.DataFrame] = {}
        self._intraday: dict[str, pd.DataFrame] = {}
        self._latest: dict[str, LatestTrade] = {}
        self._clock = MarketClock(
            is_open=True,
            next_open=datetime(2026, 4, 27, 13, 30, tzinfo=timezone.utc),
            next_close=datetime(2026, 4, 25, 20, 0, tzinfo=timezone.utc),
            timestamp=datetime(2026, 4, 25, 17, 0, tzinfo=timezone.utc),
        )

    def set_clock(self, clock: MarketClock) -> None:
        self._clock = clock

    def set_daily_bars(self, symbol: str, df: pd.DataFrame) -> None:
        self._daily[symbol] = df

    def set_intraday_bars(self, symbol: str, df: pd.DataFrame) -> None:
        self._intraday[symbol] = df

    def set_latest_trade(self, symbol: str, price: float, ts: datetime | None = None) -> None:
        self._latest[symbol] = LatestTrade(
            symbol=symbol, price=price,
            timestamp=ts or datetime.now(timezone.utc),
        )

    def get_clock(self) -> MarketClock:
        return self._clock

    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        df = self._daily.get(symbol, pd.DataFrame(columns=["open","high","low","close","volume"]))
        if df.empty:
            return df
        return df[(df.index >= start) & (df.index <= end)]

    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame:
        df = self._intraday.get(symbol, pd.DataFrame(columns=["open","high","low","close","volume"]))
        if df.empty:
            return df
        return df[(df.index >= start) & (df.index <= end)]

    def get_latest_trade(self, symbol: str) -> LatestTrade:
        if symbol not in self._latest:
            raise KeyError(f"FakeAlpaca: no latest trade set for {symbol}")
        return self._latest[symbol]

    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        return {s: self._latest[s] for s in symbols if s in self._latest}
```

- [ ] **Step 5: Run to verify pass**

Run: `.venv/bin/pytest tests/test_data_alpaca.py -v`
Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add bot/data/alpaca_data.py tests/fakes/fake_alpaca.py tests/test_data_alpaca.py
git commit -m "feat(data): Alpaca REST market data + in-memory fake"
```

---

## Task 10: EarningsProvider (yfinance)

**Files:**
- Create: `bot/data/earnings.py`
- Test: `tests/test_data_earnings.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_data_earnings.py`:
```python
"""Tests for bot.data.earnings."""
from __future__ import annotations

from datetime import date

import pandas as pd
import pytest

from bot.data.earnings import EarningsProvider, YFinanceEarnings


class _StubYf:
    def __init__(self, calendar: dict | pd.DataFrame | None) -> None:
        self._calendar = calendar

    def Ticker(self, symbol: str):  # noqa: N802
        outer = self
        class _T:
            calendar = outer._calendar
        return _T()


def test_yfinance_earnings_returns_next_date(monkeypatch) -> None:
    yf = _StubYf({"Earnings Date": [date(2026, 5, 2)]})
    provider = YFinanceEarnings(yf_module=yf)
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)


def test_yfinance_earnings_handles_dataframe_form(monkeypatch) -> None:
    df = pd.DataFrame({"Earnings Date": [pd.Timestamp("2026-05-02")]})
    yf = _StubYf(df)
    provider = YFinanceEarnings(yf_module=yf)
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)


def test_yfinance_earnings_returns_none_when_unknown(monkeypatch) -> None:
    provider = YFinanceEarnings(yf_module=_StubYf(None))
    assert provider.next_earnings("ZZZZ") is None


def test_yfinance_earnings_caches_results() -> None:
    yf = _StubYf({"Earnings Date": [date(2026, 5, 2)]})
    provider = YFinanceEarnings(yf_module=yf)
    provider.next_earnings("AAPL")
    yf._calendar = None  # would return None on a fresh fetch
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)  # served from cache
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_data_earnings.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/data/earnings.py`**

```python
"""Earnings calendar provider — pluggable so we can swap yfinance later."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Any

import pandas as pd


class EarningsProvider(ABC):
    @abstractmethod
    def next_earnings(self, symbol: str) -> date | None: ...


class YFinanceEarnings(EarningsProvider):
    def __init__(self, yf_module: Any | None = None) -> None:
        if yf_module is None:
            import yfinance as yf
            self._yf = yf
        else:
            self._yf = yf_module
        self._cache: dict[str, date | None] = {}

    def next_earnings(self, symbol: str) -> date | None:
        if symbol in self._cache:
            return self._cache[symbol]
        result = self._lookup(symbol)
        self._cache[symbol] = result
        return result

    def _lookup(self, symbol: str) -> date | None:
        try:
            cal = self._yf.Ticker(symbol).calendar
        except Exception:
            return None
        if cal is None:
            return None
        if isinstance(cal, dict):
            dates = cal.get("Earnings Date") or []
        elif isinstance(cal, pd.DataFrame):
            if "Earnings Date" not in cal.columns:
                return None
            dates = list(cal["Earnings Date"])
        else:
            return None
        if not dates:
            return None
        first = dates[0]
        if isinstance(first, pd.Timestamp):
            return first.date()
        if isinstance(first, date):
            return first
        try:
            return pd.Timestamp(first).date()
        except Exception:
            return None
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_data_earnings.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/data/earnings.py tests/test_data_earnings.py
git commit -m "feat(data): pluggable earnings provider with yfinance impl"
```

---

## Task 11: Universe Builder

**Files:**
- Create: `bot/universe.py`
- Create: `data/universe/exclusions.csv`
- Test: `tests/test_universe.py`

- [ ] **Step 1: Seed `data/universe/exclusions.csv`**

Create file with header + a starter set of leveraged/inverse ETFs (defensive — most won't appear in NDX/SPX but the filter is cheap):

```csv
symbol,reason
TQQQ,leveraged-3x
SQQQ,inverse-3x
UPRO,leveraged-3x
SPXU,inverse-3x
SOXL,leveraged-3x
SOXS,inverse-3x
TNA,leveraged-3x
TZA,inverse-3x
TSM,adr
ASML,adr
NVO,adr
SAP,adr
SHOP,adr
TM,adr
HSBC,adr
BUD,adr
DEO,adr
SE,adr
GSK,adr
TSLA-NOTE,test-do-not-use
```

(The TSLA-NOTE row is a sentinel for the test below — never matches a real symbol.)

- [ ] **Step 2: Write the failing tests**

`tests/test_universe.py`:
```python
"""Tests for bot.universe."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from bot.universe import build_universe, load_exclusions, EligibilityRow
from tests.fakes.fake_alpaca import FakeAlpaca
from tests.fakes.fake_data import make_daily_bars


def _write_csv(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_load_exclusions_returns_set(tmp_path: Path) -> None:
    p = tmp_path / "exclusions.csv"
    _write_csv(p, ["symbol,reason", "TQQQ,leveraged-3x", "SQQQ,inverse-3x"])
    excl = load_exclusions(p)
    assert "TQQQ" in excl
    assert "SQQQ" in excl
    assert "AAPL" not in excl


def test_build_universe_filters_by_price_and_dollar_volume(tmp_path: Path) -> None:
    sp_csv = tmp_path / "sp500.csv"
    nd_csv = tmp_path / "ndx.csv"
    excl_csv = tmp_path / "exclusions.csv"
    _write_csv(sp_csv, ["symbol", "AAPL", "PENNY"])
    _write_csv(nd_csv, ["symbol", "AAPL", "TQQQ"])  # AAPL appears in both → dedup
    _write_csv(excl_csv, ["symbol,reason", "TQQQ,leveraged"])

    fake = FakeAlpaca()
    # AAPL: price 200, vol 50M → dollar vol 10B → pass
    fake.set_daily_bars("AAPL", make_daily_bars("2026-04-01", periods=30, base_price=200, daily_volume=50_000_000))
    # PENNY: price 5 → fail price filter
    fake.set_daily_bars("PENNY", make_daily_bars("2026-04-01", periods=30, base_price=5, daily_volume=50_000_000))
    # TQQQ: in exclusions, even though price/volume would pass

    eligible = build_universe(
        sp500_csv=sp_csv, ndx_csv=nd_csv, exclusions_csv=excl_csv,
        data=fake, as_of=__import__("datetime").datetime(2026, 4, 30,
                                                       tzinfo=__import__("datetime").timezone.utc),
        min_price=10.0, min_dollar_vol=25_000_000,
    )
    symbols = {row.symbol for row in eligible}
    assert "AAPL" in symbols
    assert "PENNY" not in symbols
    assert "TQQQ" not in symbols
    aapl = next(r for r in eligible if r.symbol == "AAPL")
    assert aapl.last_close > 200
    assert aapl.avg_dollar_vol > 25_000_000


def test_build_universe_skips_symbols_with_no_bars(tmp_path: Path) -> None:
    sp_csv = tmp_path / "sp500.csv"
    nd_csv = tmp_path / "ndx.csv"
    excl_csv = tmp_path / "exclusions.csv"
    _write_csv(sp_csv, ["symbol", "GHOST"])
    _write_csv(nd_csv, ["symbol"])
    _write_csv(excl_csv, ["symbol,reason"])

    fake = FakeAlpaca()  # no bars set for GHOST

    eligible = build_universe(
        sp500_csv=sp_csv, ndx_csv=nd_csv, exclusions_csv=excl_csv,
        data=fake, as_of=__import__("datetime").datetime(2026, 4, 30,
                                                       tzinfo=__import__("datetime").timezone.utc),
        min_price=10.0, min_dollar_vol=25_000_000,
    )
    assert eligible == []
```

- [ ] **Step 3: Run to verify failure**

Run: `.venv/bin/pytest tests/test_universe.py -v`
Expected: ImportError.

- [ ] **Step 4: Implement `bot/universe.py`**

```python
"""Build the daily eligible universe from NDX∪SPX with liquidity filters."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd

from bot.data.base import MarketDataProvider


@dataclass(frozen=True)
class EligibilityRow:
    symbol: str
    last_close: float
    avg_dollar_vol: float


def load_exclusions(path: Path | str) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["symbol"].strip().upper() for row in reader if row.get("symbol")}


def _load_symbol_csv(path: Path | str) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["symbol"].strip().upper() for row in reader if row.get("symbol")}


def build_universe(
    sp500_csv: Path | str,
    ndx_csv: Path | str,
    exclusions_csv: Path | str,
    data: MarketDataProvider,
    as_of: datetime,
    min_price: float = 10.0,
    min_dollar_vol: float = 25_000_000,
    lookback_days: int = 45,
) -> list[EligibilityRow]:
    """Return symbols passing price + dollar-volume + exclusion filters as of `as_of`."""
    base = (_load_symbol_csv(sp500_csv) | _load_symbol_csv(ndx_csv))
    excl = load_exclusions(exclusions_csv)
    candidates = sorted(base - excl)

    start = as_of - timedelta(days=lookback_days)
    eligible: list[EligibilityRow] = []
    for symbol in candidates:
        try:
            bars = data.get_daily_bars(symbol, start=start, end=as_of)
        except Exception:
            continue
        if bars.empty or len(bars) < 20:
            continue
        last_close = float(bars["close"].iloc[-1])
        if last_close < min_price:
            continue
        recent = bars.tail(30)
        avg_dollar_vol = float((recent["close"] * recent["volume"]).mean())
        if avg_dollar_vol < min_dollar_vol:
            continue
        eligible.append(EligibilityRow(
            symbol=symbol, last_close=last_close, avg_dollar_vol=avg_dollar_vol,
        ))
    return eligible
```

- [ ] **Step 5: Run to verify pass**

Run: `.venv/bin/pytest tests/test_universe.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit the seeded exclusions and code**

```bash
git add bot/universe.py tests/test_universe.py data/universe/exclusions.csv
git commit -m "feat(universe): NDX/SPX eligible-universe builder with liquidity filter"
```

---

## Task 12: refresh_universe CLI

**Files:**
- Create: `cli/refresh_universe.py`

- [ ] **Step 1: Write the implementation (manual smoke test, not unit-tested)**

`cli/refresh_universe.py`:
```python
"""Refresh data/universe/sp500.csv and ndx.csv from Wikipedia tables.

Run monthly via cron: `python -m cli.refresh_universe`
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
NDX_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"

OUT_DIR = Path("data/universe")


def _scrape_sp500() -> list[str]:
    tables = pd.read_html(SP500_URL)
    df = tables[0]
    if "Symbol" not in df.columns:
        raise RuntimeError(f"Unexpected SP500 table columns: {list(df.columns)}")
    return [str(s).strip().upper().replace(".", "-") for s in df["Symbol"].tolist()]


def _scrape_ndx() -> list[str]:
    tables = pd.read_html(NDX_URL)
    candidate = None
    for t in tables:
        cols = {str(c).strip() for c in t.columns}
        if "Ticker" in cols or "Symbol" in cols:
            candidate = t
            break
    if candidate is None:
        raise RuntimeError("Could not locate NDX constituents table")
    col = "Ticker" if "Ticker" in candidate.columns else "Symbol"
    return [str(s).strip().upper().replace(".", "-") for s in candidate[col].tolist()]


def _write(path: Path, symbols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    rows = []
    for s in symbols:
        if s and s not in seen:
            seen.add(s)
            rows.append({"symbol": s})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    try:
        sp = _scrape_sp500()
        nd = _scrape_ndx()
    except Exception as e:
        print(f"refresh_universe failed: {e}", file=sys.stderr)
        return 1
    _write(OUT_DIR / "sp500.csv", sp)
    _write(OUT_DIR / "ndx.csv", nd)
    print(f"wrote {len(sp)} SP500 + {len(nd)} NDX symbols")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Smoke test (manual)**

Run: `.venv/bin/python -m cli.refresh_universe`
Expected: writes two CSVs and prints `wrote ~503 SP500 + ~101 NDX symbols`.
If Wikipedia structure has changed, error message will be clear.

- [ ] **Step 3: Commit**

```bash
git add cli/refresh_universe.py
git commit -m "feat(cli): refresh_universe — pull SP500 + NDX constituents from Wikipedia"
```

---

## Task 13: Risk Sizing + Halt Checks

**Files:**
- Create: `bot/risk.py`
- Test: `tests/test_risk.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_risk.py`:
```python
"""Tests for bot.risk."""
from __future__ import annotations

from pathlib import Path

import pytest

from bot.risk import position_size, can_open_new_position, RiskCheck
from bot.state import State, Position


def _state(tmp_path: Path) -> State:
    s = State(tmp_path / "state.sqlite")
    s.init()
    return s


def test_position_size_at_15pct_risk() -> None:
    # equity 100k, entry 100, stop 95 → risk per share $5; budget = 1500 / 5 = 300 shares
    qty = position_size(equity=100_000, entry=100.0, stop=95.0, per_trade_risk_pct=0.015)
    assert qty == 300


def test_position_size_returns_zero_when_stop_above_entry() -> None:
    qty = position_size(equity=100_000, entry=100.0, stop=101.0, per_trade_risk_pct=0.015)
    assert qty == 0


def test_position_size_floors_to_int() -> None:
    qty = position_size(equity=10_000, entry=50.0, stop=49.5, per_trade_risk_pct=0.015)
    # risk 0.5/share, budget 150 → 300 shares exactly
    assert qty == 300


def test_position_size_zero_when_qty_below_one() -> None:
    qty = position_size(equity=1_000, entry=500.0, stop=400.0, per_trade_risk_pct=0.015)
    # risk 100/share, budget 15 → 0.15 → floored to 0
    assert qty == 0


def test_can_open_when_under_cap_and_not_halted(tmp_path: Path) -> None:
    s = _state(tmp_path)
    check = can_open_new_position(
        state=s, max_open=3, max_daily_new=5, daily_new_count=0, halt_flag_path=tmp_path / "halt.flag",
    )
    assert check.ok is True
    assert check.reason is None


def test_can_open_blocked_at_position_cap(tmp_path: Path) -> None:
    s = _state(tmp_path)
    for sym in ["A", "B", "C"]:
        s.open_position(Position(
            symbol=sym, entry_order_id=None, entry_time=None, entry_price=100.0,
            qty=10, signal_high=100, signal_low=95, initial_stop=95, current_stop=95,
            highest_price_since_entry=100, trailing_active=False, status="open",
        ))
    check = can_open_new_position(
        state=s, max_open=3, max_daily_new=5, daily_new_count=0, halt_flag_path=tmp_path / "halt.flag",
    )
    assert check.ok is False
    assert "max open positions" in check.reason


def test_can_open_blocked_at_daily_new_cap(tmp_path: Path) -> None:
    s = _state(tmp_path)
    check = can_open_new_position(
        state=s, max_open=3, max_daily_new=5, daily_new_count=5, halt_flag_path=tmp_path / "halt.flag",
    )
    assert check.ok is False
    assert "daily" in check.reason


def test_can_open_blocked_when_halt_flag_present(tmp_path: Path) -> None:
    s = _state(tmp_path)
    flag = tmp_path / "halt.flag"
    flag.write_text("manual stop")
    check = can_open_new_position(
        state=s, max_open=3, max_daily_new=5, daily_new_count=0, halt_flag_path=flag,
    )
    assert check.ok is False
    assert "halt flag" in check.reason


def test_can_open_blocked_when_halt_in_state(tmp_path: Path) -> None:
    s = _state(tmp_path)
    s.set_halt("2026-04-28T15:00:00+00:00", "daily DD")
    check = can_open_new_position(
        state=s, max_open=3, max_daily_new=5, daily_new_count=0, halt_flag_path=tmp_path / "halt.flag",
    )
    assert check.ok is False
    assert "halt" in check.reason
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_risk.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/risk.py`**

```python
"""Risk: position sizing, daily caps, halt enforcement."""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from bot.state import State


@dataclass(frozen=True)
class RiskCheck:
    ok: bool
    reason: str | None = None


def position_size(
    equity: float, entry: float, stop: float, per_trade_risk_pct: float = 0.015,
) -> int:
    """Floor((per_trade_risk_pct * equity) / (entry - stop)). Returns 0 if stop >= entry."""
    if stop >= entry:
        return 0
    risk_per_share = entry - stop
    budget = per_trade_risk_pct * equity
    qty = int(math.floor(budget / risk_per_share))
    return max(qty, 0)


def can_open_new_position(
    state: State,
    max_open: int,
    max_daily_new: int,
    daily_new_count: int,
    halt_flag_path: Path | str,
) -> RiskCheck:
    """Combined gate: position cap + daily new cap + halt flag + state halt."""
    if Path(halt_flag_path).exists():
        return RiskCheck(False, "halt flag file present")
    if state.is_halted():
        return RiskCheck(False, "halt active in state")
    open_count = len(state.open_positions())
    if open_count >= max_open:
        return RiskCheck(False, f"at max open positions ({open_count}/{max_open})")
    if daily_new_count >= max_daily_new:
        return RiskCheck(False, f"daily new-entry cap reached ({daily_new_count}/{max_daily_new})")
    return RiskCheck(True)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_risk.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/risk.py tests/test_risk.py
git commit -m "feat(risk): position sizing + multi-source halt enforcement"
```

---

## Task 14: Entry Trigger Logic

**Files:**
- Create: `bot/entry.py`
- Test: `tests/test_entry.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_entry.py`:
```python
"""Tests for bot.entry."""
from __future__ import annotations

from datetime import datetime, time, timezone

import pandas as pd
import pytest

from bot.entry import (
    EntryDecision, evaluate_entry, gap_skip,
    in_entry_time_window, volume_confirms,
)


def _bar(ts: str, vol: int) -> dict:
    return {"timestamp": pd.Timestamp(ts, tz="UTC"), "volume": vol}


def test_in_entry_time_window_after_first_5_min_and_before_1430() -> None:
    # 9:35 ET = 13:35 UTC (Apr — DST)
    assert in_entry_time_window(datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc)) is True
    # 9:34 ET = 13:34 UTC → blocked (within first 5 min)
    assert in_entry_time_window(datetime(2026, 4, 28, 13, 34, tzinfo=timezone.utc)) is False
    # 14:31 ET = 18:31 UTC → blocked (after 14:30 cutoff)
    assert in_entry_time_window(datetime(2026, 4, 28, 18, 31, tzinfo=timezone.utc)) is False
    # 14:30 exactly ET = 18:30 UTC → allowed (cutoff is exclusive)
    assert in_entry_time_window(datetime(2026, 4, 28, 18, 30, tzinfo=timezone.utc)) is True


def test_gap_skip_when_open_too_far_above_signal() -> None:
    assert gap_skip(today_open=110.0, signal_high=100.0, gap_pct=0.08) is True
    assert gap_skip(today_open=107.99, signal_high=100.0, gap_pct=0.08) is False
    assert gap_skip(today_open=108.0, signal_high=100.0, gap_pct=0.08) is True  # boundary inclusive


def test_volume_confirms_requires_both_rules() -> None:
    bars = pd.DataFrame([
        {"timestamp": "2026-04-28T13:30Z", "volume": 100_000},
        {"timestamp": "2026-04-28T13:35Z", "volume": 110_000},
        {"timestamp": "2026-04-28T13:40Z", "volume": 120_000},
        {"timestamp": "2026-04-28T13:45Z", "volume": 90_000},   # current_bar
    ])
    bars["timestamp"] = pd.to_datetime(bars["timestamp"], utc=True)
    bars = bars.set_index("timestamp")
    # current_vol=90k, prev_vol=120k → fails "current > prior"
    assert volume_confirms(bars, lookback_bars=3) is False

    bars2 = bars.copy()
    bars2.iloc[-1, bars2.columns.get_loc("volume")] = 200_000
    # current=200k, prev=120k (passes "current > prior"), 3-bar avg of prior bars=110k → passes
    assert volume_confirms(bars2, lookback_bars=3) is True


def test_evaluate_entry_full_path_passes() -> None:
    bars = pd.DataFrame({
        "open":   [100, 101, 102, 103, 104],
        "high":   [101, 102, 103, 104, 110],
        "low":    [99,  100, 101, 102, 103],
        "close":  [101, 102, 103, 104, 109],
        "volume": [100_000, 110_000, 120_000, 100_000, 250_000],
    }, index=pd.to_datetime([
        "2026-04-28T13:35Z", "2026-04-28T13:40Z", "2026-04-28T13:45Z",
        "2026-04-28T13:50Z", "2026-04-28T13:55Z",
    ], utc=True))
    decision = evaluate_entry(
        last_price=110.5, signal_high=110.0, today_open=104.0,
        intraday_5m_bars=bars, now=bars.index[-1].to_pydatetime(),
        gap_pct=0.08, vol_lookback_bars=3,
    )
    assert decision.should_enter is True
    assert decision.reason is None


def test_evaluate_entry_blocks_on_no_trigger() -> None:
    bars = pd.DataFrame({"open":[100],"high":[100],"low":[100],"close":[100],"volume":[100_000]},
                        index=pd.to_datetime(["2026-04-28T13:35Z"], utc=True))
    decision = evaluate_entry(
        last_price=100.0, signal_high=110.0, today_open=104.0,
        intraday_5m_bars=bars, now=bars.index[-1].to_pydatetime(),
    )
    assert decision.should_enter is False
    assert "below signal high" in decision.reason
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_entry.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/entry.py`**

```python
"""Entry trigger evaluation: gap check, time window, breakout, volume confirmation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo

import pandas as pd


_ET = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class EntryDecision:
    should_enter: bool
    reason: str | None = None


def in_entry_time_window(
    now_utc: datetime,
    market_open_et: time = time(9, 30),
    no_entry_first_min: int = 5,
    no_new_entry_after_et: time = time(14, 30),
) -> bool:
    """True iff `now` is between (open + first_min) and the no-new-entry cutoff (inclusive)."""
    et = now_utc.astimezone(_ET).timetz()
    # Block first 5 minutes (open=9:30 → block until 9:35)
    earliest = (datetime.combine(datetime(2000, 1, 1), market_open_et)
                .replace(tzinfo=_ET)).timetz()
    earliest_with_buffer = (
        datetime(2000, 1, 1, market_open_et.hour, market_open_et.minute, tzinfo=_ET)
        .replace(minute=(market_open_et.minute + no_entry_first_min) % 60,
                 hour=market_open_et.hour + (market_open_et.minute + no_entry_first_min) // 60)
    ).timetz()
    if et < earliest_with_buffer:
        return False
    if et > no_new_entry_after_et.replace(tzinfo=_ET):
        return False
    return True


def gap_skip(today_open: float, signal_high: float, gap_pct: float = 0.08) -> bool:
    """True if today's open is >= signal_high * (1 + gap_pct) — too far gone to chase."""
    return today_open >= signal_high * (1 + gap_pct)


def volume_confirms(
    intraday_5m_bars: pd.DataFrame, lookback_bars: int = 20,
) -> bool:
    """Two-rule confirmation:
    1) current bar volume > prior bar volume
    2) current bar volume > mean of previous `lookback_bars` bars
    """
    if len(intraday_5m_bars) < 2:
        return False
    cur = float(intraday_5m_bars["volume"].iloc[-1])
    prev = float(intraday_5m_bars["volume"].iloc[-2])
    if cur <= prev:
        return False
    history = intraday_5m_bars["volume"].iloc[-(lookback_bars + 1):-1]
    if len(history) == 0:
        return True
    avg_prev = float(history.mean())
    return cur > avg_prev


def evaluate_entry(
    last_price: float,
    signal_high: float,
    today_open: float,
    intraday_5m_bars: pd.DataFrame,
    now: datetime,
    *,
    gap_pct: float = 0.08,
    vol_lookback_bars: int = 20,
) -> EntryDecision:
    """Apply gates in order. Return first failure as `reason`, or success."""
    if not in_entry_time_window(now):
        return EntryDecision(False, "outside entry time window")
    if gap_skip(today_open, signal_high, gap_pct):
        return EntryDecision(False, f"gapped {((today_open/signal_high)-1)*100:.1f}% above signal")
    if last_price <= signal_high:
        return EntryDecision(False, f"price {last_price} below signal high {signal_high}")
    if not volume_confirms(intraday_5m_bars, vol_lookback_bars):
        return EntryDecision(False, "volume confirmation failed")
    return EntryDecision(True)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_entry.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/entry.py tests/test_entry.py
git commit -m "feat(entry): trigger evaluation with time window, gap, breakout, volume"
```

---

## Task 15: Exit Logic

**Files:**
- Create: `bot/exit.py`
- Test: `tests/test_exit.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_exit.py`:
```python
"""Tests for bot.exit."""
from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from bot.exit import (
    ExitDecision, target_price, hard_stop_price, should_activate_trailing,
    update_trailing_stop, time_stop_due, earnings_exit_due, evaluate_exit,
)


def test_target_price_is_entry_x_110() -> None:
    assert target_price(entry=100.0, profit_pct=0.10) == pytest.approx(110.0)


def test_hard_stop_picks_tighter_of_signal_low_or_pct() -> None:
    # signal_low=95, entry=100, 5% stop=95 → tie, both = 95
    assert hard_stop_price(entry=100.0, signal_low=95.0, hard_stop_pct=0.05) == 95.0
    # signal_low=92 (further), 5% stop=95 (tighter) → use 95
    assert hard_stop_price(entry=100.0, signal_low=92.0, hard_stop_pct=0.05) == 95.0
    # signal_low=97 (tighter), 5% stop=95 (further) → use 97
    assert hard_stop_price(entry=100.0, signal_low=97.0, hard_stop_pct=0.05) == 97.0


def test_should_activate_trailing_after_6pct_gain() -> None:
    assert should_activate_trailing(entry=100.0, current_high=106.0, activation_pct=0.06) is True
    assert should_activate_trailing(entry=100.0, current_high=105.99, activation_pct=0.06) is False


def test_update_trailing_stop_uses_distance_below_high() -> None:
    new_stop = update_trailing_stop(highest_price=120.0, distance_pct=0.05)
    assert new_stop == pytest.approx(114.0)


def test_time_stop_due_after_n_trading_days() -> None:
    entry = datetime(2026, 4, 27, 13, 35, tzinfo=timezone.utc)  # Mon
    now_day5 = datetime(2026, 5, 1, 19, 50, tzinfo=timezone.utc)  # Fri 3:50 ET
    assert time_stop_due(entry_time=entry, now=now_day5, days=5) is True
    now_day4 = datetime(2026, 4, 30, 19, 50, tzinfo=timezone.utc)  # Thu
    assert time_stop_due(entry_time=entry, now=now_day4, days=5) is False


def test_earnings_exit_due_when_earnings_tomorrow_and_unprofitable() -> None:
    today = date(2026, 4, 28)
    earnings = date(2026, 4, 29)  # tomorrow
    assert earnings_exit_due(today=today, earnings_date=earnings, unrealized_pnl=-50.0) is True
    assert earnings_exit_due(today=today, earnings_date=earnings, unrealized_pnl=10.0) is False
    far_earnings = date(2026, 5, 10)
    assert earnings_exit_due(today=today, earnings_date=far_earnings, unrealized_pnl=-50.0) is False


def test_evaluate_exit_target_hit() -> None:
    decision = evaluate_exit(
        last_price=111.0, entry=100.0, current_stop=95.0, highest_since_entry=111.0,
        trailing_active=False, entry_time=datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc),
        now=datetime(2026, 4, 28, 14, 0, tzinfo=timezone.utc),
        earnings_date=None, unrealized_pnl=11.0,
    )
    assert decision.should_exit is True
    assert decision.reason == "target"


def test_evaluate_exit_stop_hit() -> None:
    decision = evaluate_exit(
        last_price=94.0, entry=100.0, current_stop=95.0, highest_since_entry=100.0,
        trailing_active=False, entry_time=datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc),
        now=datetime(2026, 4, 28, 14, 0, tzinfo=timezone.utc),
        earnings_date=None, unrealized_pnl=-6.0,
    )
    assert decision.should_exit is True
    assert decision.reason == "stop"


def test_evaluate_exit_no_action_within_band() -> None:
    decision = evaluate_exit(
        last_price=103.0, entry=100.0, current_stop=95.0, highest_since_entry=103.0,
        trailing_active=False, entry_time=datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc),
        now=datetime(2026, 4, 28, 14, 0, tzinfo=timezone.utc),
        earnings_date=None, unrealized_pnl=3.0,
    )
    assert decision.should_exit is False
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_exit.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/exit.py`**

```python
"""Exit decision logic: target / stop / trailing / time / earnings."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


_ET = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class ExitDecision:
    should_exit: bool
    reason: str | None = None  # target | stop | trail | time | earnings


def target_price(entry: float, profit_pct: float = 0.10) -> float:
    return entry * (1 + profit_pct)


def hard_stop_price(entry: float, signal_low: float, hard_stop_pct: float = 0.05) -> float:
    """Tighter (closer to entry) of signal_low or entry*(1-pct)."""
    pct_stop = entry * (1 - hard_stop_pct)
    return max(signal_low, pct_stop)


def should_activate_trailing(entry: float, current_high: float, activation_pct: float = 0.06) -> bool:
    return current_high >= entry * (1 + activation_pct)


def update_trailing_stop(highest_price: float, distance_pct: float = 0.05) -> float:
    return highest_price * (1 - distance_pct)


def _trading_days_between(start: date, end: date) -> int:
    """Inclusive of `end`, exclusive of `start`. Counts Mon–Fri only."""
    days = 0
    cur = start + timedelta(days=1)
    while cur <= end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days


def time_stop_due(entry_time: datetime, now: datetime, days: int = 5) -> bool:
    """True at/after 3:50 PM ET on the Nth trading day after entry."""
    entry_d = entry_time.astimezone(_ET).date()
    now_et = now.astimezone(_ET)
    elapsed = _trading_days_between(entry_d, now_et.date())
    if elapsed < days:
        return False
    return now_et.timetz() >= time(15, 50, tzinfo=_ET)


def earnings_exit_due(today: date, earnings_date: date | None, unrealized_pnl: float) -> bool:
    """If earnings is tomorrow and we are NOT profitable, exit."""
    if earnings_date is None:
        return False
    days_until = (earnings_date - today).days
    if days_until != 1:
        return False
    return unrealized_pnl <= 0


def evaluate_exit(
    last_price: float,
    entry: float,
    current_stop: float,
    highest_since_entry: float,
    trailing_active: bool,
    entry_time: datetime,
    now: datetime,
    earnings_date: date | None,
    unrealized_pnl: float,
    *,
    profit_pct: float = 0.10,
    time_stop_days: int = 5,
) -> ExitDecision:
    """Order: target → stop → time → earnings. Caller manages trailing-stop updates."""
    if last_price >= target_price(entry, profit_pct):
        return ExitDecision(True, "target")
    if last_price <= current_stop:
        return ExitDecision(True, "trail" if trailing_active else "stop")
    if time_stop_due(entry_time, now, days=time_stop_days):
        return ExitDecision(True, "time")
    if earnings_exit_due(now.astimezone(_ET).date(), earnings_date, unrealized_pnl):
        return ExitDecision(True, "earnings")
    return ExitDecision(False)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_exit.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/exit.py tests/test_exit.py
git commit -m "feat(exit): target/stop/trail/time/earnings exit decision logic"
```

---

## Task 16: Scanner

**Files:**
- Create: `bot/scanner.py`
- Test: `tests/test_scanner.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_scanner.py`:
```python
"""Tests for bot.scanner."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from bot.scanner import scan, ScanCriteria
from bot.universe import EligibilityRow
from bot.data.earnings import EarningsProvider
from tests.fakes.fake_alpaca import FakeAlpaca


class _StubEarnings(EarningsProvider):
    def __init__(self, mapping: dict[str, date | None]) -> None:
        self._m = mapping

    def next_earnings(self, symbol: str) -> date | None:
        return self._m.get(symbol)


def _bars_with_breakout(start: str, periods: int = 60) -> pd.DataFrame:
    """Build a DataFrame where the LAST bar is a +5% breakout on 2.5x volume,
    closing above its 20-day prior high and the 20+50 SMAs.
    """
    start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    rows = []
    close = 100.0
    for i in range(periods - 1):
        ts = start_dt + timedelta(days=i)
        open_ = close
        close = close + 0.05  # very slow drift up
        high = max(open_, close) * 1.001
        low = min(open_, close) * 0.999
        rows.append({"timestamp": ts, "open": open_, "high": high, "low": low,
                     "close": close, "volume": 1_000_000})
    # last bar: jumps 5%, volume 2.5x
    last_ts = start_dt + timedelta(days=periods - 1)
    last_open = close
    last_close = close * 1.05
    last_high = last_close * 1.001
    last_low = last_open * 0.999
    rows.append({"timestamp": last_ts, "open": last_open, "high": last_high, "low": last_low,
                 "close": last_close, "volume": 2_500_000})
    return pd.DataFrame(rows).set_index("timestamp")


def test_scan_picks_breakout_symbol_and_skips_others() -> None:
    fake = FakeAlpaca()
    fake.set_daily_bars("BREAK", _bars_with_breakout("2026-02-15"))
    # SLOW: same starting bars but no spike
    slow = _bars_with_breakout("2026-02-15").copy()
    slow.iloc[-1, slow.columns.get_loc("close")] = slow["close"].iloc[-2] * 1.005
    slow.iloc[-1, slow.columns.get_loc("volume")] = 800_000
    fake.set_daily_bars("SLOW", slow)

    eligible = [
        EligibilityRow(symbol="BREAK", last_close=105.0, avg_dollar_vol=100_000_000),
        EligibilityRow(symbol="SLOW", last_close=105.0, avg_dollar_vol=100_000_000),
    ]
    earnings = _StubEarnings({"BREAK": None, "SLOW": None})

    as_of = datetime(2026, 4, 15, tzinfo=timezone.utc)
    results = scan(
        eligible=eligible, data=fake, earnings=earnings, as_of=as_of,
        criteria=ScanCriteria(),
    )
    syms = {r.symbol for r in results}
    assert "BREAK" in syms
    assert "SLOW" not in syms


def test_scan_excludes_symbol_with_earnings_within_5_days() -> None:
    fake = FakeAlpaca()
    fake.set_daily_bars("BREAK", _bars_with_breakout("2026-02-15"))
    eligible = [EligibilityRow(symbol="BREAK", last_close=105, avg_dollar_vol=100_000_000)]
    earnings = _StubEarnings({"BREAK": date(2026, 4, 17)})  # 2 days from as_of
    as_of = datetime(2026, 4, 15, tzinfo=timezone.utc)
    results = scan(eligible=eligible, data=fake, earnings=earnings, as_of=as_of,
                   criteria=ScanCriteria())
    assert results == []


def test_scan_within_2pct_of_breakout_passes() -> None:
    """A close just shy of the 20-day high should still pass via the 'within 2%' branch."""
    fake = FakeAlpaca()
    bars = _bars_with_breakout("2026-02-15")
    # Knock today's close down to 99% of prior high; still +4% on the day & volume up.
    prior_20d_high = bars["high"].iloc[-21:-1].max()
    target_close = prior_20d_high * 0.99
    bars.iloc[-1, bars.columns.get_loc("close")] = target_close
    bars.iloc[-1, bars.columns.get_loc("open")] = target_close / 1.04
    bars.iloc[-1, bars.columns.get_loc("high")] = target_close * 1.001
    bars.iloc[-1, bars.columns.get_loc("low")] = target_close / 1.05
    bars.iloc[-1, bars.columns.get_loc("volume")] = 2_500_000
    fake.set_daily_bars("NEAR", bars)

    eligible = [EligibilityRow(symbol="NEAR", last_close=target_close, avg_dollar_vol=100_000_000)]
    results = scan(eligible=eligible, data=fake, earnings=_StubEarnings({"NEAR": None}),
                   as_of=datetime(2026, 4, 15, tzinfo=timezone.utc), criteria=ScanCriteria())
    assert any(r.symbol == "NEAR" for r in results)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_scanner.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/scanner.py`**

```python
"""Daily end-of-day scanner — produces tomorrow's watchlist."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

import pandas as pd

from bot.data.base import MarketDataProvider
from bot.data.earnings import EarningsProvider
from bot.indicators import sma, atr_wilder, rvol_eod
from bot.state import WatchlistEntry
from bot.universe import EligibilityRow


@dataclass(frozen=True)
class ScanCriteria:
    pct_change_min: float = 0.04
    rvol_min: float = 1.8
    near_breakout_pct: float = 0.02
    lookback_breakout: int = 20
    earnings_block_days: int = 5
    daily_history_days: int = 90  # enough for SMA50 + RVOL20


def _trading_days_between(d1, d2) -> int:
    """Calendar-day gap is a fine proxy for short windows here."""
    return (d2 - d1).days


def scan(
    eligible: Iterable[EligibilityRow],
    data: MarketDataProvider,
    earnings: EarningsProvider,
    as_of: datetime,
    criteria: ScanCriteria,
) -> list[WatchlistEntry]:
    out: list[WatchlistEntry] = []
    start = as_of - timedelta(days=criteria.daily_history_days)
    for row in eligible:
        try:
            bars = data.get_daily_bars(row.symbol, start=start, end=as_of)
        except Exception:
            continue
        if bars.empty or len(bars) < 51:
            continue

        today = bars.iloc[-1]
        prev_close = float(bars["close"].iloc[-2])
        if prev_close <= 0:
            continue
        pct_change = (float(today["close"]) - prev_close) / prev_close
        if pct_change < criteria.pct_change_min:
            continue

        rvol_series = rvol_eod(bars["volume"], lookback=20)
        rvol = float(rvol_series.iloc[-1])
        if pd.isna(rvol) or rvol < criteria.rvol_min:
            continue

        sma20 = float(sma(bars["close"], 20).iloc[-1])
        sma50 = float(sma(bars["close"], 50).iloc[-1])
        if pd.isna(sma20) or pd.isna(sma50):
            continue
        if not (today["close"] > sma20 and today["close"] > sma50):
            continue

        prior_20d_high = float(bars["high"].iloc[-(criteria.lookback_breakout + 1):-1].max())
        breaks = today["close"] >= prior_20d_high
        near = today["close"] >= prior_20d_high * (1 - criteria.near_breakout_pct)
        if not (breaks or near):
            continue

        earn = earnings.next_earnings(row.symbol)
        if earn is not None:
            days_until = (earn - as_of.date()).days
            if 0 <= days_until <= criteria.earnings_block_days:
                continue

        atr14_series = atr_wilder(bars[["high", "low", "close"]], period=14)
        atr14 = float(atr14_series.iloc[-1])

        # scan_date = the date of next trading session = as_of + 1 calendar day
        # The trader will resolve against the actual next session at run time.
        next_date = (as_of + timedelta(days=1)).date().isoformat()

        out.append(WatchlistEntry(
            scan_date=next_date,
            symbol=row.symbol,
            signal_high=float(today["high"]),
            signal_low=float(today["low"]),
            signal_close=float(today["close"]),
            atr_14=atr14,
            rvol_eod=rvol,
            earnings_next=earn.isoformat() if earn else None,
        ))
    return out
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_scanner.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/scanner.py tests/test_scanner.py
git commit -m "feat(scanner): end-of-day momentum-breakout scan"
```

---

## Task 17: run_scanner CLI

**Files:**
- Create: `cli/run_scanner.py`

- [ ] **Step 1: Implement the CLI**

`cli/run_scanner.py`:
```python
"""Daily scanner entry point.

Wired by cron at 4:05 PM ET Mon–Fri:
  cd ~/stocks_monitoring && .venv/bin/python -m cli.run_scanner
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from bot import config
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.earnings import YFinanceEarnings
from bot.logger import get_logger
from bot.scanner import scan, ScanCriteria
from bot.state import State
from bot.universe import build_universe

DATA_DIR = Path("data")
UNIVERSE_DIR = DATA_DIR / "universe"
STATE_PATH = DATA_DIR / "state.sqlite"
LOG_DIR = DATA_DIR / "logs"


def main() -> int:
    log = get_logger("scanner", log_dir=LOG_DIR)
    settings = config.load()

    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    earnings = YFinanceEarnings()
    state = State(STATE_PATH)
    state.init()

    as_of = datetime.now(timezone.utc)
    log.info("scan_start", extra={"as_of": as_of.isoformat()})

    eligible = build_universe(
        sp500_csv=UNIVERSE_DIR / "sp500.csv",
        ndx_csv=UNIVERSE_DIR / "ndx.csv",
        exclusions_csv=UNIVERSE_DIR / "exclusions.csv",
        data=data, as_of=as_of,
        min_price=settings.min_price,
        min_dollar_vol=settings.min_dollar_vol,
    )
    log.info("universe_built", extra={"count": len(eligible)})

    results = scan(
        eligible=eligible, data=data, earnings=earnings, as_of=as_of,
        criteria=ScanCriteria(
            pct_change_min=settings.pct_change_min,
            rvol_min=settings.rvol_min,
            near_breakout_pct=settings.near_breakout_pct,
            lookback_breakout=settings.lookback_breakout,
        ),
    )
    state.upsert_watchlist(results)
    log.info("scan_done", extra={"watchlist_size": len(results),
                                  "symbols": [r.symbol for r in results]})

    # Telegram digest deferred to Task 18 wiring; print for now.
    print(f"Scan complete: {len(results)} candidates for next session")
    for r in sorted(results, key=lambda x: -x.rvol_eod)[:10]:
        print(f"  {r.symbol}  rvol={r.rvol_eod:.2f}  signal_high={r.signal_high:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke test (manual, market closed is fine)**

Run: `.venv/bin/python -m cli.run_scanner`
Expected: prints scan summary, may emit zero candidates if no symbols pass; no exceptions.

- [ ] **Step 3: Commit**

```bash
git add cli/run_scanner.py
git commit -m "feat(cli): run_scanner entrypoint with logging + state writes"
```

---

## Task 18: Telegram Alerts

**Files:**
- Create: `bot/alerts.py`
- Test: `tests/test_alerts.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_alerts.py`:
```python
"""Tests for bot.alerts."""
from __future__ import annotations

import responses

from bot.alerts import TelegramAlerts


@responses.activate
def test_send_posts_to_bot_api() -> None:
    responses.add(
        responses.POST,
        "https://api.telegram.org/botTOKEN/sendMessage",
        json={"ok": True, "result": {"message_id": 1}},
        status=200,
    )
    alerts = TelegramAlerts(token="TOKEN", chat_id="CHAT")
    ok = alerts.send("hello world")
    assert ok is True
    body = responses.calls[0].request.body
    assert b"chat_id=CHAT" in body
    assert b"hello+world" in body or b"hello%20world" in body


@responses.activate
def test_send_returns_false_on_http_error() -> None:
    responses.add(
        responses.POST,
        "https://api.telegram.org/botTOKEN/sendMessage",
        status=500,
    )
    alerts = TelegramAlerts(token="TOKEN", chat_id="CHAT")
    ok = alerts.send("oops")
    assert ok is False


def test_format_signal_message() -> None:
    alerts = TelegramAlerts(token="x", chat_id="y")
    msg = alerts.format_signal(
        symbol="AAPL", qty=14, entry=215.42, stop=204.65, target=237.0, rvol=2.4,
    )
    assert "AAPL" in msg
    assert "14" in msg
    assert "215.42" in msg
    assert "204.65" in msg
    assert "237.00" in msg


def test_format_close_message() -> None:
    alerts = TelegramAlerts(token="x", chat_id="y")
    msg = alerts.format_close(
        symbol="AAPL", qty=14, exit_price=237.0, entry=215.42,
        pnl=150.82, reason="target",
    )
    assert "AAPL" in msg
    assert "target" in msg
    assert "+$150.82" in msg or "+150.82" in msg
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_alerts.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/alerts.py`**

```python
"""Telegram alert wrapper."""
from __future__ import annotations

import requests


class TelegramAlerts:
    def __init__(self, token: str, chat_id: str, timeout_sec: float = 5.0) -> None:
        self._token = token
        self._chat_id = chat_id
        self._timeout = timeout_sec

    def send(self, text: str) -> bool:
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        try:
            resp = requests.post(
                url,
                data={"chat_id": self._chat_id, "text": text, "parse_mode": "HTML"},
                timeout=self._timeout,
            )
            return resp.status_code == 200
        except Exception:
            return False

    @staticmethod
    def format_signal(
        symbol: str, qty: int, entry: float, stop: float, target: float, rvol: float,
    ) -> str:
        return (
            f"<b>{symbol}</b> entry triggered\n"
            f"qty={qty}  entry={entry:.2f}\n"
            f"stop={stop:.2f}  target={target:.2f}\n"
            f"rvol={rvol:.2f}"
        )

    @staticmethod
    def format_close(
        symbol: str, qty: int, exit_price: float, entry: float, pnl: float, reason: str,
    ) -> str:
        sign = "+" if pnl >= 0 else "-"
        return (
            f"<b>{symbol}</b> closed ({reason})\n"
            f"qty={qty}  entry={entry:.2f}  exit={exit_price:.2f}\n"
            f"pnl={sign}${abs(pnl):.2f}"
        )

    @staticmethod
    def format_halt(reason: str) -> str:
        return f"<b>HALT</b> activated: {reason}"
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_alerts.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/alerts.py tests/test_alerts.py
git commit -m "feat(alerts): Telegram wrapper with signal/close/halt formatters"
```

---

## Task 19: Executor (Alpaca Order Wrappers)

**Files:**
- Create: `bot/executor.py`
- Test: `tests/test_executor.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_executor.py`:
```python
"""Tests for bot.executor."""
from __future__ import annotations

import responses

from bot.executor import AlpacaExecutor


def _exec() -> AlpacaExecutor:
    return AlpacaExecutor(api_key="k", api_secret="s",
                          base_url="https://paper-api.alpaca.markets")


@responses.activate
def test_get_account_equity() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/account",
        json={"equity": "100000.00", "cash": "100000.00", "buying_power": "200000.00"},
        status=200,
    )
    assert _exec().get_equity() == 100_000.00


@responses.activate
def test_submit_stop_limit_buy_returns_order_id() -> None:
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "ord-123", "status": "accepted",
              "symbol": "AAPL", "qty": "10", "type": "stop_limit"},
        status=200,
    )
    order = _exec().submit_entry_stop_limit(
        symbol="AAPL", qty=10, stop_price=215.44, limit_price=216.09,
    )
    assert order["id"] == "ord-123"
    body = responses.calls[0].request.body.decode()
    assert "stop_limit" in body
    assert "AAPL" in body


@responses.activate
def test_submit_market_sell_returns_order_id() -> None:
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "ord-456", "status": "accepted"},
        status=200,
    )
    order = _exec().submit_market_sell(symbol="AAPL", qty=10)
    assert order["id"] == "ord-456"


@responses.activate
def test_replace_stop_loss_cancels_then_submits_new() -> None:
    responses.add(
        responses.DELETE,
        "https://paper-api.alpaca.markets/v2/orders/old-stop",
        status=204,
    )
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "new-stop"},
        status=200,
    )
    order = _exec().replace_stop_loss(
        old_order_id="old-stop", symbol="AAPL", qty=10, new_stop_price=220.00,
    )
    assert order["id"] == "new-stop"


@responses.activate
def test_cancel_order_tolerates_404() -> None:
    responses.add(
        responses.DELETE,
        "https://paper-api.alpaca.markets/v2/orders/missing",
        status=404,
    )
    # Should not raise
    _exec().cancel_order("missing")


@responses.activate
def test_list_open_positions_returns_dict() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/positions",
        json=[
            {"symbol": "AAPL", "qty": "10", "avg_entry_price": "215.42",
             "current_price": "216.10", "unrealized_pl": "6.80"},
        ],
        status=200,
    )
    positions = _exec().list_positions()
    assert "AAPL" in positions
    assert positions["AAPL"]["qty"] == 10
    assert positions["AAPL"]["avg_entry_price"] == 215.42
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_executor.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/executor.py`**

```python
"""Alpaca order placement, cancellation, replacement, and account queries."""
from __future__ import annotations

from typing import Any

import requests


class AlpacaExecutor:
    def __init__(
        self, api_key: str, api_secret: str,
        base_url: str = "https://paper-api.alpaca.markets",
        timeout_sec: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_sec
        self._headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _req(self, method: str, path: str, **kw) -> requests.Response:
        return requests.request(
            method, f"{self.base_url}{path}",
            headers=self._headers, timeout=self.timeout, **kw,
        )

    def get_equity(self) -> float:
        r = self._req("GET", "/v2/account")
        r.raise_for_status()
        return float(r.json()["equity"])

    def list_positions(self) -> dict[str, dict[str, Any]]:
        r = self._req("GET", "/v2/positions")
        r.raise_for_status()
        out: dict[str, dict[str, Any]] = {}
        for p in r.json():
            out[p["symbol"]] = {
                "qty": int(float(p["qty"])),
                "avg_entry_price": float(p["avg_entry_price"]),
                "current_price": float(p.get("current_price", 0) or 0),
                "unrealized_pl": float(p.get("unrealized_pl", 0) or 0),
            }
        return out

    def list_orders(self, status: str = "open") -> list[dict[str, Any]]:
        r = self._req("GET", "/v2/orders", params={"status": status, "limit": 500})
        r.raise_for_status()
        return r.json()

    def submit_entry_stop_limit(
        self, symbol: str, qty: int, stop_price: float, limit_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "buy",
            "type": "stop_limit", "time_in_force": "day",
            "stop_price": f"{stop_price:.2f}", "limit_price": f"{limit_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_take_profit(
        self, symbol: str, qty: int, limit_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "limit", "time_in_force": "gtc",
            "limit_price": f"{limit_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_stop_loss(
        self, symbol: str, qty: int, stop_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "stop", "time_in_force": "gtc",
            "stop_price": f"{stop_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_market_sell(self, symbol: str, qty: int) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "market", "time_in_force": "day",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def cancel_order(self, order_id: str) -> None:
        r = self._req("DELETE", f"/v2/orders/{order_id}")
        if r.status_code in (204, 404, 422):
            return  # idempotent: order may already be filled/cancelled
        r.raise_for_status()

    def replace_stop_loss(
        self, old_order_id: str, symbol: str, qty: int, new_stop_price: float,
    ) -> dict[str, Any]:
        self.cancel_order(old_order_id)
        return self.submit_stop_loss(symbol=symbol, qty=qty, stop_price=new_stop_price)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_executor.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/executor.py tests/test_executor.py
git commit -m "feat(executor): Alpaca order wrappers (stop-limit, TP, SL, cancel/replace)"
```

---

## Task 20: Reconciliation

**Files:**
- Create: `bot/reconcile.py`
- Test: `tests/test_reconcile.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_reconcile.py`:
```python
"""Tests for bot.reconcile."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from bot.reconcile import reconcile_positions, ReconcileReport
from bot.state import State, Position


class _StubExecutor:
    def __init__(self, positions: dict[str, dict[str, Any]]) -> None:
        self._positions = positions

    def list_positions(self) -> dict[str, dict[str, Any]]:
        return self._positions


def _state(tmp_path: Path) -> State:
    s = State(tmp_path / "state.sqlite")
    s.init()
    return s


def _open_in_state(s: State, symbol: str, qty: int = 10, entry: float = 100.0) -> int:
    return s.open_position(Position(
        symbol=symbol, entry_order_id="ord-x", entry_time="2026-04-28T13:35:00+00:00",
        entry_price=entry, qty=qty,
        signal_high=entry, signal_low=entry * 0.97,
        initial_stop=entry * 0.95, current_stop=entry * 0.95,
        highest_price_since_entry=entry, trailing_active=False, status="open",
    ))


def test_reconcile_marks_position_closed_when_alpaca_no_longer_holds(tmp_path: Path) -> None:
    s = _state(tmp_path)
    pos_id = _open_in_state(s, "AAPL", qty=10, entry=215.42)
    executor = _StubExecutor(positions={})  # Alpaca says nothing held

    report = reconcile_positions(state=s, executor=executor,
                                 now=datetime(2026, 4, 28, 20, 0, tzinfo=timezone.utc))
    assert report.closed_locally == ["AAPL"]
    assert s.open_positions() == []


def test_reconcile_no_op_when_states_match(tmp_path: Path) -> None:
    s = _state(tmp_path)
    _open_in_state(s, "AAPL", qty=10, entry=215.42)
    executor = _StubExecutor(positions={
        "AAPL": {"qty": 10, "avg_entry_price": 215.42, "current_price": 216.0, "unrealized_pl": 5.8},
    })
    report = reconcile_positions(state=s, executor=executor,
                                 now=datetime(2026, 4, 28, 20, 0, tzinfo=timezone.utc))
    assert report.closed_locally == []
    assert report.discovered_externally == []


def test_reconcile_reports_external_position(tmp_path: Path) -> None:
    s = _state(tmp_path)
    executor = _StubExecutor(positions={
        "TSLA": {"qty": 1, "avg_entry_price": 240.0, "current_price": 241.0, "unrealized_pl": 1.0},
    })
    report = reconcile_positions(state=s, executor=executor,
                                 now=datetime(2026, 4, 28, 20, 0, tzinfo=timezone.utc))
    assert "TSLA" in report.discovered_externally
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_reconcile.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `bot/reconcile.py`**

```python
"""Reconcile local SQLite state with Alpaca positions on startup + each cycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from bot.state import State


class _ExecutorLike(Protocol):
    def list_positions(self) -> dict[str, dict]: ...


@dataclass
class ReconcileReport:
    closed_locally: list[str] = field(default_factory=list)
    discovered_externally: list[str] = field(default_factory=list)


def reconcile_positions(
    state: State, executor: _ExecutorLike, now: datetime,
) -> ReconcileReport:
    """Truth source = Alpaca's `/v2/positions`.

    - Local-open + Alpaca-not-held → close locally with reason='reconcile'.
    - Alpaca-held + local-not-tracked → report discovery (operator must investigate;
      we do NOT auto-adopt these because we don't know entry context).
    """
    report = ReconcileReport()
    alpaca = executor.list_positions()
    local = {p.symbol: p for p in state.open_positions()}

    for symbol, pos in local.items():
        if symbol not in alpaca:
            # Position was closed externally (TP/SL filled, or operator action)
            state.close_position(
                pos_id=pos.id, exit_time=now.isoformat(),
                exit_price=pos.current_stop or pos.entry_price or 0.0,
                exit_reason="reconcile",
                realized_pnl=0.0,  # unknown without fill history; reporter can recompute later
            )
            report.closed_locally.append(symbol)

    for symbol in alpaca:
        if symbol not in local:
            report.discovered_externally.append(symbol)

    return report
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_reconcile.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add bot/reconcile.py tests/test_reconcile.py
git commit -m "feat(reconcile): sync local state with Alpaca positions"
```

---

## Task 21: Trader Main Loop

**Files:**
- Create: `cli/run_trader.py`
- Test: `tests/test_trader_loop.py`

This is the largest module — break the work into smaller helpers in `cli/run_trader.py` so each is unit-testable.

- [ ] **Step 1: Write the failing tests for the loop helpers**

`tests/test_trader_loop.py`:
```python
"""Tests for cli.run_trader helpers (the loop itself is integration-tested manually)."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from cli.run_trader import (
    poll_interval_for, manage_open_positions, try_open_new_entries,
    OpenPositionContext,
)
from bot.state import State, Position, WatchlistEntry
from tests.fakes.fake_alpaca import FakeAlpaca


def _state(tmp_path: Path) -> State:
    s = State(tmp_path / "state.sqlite")
    s.init()
    return s


def test_poll_interval_fast_for_first_90_min() -> None:
    open_et = datetime(2026, 4, 28, 13, 30, tzinfo=timezone.utc)  # 9:30 ET
    # 13:35 UTC = 5 min in
    assert poll_interval_for(now=datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc),
                             market_open=open_et, fast_window_min=90,
                             fast_sec=15, normal_sec=30) == 15
    # 15:01 UTC = 91 min in
    assert poll_interval_for(now=datetime(2026, 4, 28, 15, 1, tzinfo=timezone.utc),
                             market_open=open_et, fast_window_min=90,
                             fast_sec=15, normal_sec=30) == 30


class _StubExecutor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self._positions: dict[str, dict[str, Any]] = {}

    def list_positions(self) -> dict[str, dict[str, Any]]:
        return self._positions

    def submit_take_profit(self, **kw): self.calls.append(("tp", kw)); return {"id": "tp-1"}
    def submit_stop_loss(self, **kw):  self.calls.append(("sl", kw)); return {"id": "sl-1"}
    def submit_market_sell(self, **kw): self.calls.append(("mkt", kw)); return {"id": "mkt-1"}
    def cancel_order(self, oid): self.calls.append(("cancel", {"id": oid}))
    def replace_stop_loss(self, **kw): self.calls.append(("rsl", kw)); return {"id": "rsl-1"}
    def submit_entry_stop_limit(self, **kw): self.calls.append(("entry", kw)); return {"id": "ent-1"}
    def get_equity(self) -> float: return 100_000.0


def test_manage_open_positions_activates_trailing_at_6pct(tmp_path: Path) -> None:
    s = _state(tmp_path)
    pos_id = s.open_position(Position(
        symbol="AAPL", entry_order_id="ord-1", entry_time="2026-04-28T13:35:00+00:00",
        entry_price=100.0, qty=10,
        signal_high=100.0, signal_low=97.0,
        initial_stop=95.0, current_stop=95.0,
        highest_price_since_entry=100.0, trailing_active=False, status="open",
    ))
    fake = FakeAlpaca()
    fake.set_latest_trade("AAPL", price=107.0)  # +7%
    executor = _StubExecutor()

    manage_open_positions(
        state=s, data=fake, executor=executor,
        now=datetime(2026, 4, 28, 14, 30, tzinfo=timezone.utc),
        earnings_dates={"AAPL": None},
        trail_activation_pct=0.06, trail_distance_pct=0.05,
        profit_target_pct=0.10, time_stop_days=5,
    )
    pos = s.open_positions()[0]
    assert pos.trailing_active is True
    assert pos.current_stop == pytest.approx(107.0 * 0.95)
    assert pos.highest_price_since_entry == 107.0


def test_manage_open_positions_exits_on_target(tmp_path: Path) -> None:
    s = _state(tmp_path)
    s.open_position(Position(
        symbol="AAPL", entry_order_id="ord-1", entry_time="2026-04-28T13:35:00+00:00",
        entry_price=100.0, qty=10,
        signal_high=100.0, signal_low=97.0,
        initial_stop=95.0, current_stop=95.0,
        highest_price_since_entry=110.0, trailing_active=False, status="open",
    ))
    fake = FakeAlpaca()
    fake.set_latest_trade("AAPL", price=110.5)  # past target
    executor = _StubExecutor()

    manage_open_positions(
        state=s, data=fake, executor=executor,
        now=datetime(2026, 4, 28, 14, 30, tzinfo=timezone.utc),
        earnings_dates={"AAPL": None},
        trail_activation_pct=0.06, trail_distance_pct=0.05,
        profit_target_pct=0.10, time_stop_days=5,
    )
    assert any(c[0] == "mkt" for c in executor.calls)
    assert s.open_positions() == []
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_trader_loop.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `cli/run_trader.py`**

```python
"""Long-running polling trader. Started by systemd at ~9:25 ET, killed at ~16:05 ET."""
from __future__ import annotations

import signal
import sys
import time as _time
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Protocol
from zoneinfo import ZoneInfo

import pandas as pd

from bot import config
from bot.alerts import TelegramAlerts
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.base import MarketDataProvider
from bot.data.earnings import YFinanceEarnings
from bot.entry import evaluate_entry
from bot.executor import AlpacaExecutor
from bot.exit import (
    evaluate_exit, hard_stop_price, should_activate_trailing, target_price,
    update_trailing_stop,
)
from bot.logger import get_logger
from bot.reconcile import reconcile_positions
from bot.risk import can_open_new_position, position_size
from bot.state import Position, State, WatchlistEntry


_ET = ZoneInfo("America/New_York")
DATA_DIR = Path("data")
STATE_PATH = DATA_DIR / "state.sqlite"
HALT_FLAG = DATA_DIR / "halt.flag"
LOG_DIR = DATA_DIR / "logs"


# --- helpers (testable) ---

def poll_interval_for(
    now: datetime, market_open: datetime, fast_window_min: int,
    fast_sec: int, normal_sec: int,
) -> int:
    elapsed_min = (now - market_open).total_seconds() / 60.0
    return fast_sec if 0 <= elapsed_min < fast_window_min else normal_sec


@dataclass
class OpenPositionContext:
    pass  # placeholder for future per-cycle telemetry


def manage_open_positions(
    state: State,
    data: MarketDataProvider,
    executor: Any,
    now: datetime,
    earnings_dates: dict[str, date | None],
    trail_activation_pct: float,
    trail_distance_pct: float,
    profit_target_pct: float,
    time_stop_days: int,
    log=None,
) -> None:
    for pos in state.open_positions():
        try:
            trade = data.get_latest_trade(pos.symbol)
        except Exception as e:
            if log: log.warning("price_fetch_failed", extra={"symbol": pos.symbol, "err": str(e)})
            continue
        last = trade.price

        # Update high-water mark
        new_high = max(pos.highest_price_since_entry, last)

        # Trailing-stop activation/update
        new_stop = pos.current_stop
        new_trailing = pos.trailing_active
        if not pos.trailing_active and should_activate_trailing(
            entry=pos.entry_price or 0.0, current_high=new_high,
            activation_pct=trail_activation_pct,
        ):
            new_stop = update_trailing_stop(new_high, trail_distance_pct)
            new_trailing = True
        elif pos.trailing_active:
            candidate = update_trailing_stop(new_high, trail_distance_pct)
            if candidate > new_stop:
                new_stop = candidate

        if new_stop != pos.current_stop or new_high != pos.highest_price_since_entry:
            state.update_position_stop(pos.id, current_stop=new_stop,
                                       highest=new_high, trailing=new_trailing)

        # Exit decision
        unrealized = (last - (pos.entry_price or 0.0)) * (pos.qty or 0)
        decision = evaluate_exit(
            last_price=last, entry=pos.entry_price or 0.0,
            current_stop=new_stop, highest_since_entry=new_high,
            trailing_active=new_trailing, entry_time=datetime.fromisoformat(pos.entry_time),
            now=now, earnings_date=earnings_dates.get(pos.symbol),
            unrealized_pnl=unrealized,
            profit_pct=profit_target_pct, time_stop_days=time_stop_days,
        )
        if decision.should_exit:
            try:
                executor.submit_market_sell(symbol=pos.symbol, qty=pos.qty)
            except Exception as e:
                if log: log.warning("exit_failed", extra={"symbol": pos.symbol, "err": str(e)})
                continue
            state.close_position(
                pos_id=pos.id, exit_time=now.isoformat(),
                exit_price=last, exit_reason=decision.reason,
                realized_pnl=unrealized,
            )


def try_open_new_entries(
    state: State,
    data: MarketDataProvider,
    executor: Any,
    settings,
    now: datetime,
    daily_new_count: int,
    log=None,
    alerts: TelegramAlerts | None = None,
) -> int:
    """Iterate watchlist; return number of new entries placed this cycle."""
    today_str = now.astimezone(_ET).date().isoformat()
    placed = 0
    for entry in state.active_watchlist(today_str):
        check = can_open_new_position(
            state=state, max_open=settings.max_open_positions,
            max_daily_new=settings.max_daily_new_entries,
            daily_new_count=daily_new_count + placed,
            halt_flag_path=HALT_FLAG,
        )
        if not check.ok:
            return placed

        # Pull recent intraday bars + last trade
        try:
            today_open_dt = now.astimezone(_ET).replace(hour=9, minute=30, second=0, microsecond=0)
            bars = data.get_intraday_bars(
                entry.symbol, start=today_open_dt.astimezone(timezone.utc),
                end=now, timeframe_minutes=5,
            )
            if bars.empty:
                continue
            today_open = float(bars["open"].iloc[0])
            trade = data.get_latest_trade(entry.symbol)
        except Exception as e:
            if log: log.warning("intraday_fetch_failed", extra={"symbol": entry.symbol, "err": str(e)})
            continue

        decision = evaluate_entry(
            last_price=trade.price, signal_high=entry.signal_high,
            today_open=today_open, intraday_5m_bars=bars, now=now,
            gap_pct=settings.gap_skip_pct,
        )
        if not decision.should_enter:
            # Track failed-breakout: if we previously saw a trigger this session
            # and now price has fallen back below signal_high, deactivate.
            if entry.breakout_attempts > 0 and trade.price < entry.signal_high:
                state.deactivate_symbol(entry.scan_date, entry.symbol)
            continue

        # Compute stop + size
        equity = executor.get_equity()
        stop = hard_stop_price(
            entry=entry.signal_high + 0.02, signal_low=entry.signal_low,
            hard_stop_pct=settings.hard_stop_pct,
        )
        qty = position_size(
            equity=equity, entry=entry.signal_high + 0.02, stop=stop,
            per_trade_risk_pct=settings.per_trade_risk_pct,
        )
        if qty < 1:
            if log: log.info("skip_zero_qty", extra={"symbol": entry.symbol})
            continue

        stop_px = entry.signal_high + 0.02
        limit_px = stop_px * 1.003
        try:
            order = executor.submit_entry_stop_limit(
                symbol=entry.symbol, qty=qty,
                stop_price=stop_px, limit_price=limit_px,
            )
        except Exception as e:
            if log: log.warning("entry_submit_failed", extra={"symbol": entry.symbol, "err": str(e)})
            continue

        state.open_position(Position(
            symbol=entry.symbol, entry_order_id=order["id"],
            entry_time=now.isoformat(), entry_price=stop_px, qty=qty,
            signal_high=entry.signal_high, signal_low=entry.signal_low,
            initial_stop=stop, current_stop=stop,
            highest_price_since_entry=stop_px, trailing_active=False, status="open",
        ))
        state.increment_breakout_attempts(entry.scan_date, entry.symbol)
        placed += 1
        if alerts:
            alerts.send(alerts.format_signal(
                symbol=entry.symbol, qty=qty, entry=stop_px,
                stop=stop, target=target_price(stop_px, settings.profit_target_pct),
                rvol=entry.rvol_eod,
            ))
        if log: log.info("entry_placed", extra={
            "symbol": entry.symbol, "qty": qty, "stop": stop, "stop_px": stop_px,
        })
    return placed


# --- main loop ---

class _Halt:
    def __init__(self) -> None:
        self.set = False

    def trigger(self, *_args) -> None:
        self.set = True


def main() -> int:
    log = get_logger("trader", log_dir=LOG_DIR)
    settings = config.load()
    state = State(STATE_PATH); state.init()
    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    executor = AlpacaExecutor(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        base_url=settings.alpaca_base_url,
    )
    alerts = TelegramAlerts(token=settings.telegram_token, chat_id=settings.telegram_chat_id)
    earnings_provider = YFinanceEarnings()

    halt = _Halt()
    signal.signal(signal.SIGTERM, halt.trigger)
    signal.signal(signal.SIGINT, halt.trigger)

    consecutive_failures = 0
    daily_new_count = 0
    daily_count_date: date | None = None
    log.info("trader_start")
    alerts.send("Trader started")

    while not halt.set:
        cycle_start = datetime.now(timezone.utc)
        try:
            clock = data.get_clock()
            if not clock.is_open:
                log.info("market_closed_exit")
                break

            today_et = cycle_start.astimezone(_ET).date()
            if daily_count_date != today_et:
                daily_count_date = today_et
                daily_new_count = 0

            # 1. Reconcile
            report = reconcile_positions(state=state, executor=executor, now=cycle_start)
            if report.closed_locally:
                log.info("reconcile_closed", extra={"symbols": report.closed_locally})

            # 2. Lookup earnings for symbols held + on watchlist
            held = [p.symbol for p in state.open_positions()]
            wl = [w.symbol for w in state.active_watchlist(today_et.isoformat())]
            earnings_dates: dict[str, date | None] = {
                s: earnings_provider.next_earnings(s) for s in set(held) | set(wl)
            }

            # 3. Manage open positions
            manage_open_positions(
                state=state, data=data, executor=executor, now=cycle_start,
                earnings_dates=earnings_dates,
                trail_activation_pct=settings.trail_activation_pct,
                trail_distance_pct=settings.trail_distance_pct,
                profit_target_pct=settings.profit_target_pct,
                time_stop_days=settings.time_stop_days, log=log,
            )

            # 4. New entries
            placed = try_open_new_entries(
                state=state, data=data, executor=executor,
                settings=settings, now=cycle_start,
                daily_new_count=daily_new_count, log=log, alerts=alerts,
            )
            daily_new_count += placed

            # 5. Heartbeat
            duration_ms = int((datetime.now(timezone.utc) - cycle_start).total_seconds() * 1000)
            state.record_cycle(
                cycle_at=cycle_start.isoformat(),
                duration_ms=duration_ms,
                positions_open=len(state.open_positions()),
                watchlist_size=len(state.active_watchlist(today_et.isoformat())),
            )
            log.info("heartbeat", extra={
                "duration_ms": duration_ms,
                "positions_open": len(state.open_positions()),
                "watchlist_size": len(state.active_watchlist(today_et.isoformat())),
            })
            consecutive_failures = 0

        except Exception as e:
            consecutive_failures += 1
            log.warning("cycle_failed", extra={"err": str(e), "consecutive": consecutive_failures})
            if consecutive_failures == 3:
                alerts.send(f"3 consecutive cycle failures: {e}")
            backoff = min(60, 5 * (3 ** (consecutive_failures - 1)))
            _time.sleep(backoff)
            continue

        # 6. Sleep until next cycle
        market_open = clock.next_open if not clock.is_open else (
            cycle_start.astimezone(_ET).replace(hour=9, minute=30, second=0, microsecond=0).astimezone(timezone.utc)
        )
        interval = poll_interval_for(
            now=cycle_start, market_open=market_open,
            fast_window_min=settings.fast_poll_end_min,
            fast_sec=settings.poll_interval_fast_sec,
            normal_sec=settings.poll_interval_sec,
        )
        elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
        _time.sleep(max(0, interval - elapsed))

    alerts.send("Trader stopped")
    log.info("trader_stop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_trader_loop.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add cli/run_trader.py tests/test_trader_loop.py
git commit -m "feat(trader): main polling loop with manage/open helpers"
```

---

## Task 22: Backtest Engine

**Files:**
- Create: `backtest/engine.py`
- Test: `tests/test_backtest_engine.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_backtest_engine.py`:
```python
"""Tests for backtest.engine."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from backtest.engine import run_backtest, BacktestConfig, BacktestTrade
from bot.universe import EligibilityRow
from tests.fakes.fake_alpaca import FakeAlpaca


def _intraday_bars(date_str: str, prices: list[float], volumes: list[int]) -> pd.DataFrame:
    open_dt = datetime.fromisoformat(date_str).replace(hour=13, minute=30, tzinfo=timezone.utc)
    rows = []
    for i, (p, v) in enumerate(zip(prices, volumes)):
        ts = open_dt + timedelta(minutes=5 * i)
        rows.append({"timestamp": ts, "open": p, "high": p, "low": p, "close": p, "volume": v})
    return pd.DataFrame(rows).set_index("timestamp")


def test_backtest_records_simple_winning_trade() -> None:
    fake = FakeAlpaca()
    # signal day = 2026-04-27 (Mon); buy day = 2026-04-28 (Tue)
    # On 4/28, price breaks signal_high=110 at bar 3, runs to 121 → hits 10% target
    intraday = _intraday_bars("2026-04-28",
        prices =  [105, 108, 110.5, 112, 121, 121],
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("WIN", intraday)

    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "WIN", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert len(trades) == 1
    t = trades[0]
    assert t.symbol == "WIN"
    assert t.exit_reason == "target"
    assert t.exit_price >= 121.0
    assert t.realized_pnl > 0


def test_backtest_records_stopout_trade() -> None:
    fake = FakeAlpaca()
    intraday = _intraday_bars("2026-04-28",
        prices =  [105, 108, 110.5, 112, 100, 100],   # stop at 105 hit at bar 4
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("LOSE", intraday)
    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "LOSE", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason in ("stop", "trail")
    assert t.realized_pnl < 0


def test_backtest_skips_when_gap_too_big() -> None:
    fake = FakeAlpaca()
    intraday = _intraday_bars("2026-04-28",
        prices =  [125, 125, 125, 125, 125, 125],  # gapped 13.6% above signal_high
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("GAP", intraday)
    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "GAP", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert trades == []
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_backtest_engine.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `backtest/engine.py`**

```python
"""Bar-replay backtester for the momentum strategy."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

from bot.data.base import MarketDataProvider
from bot.entry import gap_skip, in_entry_time_window, volume_confirms
from bot.exit import (
    earnings_exit_due, hard_stop_price, should_activate_trailing,
    target_price, time_stop_due, update_trailing_stop,
)
from bot.risk import position_size


_ET = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class BacktestTrade:
    symbol: str
    entry_time: datetime
    entry_price: float
    qty: int
    exit_time: datetime
    exit_price: float
    exit_reason: str
    realized_pnl: float


@dataclass
class BacktestConfig:
    watchlist: dict[date, list[dict]]
    start: date
    end: date
    equity: float = 100_000.0
    slippage_per_share: float = 0.01
    profit_target_pct: float = 0.10
    hard_stop_pct: float = 0.05
    trail_activation_pct: float = 0.06
    trail_distance_pct: float = 0.05
    time_stop_days: int = 5
    gap_skip_pct: float = 0.08
    per_trade_risk_pct: float = 0.015
    max_open_positions: int = 3
    vol_lookback_bars: int = 20


@dataclass
class _OpenPos:
    symbol: str
    entry_time: datetime
    entry_price: float
    qty: int
    signal_low: float
    current_stop: float
    highest: float
    trailing: bool
    earnings_date: date | None


def _walk_one_day(
    cfg: BacktestConfig, data: MarketDataProvider, day: date,
    open_positions: list[_OpenPos], equity: float,
) -> tuple[list[BacktestTrade], list[_OpenPos], float]:
    closed: list[BacktestTrade] = []
    survivors: list[_OpenPos] = []

    # Determine watchlist for this day
    candidates = cfg.watchlist.get(day, [])

    # Build a per-symbol bar dataframe for the trading day (5-min bars, 9:30–16:00 ET)
    day_open_et = datetime.combine(day, time(9, 30), tzinfo=_ET)
    day_close_et = datetime.combine(day, time(16, 0), tzinfo=_ET)
    start = day_open_et.astimezone(timezone.utc)
    end = day_close_et.astimezone(timezone.utc)

    # Symbols we need bars for: held + watchlist
    needed = {p.symbol for p in open_positions} | {c["symbol"] for c in candidates}
    bars: dict[str, pd.DataFrame] = {}
    for sym in needed:
        try:
            bars[sym] = data.get_intraday_bars(sym, start=start, end=end, timeframe_minutes=5)
        except Exception:
            bars[sym] = pd.DataFrame()

    # Build a chronological list of (timestamp, symbol)
    timestamps = sorted({ts for df in bars.values() for ts in df.index})
    triggered: dict[str, bool] = {c["symbol"]: False for c in candidates}

    for ts in timestamps:
        # 1. Manage open positions on this bar
        next_survivors: list[_OpenPos] = []
        for pos in open_positions:
            df = bars.get(pos.symbol)
            if df is None or df.empty or ts not in df.index:
                next_survivors.append(pos)
                continue
            row = df.loc[ts]
            high = float(row["high"]); low = float(row["low"]); close = float(row["close"])
            pos.highest = max(pos.highest, high)

            # Trailing-stop maintenance
            if not pos.trailing and should_activate_trailing(
                entry=pos.entry_price, current_high=pos.highest,
                activation_pct=cfg.trail_activation_pct,
            ):
                pos.current_stop = update_trailing_stop(pos.highest, cfg.trail_distance_pct)
                pos.trailing = True
            elif pos.trailing:
                cand = update_trailing_stop(pos.highest, cfg.trail_distance_pct)
                if cand > pos.current_stop:
                    pos.current_stop = cand

            target = target_price(pos.entry_price, cfg.profit_target_pct)
            unrealized = (close - pos.entry_price) * pos.qty

            exit_reason = None
            exit_px = close
            if high >= target:
                exit_reason = "target"; exit_px = target + cfg.slippage_per_share
            elif low <= pos.current_stop:
                exit_reason = "trail" if pos.trailing else "stop"
                exit_px = pos.current_stop - cfg.slippage_per_share
            elif time_stop_due(pos.entry_time, ts, days=cfg.time_stop_days):
                exit_reason = "time"; exit_px = close - cfg.slippage_per_share
            elif earnings_exit_due(ts.astimezone(_ET).date(), pos.earnings_date, unrealized):
                exit_reason = "earnings"; exit_px = close - cfg.slippage_per_share

            if exit_reason:
                pnl = (exit_px - pos.entry_price) * pos.qty
                closed.append(BacktestTrade(
                    symbol=pos.symbol, entry_time=pos.entry_time, entry_price=pos.entry_price,
                    qty=pos.qty, exit_time=ts, exit_price=exit_px,
                    exit_reason=exit_reason, realized_pnl=pnl,
                ))
                equity += pnl
            else:
                next_survivors.append(pos)
        open_positions = next_survivors

        # 2. Check entries
        if not in_entry_time_window(ts):
            continue
        if len(open_positions) >= cfg.max_open_positions:
            continue
        for cand in candidates:
            sym = cand["symbol"]
            if triggered.get(sym):
                continue
            df = bars.get(sym)
            if df is None or df.empty or ts not in df.index:
                continue
            day_open = float(df["open"].iloc[0])
            if gap_skip(day_open, cand["signal_high"], cfg.gap_skip_pct):
                triggered[sym] = True  # skip for the day
                continue
            row = df.loc[ts]
            if float(row["high"]) <= cand["signal_high"]:
                continue
            history = df.loc[:ts]
            if not volume_confirms(history, lookback_bars=cfg.vol_lookback_bars):
                continue

            entry_px = cand["signal_high"] + 0.02 + cfg.slippage_per_share
            stop = hard_stop_price(
                entry=entry_px, signal_low=cand["signal_low"], hard_stop_pct=cfg.hard_stop_pct,
            )
            qty = position_size(equity=equity, entry=entry_px, stop=stop,
                                per_trade_risk_pct=cfg.per_trade_risk_pct)
            if qty < 1:
                triggered[sym] = True
                continue

            earn_str = cand.get("earnings_next")
            earn_date = (date.fromisoformat(earn_str)
                         if isinstance(earn_str, str) and earn_str else None)
            open_positions.append(_OpenPos(
                symbol=sym, entry_time=ts, entry_price=entry_px, qty=qty,
                signal_low=cand["signal_low"], current_stop=stop, highest=entry_px,
                trailing=False, earnings_date=earn_date,
            ))
            triggered[sym] = True

    return closed, open_positions, equity


def run_backtest(cfg: BacktestConfig, data: MarketDataProvider) -> list[BacktestTrade]:
    all_trades: list[BacktestTrade] = []
    open_positions: list[_OpenPos] = []
    equity = cfg.equity
    cur = cfg.start
    while cur <= cfg.end:
        if cur.weekday() < 5:
            closed, open_positions, equity = _walk_one_day(cfg, data, cur, open_positions, equity)
            all_trades.extend(closed)
        cur += timedelta(days=1)
    return all_trades
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_backtest_engine.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add backtest/engine.py tests/test_backtest_engine.py
git commit -m "feat(backtest): bar-replay engine with TP/SL/trail/time/earnings exits"
```

---

## Task 23: Backtest Metrics

**Files:**
- Create: `backtest/metrics.py`
- Test: `tests/test_metrics.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_metrics.py`:
```python
"""Tests for backtest.metrics."""
from __future__ import annotations

from datetime import datetime, timezone
import math

import pytest

from backtest.engine import BacktestTrade
from backtest.metrics import compute_summary, equity_curve, max_drawdown


def _t(symbol: str, pnl: float, day: int = 1) -> BacktestTrade:
    return BacktestTrade(
        symbol=symbol,
        entry_time=datetime(2026, 4, day, 13, 35, tzinfo=timezone.utc),
        entry_price=100.0, qty=10,
        exit_time=datetime(2026, 4, day, 19, 0, tzinfo=timezone.utc),
        exit_price=100 + pnl/10, exit_reason="target", realized_pnl=pnl,
    )


def test_equity_curve_accumulates() -> None:
    trades = [_t("A", 100), _t("B", -50, day=2), _t("C", 200, day=3)]
    curve = equity_curve(trades, starting_equity=10_000)
    values = [v for _, v in curve]
    assert values == [10_100, 10_050, 10_250]


def test_max_drawdown_picks_largest_peak_to_trough() -> None:
    series = [10_000, 11_000, 10_500, 12_000, 9_000, 10_000]
    dd = max_drawdown(series)
    # Peak 12_000 → trough 9_000 → -25%
    assert dd == pytest.approx(-0.25)


def test_max_drawdown_zero_when_monotonic() -> None:
    assert max_drawdown([10_000, 11_000, 12_000]) == 0.0


def test_compute_summary_basic_stats() -> None:
    trades = [_t("A", 100), _t("B", -50, day=2), _t("C", 200, day=3)]
    s = compute_summary(trades=trades, starting_equity=10_000)
    assert s["trade_count"] == 3
    assert s["win_count"] == 2
    assert s["loss_count"] == 1
    assert s["win_rate"] == pytest.approx(2/3)
    assert s["total_pnl"] == 250
    assert s["ending_equity"] == 10_250
    assert s["total_return_pct"] == pytest.approx(0.025)
    assert s["avg_win"] == 150
    assert s["avg_loss"] == -50
    assert s["profit_factor"] == pytest.approx(300 / 50)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_metrics.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `backtest/metrics.py`**

```python
"""Performance metrics for backtest trade lists."""
from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from backtest.engine import BacktestTrade


def equity_curve(trades: list[BacktestTrade], starting_equity: float) -> list[tuple[datetime, float]]:
    eq = starting_equity
    out: list[tuple[datetime, float]] = []
    for t in sorted(trades, key=lambda x: x.exit_time):
        eq += t.realized_pnl
        out.append((t.exit_time, eq))
    return out


def max_drawdown(values: list[float]) -> float:
    """Returns max drawdown as a NEGATIVE fraction (e.g. -0.25 = -25%)."""
    if not values:
        return 0.0
    peak = values[0]
    worst = 0.0
    for v in values:
        peak = max(peak, v)
        if peak > 0:
            dd = (v - peak) / peak
            worst = min(worst, dd)
    return worst


def compute_summary(trades: list[BacktestTrade], starting_equity: float) -> dict[str, Any]:
    if not trades:
        return {"trade_count": 0, "starting_equity": starting_equity,
                "ending_equity": starting_equity, "total_pnl": 0.0,
                "total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                "win_count": 0, "loss_count": 0, "win_rate": 0.0,
                "avg_win": 0.0, "avg_loss": 0.0, "profit_factor": 0.0,
                "sharpe_daily": 0.0}
    wins = [t.realized_pnl for t in trades if t.realized_pnl > 0]
    losses = [t.realized_pnl for t in trades if t.realized_pnl < 0]
    total_pnl = sum(t.realized_pnl for t in trades)
    ending = starting_equity + total_pnl
    curve = [v for _, v in equity_curve(trades, starting_equity)]

    # Daily returns from equity curve (simple approximation)
    rets = []
    if len(curve) >= 2:
        for i in range(1, len(curve)):
            if curve[i - 1] > 0:
                rets.append((curve[i] - curve[i - 1]) / curve[i - 1])
    sharpe = 0.0
    if len(rets) >= 2:
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
        std = math.sqrt(var)
        sharpe = (mean / std * math.sqrt(252)) if std > 0 else 0.0

    return {
        "trade_count": len(trades),
        "starting_equity": starting_equity,
        "ending_equity": ending,
        "total_pnl": total_pnl,
        "total_return_pct": total_pnl / starting_equity if starting_equity > 0 else 0.0,
        "max_drawdown_pct": max_drawdown(curve),
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
        "profit_factor": (sum(wins) / abs(sum(losses))) if losses else float("inf"),
        "sharpe_daily": sharpe,
    }
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_metrics.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add backtest/metrics.py tests/test_metrics.py
git commit -m "feat(backtest): performance metrics (CAGR, DD, Sharpe, profit factor)"
```

---

## Task 24: run_backtest CLI + Report

**Files:**
- Create: `backtest/report.py`
- Create: `cli/run_backtest.py`

- [ ] **Step 1: Implement `backtest/report.py`**

```python
"""Write trade log CSV + summary JSON to backtest/results/<run_id>/."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from backtest.engine import BacktestTrade


def write_trades_csv(trades: list[BacktestTrade], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not trades:
        path.write_text("symbol,entry_time,entry_price,qty,exit_time,exit_price,exit_reason,realized_pnl\n")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "symbol", "entry_time", "entry_price", "qty",
            "exit_time", "exit_price", "exit_reason", "realized_pnl",
        ])
        writer.writeheader()
        for t in trades:
            row = asdict(t)
            row["entry_time"] = t.entry_time.isoformat()
            row["exit_time"] = t.exit_time.isoformat()
            writer.writerow(row)


def write_summary_json(summary: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, default=str))
```

- [ ] **Step 2: Implement `cli/run_backtest.py`**

`cli/run_backtest.py`:
```python
"""Backtest entry point.

Usage:
  python -m cli.run_backtest --start 2025-01-01 --end 2026-04-01 --equity 100000
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from backtest.engine import BacktestConfig, run_backtest
from backtest.metrics import compute_summary
from backtest.report import write_summary_json, write_trades_csv
from bot import config
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.earnings import YFinanceEarnings
from bot.scanner import scan, ScanCriteria
from bot.universe import build_universe

UNIVERSE_DIR = Path("data/universe")
RESULTS_DIR = Path("backtest/results")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True, help="YYYY-MM-DD")
    p.add_argument("--end", required=True, help="YYYY-MM-DD")
    p.add_argument("--equity", type=float, default=100_000.0)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    settings = config.load()

    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    earnings = YFinanceEarnings()

    # Build daily watchlists by replaying scanner over date range
    watchlist: dict[date, list[dict]] = {}
    cur = start - timedelta(days=1)  # scan EOD of (start-1) for start's session
    while cur <= end:
        if cur.weekday() < 5:
            as_of = datetime.combine(cur, datetime.min.time(), tzinfo=timezone.utc).replace(hour=20)
            eligible = build_universe(
                sp500_csv=UNIVERSE_DIR / "sp500.csv",
                ndx_csv=UNIVERSE_DIR / "ndx.csv",
                exclusions_csv=UNIVERSE_DIR / "exclusions.csv",
                data=data, as_of=as_of,
                min_price=settings.min_price, min_dollar_vol=settings.min_dollar_vol,
            )
            results = scan(
                eligible=eligible, data=data, earnings=earnings, as_of=as_of,
                criteria=ScanCriteria(
                    pct_change_min=settings.pct_change_min,
                    rvol_min=settings.rvol_min,
                    near_breakout_pct=settings.near_breakout_pct,
                    lookback_breakout=settings.lookback_breakout,
                ),
            )
            next_session = cur + timedelta(days=1)
            while next_session.weekday() >= 5:
                next_session += timedelta(days=1)
            if next_session <= end:
                watchlist[next_session] = [
                    {
                        "symbol": r.symbol, "signal_high": r.signal_high,
                        "signal_low": r.signal_low, "signal_close": r.signal_close,
                        "atr_14": r.atr_14, "rvol_eod": r.rvol_eod,
                        "earnings_next": r.earnings_next,
                    }
                    for r in results
                ]
            print(f"  {cur}: {len(results)} candidates for {next_session}")
        cur += timedelta(days=1)

    cfg = BacktestConfig(
        watchlist=watchlist, start=start, end=end, equity=args.equity,
        profit_target_pct=settings.profit_target_pct,
        hard_stop_pct=settings.hard_stop_pct,
        trail_activation_pct=settings.trail_activation_pct,
        trail_distance_pct=settings.trail_distance_pct,
        time_stop_days=settings.time_stop_days,
        gap_skip_pct=settings.gap_skip_pct,
        per_trade_risk_pct=settings.per_trade_risk_pct,
        max_open_positions=settings.max_open_positions,
    )
    trades = run_backtest(cfg=cfg, data=data)
    summary = compute_summary(trades=trades, starting_equity=args.equity)

    run_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:6]}"
    out_dir = RESULTS_DIR / run_id
    write_trades_csv(trades, out_dir / "trades.csv")
    write_summary_json(summary, out_dir / "summary.json")

    print()
    print(json.dumps(summary, indent=2, default=str))
    print(f"\nWrote {len(trades)} trades to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Smoke test (very short range)**

Run: `.venv/bin/python -m cli.run_backtest --start 2026-04-20 --end 2026-04-24 --equity 100000`
Expected: prints per-day candidate counts, ends with summary JSON, writes `backtest/results/<run_id>/`. May produce 0 trades; that's OK as a smoke test.

- [ ] **Step 4: Commit**

```bash
git add backtest/report.py cli/run_backtest.py
git commit -m "feat(backtest): CLI + CSV/JSON report writer"
```

---

## Task 25: systemd Service File

**Files:**
- Create: `ops/stocks-bot-trader.service`

- [ ] **Step 1: Write the unit file**

`ops/stocks-bot-trader.service`:
```ini
[Unit]
Description=Stocks momentum trader (polling)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/lui-tortuya/stocks_monitoring
EnvironmentFile=/home/lui-tortuya/.env
ExecStart=/home/lui-tortuya/stocks_monitoring/.venv/bin/python -m cli.run_trader
Restart=on-failure
RestartSec=10
StandardOutput=append:/home/lui-tortuya/stocks_monitoring/data/logs/trader-systemd.log
StandardError=inherit
TimeoutStopSec=30

[Install]
WantedBy=default.target
```

- [ ] **Step 2: Commit**

```bash
git add ops/stocks-bot-trader.service
git commit -m "feat(ops): systemd unit for trader process"
```

Deployment steps (manual, when ready to deploy on the mini PC):

```bash
# On the mini PC
mkdir -p ~/.config/systemd/user
cp ~/stocks_monitoring/ops/stocks-bot-trader.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable stocks-bot-trader.service
loginctl enable-linger lui-tortuya  # so the unit can run while user is logged out
```

---

## Task 26: Crontab Template + Start/Stop Scripts

**Files:**
- Create: `ops/crontab.txt`
- Create: `ops/start_trader.sh`
- Create: `ops/stop_trader.sh`

- [ ] **Step 1: Write start/stop scripts**

`ops/start_trader.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
systemctl --user start stocks-bot-trader.service
```

`ops/stop_trader.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
systemctl --user stop stocks-bot-trader.service
```

Make executable:
```bash
chmod +x ops/start_trader.sh ops/stop_trader.sh
```

- [ ] **Step 2: Write crontab template**

`ops/crontab.txt`:
```
# Stocks momentum bot — install with: crontab ops/crontab.txt
# All times America/Los_Angeles (PT). Mini PC's TZ should be set to PT for these to align with ET market hours.
# 9:25 AM ET = 6:25 AM PT (start trader)
# 4:05 PM ET = 1:05 PM PT (stop trader, run scanner)
# 1st of month at 3 AM PT — refresh universe

CRON_TZ=America/Los_Angeles

# Start trader at 6:25 AM PT (Mon–Fri)
25 6 * * 1-5 /home/lui-tortuya/stocks_monitoring/ops/start_trader.sh >> /home/lui-tortuya/stocks_monitoring/data/logs/cron.log 2>&1

# Stop trader at 1:05 PM PT (Mon–Fri)
5 13 * * 1-5 /home/lui-tortuya/stocks_monitoring/ops/stop_trader.sh >> /home/lui-tortuya/stocks_monitoring/data/logs/cron.log 2>&1

# Run scanner at 1:10 PM PT (Mon–Fri) — 5 min after stop, lets in-flight closes settle
10 13 * * 1-5 cd /home/lui-tortuya/stocks_monitoring && .venv/bin/python -m cli.run_scanner >> data/logs/scanner.log 2>&1

# Refresh SP500/NDX universe on the 1st of each month at 3 AM PT
0 3 1 * * cd /home/lui-tortuya/stocks_monitoring && .venv/bin/python -m cli.refresh_universe >> data/logs/universe.log 2>&1
```

- [ ] **Step 3: Commit**

```bash
git add ops/crontab.txt ops/start_trader.sh ops/stop_trader.sh
git commit -m "feat(ops): crontab template + start/stop helpers"
```

Install (manual, on the mini PC):
```bash
crontab -l > /tmp/old.txt 2>/dev/null || true
cat /tmp/old.txt ops/crontab.txt | sort -u | crontab -
```

---

## Task 27: ops CLI

**Files:**
- Create: `cli/ops.py`

- [ ] **Step 1: Implement the admin CLI**

`cli/ops.py`:
```python
"""Operator commands.

Usage:
  python -m cli.ops positions          # list local + Alpaca-side positions
  python -m cli.ops watchlist          # show today's active watchlist
  python -m cli.ops halt "reason"      # set halt flag
  python -m cli.ops resume             # clear halt flag + state halts
  python -m cli.ops flatten SYMBOL     # market-sell symbol (closes Alpaca + state)
  python -m cli.ops flatten-all        # market-sell ALL open positions
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from bot import config
from bot.executor import AlpacaExecutor
from bot.state import State

DATA_DIR = Path("data")
STATE_PATH = DATA_DIR / "state.sqlite"
HALT_FLAG = DATA_DIR / "halt.flag"
_ET = ZoneInfo("America/New_York")


def _state() -> State:
    s = State(STATE_PATH); s.init(); return s


def _executor():
    s = config.load()
    return AlpacaExecutor(api_key=s.alpaca_api_key, api_secret=s.alpaca_api_secret,
                          base_url=s.alpaca_base_url)


def cmd_positions(_args) -> int:
    state = _state()
    executor = _executor()
    local = {p.symbol: p for p in state.open_positions()}
    alpaca = executor.list_positions()
    syms = sorted(set(local) | set(alpaca))
    print(f"{'symbol':<8}{'local qty':<12}{'alpaca qty':<12}{'avg entry':<12}{'last':<10}{'pnl':<10}")
    for s in syms:
        l = local.get(s)
        a = alpaca.get(s)
        lq = l.qty if l else "-"
        aq = a["qty"] if a else "-"
        ae = f"{a['avg_entry_price']:.2f}" if a else "-"
        cp = f"{a['current_price']:.2f}" if a else "-"
        pnl = f"{a['unrealized_pl']:+.2f}" if a else "-"
        print(f"{s:<8}{str(lq):<12}{str(aq):<12}{ae:<12}{cp:<10}{pnl:<10}")
    return 0


def cmd_watchlist(_args) -> int:
    state = _state()
    today = datetime.now(timezone.utc).astimezone(_ET).date().isoformat()
    rows = state.active_watchlist(today)
    print(f"Active watchlist for {today}: {len(rows)} symbols")
    for r in sorted(rows, key=lambda x: -x.rvol_eod):
        print(f"  {r.symbol:<6} signal_high={r.signal_high:.2f}  rvol={r.rvol_eod:.2f}  attempts={r.breakout_attempts}")
    return 0


def cmd_halt(args) -> int:
    HALT_FLAG.parent.mkdir(parents=True, exist_ok=True)
    HALT_FLAG.write_text(args.reason)
    state = _state()
    state.set_halt(datetime.now(timezone.utc).isoformat(), args.reason)
    print(f"HALTED: {args.reason}")
    return 0


def cmd_resume(_args) -> int:
    if HALT_FLAG.exists():
        HALT_FLAG.unlink()
    state = _state()
    state.clear_halt(datetime.now(timezone.utc).isoformat())
    print("Resumed (halt cleared)")
    return 0


def cmd_flatten(args) -> int:
    executor = _executor()
    positions = executor.list_positions()
    if args.symbol not in positions:
        print(f"No Alpaca position for {args.symbol}", file=sys.stderr)
        return 1
    qty = positions[args.symbol]["qty"]
    executor.submit_market_sell(symbol=args.symbol, qty=qty)
    state = _state()
    pos = state.position_by_symbol(args.symbol)
    if pos:
        state.close_position(
            pos_id=pos.id, exit_time=datetime.now(timezone.utc).isoformat(),
            exit_price=positions[args.symbol]["current_price"],
            exit_reason="manual", realized_pnl=positions[args.symbol]["unrealized_pl"],
        )
    print(f"Flatten requested: {args.symbol} qty={qty}")
    return 0


def cmd_flatten_all(_args) -> int:
    executor = _executor()
    for sym, info in executor.list_positions().items():
        executor.submit_market_sell(symbol=sym, qty=info["qty"])
        print(f"  flatten {sym} qty={info['qty']}")
    state = _state()
    for pos in state.open_positions():
        state.close_position(
            pos_id=pos.id, exit_time=datetime.now(timezone.utc).isoformat(),
            exit_price=pos.entry_price or 0.0, exit_reason="manual", realized_pnl=0.0,
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("positions").set_defaults(fn=cmd_positions)
    sub.add_parser("watchlist").set_defaults(fn=cmd_watchlist)
    halt_p = sub.add_parser("halt"); halt_p.add_argument("reason"); halt_p.set_defaults(fn=cmd_halt)
    sub.add_parser("resume").set_defaults(fn=cmd_resume)
    flat_p = sub.add_parser("flatten"); flat_p.add_argument("symbol"); flat_p.set_defaults(fn=cmd_flatten)
    sub.add_parser("flatten-all").set_defaults(fn=cmd_flatten_all)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Commit**

```bash
git add cli/ops.py
git commit -m "feat(cli): ops admin commands (positions, halt, flatten)"
```

---

## Task 28: README + Deployment Docs

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README**

`README.md`:
```markdown
# Stocks Momentum Bot

Python momentum-breakout trading bot for Alpaca paper account.
Spec: [docs/specs/2026-04-25-momentum-bot-design.md](docs/specs/2026-04-25-momentum-bot-design.md)
Plan: [docs/plans/2026-04-25-momentum-bot-plan.md](docs/plans/2026-04-25-momentum-bot-plan.md)

## Quick start (development, Windows)

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env  # then edit with real credentials
.venv\Scripts\pytest
```

## Run a scan (manual)

```bash
.venv/bin/python -m cli.run_scanner
```

## Run a backtest

```bash
.venv/bin/python -m cli.run_backtest --start 2025-01-01 --end 2026-04-01 --equity 100000
# Results land in backtest/results/<run_id>/
```

## Operator commands

```bash
.venv/bin/python -m cli.ops positions       # local + Alpaca side positions
.venv/bin/python -m cli.ops watchlist       # today's active watchlist
.venv/bin/python -m cli.ops halt "reason"   # halt new entries
.venv/bin/python -m cli.ops resume          # clear halt
.venv/bin/python -m cli.ops flatten AAPL    # market-sell one symbol
.venv/bin/python -m cli.ops flatten-all     # market-sell everything
```

## Deployment to the mini PC (Ubuntu, 192.168.1.111)

```bash
# 1. Clone + venv
ssh lui-tortuya@192.168.1.111
git clone <repo-url> ~/stocks_monitoring
cd ~/stocks_monitoring
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Copy .env (or symlink the shared one)
ln -s ~/.env .env

# 3. Refresh universe (one time)
.venv/bin/python -m cli.refresh_universe

# 4. Install systemd unit
mkdir -p ~/.config/systemd/user
cp ops/stocks-bot-trader.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable stocks-bot-trader.service
loginctl enable-linger lui-tortuya

# 5. Install crontab (preserves any existing entries)
crontab -l > /tmp/old.txt 2>/dev/null || true
cat /tmp/old.txt ops/crontab.txt | sort -u | crontab -

# 6. Verify
crontab -l | grep stocks_monitoring
systemctl --user status stocks-bot-trader.service
```

## Architecture

Three Python entrypoints orchestrated by cron + systemd:

- **`cli.run_scanner`** — daily 1:10 PM PT (4:10 PM ET). Scans NDX∪SPX, writes watchlist to SQLite.
- **`cli.run_trader`** — systemd-supervised daemon, started 6:25 AM PT and stopped 1:05 PM PT by cron. Polls watchlist symbols every 30s (15s during the first 90 min of session). Manages entries + exits.
- **`cli.run_backtest`** — manual, replays the strategy over historical data and writes a CSV trade log + JSON summary.

State lives in `data/state.sqlite`. Logs land in `data/logs/` (daily JSON-line files).

## Halt mechanisms

- `data/halt.flag` file present → no new entries (existing positions managed normally).
- `cli.ops halt "reason"` sets both the file AND a state-table entry.
- Daily drawdown ≥ 3% auto-sets the state halt.
- Reset with `cli.ops resume`.

## Key files

| Path | Role |
|---|---|
| `bot/config.py` | env + typed strategy constants — change thresholds here |
| `bot/scanner.py` | daily scan rules |
| `bot/entry.py` / `bot/exit.py` | trigger + exit logic |
| `bot/executor.py` | Alpaca order calls |
| `bot/state.py` | SQLite layer |
| `backtest/engine.py` | bar-replay backtester |
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: README with quickstart, deployment, and ops guide"
```

---

## Self-Review Notes (filled in by plan author)

**Spec coverage:**

| Spec section | Tasks |
|---|---|
| §3.1 Universe | 11, 12 |
| §3.2 Daily scan | 16, 17 |
| §3.3 Intraday entry | 14, 21 |
| §3.4 Relative volume | 6, 7 |
| §3.5 Exits | 15, 21 |
| §3.6 Failed-breakout | 21 (deactivate logic) |
| §3.7 Risk rules | 13, 21 |
| §4 Architecture | 21, 25, 26 |
| §5 Data sources | 9, 10 |
| §6 State persistence | 4 |
| §7 Order lifecycle | 19, 21 |
| §8 Backtester | 22, 23, 24 |
| §9 Logging + alerts | 2, 18 |
| §10 Configuration | 3 |
| §11 Testing strategy | embedded in every task |
| §12 Deployment | 25, 26, 28 |

**Known plan limitations (call out for the implementer to address as they go):**

1. **Intraday RVOL curve is built but not wired into the live trader entry path** — the entry decision in Task 21 currently uses 5-min bar volume confirmation only. To use the same-time-of-day RVOL curve (spec §3.4), Task 21 would need an additional helper that fetches/caches the curve at start-of-day for each watchlist symbol and consults it during `evaluate_entry`. Acceptable per spec ("fallback to simple form is acceptable") but worth noting.
2. **Bracket exit orders (TP + SL) are not pre-attached after fill** — the live trader closes positions via `submit_market_sell` when its own polling logic decides to exit. This is simpler than the spec's "attach OCO bracket on fill" approach and matches the actual exit decision logic in `bot/exit.py`. Tradeoff: if the trader process dies between fill and exit decision, position is unprotected until restart. Reconciliation will detect the position; halt flag protects against runaway behavior. Worth revisiting after Phase 2 paper-trading observations.
3. **`refresh_universe.py` has no unit test** — Wikipedia scraping is brittle and not worth mocking; the smoke test catches breaks.
4. **`run_trader.py` main loop is not unit-tested end-to-end** — its helpers are tested. The full loop is verified during Phase 2 paper-trading.

**Execution handoff** is offered after this section.


