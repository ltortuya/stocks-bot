"""Helpers to build canned bar DataFrames for tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd


def make_daily_bars(
    start: str, periods: int, base_price: float = 100.0,
    daily_volume: int = 1_000_000, daily_change_pct: float = 0.005,
) -> pd.DataFrame:
    start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    rows = []
    close = base_price
    for i in range(periods):
        ts = start_dt + timedelta(days=i)
        open_ = close
        close = close * (1 + daily_change_pct)
        high = max(open_, close) * 1.002
        low = min(open_, close) * 0.998
        rows.append({
            "timestamp": ts, "open": open_, "high": high,
            "low": low, "close": close, "volume": daily_volume,
        })
    return pd.DataFrame(rows).set_index("timestamp")
