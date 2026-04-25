"""Refresh data/universe/sp500.csv and ndx.csv from Wikipedia tables.

Run monthly via cron: `python -m cli.refresh_universe`
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
NDX_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"

OUT_DIR = Path("data/universe")


def _scrape_sp500() -> list[str]:
    tables = pd.read_html(SP500_URL)
    df = tables[0]
    if "Symbol" not in df.columns:
        raise RuntimeError(f"Unexpected SP500 table columns: {list(df.columns)}")
    return [str(s).strip().upper().replace(".", "-") for s in df["Symbol"].tolist()]


def _scrape_ndx() -> list[str]:
    tables = pd.read_html(NDX_URL)
    candidate = None
    for t in tables:
        cols = {str(c).strip() for c in t.columns}
        if "Ticker" in cols or "Symbol" in cols:
            candidate = t
            break
    if candidate is None:
        raise RuntimeError("Could not locate NDX constituents table")
    col = "Ticker" if "Ticker" in candidate.columns else "Symbol"
    return [str(s).strip().upper().replace(".", "-") for s in candidate[col].tolist()]


def _write(path: Path, symbols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    rows = []
    for s in symbols:
        if s and s not in seen:
            seen.add(s)
            rows.append({"symbol": s})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    try:
        sp = _scrape_sp500()
        nd = _scrape_ndx()
    except Exception as e:
        print(f"refresh_universe failed: {e}", file=sys.stderr)
        return 1
    _write(OUT_DIR / "sp500.csv", sp)
    _write(OUT_DIR / "ndx.csv", nd)
    print(f"wrote {len(sp)} SP500 + {len(nd)} NDX symbols")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
