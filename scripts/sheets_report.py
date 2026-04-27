"""Helpers + entrypoint for writing the Trading Bot Dashboard.

This file has two sections:
  1. Pure helper functions (parsers, formatters, row builders) — covered by tests.
  2. Sheets API integration + main() — added in Task 6.
"""

import re
from typing import List, Tuple, Dict, Any


# ---------- helpers ----------

def parse_research_log(log: str) -> Tuple[str, str]:
    """Return (decision, headline) from the most recent dated section.

    decision: "TRADE" / "HOLD" / "—"
    headline: first non-empty content line of the latest section, truncated to 200 chars.
    """
    if not log:
        return ("—", "—")

    # Split on top-level dated headings: "## 2026-..." starts a section.
    sections = re.split(r"^## \d{4}-\d{2}-\d{2}", log, flags=re.MULTILINE)
    if len(sections) < 2:
        return ("—", "—")
    latest = sections[-1]

    # Decision: first word after "### Decision" (TRADE or HOLD).
    decision_match = re.search(
        r"### Decision\s*\n\s*(TRADE|HOLD)", latest, flags=re.IGNORECASE
    )
    decision = decision_match.group(1).upper() if decision_match else "—"

    # Headline: first content line that isn't a header, blank, or note.
    # latest starts with the remainder of the heading line (e.g. " — Pre-market Research"),
    # so skip the first line entirely before scanning for content.
    lines = latest.splitlines()
    headline = "—"
    for line in lines[1:]:
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("("):
            continue
        headline = s[:200]
        break

    return (decision, headline)


def compute_day_pnl(equity: float, last_equity: float) -> Tuple[float, float]:
    """Return (day_pnl_dollars, day_pnl_pct)."""
    pnl = equity - last_equity
    pct = (pnl / last_equity * 100.0) if last_equity else 0.0
    return (pnl, pct)


def compute_spy_change(snapshot: Dict[str, Any]) -> float:
    """Return SPY day change percent from an Alpaca snapshot blob."""
    try:
        latest = float(snapshot["latestTrade"]["p"])
        prev = float(snapshot["prevDailyBar"]["c"])
    except (KeyError, TypeError, ValueError):
        return 0.0
    if prev == 0:
        return 0.0
    return (latest - prev) / prev * 100.0


def _fmt_money(x: float) -> str:
    return f"${x:.2f}"


def _fmt_pct(x: float) -> str:
    return f"{x:+.2f}%"


def build_snapshot_grid(
    as_of: str,
    equity: float,
    cash: float,
    day_pnl: float,
    day_pnl_pct: float,
    n_positions: int,
    spy_pct: float,
    decision: str,
    headline: str,
    routine: str,
    positions: List[Dict[str, Any]],
) -> List[List[str]]:
    """Build the 2-D grid for the Snapshot tab (A1:H? range)."""
    grid: List[List[str]] = []
    grid.append(["As of", as_of])
    grid.append(["Equity", _fmt_money(equity)])
    grid.append(["Cash", _fmt_money(cash)])
    grid.append(["Day P&L", _fmt_money(day_pnl)])
    grid.append(["Day P&L %", _fmt_pct(day_pnl_pct)])
    grid.append(["Open positions", str(n_positions)])
    grid.append(["S&P 500 today", _fmt_pct(spy_pct)])
    grid.append(["Last decision", decision])
    grid.append(["Last research headline", headline])
    grid.append(["Routine that wrote this", routine])
    grid.append([])  # row 11 blank
    grid.append(["Positions"])  # row 12 header
    grid.append(
        ["Ticker", "Shares", "Entry", "Current", "P&L $", "P&L %", "Stop", "Days held"]
    )
    if not positions:
        grid.append(["No open positions"])
    else:
        for p in positions:
            grid.append([
                p.get("symbol", ""),
                p.get("qty", ""),
                _fmt_money(float(p.get("avg_entry_price", 0))),
                _fmt_money(float(p.get("current_price", 0))),
                _fmt_money(float(p.get("unrealized_pl", 0))),
                _fmt_pct(float(p.get("unrealized_plpc", 0)) * 100.0),
                _fmt_money(float(p.get("stop_price", 0))) if p.get("stop_price") else "—",
                str(p.get("days_held", "")),
            ])
    return grid


def build_history_row(
    timestamp_pt: str,
    routine: str,
    equity: float,
    cash: float,
    day_pnl: float,
    day_pnl_pct: float,
    n_positions: int,
    decision: str,
    headline: str,
) -> List[str]:
    """One row appended to the History tab.

    Column order matches HISTORY_HEADER:
    ["Timestamp (PT)", "Routine", "Equity", "Cash", "Day P&L", "Day P&L %",
     "# Positions", "Decision", "Headline"]
    """
    return [
        timestamp_pt,        # 0 — Timestamp (PT)
        routine,             # 1 — Routine
        _fmt_money(equity),  # 2 — Equity
        _fmt_money(cash),    # 3 — Cash
        _fmt_money(day_pnl), # 4 — Day P&L
        _fmt_pct(day_pnl_pct),  # 5 — Day P&L %
        str(n_positions),    # 6 — # Positions
        decision,            # 7 — Decision
        headline,            # 8 — Headline
    ]
