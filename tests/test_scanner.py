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
    # Inject an earlier spike into the 20-day window so prior_20d_high is well above
    # the recent trend; today's close at 99% of that spike will then still be above SMAs.
    spike_idx = -10  # 10 bars before the last
    spike_high = bars["high"].iloc[-2] * 1.10  # 10% above recent
    bars.iloc[spike_idx, bars.columns.get_loc("high")] = spike_high
    prior_20d_high = bars["high"].iloc[-21:-1].max()
    target_close = prior_20d_high * 0.99
    # Adjust previous bar's close so today's close is a +4% move.
    new_prev_close = target_close / 1.04
    bars.iloc[-2, bars.columns.get_loc("close")] = new_prev_close
    bars.iloc[-1, bars.columns.get_loc("close")] = target_close
    bars.iloc[-1, bars.columns.get_loc("open")] = new_prev_close
    bars.iloc[-1, bars.columns.get_loc("high")] = target_close * 1.001
    bars.iloc[-1, bars.columns.get_loc("low")] = new_prev_close * 0.999
    bars.iloc[-1, bars.columns.get_loc("volume")] = 2_500_000
    fake.set_daily_bars("NEAR", bars)

    eligible = [EligibilityRow(symbol="NEAR", last_close=target_close, avg_dollar_vol=100_000_000)]
    results = scan(eligible=eligible, data=fake, earnings=_StubEarnings({"NEAR": None}),
                   as_of=datetime(2026, 4, 15, tzinfo=timezone.utc), criteria=ScanCriteria())
    assert any(r.symbol == "NEAR" for r in results)
