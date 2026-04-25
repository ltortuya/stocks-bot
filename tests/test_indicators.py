"""Tests for bot.indicators."""
from __future__ import annotations

import math

import pandas as pd
import pytest

from bot.indicators import sma, atr_wilder


def test_sma_window_3() -> None:
    series = pd.Series([10.0, 11.0, 12.0, 13.0, 14.0])
    result = sma(series, window=3)
    assert math.isnan(result.iloc[0])
    assert math.isnan(result.iloc[1])
    assert result.iloc[2] == pytest.approx(11.0)
    assert result.iloc[3] == pytest.approx(12.0)
    assert result.iloc[4] == pytest.approx(13.0)


def test_sma_full_series_average() -> None:
    series = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = sma(series, window=5)
    assert result.iloc[-1] == pytest.approx(3.0)


def test_atr_wilder_matches_known_values() -> None:
    df = pd.DataFrame({
        "high":  [10.0, 11.0, 12.0, 11.5, 13.0],
        "low":   [9.0,  10.0, 10.5, 10.5, 11.5],
        "close": [9.5,  10.5, 11.5, 11.0, 12.5],
    })
    result = atr_wilder(df, period=3)
    # First TR uses high-low fallback (no prev_close):
    #   TR1=1.0, TR2=max(1,1.5,0.5)=1.5, TR3=max(1.5,1.5,0)=1.5
    # Initial ATR = mean(1.0, 1.5, 1.5) = 1.3333
    assert result.iloc[2] == pytest.approx(1.3333333, rel=1e-4)
    # TR4 = max(1.0, 0.0, 1.0) = 1.0; ATR4 = (1.3333*2 + 1.0)/3 = 1.2222
    assert result.iloc[3] == pytest.approx(1.2222222, rel=1e-4)
    # TR5 = max(1.5, 2.0, 0.5) = 2.0; ATR5 = (1.2222*2 + 2.0)/3 = 1.4815
    assert result.iloc[4] == pytest.approx(1.4814814, rel=1e-4)


from bot.indicators import rvol_eod


def test_rvol_eod_uses_prior_n_sessions() -> None:
    volumes = [1_000_000] * 20 + [2_500_000]
    series = pd.Series(volumes)
    rvol = rvol_eod(series, lookback=20)
    assert rvol.iloc[-1] == pytest.approx(2.5)
    assert math.isnan(rvol.iloc[19])


def test_rvol_eod_excludes_today_from_average() -> None:
    volumes = list(range(1, 22))  # 1..21
    series = pd.Series(volumes, dtype=float)
    rvol = rvol_eod(series, lookback=20)
    # day 21 vol=21; mean(1..20)=10.5; rvol=21/10.5=2.0
    assert rvol.iloc[20] == pytest.approx(2.0)
