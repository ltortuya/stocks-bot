"""Shared pytest fixtures."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def tmp_state_db(tmp_path: Path) -> Path:
    """Returns a path to a fresh empty SQLite file for each test."""
    return tmp_path / "state.sqlite"


@pytest.fixture
def env_paper(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stubs Alpaca + Telegram env vars for tests that read config."""
    monkeypatch.setenv("ALPACA_API_KEY", "test_key")
    monkeypatch.setenv("ALPACA_API_SECRET", "test_secret")
    monkeypatch.setenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
    monkeypatch.setenv("TELEGRAM_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
