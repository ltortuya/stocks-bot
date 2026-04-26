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
