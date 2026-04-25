"""Alpaca REST implementation of MarketDataProvider."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

import pandas as pd
import requests

from bot.data.base import Bar, LatestTrade, MarketClock, MarketDataProvider


def _parse_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


class AlpacaMarketData(MarketDataProvider):
    def __init__(
        self, api_key: str, api_secret: str,
        trading_base_url: str = "https://paper-api.alpaca.markets",
        data_base_url: str = "https://data.alpaca.markets",
        timeout_sec: float = 10.0,
    ) -> None:
        self.trading_base_url = trading_base_url.rstrip("/")
        self.data_base_url = data_base_url.rstrip("/")
        self.timeout = timeout_sec
        self._headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Accept": "application/json",
        }

    def _get(self, url: str, params: dict | None = None) -> dict:
        resp = requests.get(url, headers=self._headers, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_clock(self) -> MarketClock:
        d = self._get(f"{self.trading_base_url}/v2/clock")
        return MarketClock(
            is_open=bool(d["is_open"]),
            next_open=_parse_iso(d["next_open"]),
            next_close=_parse_iso(d["next_close"]),
            timestamp=_parse_iso(d["timestamp"]),
        )

    def _bars_to_df(self, bars: list[dict]) -> pd.DataFrame:
        if not bars:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        rows = [
            {
                "timestamp": _parse_iso(b["t"]),
                "open": b["o"], "high": b["h"], "low": b["l"],
                "close": b["c"], "volume": b["v"],
            }
            for b in bars
        ]
        return pd.DataFrame(rows).set_index("timestamp")

    def _fetch_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe: str,
    ) -> pd.DataFrame:
        all_bars: list[dict] = []
        page_token: str | None = None
        while True:
            params = {
                "timeframe": timeframe,
                "start": start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end": end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "limit": 10000,
                "feed": "iex",
                "adjustment": "split",
            }
            if page_token:
                params["page_token"] = page_token
            d = self._get(f"{self.data_base_url}/v2/stocks/{symbol}/bars", params=params)
            all_bars.extend(d.get("bars", []) or [])
            page_token = d.get("next_page_token")
            if not page_token:
                break
        return self._bars_to_df(all_bars)

    def get_daily_bars(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        return self._fetch_bars(symbol, start, end, timeframe="1Day")

    def get_intraday_bars(
        self, symbol: str, start: datetime, end: datetime, timeframe_minutes: int = 5,
    ) -> pd.DataFrame:
        return self._fetch_bars(symbol, start, end, timeframe=f"{timeframe_minutes}Min")

    def get_latest_trade(self, symbol: str) -> LatestTrade:
        d = self._get(f"{self.data_base_url}/v2/stocks/{symbol}/trades/latest")
        t = d["trade"]
        return LatestTrade(symbol=d["symbol"], price=t["p"], timestamp=_parse_iso(t["t"]))

    def get_latest_trades(self, symbols: Iterable[str]) -> dict[str, LatestTrade]:
        symbols = list(symbols)
        if not symbols:
            return {}
        d = self._get(
            f"{self.data_base_url}/v2/stocks/trades/latest",
            params={"symbols": ",".join(symbols), "feed": "iex"},
        )
        out: dict[str, LatestTrade] = {}
        for sym, payload in (d.get("trades") or {}).items():
            out[sym] = LatestTrade(symbol=sym, price=payload["p"], timestamp=_parse_iso(payload["t"]))
        return out
