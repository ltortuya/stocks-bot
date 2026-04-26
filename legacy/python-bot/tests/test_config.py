"""Tests for bot.config."""
from __future__ import annotations

import pytest

from bot import config as cfg


def test_load_returns_typed_settings(env_paper) -> None:
    settings = cfg.load()
    assert settings.alpaca_api_key == "test_key"
    assert settings.alpaca_api_secret == "test_secret"
    assert settings.alpaca_base_url == "https://paper-api.alpaca.markets"
    assert settings.telegram_chat_id == "12345"


def test_load_uses_strategy_defaults(env_paper) -> None:
    settings = cfg.load()
    assert settings.poll_interval_sec == 30
    assert settings.poll_interval_fast_sec == 15
    assert settings.fast_poll_end_min == 90
    assert settings.min_price == 10.0
    assert settings.min_dollar_vol == 25_000_000
    assert settings.pct_change_min == 0.04
    assert settings.rvol_min == 1.8
    assert settings.near_breakout_pct == 0.02
    assert settings.lookback_breakout == 20
    assert settings.per_trade_risk_pct == 0.015
    assert settings.max_open_positions == 3
    assert settings.max_daily_new_entries == 5
    assert settings.daily_drawdown_halt_pct == -0.03
    assert settings.profit_target_pct == 0.10
    assert settings.hard_stop_pct == 0.05
    assert settings.trail_activation_pct == 0.06
    assert settings.trail_distance_pct == 0.05
    assert settings.time_stop_days == 5
    assert settings.gap_skip_pct == 0.08
    assert settings.no_entry_first_min == 0
    assert settings.no_new_entry_after == "14:30"
    assert settings.trader_end_time == "15:55"
    assert settings.exchange_tz == "America/New_York"


def test_load_raises_when_required_env_missing(monkeypatch, tmp_path) -> None:
    for key in ["ALPACA_API_KEY", "ALPACA_API_SECRET", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]:
        monkeypatch.delenv(key, raising=False)
    nonexistent = tmp_path / "doesnt_exist.env"
    with pytest.raises(cfg.MissingConfigError) as excinfo:
        cfg.load(env_file=nonexistent)
    assert "ALPACA_API_KEY" in str(excinfo.value)
