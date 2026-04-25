"""Tests for backtest.engine."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from backtest.engine import run_backtest, BacktestConfig, BacktestTrade
from bot.universe import EligibilityRow
from tests.fakes.fake_alpaca import FakeAlpaca


def _intraday_bars(date_str: str, prices: list[float], volumes: list[int]) -> pd.DataFrame:
    open_dt = datetime.fromisoformat(date_str).replace(hour=13, minute=30, tzinfo=timezone.utc)
    rows = []
    for i, (p, v) in enumerate(zip(prices, volumes)):
        ts = open_dt + timedelta(minutes=5 * i)
        rows.append({"timestamp": ts, "open": p, "high": p, "low": p, "close": p, "volume": v})
    return pd.DataFrame(rows).set_index("timestamp")


def test_backtest_records_simple_winning_trade() -> None:
    fake = FakeAlpaca()
    # signal day = 2026-04-27 (Mon); buy day = 2026-04-28 (Tue)
    # On 4/28, price breaks signal_high=110 at bar 3, runs to 121 → hits 10% target
    intraday = _intraday_bars("2026-04-28",
        prices =  [105, 108, 110.5, 112, 121, 121],
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("WIN", intraday)

    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "WIN", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert len(trades) == 1
    t = trades[0]
    assert t.symbol == "WIN"
    assert t.exit_reason == "target"
    assert t.exit_price >= 121.0
    assert t.realized_pnl > 0


def test_backtest_records_stopout_trade() -> None:
    fake = FakeAlpaca()
    intraday = _intraday_bars("2026-04-28",
        prices =  [105, 108, 110.5, 112, 100, 100],   # stop at 105 hit at bar 4
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("LOSE", intraday)
    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "LOSE", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert len(trades) == 1
    t = trades[0]
    assert t.exit_reason in ("stop", "trail")
    assert t.realized_pnl < 0


def test_backtest_skips_when_gap_too_big() -> None:
    fake = FakeAlpaca()
    intraday = _intraday_bars("2026-04-28",
        prices =  [125, 125, 125, 125, 125, 125],  # gapped 13.6% above signal_high
        volumes = [10_000, 12_000, 30_000, 35_000, 25_000, 25_000],
    )
    fake.set_intraday_bars("GAP", intraday)
    cfg = BacktestConfig(
        watchlist={
            date(2026, 4, 28): [{
                "symbol": "GAP", "signal_high": 110.0, "signal_low": 105.0,
                "signal_close": 109.0, "atr_14": 3.0, "rvol_eod": 2.4, "earnings_next": None,
            }],
        },
        start=date(2026, 4, 28), end=date(2026, 4, 28),
        equity=100_000, slippage_per_share=0.01,
    )
    trades = run_backtest(cfg=cfg, data=fake)
    assert trades == []
