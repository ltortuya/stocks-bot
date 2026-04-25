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
