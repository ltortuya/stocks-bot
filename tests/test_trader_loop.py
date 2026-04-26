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


def test_check_drawdown_halt_triggers_at_threshold(tmp_path: Path) -> None:
    from cli.run_trader import check_drawdown_halt, _DAILY_START_EQUITY
    _DAILY_START_EQUITY.clear()
    s = _state(tmp_path)

    class _E:
        def __init__(self, eq: float) -> None:
            self._eq = eq
        def get_equity(self) -> float:
            return self._eq

    class _Settings:
        daily_drawdown_halt_pct = -0.03

    now = datetime(2026, 4, 28, 19, 0, tzinfo=timezone.utc)
    # First call seeds start equity at 100k
    assert check_drawdown_halt(state=s, executor=_E(100_000), settings=_Settings(), now=now) is False
    # Second call with 96k = -4% → triggers halt
    triggered = check_drawdown_halt(state=s, executor=_E(96_000), settings=_Settings(), now=now)
    assert triggered is True
    assert s.is_halted() is True


def test_check_drawdown_halt_no_op_when_already_halted(tmp_path: Path) -> None:
    from cli.run_trader import check_drawdown_halt
    s = _state(tmp_path)
    s.set_halt("2026-04-28T15:00:00+00:00", "manual")

    class _E:
        def get_equity(self) -> float:
            return 50_000  # would trigger if checked

    class _Settings:
        daily_drawdown_halt_pct = -0.03

    triggered = check_drawdown_halt(
        state=s, executor=_E(), settings=_Settings(),
        now=datetime(2026, 4, 28, 19, 0, tzinfo=timezone.utc),
    )
    assert triggered is False  # already halted, no-op
