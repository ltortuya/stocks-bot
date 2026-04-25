"""Centralized typed configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class MissingConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    # secrets
    alpaca_api_key: str
    alpaca_api_secret: str
    alpaca_base_url: str
    telegram_token: str
    telegram_chat_id: str

    # poll cadence
    poll_interval_sec: int = 30
    poll_interval_fast_sec: int = 15
    fast_poll_end_min: int = 90

    # universe
    min_price: float = 10.0
    min_dollar_vol: float = 25_000_000

    # scan
    pct_change_min: float = 0.04
    rvol_min: float = 1.8
    near_breakout_pct: float = 0.02
    lookback_breakout: int = 20

    # risk
    per_trade_risk_pct: float = 0.015
    max_open_positions: int = 3
    max_daily_new_entries: int = 5
    daily_drawdown_halt_pct: float = -0.03

    # exits
    profit_target_pct: float = 0.10
    hard_stop_pct: float = 0.05
    trail_activation_pct: float = 0.06
    trail_distance_pct: float = 0.05
    time_stop_days: int = 5
    gap_skip_pct: float = 0.08

    # session timing (ET)
    no_entry_first_min: int = 5
    no_new_entry_after: str = "14:30"
    trader_end_time: str = "15:55"
    exchange_tz: str = "America/New_York"


_REQUIRED = ("ALPACA_API_KEY", "ALPACA_API_SECRET", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID")


def load(env_file: Path | str | None = None) -> Settings:
    """Load Settings from env (and optionally a .env file)."""
    if env_file is None:
        # default to user-level shared .env if present
        candidate = Path("C:/Users/ltort/.env")
        if candidate.exists():
            load_dotenv(candidate)
    else:
        load_dotenv(env_file)

    missing = [k for k in _REQUIRED if not os.environ.get(k)]
    if missing:
        raise MissingConfigError(f"Missing required env vars: {', '.join(missing)}")

    return Settings(
        alpaca_api_key=os.environ["ALPACA_API_KEY"],
        alpaca_api_secret=os.environ["ALPACA_API_SECRET"],
        alpaca_base_url=os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"),
        telegram_token=os.environ["TELEGRAM_TOKEN"],
        telegram_chat_id=os.environ["TELEGRAM_CHAT_ID"],
    )
