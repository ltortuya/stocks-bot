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
