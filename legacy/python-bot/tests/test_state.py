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
