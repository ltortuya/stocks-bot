"""Daily scanner entry point.

Wired by cron at 4:05 PM ET Mon–Fri:
  cd ~/stocks_monitoring && .venv/bin/python -m cli.run_scanner
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from bot import config
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.earnings import YFinanceEarnings
from bot.logger import get_logger
from bot.scanner import scan, ScanCriteria
from bot.state import State
from bot.universe import build_universe

DATA_DIR = Path("data")
UNIVERSE_DIR = DATA_DIR / "universe"
STATE_PATH = DATA_DIR / "state.sqlite"
LOG_DIR = DATA_DIR / "logs"


def main() -> int:
    log = get_logger("scanner", log_dir=LOG_DIR)
    settings = config.load()

    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    earnings = YFinanceEarnings()
    state = State(STATE_PATH)
    state.init()

    as_of = datetime.now(timezone.utc)
    log.info("scan_start", extra={"as_of": as_of.isoformat()})

    eligible = build_universe(
        sp500_csv=UNIVERSE_DIR / "sp500.csv",
        ndx_csv=UNIVERSE_DIR / "ndx.csv",
        exclusions_csv=UNIVERSE_DIR / "exclusions.csv",
        data=data, as_of=as_of,
        min_price=settings.min_price,
        min_dollar_vol=settings.min_dollar_vol,
    )
    log.info("universe_built", extra={"count": len(eligible)})

    results = scan(
        eligible=eligible, data=data, earnings=earnings, as_of=as_of,
        criteria=ScanCriteria(
            pct_change_min=settings.pct_change_min,
            rvol_min=settings.rvol_min,
            near_breakout_pct=settings.near_breakout_pct,
            lookback_breakout=settings.lookback_breakout,
        ),
    )
    state.upsert_watchlist(results)
    log.info("scan_done", extra={"watchlist_size": len(results),
                                  "symbols": [r.symbol for r in results]})

    # Telegram digest deferred to Task 18 wiring; print for now.
    print(f"Scan complete: {len(results)} candidates for next session")
    for r in sorted(results, key=lambda x: -x.rvol_eod)[:10]:
        print(f"  {r.symbol}  rvol={r.rvol_eod:.2f}  signal_high={r.signal_high:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
