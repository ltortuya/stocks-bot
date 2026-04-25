"""Tests for bot.data.earnings."""
from __future__ import annotations

from datetime import date

import pandas as pd
import pytest

from bot.data.earnings import EarningsProvider, YFinanceEarnings


class _StubYf:
    def __init__(self, calendar: dict | pd.DataFrame | None) -> None:
        self._calendar = calendar

    def Ticker(self, symbol: str):  # noqa: N802
        outer = self
        class _T:
            calendar = outer._calendar
        return _T()


def test_yfinance_earnings_returns_next_date(monkeypatch) -> None:
    yf = _StubYf({"Earnings Date": [date(2026, 5, 2)]})
    provider = YFinanceEarnings(yf_module=yf)
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)


def test_yfinance_earnings_handles_dataframe_form(monkeypatch) -> None:
    df = pd.DataFrame({"Earnings Date": [pd.Timestamp("2026-05-02")]})
    yf = _StubYf(df)
    provider = YFinanceEarnings(yf_module=yf)
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)


def test_yfinance_earnings_returns_none_when_unknown(monkeypatch) -> None:
    provider = YFinanceEarnings(yf_module=_StubYf(None))
    assert provider.next_earnings("ZZZZ") is None


def test_yfinance_earnings_caches_results() -> None:
    yf = _StubYf({"Earnings Date": [date(2026, 5, 2)]})
    provider = YFinanceEarnings(yf_module=yf)
    provider.next_earnings("AAPL")
    yf._calendar = None  # would return None on a fresh fetch
    assert provider.next_earnings("AAPL") == date(2026, 5, 2)  # served from cache
