"""Bar-replay backtester for the momentum strategy."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

from bot.data.base import MarketDataProvider
from bot.entry import gap_skip, in_entry_time_window, volume_confirms
from bot.exit import (
    earnings_exit_due, hard_stop_price, should_activate_trailing,
    target_price, time_stop_due, update_trailing_stop,
)
from bot.risk import position_size


_ET = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class BacktestTrade:
    symbol: str
    entry_time: datetime
    entry_price: float
    qty: int
    exit_time: datetime
    exit_price: float
    exit_reason: str
    realized_pnl: float


@dataclass
class BacktestConfig:
    watchlist: dict[date, list[dict]]
    start: date
    end: date
    equity: float = 100_000.0
    slippage_per_share: float = 0.01
    profit_target_pct: float = 0.10
    hard_stop_pct: float = 0.05
    trail_activation_pct: float = 0.06
    trail_distance_pct: float = 0.05
    time_stop_days: int = 5
    gap_skip_pct: float = 0.08
    per_trade_risk_pct: float = 0.015
    max_open_positions: int = 3
    vol_lookback_bars: int = 20


@dataclass
class _OpenPos:
    symbol: str
    entry_time: datetime
    entry_price: float
    qty: int
    signal_low: float
    current_stop: float
    highest: float
    trailing: bool
    earnings_date: date | None


def _walk_one_day(
    cfg: BacktestConfig, data: MarketDataProvider, day: date,
    open_positions: list[_OpenPos], equity: float,
) -> tuple[list[BacktestTrade], list[_OpenPos], float]:
    closed: list[BacktestTrade] = []
    survivors: list[_OpenPos] = []

    # Determine watchlist for this day
    candidates = cfg.watchlist.get(day, [])

    # Build a per-symbol bar dataframe for the trading day (5-min bars, 9:30–16:00 ET)
    day_open_et = datetime.combine(day, time(9, 30), tzinfo=_ET)
    day_close_et = datetime.combine(day, time(16, 0), tzinfo=_ET)
    start = day_open_et.astimezone(timezone.utc)
    end = day_close_et.astimezone(timezone.utc)

    # Symbols we need bars for: held + watchlist
    needed = {p.symbol for p in open_positions} | {c["symbol"] for c in candidates}
    bars: dict[str, pd.DataFrame] = {}
    for sym in needed:
        try:
            bars[sym] = data.get_intraday_bars(sym, start=start, end=end, timeframe_minutes=5)
            if bars[sym].empty:
                print(f"  [warn] {day} {sym}: bars empty (no intraday data)", flush=True)
        except Exception as e:
            print(f"  [warn] {day} {sym}: bars fetch failed: {e}", flush=True)
            bars[sym] = pd.DataFrame()

    # Build a chronological list of (timestamp, symbol)
    timestamps = sorted({ts for df in bars.values() for ts in df.index})
    triggered: dict[str, bool] = {c["symbol"]: False for c in candidates}

    for ts in timestamps:
        # 1. Manage open positions on this bar
        next_survivors: list[_OpenPos] = []
        for pos in open_positions:
            df = bars.get(pos.symbol)
            if df is None or df.empty or ts not in df.index:
                next_survivors.append(pos)
                continue
            row = df.loc[ts]
            high = float(row["high"]); low = float(row["low"]); close = float(row["close"])
            pos.highest = max(pos.highest, high)

            # Trailing-stop maintenance
            if not pos.trailing and should_activate_trailing(
                entry=pos.entry_price, current_high=pos.highest,
                activation_pct=cfg.trail_activation_pct,
            ):
                pos.current_stop = update_trailing_stop(pos.highest, cfg.trail_distance_pct)
                pos.trailing = True
            elif pos.trailing:
                cand = update_trailing_stop(pos.highest, cfg.trail_distance_pct)
                if cand > pos.current_stop:
                    pos.current_stop = cand

            target = target_price(pos.entry_price, cfg.profit_target_pct)
            unrealized = (close - pos.entry_price) * pos.qty

            exit_reason = None
            exit_px = close
            if high >= target:
                exit_reason = "target"; exit_px = target + cfg.slippage_per_share
            elif low <= pos.current_stop:
                exit_reason = "trail" if pos.trailing else "stop"
                exit_px = pos.current_stop - cfg.slippage_per_share
            elif time_stop_due(pos.entry_time, ts, days=cfg.time_stop_days):
                exit_reason = "time"; exit_px = close - cfg.slippage_per_share
            elif earnings_exit_due(ts.astimezone(_ET).date(), pos.earnings_date, unrealized):
                exit_reason = "earnings"; exit_px = close - cfg.slippage_per_share

            if exit_reason:
                pnl = (exit_px - pos.entry_price) * pos.qty
                closed.append(BacktestTrade(
                    symbol=pos.symbol, entry_time=pos.entry_time, entry_price=pos.entry_price,
                    qty=pos.qty, exit_time=ts, exit_price=exit_px,
                    exit_reason=exit_reason, realized_pnl=pnl,
                ))
                equity += pnl
            else:
                next_survivors.append(pos)
        open_positions = next_survivors

        # 2. Check entries
        if not in_entry_time_window(ts):
            continue
        if len(open_positions) >= cfg.max_open_positions:
            continue
        for cand in candidates:
            sym = cand["symbol"]
            if triggered.get(sym):
                continue
            df = bars.get(sym)
            if df is None or df.empty:
                if not triggered.get(sym):
                    print(f"  [skip] {day} {sym}: no bars", flush=True)
                    triggered[sym] = True
                continue
            if ts not in df.index:
                continue  # this candidate has no bar at this ts; try next ts
            day_open = float(df["open"].iloc[0])
            if gap_skip(day_open, cand["signal_high"], cfg.gap_skip_pct):
                gap_pct = (day_open / cand["signal_high"] - 1) * 100
                print(f"  [skip] {day} {sym}: gap_skip open={day_open:.2f} sig_hi={cand['signal_high']:.2f} ({gap_pct:+.2f}%)", flush=True)
                triggered[sym] = True
                continue
            row = df.loc[ts]
            if float(row["high"]) <= cand["signal_high"]:
                # No breakout yet at this ts; try next ts (don't set triggered)
                continue
            history = df.loc[:ts]
            if not volume_confirms(history, lookback_bars=cfg.vol_lookback_bars):
                cur_vol = float(history["volume"].iloc[-1]) if len(history) else 0
                prev_vol = float(history["volume"].iloc[-2]) if len(history) >= 2 else None
                print(f"  [skip] {day} {sym} @ {ts.strftime('%H:%M')}: vol_confirm fail (cur={cur_vol:.0f} prev={prev_vol})", flush=True)
                continue

            entry_px = cand["signal_high"] + 0.02 + cfg.slippage_per_share
            stop = hard_stop_price(
                entry=entry_px, signal_low=cand["signal_low"], hard_stop_pct=cfg.hard_stop_pct,
            )
            qty = position_size(equity=equity, entry=entry_px, stop=stop,
                                per_trade_risk_pct=cfg.per_trade_risk_pct)
            if qty < 1:
                print(f"  [skip] {day} {sym}: qty<1 entry={entry_px:.2f} stop={stop:.2f}", flush=True)
                triggered[sym] = True
                continue
            print(f"  [TRADE] {day} {sym} @ {ts.strftime('%H:%M')}: qty={qty} entry={entry_px:.2f} stop={stop:.2f}", flush=True)

            earn_str = cand.get("earnings_next")
            earn_date = (date.fromisoformat(earn_str)
                         if isinstance(earn_str, str) and earn_str else None)
            open_positions.append(_OpenPos(
                symbol=sym, entry_time=ts, entry_price=entry_px, qty=qty,
                signal_low=cand["signal_low"], current_stop=stop, highest=entry_px,
                trailing=False, earnings_date=earn_date,
            ))
            triggered[sym] = True

    return closed, open_positions, equity


def run_backtest(cfg: BacktestConfig, data: MarketDataProvider) -> list[BacktestTrade]:
    all_trades: list[BacktestTrade] = []
    open_positions: list[_OpenPos] = []
    equity = cfg.equity
    cur = cfg.start
    while cur <= cfg.end:
        if cur.weekday() < 5:
            closed, open_positions, equity = _walk_one_day(cfg, data, cur, open_positions, equity)
            all_trades.extend(closed)
        cur += timedelta(days=1)
    return all_trades
