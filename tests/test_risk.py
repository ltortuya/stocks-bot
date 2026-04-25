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
    # equity 100k, entry 100, stop 95 -> risk per share $5; budget = 1500 / 5 = 300 shares
    qty = position_size(equity=100_000, entry=100.0, stop=95.0, per_trade_risk_pct=0.015)
    assert qty == 300


def test_position_size_returns_zero_when_stop_above_entry() -> None:
    qty = position_size(equity=100_000, entry=100.0, stop=101.0, per_trade_risk_pct=0.015)
    assert qty == 0


def test_position_size_floors_to_int() -> None:
    qty = position_size(equity=10_000, entry=50.0, stop=49.5, per_trade_risk_pct=0.015)
    # risk 0.5/share, budget 150 -> 300 shares exactly
    assert qty == 300


def test_position_size_zero_when_qty_below_one() -> None:
    qty = position_size(equity=1_000, entry=500.0, stop=400.0, per_trade_risk_pct=0.015)
    # risk 100/share, budget 15 -> 0.15 -> floored to 0
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
