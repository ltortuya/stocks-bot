"""Unit tests for scripts/sheets_report.py."""

import sys
from pathlib import Path

# Make the scripts/ dir importable.
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import sheets_report as sr  # noqa: E402


# ---------- parse_research_log ----------

def test_parse_research_log_extracts_latest_decision_and_headline():
    log = """## 2026-04-26 — Pre-market Research

(some text)

### Decision
HOLD. Sunday, no edge.

## 2026-04-27 — Pre-market Research

Iran tape, FOMC stacked.

### Decision
HOLD. Three binary catalysts this week.
"""
    decision, headline = sr.parse_research_log(log)
    assert decision == "HOLD"
    assert "FOMC" in headline or "Iran" in headline


def test_parse_research_log_handles_trade_decision():
    log = """## 2026-04-28 — Midday

short note.

### Decision
TRADE. Buy XLE 20%.
"""
    decision, headline = sr.parse_research_log(log)
    assert decision == "TRADE"


def test_parse_research_log_handles_empty_log():
    decision, headline = sr.parse_research_log("")
    assert decision == "—"
    assert headline == "—"


def test_parse_research_log_handles_no_decision_section():
    log = "## 2026-04-27 — Notes\n\nSome content.\n"
    decision, headline = sr.parse_research_log(log)
    assert decision == "—"


# ---------- compute_day_pnl ----------

def test_compute_day_pnl_basic():
    pnl, pnl_pct = sr.compute_day_pnl(equity=101000.0, last_equity=100000.0)
    assert pnl == 1000.0
    assert round(pnl_pct, 2) == 1.0


def test_compute_day_pnl_negative():
    pnl, pnl_pct = sr.compute_day_pnl(equity=99000.0, last_equity=100000.0)
    assert pnl == -1000.0
    assert round(pnl_pct, 2) == -1.0


def test_compute_day_pnl_zero_last_equity():
    pnl, pnl_pct = sr.compute_day_pnl(equity=100.0, last_equity=0.0)
    assert pnl == 100.0
    assert pnl_pct == 0.0


# ---------- compute_spy_change ----------

def test_compute_spy_change_from_snapshot():
    snapshot = {
        "latestTrade": {"p": 510.0},
        "prevDailyBar": {"c": 500.0},
    }
    pct = sr.compute_spy_change(snapshot)
    assert round(pct, 2) == 2.0


def test_compute_spy_change_missing_data():
    assert sr.compute_spy_change({}) == 0.0
    assert sr.compute_spy_change({"latestTrade": {"p": 510.0}}) == 0.0


# ---------- build_snapshot_grid ----------

def test_build_snapshot_grid_empty_positions():
    grid = sr.build_snapshot_grid(
        as_of="2026-04-27 09:30 PT",
        equity=100000.0,
        cash=100000.0,
        day_pnl=0.0,
        day_pnl_pct=0.0,
        n_positions=0,
        spy_pct=0.5,
        decision="HOLD",
        headline="No edge today",
        routine="market-open",
        positions=[],
    )
    flat = "\n".join("|".join(str(c) for c in row) for row in grid)
    assert "Equity" in flat
    assert "100000" in flat
    assert "No open positions" in flat


def test_build_snapshot_grid_with_positions():
    positions = [
        {
            "symbol": "XLE",
            "qty": "100",
            "avg_entry_price": "95.00",
            "current_price": "96.50",
            "unrealized_pl": "150.00",
            "unrealized_plpc": "0.0158",
            "stop_price": "85.50",
            "days_held": 3,
        },
    ]
    grid = sr.build_snapshot_grid(
        as_of="2026-04-27 09:30 PT",
        equity=100150.0,
        cash=90550.0,
        day_pnl=150.0,
        day_pnl_pct=0.15,
        n_positions=1,
        spy_pct=0.5,
        decision="HOLD",
        headline="Energy holding",
        routine="midday",
        positions=positions,
    )
    flat = "\n".join("|".join(str(c) for c in row) for row in grid)
    assert "XLE" in flat
    assert "Positions" in flat


# ---------- build_history_row ----------

def test_build_history_row():
    row = sr.build_history_row(
        timestamp_pt="2026-04-27 09:30 PT",
        routine="market-open",
        equity=100000.0,
        cash=100000.0,
        day_pnl=0.0,
        day_pnl_pct=0.0,
        n_positions=0,
        decision="HOLD",
        headline="No edge today",
    )
    assert row[0] == "2026-04-27 09:30 PT"
    assert row[1] == "market-open"
    assert row[7] == "HOLD"
    assert len(row) == 9
