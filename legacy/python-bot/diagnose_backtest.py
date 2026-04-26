"""Diagnose why backtest 2026-04-20 to 2026-04-24 produced 0 trades from 10 candidates.

For every candidate the scanner produced for sessions 4/21–4/24, fetch that session's
5-min bars (Alpaca IEX feed), walk them, and identify the FIRST blocking gate
(gap_skip → high > signal_high → in_entry_time_window → volume_confirms → qty<1).

Usage: .venv/Scripts/python.exe scripts/diagnose_backtest.py
"""
from __future__ import annotations

import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

# Force UTF-8 stdout so Windows cp1252 doesn't choke on any non-ASCII glyphs.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Make project root importable regardless of cwd
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bot import config
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.earnings import YFinanceEarnings
from bot.entry import gap_skip, in_entry_time_window, volume_confirms
from bot.exit import hard_stop_price
from bot.risk import position_size
from bot.scanner import ScanCriteria, scan
from bot.universe import build_universe


_ET = ZoneInfo("America/New_York")
UNIVERSE_DIR = ROOT / "data" / "universe"

SCAN_START = date(2026, 4, 20)
SCAN_END = date(2026, 4, 24)
BACKTEST_RANGE_END = date(2026, 4, 24)  # candidates with target session > this excluded
EQUITY = 100_000.0
HARD_STOP_PCT = 0.05
PER_TRADE_RISK_PCT = 0.015
GAP_PCT = 0.08
VOL_LOOKBACK_BARS = 20
SLIPPAGE = 0.01


def next_weekday(d: date) -> date:
    nxt = d + timedelta(days=1)
    while nxt.weekday() >= 5:
        nxt += timedelta(days=1)
    return nxt


def rebuild_watchlist(data: AlpacaMarketData, earnings: YFinanceEarnings,
                      settings) -> dict[date, list[dict]]:
    """Replicate cli.run_backtest watchlist generation for the diagnostic window."""
    watchlist: dict[date, list[dict]] = {}
    cur = SCAN_START
    while cur <= SCAN_END:
        if cur.weekday() < 5:
            as_of = datetime.combine(cur, time(0, 0), tzinfo=timezone.utc).replace(hour=20)
            print(f"[scan] building universe + scanning EOD {cur} ...", flush=True)
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
            target = next_weekday(cur)
            print(f"  -> {len(results)} candidates for {target}", flush=True)
            if target <= BACKTEST_RANGE_END:
                watchlist[target] = [
                    {
                        "symbol": r.symbol, "signal_high": r.signal_high,
                        "signal_low": r.signal_low, "signal_close": r.signal_close,
                        "atr_14": r.atr_14, "rvol_eod": r.rvol_eod,
                        "earnings_next": r.earnings_next,
                    }
                    for r in results
                ]
        cur += timedelta(days=1)
    return watchlist


def diagnose_candidate(data: AlpacaMarketData, target_session: date,
                       cand: dict) -> dict:
    """Walk target_session bars; return diagnosis dict for this candidate."""
    sym = cand["symbol"]
    sh = float(cand["signal_high"])
    sl = float(cand["signal_low"])
    sc = float(cand["signal_close"])

    out = {
        "symbol": sym, "session": target_session,
        "signal_high": sh, "signal_low": sl, "signal_close": sc,
        "open": None, "gap_pct": None, "max_high": None,
        "trigger_time_et": None, "trigger_high": None, "trigger_low": None,
        "trigger_open": None, "trigger_close": None, "trigger_vol": None,
        "prior_vol": None, "avg20_vol": None,
        "in_window": None, "vol_pass": None, "qty": None,
        "result": None, "detail": None,
    }

    day_open_et = datetime.combine(target_session, time(9, 30), tzinfo=_ET)
    day_close_et = datetime.combine(target_session, time(16, 0), tzinfo=_ET)
    start = day_open_et.astimezone(timezone.utc)
    end = day_close_et.astimezone(timezone.utc)
    try:
        df = data.get_intraday_bars(sym, start=start, end=end, timeframe_minutes=5)
    except Exception as e:
        out["result"] = "NO_BARS"
        out["detail"] = f"fetch error: {e}"
        return out

    if df is None or df.empty:
        out["result"] = "NO_BARS"
        out["detail"] = "Alpaca returned empty bars"
        return out

    df = df.sort_index()
    day_open = float(df["open"].iloc[0])
    out["open"] = day_open
    out["gap_pct"] = (day_open / sh - 1.0) * 100.0
    out["max_high"] = float(df["high"].max())

    # 1. gap_skip
    if gap_skip(day_open, sh, GAP_PCT):
        out["result"] = "GAP_SKIP"
        out["detail"] = f"open {day_open:.2f} >= signal_high*{1+GAP_PCT:.2f} = {sh*(1+GAP_PCT):.2f}"
        return out

    # 2. find first bar where high > signal_high
    breakout = df[df["high"] > sh]
    if breakout.empty:
        out["result"] = "NO_BREAKOUT"
        out["detail"] = f"max high {out['max_high']:.2f} <= signal_high {sh:.2f}"
        return out

    first_ts = breakout.index[0]
    row = df.loc[first_ts]
    et_ts = first_ts.astimezone(_ET)
    out["trigger_time_et"] = et_ts.strftime("%H:%M ET")
    out["trigger_high"] = float(row["high"])
    out["trigger_low"] = float(row["low"])
    out["trigger_open"] = float(row["open"])
    out["trigger_close"] = float(row["close"])
    out["trigger_vol"] = float(row["volume"])

    history = df.loc[:first_ts]
    if len(history) >= 2:
        out["prior_vol"] = float(history["volume"].iloc[-2])
    if len(history) >= 2:
        prev_window = history["volume"].iloc[-(VOL_LOOKBACK_BARS + 1):-1]
        if len(prev_window) > 0:
            out["avg20_vol"] = float(prev_window.mean())

    # 3. window check (matches engine: in_entry_time_window of trigger ts)
    out["in_window"] = bool(in_entry_time_window(first_ts.to_pydatetime()))

    # 4. volume_confirms on history slice
    out["vol_pass"] = bool(volume_confirms(history, lookback_bars=VOL_LOOKBACK_BARS))

    # First blocking gate (engine order: window → max_open → triggered → gap → high → vol → qty)
    if not out["in_window"]:
        out["result"] = "OUT_OF_WINDOW"
        out["detail"] = f"first breakout at {et_ts.strftime('%H:%M')} ET outside 9:35–14:30"
        return out

    if not out["vol_pass"]:
        sub = []
        if out["prior_vol"] is not None and out["trigger_vol"] <= out["prior_vol"]:
            sub.append(f"vol {out['trigger_vol']:.0f} <= prior {out['prior_vol']:.0f}")
        if out["avg20_vol"] is not None and out["trigger_vol"] <= out["avg20_vol"]:
            sub.append(f"vol {out['trigger_vol']:.0f} <= avg20 {out['avg20_vol']:.0f}")
        if not sub:
            sub.append("history < 2 bars (cannot confirm)")
        out["result"] = "VOL_FAIL"
        out["detail"] = "; ".join(sub)
        return out

    # 5. position size
    entry_px = sh + 0.02 + SLIPPAGE
    stop = hard_stop_price(entry=entry_px, signal_low=sl, hard_stop_pct=HARD_STOP_PCT)
    qty = position_size(equity=EQUITY, entry=entry_px, stop=stop,
                        per_trade_risk_pct=PER_TRADE_RISK_PCT)
    out["qty"] = qty
    if qty < 1:
        out["result"] = "QTY_LT_1"
        out["detail"] = (f"entry {entry_px:.2f} stop {stop:.2f} risk/share "
                         f"{entry_px-stop:.2f} budget {PER_TRADE_RISK_PCT*EQUITY:.0f}")
        return out

    out["result"] = "WOULD_TRADE"
    out["detail"] = f"qty={qty} entry={entry_px:.2f} stop={stop:.2f}"
    return out


def fmt_num(v, w=8, dec=2):
    if v is None:
        return "  N/A   "[:w]
    if isinstance(v, float):
        return f"{v:>{w}.{dec}f}"
    return f"{str(v):>{w}}"


def fmt_vol(v):
    if v is None:
        return "   N/A"
    if v >= 1_000_000:
        return f"{v/1_000_000:>4.1f}M"
    if v >= 1_000:
        return f"{v/1_000:>4.1f}k"
    return f"{v:>5.0f}"


def print_table(rows: list[dict]) -> None:
    print()
    print("=" * 160)
    print("DIAGNOSTIC TABLE")
    print("=" * 160)
    header = (f"{'Symbol':<7}{'Session':<8}{'sigHi':>8} {'open':>8} {'gap%':>7}  "
              f"{'trigger':<10} {'trigHi':>8} {'vol':>7} {'prior':>7} {'avg20':>7}  "
              f"{'window':>7} {'qty':>5}  result / detail")
    print(header)
    print("-" * 160)
    for r in rows:
        try:
            sess = r["session"].strftime("%m/%d")
        except Exception:
            sess = str(r["session"])
        line = (
            f"{r['symbol']:<7}"
            f"{sess:<8}"
            f"{fmt_num(r['signal_high'])} "
            f"{fmt_num(r['open'])} "
            f"{fmt_num(r['gap_pct'], 7, 2)}  "
            f"{(r['trigger_time_et'] or 'N/A'):<10} "
            f"{fmt_num(r['trigger_high'])} "
            f"{fmt_vol(r['trigger_vol']):>7} "
            f"{fmt_vol(r['prior_vol']):>7} "
            f"{fmt_vol(r['avg20_vol']):>7}  "
            f"{('Y' if r['in_window'] else ('N' if r['in_window'] is False else '-')):>7} "
            f"{(str(r['qty']) if r['qty'] is not None else '-'):>5}  "
            f"{r['result']}: {r['detail']}"
        )
        print(line)
    print("=" * 160)


def print_summary(rows: list[dict]) -> None:
    print()
    print("RESULT TALLY")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<14} {v}")


def main() -> int:
    settings = config.load()
    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    earnings = YFinanceEarnings()

    print(f"Diagnosing backtest window {SCAN_START} -> {SCAN_END}")
    print(f"Equity ${EQUITY:,.0f}  hard_stop {HARD_STOP_PCT:.2%}  "
          f"per_trade_risk {PER_TRADE_RISK_PCT:.2%}  gap_skip {GAP_PCT:.2%}")
    print()

    watchlist = rebuild_watchlist(data, earnings, settings)
    total = sum(len(v) for v in watchlist.values())
    print(f"\n[scan] total candidates with target session in range: {total}")

    rows: list[dict] = []
    for session in sorted(watchlist.keys()):
        for cand in watchlist[session]:
            print(f"[diag] {cand['symbol']} for {session} ...", flush=True)
            rows.append(diagnose_candidate(data, session, cand))

    print_table(rows)
    print_summary(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
