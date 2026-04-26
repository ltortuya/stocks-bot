"""In-memory MarketDataProvider used in unit tests + backtest dry-runs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import pandas as pd

from bot.data.base import LatestTrade, MarketClock, MarketDataProvider


class FakeAlpaca(MarketDataProvider):
    def __init__(self) -> None:
        self._daily: dict[str, pd.DataFrame] = {}
        self._intraday: dict[str, pd.DataFrame] = {}
        self._latest: dict[str, LatestTrade] = {}
        self._clock = MarketClock(
            is_open=True,
            next_open=datetime(2026, 4, 27, 13, 30, tzinfo=timezone.utc),
            next_close=datetime(2026, 4, 25, 20, 0, tzinfo=timezone.utc),
            timestamp=datetime(2026, 4, 25, 17, 0, tzinfo=timezone.utc),
        )

    def set_clock(self, clock: MarketClock) -> None:
        self._clock = clock

    def set_daily_bars(self, symbol: str, df: pd.DataFrame) -> None:
        self._daily[symbol] = df

    def set_intraday_bars(self, symbol: str, df: pd.DataFrame) -> None:
        self._intraday[symbol] = df

    def set_latest_trade(self, symbol: str, price: float, ts: datetime | None = None) -> None:
        self._latest[symbol] = LatestTrade(
            symbol=symbol, price=price,
            timestamp=ts or datetime.now(timezone.utc),
        )

    def get_clock(self) -> MarketClock:
        return self._clock

    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        df = self._daily.get(symbol, pd.DataFrame(columns=["open","high","low","close","volume"]))
        if df.empty:
            return df
        return df[(df.index >= start) & (df.index <= end)]

    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame:
        df = self._intraday.get(symbol, pd.DataFrame(columns=["open","high","low","close","volume"]))
        if df.empty:
            return df
        return df[(df.index >= start) & (df.index <= end)]

    def get_latest_trade(self, symbol: str) -> LatestTrade:
        if symbol not in self._latest:
            raise KeyError(f"FakeAlpaca: no latest trade set for {symbol}")
        return self._latest[symbol]

    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        return {s: self._latest[s] for s in symbols if s in self._latest}
