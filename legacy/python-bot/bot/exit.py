"""Exit decision logic: target / stop / trailing / time / earnings."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


_ET = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class ExitDecision:
    should_exit: bool
    reason: str | None = None  # target | stop | trail | time | earnings


def target_price(entry: float, profit_pct: float = 0.10) -> float:
    return entry * (1 + profit_pct)


def hard_stop_price(entry: float, signal_low: float, hard_stop_pct: float = 0.05) -> float:
    """Tighter (closer to entry) of signal_low or entry*(1-pct)."""
    pct_stop = entry * (1 - hard_stop_pct)
    return max(signal_low, pct_stop)


def should_activate_trailing(entry: float, current_high: float, activation_pct: float = 0.06) -> bool:
    return current_high >= entry * (1 + activation_pct)


def update_trailing_stop(highest_price: float, distance_pct: float = 0.05) -> float:
    return highest_price * (1 - distance_pct)


def _trading_days_between(start: date, end: date) -> int:
    """Counts trading days (Mon–Fri) from `start` through `end` inclusive on both ends.
    Entry day counts as day 1, so this returns the ordinal day number of `end`
    relative to `start` when both are weekdays."""
    if end < start:
        return 0
    days = 0
    cur = start
    while cur <= end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days


def time_stop_due(entry_time: datetime, now: datetime, days: int = 5) -> bool:
    """True at/after 3:50 PM ET on the Nth trading day OF THE TRADE.

    Convention: the entry day counts as day 1. So with `days=5`, a Monday entry
    triggers the time stop at Friday 3:50 PM ET (Mon=1, Tue=2, Wed=3, Thu=4, Fri=5).
    """
    entry_d = entry_time.astimezone(_ET).date()
    now_et = now.astimezone(_ET)
    elapsed = _trading_days_between(entry_d, now_et.date())
    if elapsed < days:
        return False
    return now_et.timetz() >= time(15, 50, tzinfo=_ET)


def earnings_exit_due(today: date, earnings_date: date | None, unrealized_pnl: float) -> bool:
    """If earnings is tomorrow and we are NOT profitable, exit."""
    if earnings_date is None:
        return False
    days_until = (earnings_date - today).days
    if days_until != 1:
        return False
    return unrealized_pnl <= 0


def evaluate_exit(
    last_price: float,
    entry: float,
    current_stop: float,
    highest_since_entry: float,
    trailing_active: bool,
    entry_time: datetime,
    now: datetime,
    earnings_date: date | None,
    unrealized_pnl: float,
    *,
    profit_pct: float = 0.10,
    time_stop_days: int = 5,
) -> ExitDecision:
    """Order: target → stop → time → earnings. Caller manages trailing-stop updates."""
    if last_price >= target_price(entry, profit_pct):
        return ExitDecision(True, "target")
    if last_price <= current_stop:
        return ExitDecision(True, "trail" if trailing_active else "stop")
    if time_stop_due(entry_time, now, days=time_stop_days):
        return ExitDecision(True, "time")
    if earnings_exit_due(now.astimezone(_ET).date(), earnings_date, unrealized_pnl):
        return ExitDecision(True, "earnings")
    return ExitDecision(False)
