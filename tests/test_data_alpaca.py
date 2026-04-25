"""Tests for the data layer."""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import pytest

from bot.data.base import MarketDataProvider, Bar, LatestTrade, MarketClock


def test_market_data_provider_is_abstract() -> None:
    with pytest.raises(TypeError):
        MarketDataProvider()  # type: ignore[abstract]


def test_bar_dataclass_round_trip() -> None:
    b = Bar(
        timestamp=datetime(2026, 4, 28, 13, 30, tzinfo=timezone.utc),
        open=100.0, high=101.0, low=99.5, close=100.5, volume=12345,
    )
    assert b.timestamp.tzinfo is not None
    assert b.high >= b.low


import responses

from bot.data.alpaca_data import AlpacaMarketData
from tests.fakes.fake_alpaca import FakeAlpaca


def _alpaca() -> AlpacaMarketData:
    return AlpacaMarketData(
        api_key="k", api_secret="s",
        trading_base_url="https://paper-api.alpaca.markets",
        data_base_url="https://data.alpaca.markets",
    )


@responses.activate
def test_get_clock_parses_alpaca_response() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/clock",
        json={
            "is_open": False,
            "next_close": "2026-04-27T16:00:00-04:00",
            "next_open": "2026-04-27T09:30:00-04:00",
            "timestamp": "2026-04-25T17:09:41-04:00",
        },
        status=200,
    )
    clock = _alpaca().get_clock()
    assert clock.is_open is False
    assert clock.next_open.isoformat().startswith("2026-04-27T09:30:00")


@responses.activate
def test_get_latest_trade_parses() -> None:
    responses.add(
        responses.GET,
        "https://data.alpaca.markets/v2/stocks/AAPL/trades/latest",
        json={"symbol": "AAPL", "trade": {"t": "2026-04-28T13:35:01Z", "p": 215.42, "s": 100}},
        status=200,
    )
    t = _alpaca().get_latest_trade("AAPL")
    assert t.symbol == "AAPL"
    assert t.price == 215.42


@responses.activate
def test_get_daily_bars_returns_dataframe() -> None:
    responses.add(
        responses.GET,
        "https://data.alpaca.markets/v2/stocks/AAPL/bars",
        json={
            "bars": [
                {"t": "2026-04-24T04:00:00Z", "o": 210, "h": 213, "l": 209, "c": 212, "v": 50_000_000},
                {"t": "2026-04-25T04:00:00Z", "o": 212, "h": 215, "l": 211, "c": 214, "v": 60_000_000},
            ],
            "next_page_token": None,
        },
        status=200,
    )
    df = _alpaca().get_daily_bars(
        "AAPL",
        start=__import__("datetime").datetime(2026, 4, 24, tzinfo=__import__("datetime").timezone.utc),
        end=__import__("datetime").datetime(2026, 4, 25, 23, 59, tzinfo=__import__("datetime").timezone.utc),
    )
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert df["close"].iloc[-1] == 214


def test_fake_alpaca_implements_interface() -> None:
    fake = FakeAlpaca()
    fake.set_latest_trade("AAPL", price=215.42)
    t = fake.get_latest_trade("AAPL")
    assert t.price == 215.42
    clock = fake.get_clock()
    assert clock.is_open in (True, False)
