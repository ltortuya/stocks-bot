"""Earnings calendar provider — pluggable so we can swap yfinance later."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Any

import pandas as pd


class EarningsProvider(ABC):
    @abstractmethod
    def next_earnings(self, symbol: str) -> date | None: ...


class YFinanceEarnings(EarningsProvider):
    def __init__(self, yf_module: Any | None = None) -> None:
        if yf_module is None:
            import yfinance as yf
            self._yf = yf
        else:
            self._yf = yf_module
        self._cache: dict[str, date | None] = {}

    def next_earnings(self, symbol: str) -> date | None:
        if symbol in self._cache:
            return self._cache[symbol]
        result = self._lookup(symbol)
        self._cache[symbol] = result
        return result

    def _lookup(self, symbol: str) -> date | None:
        try:
            cal = self._yf.Ticker(symbol).calendar
        except Exception:
            return None
        if cal is None:
            return None
        if isinstance(cal, dict):
            dates = cal.get("Earnings Date") or []
        elif isinstance(cal, pd.DataFrame):
            if "Earnings Date" not in cal.columns:
                return None
            dates = list(cal["Earnings Date"])
        else:
            return None
        if not dates:
            return None
        first = dates[0]
        if isinstance(first, pd.Timestamp):
            return first.date()
        if isinstance(first, date):
            return first
        try:
            return pd.Timestamp(first).date()
        except Exception:
            return None
