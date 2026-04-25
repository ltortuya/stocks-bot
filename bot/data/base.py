"""Abstract market data interface — concrete impls in alpaca_data.py etc."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class LatestTrade:
    symbol: str
    price: float
    timestamp: datetime


@dataclass(frozen=True)
class MarketClock:
    is_open: bool
    next_open: datetime
    next_close: datetime
    timestamp: datetime


class MarketDataProvider(ABC):
    """Strategy code depends only on this interface, not on Alpaca specifically."""

    @abstractmethod
    def get_clock(self) -> MarketClock: ...

    @abstractmethod
    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        """Returns DataFrame indexed by timestamp with columns [open,high,low,close,volume]."""

    @abstractmethod
    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame: ...

    @abstractmethod
    def get_latest_trade(self, symbol: str) -> LatestTrade: ...

    @abstractmethod
    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        """Batch latest-trade lookup. Default impl in subclasses can iterate get_latest_trade."""
