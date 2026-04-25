"""Technical indicators (SMA, ATR, relative volume)."""
from __future__ import annotations

import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple moving average. NaN for the first (window-1) entries."""
    return series.rolling(window=window, min_periods=window).mean()


def atr_wilder(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Wilder's ATR.

    df must have columns: high, low, close (in chronological order).
    Returns a Series aligned with df.index. First (period-1) values are NaN.
    """
    high = df["high"]
    low = df["low"]
    prev_close = df["close"].shift(1)

    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    tr.iloc[0] = high.iloc[0] - low.iloc[0]

    atr = pd.Series(index=df.index, dtype=float)
    if len(df) < period:
        return atr
    initial = tr.iloc[:period].mean()
    atr.iloc[period - 1] = initial
    for i in range(period, len(df)):
        atr.iloc[i] = (atr.iloc[i - 1] * (period - 1) + tr.iloc[i]) / period
    return atr
