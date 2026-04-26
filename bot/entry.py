"""Entry trigger evaluation: gap check, time window, breakout, volume confirmation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
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
    no_entry_first_min: int = 0,
    no_new_entry_after_et: time = time(14, 30),
) -> bool:
    """True iff `now_utc` (in ET) is between (open + first_min) and the no-new-entry cutoff (inclusive).

    The cutoff is INCLUSIVE — exactly 14:30 ET is still allowed (matches plan/spec wording).
    """
    et_now = now_utc.astimezone(_ET)
    et_today = et_now.date()
    open_dt = datetime.combine(et_today, market_open_et, tzinfo=_ET)
    earliest_entry_dt = open_dt + timedelta(minutes=no_entry_first_min)
    latest_entry_dt = datetime.combine(et_today, no_new_entry_after_et, tzinfo=_ET)
    if et_now < earliest_entry_dt:
        return False
    if et_now > latest_entry_dt:
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
