"""Operator commands.

Usage:
  python -m cli.ops positions          # list local + Alpaca-side positions
  python -m cli.ops watchlist          # show today's active watchlist
  python -m cli.ops halt "reason"      # set halt flag
  python -m cli.ops resume             # clear halt flag + state halts
  python -m cli.ops flatten SYMBOL     # market-sell symbol (closes Alpaca + state)
  python -m cli.ops flatten-all        # market-sell ALL open positions
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from bot import config
from bot.executor import AlpacaExecutor
from bot.state import State

DATA_DIR = Path("data")
STATE_PATH = DATA_DIR / "state.sqlite"
HALT_FLAG = DATA_DIR / "halt.flag"
_ET = ZoneInfo("America/New_York")


def _state() -> State:
    s = State(STATE_PATH); s.init(); return s


def _executor():
    s = config.load()
    return AlpacaExecutor(api_key=s.alpaca_api_key, api_secret=s.alpaca_api_secret,
                          base_url=s.alpaca_base_url)


def cmd_positions(_args) -> int:
    state = _state()
    executor = _executor()
    local = {p.symbol: p for p in state.open_positions()}
    alpaca = executor.list_positions()
    syms = sorted(set(local) | set(alpaca))
    print(f"{'symbol':<8}{'local qty':<12}{'alpaca qty':<12}{'avg entry':<12}{'last':<10}{'pnl':<10}")
    for s in syms:
        l = local.get(s)
        a = alpaca.get(s)
        lq = l.qty if l else "-"
        aq = a["qty"] if a else "-"
        ae = f"{a['avg_entry_price']:.2f}" if a else "-"
        cp = f"{a['current_price']:.2f}" if a else "-"
        pnl = f"{a['unrealized_pl']:+.2f}" if a else "-"
        print(f"{s:<8}{str(lq):<12}{str(aq):<12}{ae:<12}{cp:<10}{pnl:<10}")
    return 0


def cmd_watchlist(_args) -> int:
    state = _state()
    today = datetime.now(timezone.utc).astimezone(_ET).date().isoformat()
    rows = state.active_watchlist(today)
    print(f"Active watchlist for {today}: {len(rows)} symbols")
    for r in sorted(rows, key=lambda x: -x.rvol_eod):
        print(f"  {r.symbol:<6} signal_high={r.signal_high:.2f}  rvol={r.rvol_eod:.2f}  attempts={r.breakout_attempts}")
    return 0


def cmd_halt(args) -> int:
    HALT_FLAG.parent.mkdir(parents=True, exist_ok=True)
    HALT_FLAG.write_text(args.reason)
    state = _state()
    state.set_halt(datetime.now(timezone.utc).isoformat(), args.reason)
    print(f"HALTED: {args.reason}")
    return 0


def cmd_resume(_args) -> int:
    if HALT_FLAG.exists():
        HALT_FLAG.unlink()
    state = _state()
    state.clear_halt(datetime.now(timezone.utc).isoformat())
    print("Resumed (halt cleared)")
    return 0


def cmd_flatten(args) -> int:
    executor = _executor()
    positions = executor.list_positions()
    if args.symbol not in positions:
        print(f"No Alpaca position for {args.symbol}", file=sys.stderr)
        return 1
    qty = positions[args.symbol]["qty"]
    executor.submit_market_sell(symbol=args.symbol, qty=qty)
    state = _state()
    pos = state.position_by_symbol(args.symbol)
    if pos:
        state.close_position(
            pos_id=pos.id, exit_time=datetime.now(timezone.utc).isoformat(),
            exit_price=positions[args.symbol]["current_price"],
            exit_reason="manual", realized_pnl=positions[args.symbol]["unrealized_pl"],
        )
    print(f"Flatten requested: {args.symbol} qty={qty}")
    return 0


def cmd_flatten_all(_args) -> int:
    executor = _executor()
    for sym, info in executor.list_positions().items():
        executor.submit_market_sell(symbol=sym, qty=info["qty"])
        print(f"  flatten {sym} qty={info['qty']}")
    state = _state()
    for pos in state.open_positions():
        state.close_position(
            pos_id=pos.id, exit_time=datetime.now(timezone.utc).isoformat(),
            exit_price=pos.entry_price or 0.0, exit_reason="manual", realized_pnl=0.0,
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("positions").set_defaults(fn=cmd_positions)
    sub.add_parser("watchlist").set_defaults(fn=cmd_watchlist)
    halt_p = sub.add_parser("halt"); halt_p.add_argument("reason"); halt_p.set_defaults(fn=cmd_halt)
    sub.add_parser("resume").set_defaults(fn=cmd_resume)
    flat_p = sub.add_parser("flatten"); flat_p.add_argument("symbol"); flat_p.set_defaults(fn=cmd_flatten)
    sub.add_parser("flatten-all").set_defaults(fn=cmd_flatten_all)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
