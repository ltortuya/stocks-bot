"""Build the daily eligible universe from NDX UNION SPX with liquidity filters."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd

from bot.data.base import MarketDataProvider


@dataclass(frozen=True)
class EligibilityRow:
    symbol: str
    last_close: float
    avg_dollar_vol: float


def load_exclusions(path: Path | str) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["symbol"].strip().upper() for row in reader if row.get("symbol")}


def _load_symbol_csv(path: Path | str) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["symbol"].strip().upper() for row in reader if row.get("symbol")}


def build_universe(
    sp500_csv: Path | str,
    ndx_csv: Path | str,
    exclusions_csv: Path | str,
    data: MarketDataProvider,
    as_of: datetime,
    min_price: float = 10.0,
    min_dollar_vol: float = 25_000_000,
    lookback_days: int = 45,
) -> list[EligibilityRow]:
    """Return symbols passing price + dollar-volume + exclusion filters as of `as_of`."""
    base = (_load_symbol_csv(sp500_csv) | _load_symbol_csv(ndx_csv))
    excl = load_exclusions(exclusions_csv)
    candidates = sorted(base - excl)

    start = as_of - timedelta(days=lookback_days)
    eligible: list[EligibilityRow] = []
    for symbol in candidates:
        try:
            bars = data.get_daily_bars(symbol, start=start, end=as_of)
        except Exception:
            continue
        if bars.empty or len(bars) < 20:
            continue
        last_close = float(bars["close"].iloc[-1])
        if last_close < min_price:
            continue
        recent = bars.tail(30)
        avg_dollar_vol = float((recent["close"] * recent["volume"]).mean())
        if avg_dollar_vol < min_dollar_vol:
            continue
        eligible.append(EligibilityRow(
            symbol=symbol, last_close=last_close, avg_dollar_vol=avg_dollar_vol,
        ))
    return eligible
