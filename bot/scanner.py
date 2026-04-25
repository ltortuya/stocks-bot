"""Daily end-of-day scanner — produces tomorrow's watchlist."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

import pandas as pd

from bot.data.base import MarketDataProvider
from bot.data.earnings import EarningsProvider
from bot.indicators import sma, atr_wilder, rvol_eod
from bot.state import WatchlistEntry
from bot.universe import EligibilityRow


@dataclass(frozen=True)
class ScanCriteria:
    pct_change_min: float = 0.04
    rvol_min: float = 1.8
    near_breakout_pct: float = 0.02
    lookback_breakout: int = 20
    earnings_block_days: int = 5
    daily_history_days: int = 90  # enough for SMA50 + RVOL20


def scan(
    eligible: Iterable[EligibilityRow],
    data: MarketDataProvider,
    earnings: EarningsProvider,
    as_of: datetime,
    criteria: ScanCriteria,
) -> list[WatchlistEntry]:
    out: list[WatchlistEntry] = []
    start = as_of - timedelta(days=criteria.daily_history_days)
    for row in eligible:
        try:
            bars = data.get_daily_bars(row.symbol, start=start, end=as_of)
        except Exception:
            continue
        if bars.empty or len(bars) < 51:
            continue

        today = bars.iloc[-1]
        prev_close = float(bars["close"].iloc[-2])
        if prev_close <= 0:
            continue
        pct_change = (float(today["close"]) - prev_close) / prev_close
        if pct_change < criteria.pct_change_min:
            continue

        rvol_series = rvol_eod(bars["volume"], lookback=20)
        rvol = float(rvol_series.iloc[-1])
        if pd.isna(rvol) or rvol < criteria.rvol_min:
            continue

        sma20 = float(sma(bars["close"], 20).iloc[-1])
        sma50 = float(sma(bars["close"], 50).iloc[-1])
        if pd.isna(sma20) or pd.isna(sma50):
            continue
        if not (today["close"] > sma20 and today["close"] > sma50):
            continue

        prior_20d_high = float(bars["high"].iloc[-(criteria.lookback_breakout + 1):-1].max())
        breaks = today["close"] >= prior_20d_high
        near = today["close"] >= prior_20d_high * (1 - criteria.near_breakout_pct)
        if not (breaks or near):
            continue

        earn = earnings.next_earnings(row.symbol)
        if earn is not None:
            days_until = (earn - as_of.date()).days
            if 0 <= days_until <= criteria.earnings_block_days:
                continue

        atr14_series = atr_wilder(bars[["high", "low", "close"]], period=14)
        atr14 = float(atr14_series.iloc[-1])

        # scan_date = the date of next trading session = as_of + 1 calendar day
        # The trader will resolve against the actual next session at run time.
        next_date = (as_of + timedelta(days=1)).date().isoformat()

        out.append(WatchlistEntry(
            scan_date=next_date,
            symbol=row.symbol,
            signal_high=float(today["high"]),
            signal_low=float(today["low"]),
            signal_close=float(today["close"]),
            atr_14=atr14,
            rvol_eod=rvol,
            earnings_next=earn.isoformat() if earn else None,
        ))
    return out
