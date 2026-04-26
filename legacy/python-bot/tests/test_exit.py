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
