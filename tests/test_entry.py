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


def test_in_entry_time_window_default_allows_market_open() -> None:
    # Default no_entry_first_min=0 — entries allowed from 9:30 ET
    # 9:30 ET = 13:30 UTC (Apr — DST)
    assert in_entry_time_window(datetime(2026, 4, 28, 13, 30, tzinfo=timezone.utc)) is True
    # 9:29 ET still blocked (before market open)
    assert in_entry_time_window(datetime(2026, 4, 28, 13, 29, tzinfo=timezone.utc)) is False
    # 14:31 ET = 18:31 UTC → blocked (after 14:30 cutoff)
    assert in_entry_time_window(datetime(2026, 4, 28, 18, 31, tzinfo=timezone.utc)) is False
    # 14:30 exactly ET = 18:30 UTC → allowed (cutoff is inclusive)
    assert in_entry_time_window(datetime(2026, 4, 28, 18, 30, tzinfo=timezone.utc)) is True


def test_in_entry_time_window_with_explicit_buffer() -> None:
    # Explicit buffer still works for callers that want it
    assert in_entry_time_window(
        datetime(2026, 4, 28, 13, 35, tzinfo=timezone.utc), no_entry_first_min=5
    ) is True
    assert in_entry_time_window(
        datetime(2026, 4, 28, 13, 34, tzinfo=timezone.utc), no_entry_first_min=5
    ) is False


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
