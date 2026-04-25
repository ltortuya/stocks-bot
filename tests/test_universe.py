"""Tests for bot.universe."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from bot.universe import build_universe, load_exclusions, EligibilityRow
from tests.fakes.fake_alpaca import FakeAlpaca
from tests.fakes.fake_data import make_daily_bars


def _write_csv(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_load_exclusions_returns_set(tmp_path: Path) -> None:
    p = tmp_path / "exclusions.csv"
    _write_csv(p, ["symbol,reason", "TQQQ,leveraged-3x", "SQQQ,inverse-3x"])
    excl = load_exclusions(p)
    assert "TQQQ" in excl
    assert "SQQQ" in excl
    assert "AAPL" not in excl


def test_build_universe_filters_by_price_and_dollar_volume(tmp_path: Path) -> None:
    sp_csv = tmp_path / "sp500.csv"
    nd_csv = tmp_path / "ndx.csv"
    excl_csv = tmp_path / "exclusions.csv"
    _write_csv(sp_csv, ["symbol", "AAPL", "PENNY"])
    _write_csv(nd_csv, ["symbol", "AAPL", "TQQQ"])  # AAPL appears in both -> dedup
    _write_csv(excl_csv, ["symbol,reason", "TQQQ,leveraged"])

    fake = FakeAlpaca()
    # AAPL: price 200, vol 50M -> dollar vol 10B -> pass
    fake.set_daily_bars("AAPL", make_daily_bars("2026-04-01", periods=30, base_price=200, daily_volume=50_000_000))
    # PENNY: price 5 -> fail price filter
    fake.set_daily_bars("PENNY", make_daily_bars("2026-04-01", periods=30, base_price=5, daily_volume=50_000_000))
    # TQQQ: in exclusions, even though price/volume would pass

    eligible = build_universe(
        sp500_csv=sp_csv, ndx_csv=nd_csv, exclusions_csv=excl_csv,
        data=fake, as_of=__import__("datetime").datetime(2026, 4, 30,
                                                       tzinfo=__import__("datetime").timezone.utc),
        min_price=10.0, min_dollar_vol=25_000_000,
    )
    symbols = {row.symbol for row in eligible}
    assert "AAPL" in symbols
    assert "PENNY" not in symbols
    assert "TQQQ" not in symbols
    aapl = next(r for r in eligible if r.symbol == "AAPL")
    assert aapl.last_close > 200
    assert aapl.avg_dollar_vol > 25_000_000


def test_build_universe_skips_symbols_with_no_bars(tmp_path: Path) -> None:
    sp_csv = tmp_path / "sp500.csv"
    nd_csv = tmp_path / "ndx.csv"
    excl_csv = tmp_path / "exclusions.csv"
    _write_csv(sp_csv, ["symbol", "GHOST"])
    _write_csv(nd_csv, ["symbol"])
    _write_csv(excl_csv, ["symbol,reason"])

    fake = FakeAlpaca()  # no bars set for GHOST

    eligible = build_universe(
        sp500_csv=sp_csv, ndx_csv=nd_csv, exclusions_csv=excl_csv,
        data=fake, as_of=__import__("datetime").datetime(2026, 4, 30,
                                                       tzinfo=__import__("datetime").timezone.utc),
        min_price=10.0, min_dollar_vol=25_000_000,
    )
    assert eligible == []
