"""Backtest entry point.

Usage:
  python -m cli.run_backtest --start 2025-01-01 --end 2026-04-01 --equity 100000
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from backtest.engine import BacktestConfig, run_backtest
from backtest.metrics import compute_summary
from backtest.report import write_summary_json, write_trades_csv
from bot import config
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.earnings import YFinanceEarnings
from bot.scanner import scan, ScanCriteria
from bot.universe import build_universe

UNIVERSE_DIR = Path("data/universe")
RESULTS_DIR = Path("backtest/results")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True, help="YYYY-MM-DD")
    p.add_argument("--end", required=True, help="YYYY-MM-DD")
    p.add_argument("--equity", type=float, default=100_000.0)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    settings = config.load()

    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    earnings = YFinanceEarnings()

    # Build daily watchlists by replaying scanner over date range
    watchlist: dict[date, list[dict]] = {}
    cur = start - timedelta(days=1)  # scan EOD of (start-1) for start's session
    while cur <= end:
        if cur.weekday() < 5:
            as_of = datetime.combine(cur, datetime.min.time(), tzinfo=timezone.utc).replace(hour=20)
            eligible = build_universe(
                sp500_csv=UNIVERSE_DIR / "sp500.csv",
                ndx_csv=UNIVERSE_DIR / "ndx.csv",
                exclusions_csv=UNIVERSE_DIR / "exclusions.csv",
                data=data, as_of=as_of,
                min_price=settings.min_price, min_dollar_vol=settings.min_dollar_vol,
            )
            results = scan(
                eligible=eligible, data=data, earnings=earnings, as_of=as_of,
                criteria=ScanCriteria(
                    pct_change_min=settings.pct_change_min,
                    rvol_min=settings.rvol_min,
                    near_breakout_pct=settings.near_breakout_pct,
                    lookback_breakout=settings.lookback_breakout,
                ),
            )
            next_session = cur + timedelta(days=1)
            while next_session.weekday() >= 5:
                next_session += timedelta(days=1)
            if next_session <= end:
                watchlist[next_session] = [
                    {
                        "symbol": r.symbol, "signal_high": r.signal_high,
                        "signal_low": r.signal_low, "signal_close": r.signal_close,
                        "atr_14": r.atr_14, "rvol_eod": r.rvol_eod,
                        "earnings_next": r.earnings_next,
                    }
                    for r in results
                ]
            print(f"  {cur}: {len(results)} candidates for {next_session}")
        cur += timedelta(days=1)

    cfg = BacktestConfig(
        watchlist=watchlist, start=start, end=end, equity=args.equity,
        profit_target_pct=settings.profit_target_pct,
        hard_stop_pct=settings.hard_stop_pct,
        trail_activation_pct=settings.trail_activation_pct,
        trail_distance_pct=settings.trail_distance_pct,
        time_stop_days=settings.time_stop_days,
        gap_skip_pct=settings.gap_skip_pct,
        per_trade_risk_pct=settings.per_trade_risk_pct,
        max_open_positions=settings.max_open_positions,
    )
    trades = run_backtest(cfg=cfg, data=data)
    summary = compute_summary(trades=trades, starting_equity=args.equity)

    run_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:6]}"
    out_dir = RESULTS_DIR / run_id
    write_trades_csv(trades, out_dir / "trades.csv")
    write_summary_json(summary, out_dir / "summary.json")

    print()
    print(json.dumps(summary, indent=2, default=str))
    print(f"\nWrote {len(trades)} trades to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
