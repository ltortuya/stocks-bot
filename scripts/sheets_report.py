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
    return f"${x:,.2f}"


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


# ---------- Sheets API + entrypoint ----------

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).parent.parent
SHEET_ID_FILE = REPO_ROOT / "data" / "dashboard-sheet-id.txt"
RESEARCH_LOG = REPO_ROOT / "memory" / "RESEARCH-LOG.md"

SNAPSHOT_RANGE_CLEAR = "Snapshot!A1:H100"
SNAPSHOT_RANGE_WRITE = "Snapshot!A1"
HISTORY_RANGE_APPEND = "History!A1"
HISTORY_HEADER = [
    "Timestamp (PT)",
    "Routine",
    "Equity",
    "Cash",
    "Day P&L",
    "Day P&L %",
    "# Positions",
    "Decision",
    "Headline",
]


def _alpaca(*args: str) -> Dict[str, Any]:
    """Call scripts/alpaca.sh with the given args, return parsed JSON."""
    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "alpaca.sh"), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def _build_sheets_service():
    """Build a Sheets API service using the GOOGLE_SERVICE_ACCOUNT_JSON env var."""
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        print("GOOGLE_SERVICE_ACCOUNT_JSON not set in environment", file=sys.stderr)
        sys.exit(4)
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: {e}", file=sys.stderr)
        sys.exit(4)

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _read_sheet_id() -> str:
    if not SHEET_ID_FILE.exists():
        print(f"sheet ID file missing: {SHEET_ID_FILE}", file=sys.stderr)
        sys.exit(5)
    return SHEET_ID_FILE.read_text(encoding="utf-8").strip()


def _ensure_history_header(service, sheet_id: str) -> None:
    """If History tab is empty, write the header row."""
    resp = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range="History!A1:I1"
    ).execute()
    if resp.get("values"):
        return
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="History!A1",
        valueInputOption="RAW",
        body={"values": [HISTORY_HEADER]},
    ).execute()


def _retry(fn):
    """Run fn(); on any exception retry once after 5s, else re-raise."""
    import time
    try:
        return fn()
    except Exception:
        time.sleep(5)
        return fn()


def _now_pt_str() -> str:
    return datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %H:%M %Z")


def main() -> int:
    routine = os.environ.get("ROUTINE_NAME", "unknown")

    # Pull state from Alpaca.
    account = _alpaca("account")
    positions_raw = _alpaca("positions")
    spy_snap = _alpaca("snapshot", "SPY")

    equity = float(account["equity"])
    last_equity = float(account["last_equity"])
    cash = float(account["cash"])
    day_pnl, day_pnl_pct = compute_day_pnl(equity, last_equity)
    spy_pct = compute_spy_change(spy_snap)

    # Normalize positions for snapshot grid.
    positions: List[Dict[str, Any]] = []
    for p in positions_raw:
        positions.append({
            "symbol": p.get("symbol", ""),
            "qty": p.get("qty", ""),
            "avg_entry_price": p.get("avg_entry_price", 0),
            "current_price": p.get("current_price", 0),
            "unrealized_pl": p.get("unrealized_pl", 0),
            "unrealized_plpc": p.get("unrealized_plpc", 0),
            "stop_price": "",  # Alpaca position object doesn't carry stop; left blank.
            "days_held": "",
        })

    # Research log tail.
    log_text = RESEARCH_LOG.read_text(encoding="utf-8") if RESEARCH_LOG.exists() else ""
    decision, headline = parse_research_log(log_text)

    as_of = _now_pt_str()
    grid = build_snapshot_grid(
        as_of=as_of,
        equity=equity,
        cash=cash,
        day_pnl=day_pnl,
        day_pnl_pct=day_pnl_pct,
        n_positions=len(positions),
        spy_pct=spy_pct,
        decision=decision,
        headline=headline,
        routine=routine,
        positions=positions,
    )
    history_row = build_history_row(
        timestamp_pt=as_of,
        routine=routine,
        equity=equity,
        cash=cash,
        day_pnl=day_pnl,
        day_pnl_pct=day_pnl_pct,
        n_positions=len(positions),
        decision=decision,
        headline=headline,
    )

    sheet_id = _read_sheet_id()
    service = _build_sheets_service()

    try:
        _retry(lambda: service.spreadsheets().values().clear(
            spreadsheetId=sheet_id, range=SNAPSHOT_RANGE_CLEAR, body={}
        ).execute())

        _retry(lambda: service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=SNAPSHOT_RANGE_WRITE,
            valueInputOption="RAW",
            body={"values": grid},
        ).execute())

        _ensure_history_header(service, sheet_id)
        _retry(lambda: service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=HISTORY_RANGE_APPEND,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [history_row]},
        ).execute())
    except Exception as e:
        print(f"Sheets API failed: {e}", file=sys.stderr)
        return 6

    print(f"Wrote snapshot ({len(grid)} rows) + history row for routine={routine}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
