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
        # Default cursors return tuples (raw test access stays simple);
        # internal reads use _row_cursor() which yields sqlite3.Row.

    def init(self) -> None:
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def _row_cursor(self) -> sqlite3.Cursor:
        cur = self.conn.cursor()
        cur.row_factory = sqlite3.Row
        return cur

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
        cur = self._row_cursor()
        return [
            self._row_to_watchlist(r)
            for r in cur.execute(
                "SELECT * FROM watchlist WHERE scan_date=? AND is_active=1",
                (scan_date,),
            )
        ]

    def all_watchlist(self, scan_date: str) -> list[WatchlistEntry]:
        cur = self._row_cursor()
        return [
            self._row_to_watchlist(r)
            for r in cur.execute(
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
        cur = self._row_cursor()
        return [
            self._row_to_position(r)
            for r in cur.execute("SELECT * FROM positions WHERE status='open'")
        ]

    def position_by_symbol(self, symbol: str) -> Position | None:
        cur = self._row_cursor()
        r = cur.execute(
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
