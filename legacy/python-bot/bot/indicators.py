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


def rvol_eod(volume_series: pd.Series, lookback: int = 20) -> pd.Series:
    """Today / mean(prior `lookback` sessions, EXCLUDING today)."""
    avg_prior = volume_series.shift(1).rolling(window=lookback, min_periods=lookback).mean()
    return volume_series / avg_prior


def build_intraday_volume_curve(sessions: list[pd.DataFrame]) -> pd.Series:
    """Per-minute-of-day average cumulative volume across N sessions.

    Each session DataFrame must have columns ['minute_of_day', 'cumulative_volume'].
    """
    if not sessions:
        return pd.Series(dtype=float)
    combined = pd.concat(sessions, ignore_index=True)
    return combined.groupby("minute_of_day")["cumulative_volume"].mean()


def rvol_intraday(today_cum_volume: float, minute_of_day: int, curve: pd.Series) -> float:
    """today_cum_volume / expected_cum_volume_at(minute). NaN if minute not in curve."""
    if minute_of_day not in curve.index:
        return float("nan")
    expected = curve.loc[minute_of_day]
    if expected <= 0:
        return float("nan")
    return today_cum_volume / expected
