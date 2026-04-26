"""Long-running polling trader. Started by systemd at ~9:25 ET, killed at ~16:05 ET."""
from __future__ import annotations

import signal
import sys
import time as _time
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Protocol
from zoneinfo import ZoneInfo

import pandas as pd

from bot import config
from bot.alerts import TelegramAlerts
from bot.data.alpaca_data import AlpacaMarketData
from bot.data.base import MarketDataProvider
from bot.data.earnings import YFinanceEarnings
from bot.entry import evaluate_entry
from bot.executor import AlpacaExecutor
from bot.exit import (
    evaluate_exit, hard_stop_price, should_activate_trailing, target_price,
    update_trailing_stop,
)
from bot.logger import get_logger
from bot.reconcile import reconcile_positions
from bot.risk import can_open_new_position, position_size
from bot.state import Position, State, WatchlistEntry


_ET = ZoneInfo("America/New_York")
DATA_DIR = Path("data")
STATE_PATH = DATA_DIR / "state.sqlite"
HALT_FLAG = DATA_DIR / "halt.flag"
LOG_DIR = DATA_DIR / "logs"


# --- helpers (testable) ---

def poll_interval_for(
    now: datetime, market_open: datetime, fast_window_min: int,
    fast_sec: int, normal_sec: int,
) -> int:
    elapsed_min = (now - market_open).total_seconds() / 60.0
    return fast_sec if 0 <= elapsed_min < fast_window_min else normal_sec


@dataclass
class OpenPositionContext:
    pass  # placeholder for future per-cycle telemetry


def manage_open_positions(
    state: State,
    data: MarketDataProvider,
    executor: Any,
    now: datetime,
    earnings_dates: dict[str, date | None],
    trail_activation_pct: float,
    trail_distance_pct: float,
    profit_target_pct: float,
    time_stop_days: int,
    log=None,
) -> None:
    for pos in state.open_positions():
        try:
            trade = data.get_latest_trade(pos.symbol)
        except Exception as e:
            if log: log.warning("price_fetch_failed", extra={"symbol": pos.symbol, "err": str(e)})
            continue
        last = trade.price

        # Update high-water mark
        new_high = max(pos.highest_price_since_entry, last)

        # Trailing-stop activation/update
        new_stop = pos.current_stop
        new_trailing = pos.trailing_active
        if not pos.trailing_active and should_activate_trailing(
            entry=pos.entry_price or 0.0, current_high=new_high,
            activation_pct=trail_activation_pct,
        ):
            new_stop = update_trailing_stop(new_high, trail_distance_pct)
            new_trailing = True
        elif pos.trailing_active:
            candidate = update_trailing_stop(new_high, trail_distance_pct)
            if candidate > new_stop:
                new_stop = candidate

        if new_stop != pos.current_stop or new_high != pos.highest_price_since_entry:
            state.update_position_stop(pos.id, current_stop=new_stop,
                                       highest=new_high, trailing=new_trailing)

        # Exit decision
        unrealized = (last - (pos.entry_price or 0.0)) * (pos.qty or 0)
        decision = evaluate_exit(
            last_price=last, entry=pos.entry_price or 0.0,
            current_stop=new_stop, highest_since_entry=new_high,
            trailing_active=new_trailing, entry_time=datetime.fromisoformat(pos.entry_time),
            now=now, earnings_date=earnings_dates.get(pos.symbol),
            unrealized_pnl=unrealized,
            profit_pct=profit_target_pct, time_stop_days=time_stop_days,
        )
        if decision.should_exit:
            try:
                executor.submit_market_sell(symbol=pos.symbol, qty=pos.qty)
            except Exception as e:
                if log: log.warning("exit_failed", extra={"symbol": pos.symbol, "err": str(e)})
                continue
            state.close_position(
                pos_id=pos.id, exit_time=now.isoformat(),
                exit_price=last, exit_reason=decision.reason,
                realized_pnl=unrealized,
            )


def try_open_new_entries(
    state: State,
    data: MarketDataProvider,
    executor: Any,
    settings,
    now: datetime,
    daily_new_count: int,
    log=None,
    alerts: TelegramAlerts | None = None,
) -> int:
    """Iterate watchlist; return number of new entries placed this cycle."""
    today_str = now.astimezone(_ET).date().isoformat()
    placed = 0
    for entry in state.active_watchlist(today_str):
        check = can_open_new_position(
            state=state, max_open=settings.max_open_positions,
            max_daily_new=settings.max_daily_new_entries,
            daily_new_count=daily_new_count + placed,
            halt_flag_path=HALT_FLAG,
        )
        if not check.ok:
            return placed

        # Pull recent intraday bars + last trade
        try:
            today_open_dt = now.astimezone(_ET).replace(hour=9, minute=30, second=0, microsecond=0)
            bars = data.get_intraday_bars(
                entry.symbol, start=today_open_dt.astimezone(timezone.utc),
                end=now, timeframe_minutes=5,
            )
            if bars.empty:
                continue
            today_open = float(bars["open"].iloc[0])
            trade = data.get_latest_trade(entry.symbol)
        except Exception as e:
            if log: log.warning("intraday_fetch_failed", extra={"symbol": entry.symbol, "err": str(e)})
            continue

        decision = evaluate_entry(
            last_price=trade.price, signal_high=entry.signal_high,
            today_open=today_open, intraday_5m_bars=bars, now=now,
            gap_pct=settings.gap_skip_pct,
        )
        if not decision.should_enter:
            # Track failed-breakout: if we previously saw a trigger this session
            # and now price has fallen back below signal_high, deactivate.
            if entry.breakout_attempts > 0 and trade.price < entry.signal_high:
                state.deactivate_symbol(entry.scan_date, entry.symbol)
            continue

        # Compute stop + size
        equity = executor.get_equity()
        stop = hard_stop_price(
            entry=entry.signal_high + 0.02, signal_low=entry.signal_low,
            hard_stop_pct=settings.hard_stop_pct,
        )
        qty = position_size(
            equity=equity, entry=entry.signal_high + 0.02, stop=stop,
            per_trade_risk_pct=settings.per_trade_risk_pct,
        )
        if qty < 1:
            if log: log.info("skip_zero_qty", extra={"symbol": entry.symbol})
            continue

        stop_px = entry.signal_high + 0.02
        limit_px = stop_px * 1.003
        try:
            order = executor.submit_entry_stop_limit(
                symbol=entry.symbol, qty=qty,
                stop_price=stop_px, limit_price=limit_px,
            )
        except Exception as e:
            if log: log.warning("entry_submit_failed", extra={"symbol": entry.symbol, "err": str(e)})
            continue

        state.open_position(Position(
            symbol=entry.symbol, entry_order_id=order["id"],
            entry_time=now.isoformat(), entry_price=stop_px, qty=qty,
            signal_high=entry.signal_high, signal_low=entry.signal_low,
            initial_stop=stop, current_stop=stop,
            highest_price_since_entry=stop_px, trailing_active=False, status="open",
        ))
        state.increment_breakout_attempts(entry.scan_date, entry.symbol)
        placed += 1
        if alerts:
            alerts.send(alerts.format_signal(
                symbol=entry.symbol, qty=qty, entry=stop_px,
                stop=stop, target=target_price(stop_px, settings.profit_target_pct),
                rvol=entry.rvol_eod,
            ))
        if log: log.info("entry_placed", extra={
            "symbol": entry.symbol, "qty": qty, "stop": stop, "stop_px": stop_px,
        })
    return placed


# --- main loop ---

class _Halt:
    def __init__(self) -> None:
        self.set = False

    def trigger(self, *_args) -> None:
        self.set = True


def main() -> int:
    log = get_logger("trader", log_dir=LOG_DIR)
    settings = config.load()
    state = State(STATE_PATH); state.init()
    data = AlpacaMarketData(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        trading_base_url=settings.alpaca_base_url,
    )
    executor = AlpacaExecutor(
        api_key=settings.alpaca_api_key,
        api_secret=settings.alpaca_api_secret,
        base_url=settings.alpaca_base_url,
    )
    alerts = TelegramAlerts(token=settings.telegram_token, chat_id=settings.telegram_chat_id)
    earnings_provider = YFinanceEarnings()

    halt = _Halt()
    signal.signal(signal.SIGTERM, halt.trigger)
    signal.signal(signal.SIGINT, halt.trigger)

    consecutive_failures = 0
    daily_new_count = 0
    daily_count_date: date | None = None
    log.info("trader_start")
    alerts.send("Trader started")

    while not halt.set:
        cycle_start = datetime.now(timezone.utc)
        try:
            clock = data.get_clock()
            if not clock.is_open:
                # Compute wait until next open. If less than 30 min, sleep through it.
                # If more than 30 min, this means market is closed for the day → exit.
                wait_sec = (clock.next_open - datetime.now(timezone.utc)).total_seconds()
                if wait_sec <= 0:
                    # Should not happen, but defensive: poll again immediately
                    _time.sleep(5)
                    continue
                if wait_sec > 1800:  # > 30 min → market closed for the day
                    log.info("market_closed_exit", extra={"wait_sec": wait_sec})
                    break
                # Within 30 min of open → sleep until then, then loop
                log.info("waiting_for_open", extra={"wait_sec": wait_sec})
                _time.sleep(wait_sec + 5)
                continue

            today_et = cycle_start.astimezone(_ET).date()
            if daily_count_date != today_et:
                daily_count_date = today_et
                daily_new_count = 0

            # 1. Reconcile
            report = reconcile_positions(state=state, executor=executor, now=cycle_start)
            if report.closed_locally:
                log.info("reconcile_closed", extra={"symbols": report.closed_locally})

            # 2. Lookup earnings for symbols held + on watchlist
            held = [p.symbol for p in state.open_positions()]
            wl = [w.symbol for w in state.active_watchlist(today_et.isoformat())]
            earnings_dates: dict[str, date | None] = {
                s: earnings_provider.next_earnings(s) for s in set(held) | set(wl)
            }

            # 3. Manage open positions
            manage_open_positions(
                state=state, data=data, executor=executor, now=cycle_start,
                earnings_dates=earnings_dates,
                trail_activation_pct=settings.trail_activation_pct,
                trail_distance_pct=settings.trail_distance_pct,
                profit_target_pct=settings.profit_target_pct,
                time_stop_days=settings.time_stop_days, log=log,
            )

            # 4. New entries
            placed = try_open_new_entries(
                state=state, data=data, executor=executor,
                settings=settings, now=cycle_start,
                daily_new_count=daily_new_count, log=log, alerts=alerts,
            )
            daily_new_count += placed

            # 5. Heartbeat
            duration_ms = int((datetime.now(timezone.utc) - cycle_start).total_seconds() * 1000)
            state.record_cycle(
                cycle_at=cycle_start.isoformat(),
                duration_ms=duration_ms,
                positions_open=len(state.open_positions()),
                watchlist_size=len(state.active_watchlist(today_et.isoformat())),
            )
            log.info("heartbeat", extra={
                "duration_ms": duration_ms,
                "positions_open": len(state.open_positions()),
                "watchlist_size": len(state.active_watchlist(today_et.isoformat())),
            })
            consecutive_failures = 0

        except Exception as e:
            consecutive_failures += 1
            log.warning("cycle_failed", extra={"err": str(e), "consecutive": consecutive_failures})
            if consecutive_failures == 3:
                alerts.send(f"3 consecutive cycle failures: {e}")
            backoff = min(60, 5 * (3 ** (consecutive_failures - 1)))
            _time.sleep(backoff)
            continue

        # 6. Sleep until next cycle
        market_open = clock.next_open if not clock.is_open else (
            cycle_start.astimezone(_ET).replace(hour=9, minute=30, second=0, microsecond=0).astimezone(timezone.utc)
        )
        interval = poll_interval_for(
            now=cycle_start, market_open=market_open,
            fast_window_min=settings.fast_poll_end_min,
            fast_sec=settings.poll_interval_fast_sec,
            normal_sec=settings.poll_interval_sec,
        )
        elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
        _time.sleep(max(0, interval - elapsed))

    alerts.send("Trader stopped")
    log.info("trader_stop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
