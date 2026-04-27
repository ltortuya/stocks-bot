# Sheets Export + Perplexity Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Export a snapshot + history report to a Google Sheet on every trading-day routine run (3x/day), and replace OpenAI with Perplexity as the research source.

**Architecture:** Two new wrapper scripts — `scripts/sheets.sh` (Python under the hood, service-account auth) and `scripts/perplexity.sh` (curl-based, parity with the old `openai.sh`). One subcommand added to `alpaca.sh`. Routine prompts updated. Failure isolation: a Sheets/Perplexity failure never blocks the routine's memory commit/push.

**Tech Stack:** bash, curl, Python 3, `google-auth`, `google-api-python-client`, pytest.

**Reference spec:** [docs/superpowers/specs/2026-04-27-sheets-export-perplexity-design.md](../specs/2026-04-27-sheets-export-perplexity-design.md)

---

## File Map

**Create:**
- `scripts/sheets.sh` — bash entrypoint for Sheets writes
- `scripts/sheets_report.py` — Python implementation (Sheets API + Alpaca subprocess + RESEARCH-LOG parsing)
- `scripts/perplexity.sh` — bash wrapper around Perplexity API
- `tests/__init__.py` — empty package marker
- `tests/test_sheets_report.py` — unit tests for parsers and row builders
- `requirements.txt` — at repo root, lists `google-auth` and `google-api-python-client` for the cloud routine to install
- `data/dashboard-sheet-id.txt` — sheet ID file (created during one-time setup, not in this code change)

**Modify:**
- `scripts/alpaca.sh` — add `snapshot <SYM>` subcommand
- `routines/pre-market.md` — replace `openai.sh` references with `perplexity.sh`
- `routines/market-open.md` — same + add `sheets.sh report` step
- `routines/midday.md` — same + add `sheets.sh report` step
- `routines/daily-summary.md` — same + add `sheets.sh report` step
- `routines/weekly-review.md` — same (no sheets call)
- `routines/README.md` — env vars + setup checklist
- `CLAUDE.md` — API Wrappers section
- `env.template` — replace OpenAI block with Perplexity, add Google service account

**Move (git mv):**
- `scripts/openai.sh` → `legacy/scripts/openai.sh`

---

## Task 1: Add `snapshot` subcommand to alpaca.sh

**Files:**
- Modify: `scripts/alpaca.sh`

**Parallelizable with:** Tasks 2, 3, 9.

- [ ] **Step 1: Add the new subcommand**

Edit `scripts/alpaca.sh`. Insert this new case branch immediately after the `quote` branch (after line 42), before `orders`:

```bash
  snapshot)
    sym="${1:?usage: snapshot SYM}"
    curl -fsS --ssl-no-revoke -H "$H_KEY" -H "$H_SEC" "$DATA/stocks/$sym/snapshot"
    ;;
```

Also update the usage line (currently line 67) to include `snapshot`:

```bash
    echo "Usage: bash scripts/alpaca.sh <account|positions|position|quote|snapshot|orders|order|cancel|cancel-all|close|close-all> [args]" >&2
```

- [ ] **Step 2: Smoke test**

Run: `bash scripts/alpaca.sh snapshot SPY | head -c 200`

Expected: a JSON blob starting with `{"latestTrade":` or similar — confirms the endpoint is reachable and the wrapper outputs JSON. If `ALPACA_API_KEY` isn't set locally, expected: `ALPACA_API_KEY not set in environment`.

- [ ] **Step 3: Commit**

```bash
git add scripts/alpaca.sh
git commit -m "feat(alpaca): add snapshot subcommand for daily-change data"
```

---

## Task 2: Create scripts/perplexity.sh

**Files:**
- Create: `scripts/perplexity.sh`

**Parallelizable with:** Tasks 1, 3, 9.

- [ ] **Step 1: Write the wrapper**

Create `scripts/perplexity.sh`:

```bash
#!/usr/bin/env bash
# Perplexity API wrapper for research routines.
# Usage: bash scripts/perplexity.sh "<prompt text>"
# Exit codes:
#   0  - success, response on stdout
#   2  - API error (after one retry)
#   3  - PERPLEXITY_API_KEY not set (caller falls back to native WebSearch)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "PERPLEXITY_API_KEY not set in environment" >&2
  exit 3
fi

PROMPT="${1:?usage: bash scripts/perplexity.sh \"<prompt text>\"}"
MODEL="${PERPLEXITY_MODEL:-sonar-pro}"

# Build JSON body via python to handle prompt escaping safely.
BODY=$(python3 -c '
import json, sys
prompt, model = sys.argv[1], sys.argv[2]
print(json.dumps({
  "model": model,
  "messages": [{"role": "user", "content": prompt}],
}))
' "$PROMPT" "$MODEL")

call_api() {
  curl -fsS --ssl-no-revoke --max-time 60 \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -X POST -d "$BODY" \
    "https://api.perplexity.ai/chat/completions"
}

RESPONSE="$(call_api 2>/dev/null)" || {
  sleep 3
  RESPONSE="$(call_api 2>/dev/null)" || {
    echo "Perplexity API failed after one retry" >&2
    exit 2
  }
}

# Extract content + citations.
python3 -c '
import json, sys
data = json.loads(sys.stdin.read())
content = data["choices"][0]["message"]["content"]
print(content)
citations = data.get("citations") or []
if citations:
    print()
    print("Sources:")
    for i, url in enumerate(citations, 1):
        print(f"  [{i}] {url}")
' <<< "$RESPONSE"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/perplexity.sh
```

- [ ] **Step 3: Smoke test missing-key path**

Run: `PERPLEXITY_API_KEY= bash scripts/perplexity.sh "hello"; echo "exit: $?"`

Expected: prints `PERPLEXITY_API_KEY not set in environment` and `exit: 3`.

- [ ] **Step 4: Commit**

```bash
git add scripts/perplexity.sh
git commit -m "feat(scripts): perplexity.sh research wrapper (replaces openai.sh)"
```

---

## Task 3: Archive openai.sh

**Files:**
- Move: `scripts/openai.sh` → `legacy/scripts/openai.sh`

**Parallelizable with:** Tasks 1, 2, 9.

- [ ] **Step 1: Move the file**

```bash
mkdir -p legacy/scripts
git mv scripts/openai.sh legacy/scripts/openai.sh
```

- [ ] **Step 2: Verify move**

Run: `ls scripts/openai.sh 2>&1; ls legacy/scripts/openai.sh`

Expected: `ls: cannot access 'scripts/openai.sh'` and a successful listing for the legacy path.

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: archive scripts/openai.sh to legacy/scripts/"
```

---

## Task 4: Replace openai.sh references in routine prompts

**Files:**
- Modify: `routines/pre-market.md`
- Modify: `routines/market-open.md`
- Modify: `routines/midday.md`
- Modify: `routines/daily-summary.md`
- Modify: `routines/weekly-review.md`

**Note:** This task only does the find/replace. Adding the `sheets.sh report` call to the three trading-day routines happens in Task 8.

- [ ] **Step 1: Find every reference**

Run: `grep -rn "openai\.sh\|OPENAI_API_KEY\|OPENAI_MODEL\|OpenAI" routines/`

Read the output and note each match.

- [ ] **Step 2: Replace per-file**

In each routine file, perform these edits:
- `scripts/openai.sh` → `scripts/perplexity.sh`
- `OPENAI_API_KEY` → `PERPLEXITY_API_KEY`
- `OPENAI_MODEL` → `PERPLEXITY_MODEL`
- "OpenAI" / "OpenAI's web-search-capable models" / similar prose → "Perplexity" / "Perplexity's web-grounded sonar-pro model"
- Any reference to `gpt-4o-search-preview` → `sonar-pro`

The semantic intent (research source with web grounding + citation fallback to native WebSearch) is unchanged. Match the surrounding wording style in each file.

- [ ] **Step 3: Verify no stragglers**

Run: `grep -rn "openai\|OPENAI\|gpt-4o" routines/`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add routines/
git commit -m "feat(routines): switch research source from OpenAI to Perplexity"
```

---

## Task 5: Python helpers — RESEARCH-LOG parsing and row builders

**Files:**
- Create: `tests/__init__.py` (empty file)
- Create: `tests/test_sheets_report.py`
- Create: `scripts/sheets_report.py` (helpers section only — Sheets API integration in Task 6)
- Create: `requirements.txt` at repo root

**Parallelizable with:** Tasks 1–4 if a separate worker takes them.

- [ ] **Step 1: Create requirements.txt**

```bash
cat > requirements.txt <<'EOF'
google-auth==2.34.0
google-api-python-client==2.149.0
EOF
```

- [ ] **Step 2: Create test file scaffold**

Create `tests/__init__.py` (empty).

Create `tests/test_sheets_report.py`:

```python
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
```

- [ ] **Step 3: Verify tests fail (no implementation yet)**

Run: `pytest tests/test_sheets_report.py -v`

Expected: ImportError or `ModuleNotFoundError: No module named 'sheets_report'`.

- [ ] **Step 4: Implement helpers in scripts/sheets_report.py**

Create `scripts/sheets_report.py`:

```python
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
    headline = "—"
    for line in latest.splitlines():
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
    """One row appended to the History tab."""
    return [
        timestamp_pt,
        routine,
        _fmt_money(equity),
        _fmt_money(cash),
        _fmt_money(day_pnl),
        _fmt_pct(day_pnl_pct),
        str(n_positions),
        decision,
        headline,
    ]
```

- [ ] **Step 5: Verify tests pass**

Run: `pytest tests/test_sheets_report.py -v`

Expected: all tests pass (12 tests). If a test fails, fix the helper code (not the test) until it passes.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt tests/__init__.py tests/test_sheets_report.py scripts/sheets_report.py
git commit -m "feat(sheets): pure helpers for snapshot grid + history row + research log parsing"
```

---

## Task 6: Sheets API integration in sheets_report.py

**Files:**
- Modify: `scripts/sheets_report.py` (add Sheets API integration + main entrypoint)

**Depends on:** Task 5.

- [ ] **Step 1: Append the Sheets integration + main()**

Append to `scripts/sheets_report.py`:

```python
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
```

- [ ] **Step 2: Verify existing tests still pass**

Run: `pytest tests/test_sheets_report.py -v`

Expected: all 12 tests still pass. The new code is below the existing helpers and doesn't touch them.

- [ ] **Step 3: Verify the script imports cleanly**

Run: `python3 -c "import sys; sys.path.insert(0, 'scripts'); import sheets_report; print('ok')"`

Expected: `ok`. (If google libs aren't installed locally yet, the import still succeeds because they're imported lazily inside `_build_sheets_service`.)

- [ ] **Step 4: Commit**

```bash
git add scripts/sheets_report.py
git commit -m "feat(sheets): Sheets API integration + main entrypoint"
```

---

## Task 7: Create scripts/sheets.sh wrapper

**Files:**
- Create: `scripts/sheets.sh`

**Depends on:** Task 6.

- [ ] **Step 1: Write the wrapper**

Create `scripts/sheets.sh`:

```bash
#!/usr/bin/env bash
# Google Sheets dashboard writer.
# Usage: ROUTINE_NAME=<name> bash scripts/sheets.sh report
# Exit codes:
#   0 - success
#   2 - bad usage
#   4 - GOOGLE_SERVICE_ACCOUNT_JSON missing/unparseable
#   5 - data/dashboard-sheet-id.txt missing
#   6 - Sheets API failed after retry

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

cmd="${1:-}"
case "$cmd" in
  report)
    PY="$(command -v python3 || command -v python)"
    if [[ -z "$PY" ]]; then
      echo "python3/python not found on PATH" >&2
      exit 2
    fi

    set +e
    "$PY" "$ROOT/scripts/sheets_report.py"
    rc=$?
    set -e

    if [[ "$rc" -ne 0 ]]; then
      # Best-effort Telegram alert. Never let the alert itself fail the script.
      if [[ -x "$ROOT/scripts/telegram.sh" ]]; then
        bash "$ROOT/scripts/telegram.sh" \
          "🟥 sheets.sh failed (exit $rc) for routine ${ROUTINE_NAME:-unknown}" \
          >/dev/null 2>&1 || true
      fi
      exit "$rc"
    fi
    ;;
  *)
    echo "Usage: ROUTINE_NAME=<name> bash scripts/sheets.sh report" >&2
    exit 2
    ;;
esac
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/sheets.sh
```

- [ ] **Step 3: Smoke test bad-usage path**

Run: `bash scripts/sheets.sh; echo "exit: $?"`

Expected: `Usage: ROUTINE_NAME=<name> bash scripts/sheets.sh report` and `exit: 2`.

- [ ] **Step 4: Smoke test missing-creds path**

Run: `GOOGLE_SERVICE_ACCOUNT_JSON= bash scripts/sheets.sh report; echo "exit: $?"`

Expected: stderr message `GOOGLE_SERVICE_ACCOUNT_JSON not set in environment` and `exit: 4`.

- [ ] **Step 5: Commit**

```bash
git add scripts/sheets.sh
git commit -m "feat(scripts): sheets.sh report wrapper with Telegram alert on failure"
```

---

## Task 8: Wire trading-day routines to call sheets.sh

**Files:**
- Modify: `routines/market-open.md`
- Modify: `routines/midday.md`
- Modify: `routines/daily-summary.md`

**Depends on:** Task 7.

- [ ] **Step 1: Inspect each routine's tail**

Read each file's last 20 lines. Identify the existing "commit + push memory" step at the end.

- [ ] **Step 2: Insert the sheets call before commit + push**

In each of the three trading-day routine markdown files, immediately before the commit/push step, insert this block (matching the file's existing prose voice):

````markdown
### Push the dashboard report

Run this before committing memory. A failure here logs to Telegram and exits non-zero, but it does NOT block the commit/push that follows.

```bash
ROUTINE_NAME=market-open bash scripts/sheets.sh report
```

(Replace `market-open` with `midday` or `daily-summary` as appropriate per routine.)
````

For each file, use the matching routine name in the `ROUTINE_NAME=` value. The other two routines (`pre-market.md`, `weekly-review.md`) get NO sheets call.

- [ ] **Step 3: Verify**

Run: `grep -l "sheets.sh report" routines/`

Expected: exactly three files listed — `market-open.md`, `midday.md`, `daily-summary.md`.

- [ ] **Step 4: Commit**

```bash
git add routines/market-open.md routines/midday.md routines/daily-summary.md
git commit -m "feat(routines): write Sheets dashboard on market-open/midday/daily-summary"
```

---

## Task 9: Update CLAUDE.md, routines/README.md, env.template

**Files:**
- Modify: `CLAUDE.md`
- Modify: `routines/README.md`
- Modify: `env.template`

**Parallelizable with:** Tasks 1, 2, 3.

- [ ] **Step 1: Update CLAUDE.md API Wrappers section**

Find the API Wrappers section in `CLAUDE.md`. Replace the `openai.sh` bullet with these two lines:

```
- `perplexity.sh` — research via Perplexity's web-grounded sonar-pro model.
  Exits 3 if `PERPLEXITY_API_KEY` unset → fall back to native WebSearch.
- `sheets.sh report` — pushes account snapshot + history row to the Trading
  Bot Dashboard Google Sheet. Called by market-open / midday / daily-summary
  routines. Failure does NOT block memory commit/push.
```

Update the wrapper enumeration line above to: ``Use `bash scripts/alpaca.sh`, `bash scripts/perplexity.sh`, `bash scripts/sheets.sh`, `bash scripts/telegram.sh`.``

- [ ] **Step 2: Update routines/README.md env vars and add setup checklist**

In `routines/README.md`, in the env vars list, replace:

```
- `OPENAI_API_KEY` (required for research)
- `OPENAI_MODEL` (optional; defaults to `gpt-4o-search-preview`)
```

with:

```
- `PERPLEXITY_API_KEY` (required for research)
- `PERPLEXITY_MODEL` (optional; defaults to `sonar-pro`)
- `GOOGLE_SERVICE_ACCOUNT_JSON` (required on market-open / midday / daily-summary
  routines; full service-account JSON, single-line)
```

Then append a new section at the bottom:

```markdown
## One-time Sheets dashboard setup

1. Create a Google Cloud project (free), enable the Google Sheets API.
2. Create a service account, generate a JSON key, download it.
3. Create the sheet titled "Trading Bot Dashboard" with two tabs: `Snapshot` and `History`.
4. Share the sheet with the service account's email (Editor permission).
5. Save the sheet ID to `data/dashboard-sheet-id.txt` and commit it.
6. Set `GOOGLE_SERVICE_ACCOUNT_JSON` (single-line JSON value) on each of the
   three trading-day routines.
7. Optional: build a `Charts` tab manually for equity curve / decision history
   off the History tab. The bot does not touch this tab.

## Local cron parity

If you also run routines on the mini PC via `scripts/run-routine.sh`, set the
same env vars in your local `.env` (see `env.template`). The `.env` file is
gitignored and only used locally.
```

- [ ] **Step 3: Update env.template**

Replace the OpenAI block with:

```
# Perplexity (research — uses web-grounded sonar-pro by default)
PERPLEXITY_API_KEY=your_perplexity_api_key_here
PERPLEXITY_MODEL=sonar-pro
```

Append at the end:

```
# Google Sheets dashboard service account (required for market-open / midday / daily-summary).
# Paste the full JSON key on a single line. Do NOT use a real key in this template.
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"..."}
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md routines/README.md env.template
git commit -m "docs: Perplexity + Sheets dashboard wrappers in CLAUDE.md and env.template"
```

---

## Task 10: End-to-end verification checklist

**Files:** none (verification only)

**Depends on:** all prior tasks.

- [ ] **Step 1: Run unit tests**

Run: `pytest tests/ -v`

Expected: all tests pass.

- [ ] **Step 2: Verify wrappers exit cleanly without keys**

```bash
PERPLEXITY_API_KEY= bash scripts/perplexity.sh "test"; echo "perplexity exit: $?"
GOOGLE_SERVICE_ACCOUNT_JSON= bash scripts/sheets.sh report; echo "sheets exit: $?"
```

Expected: `perplexity exit: 3` and `sheets exit: 4`.

- [ ] **Step 3: Verify routines have correct call sites**

```bash
grep -l "sheets.sh report" routines/  # exactly 3 files
grep -rn "openai\|OPENAI\|gpt-4o" routines/ scripts/  # no matches
ls scripts/openai.sh 2>&1  # cannot access
ls legacy/scripts/openai.sh  # exists
```

- [ ] **Step 4: Document the manual cloud-run verification**

Add a single line at the bottom of this plan file (do not commit if running fresh):

> Manual verification: after the user completes the one-time setup checklist, run "Run now" on each of the three trading-day routines and confirm (a) the Snapshot tab gets written, (b) the History tab gains one new row per run, (c) Telegram does NOT receive a 🟥 alert.

- [ ] **Step 5: Final push**

```bash
git push origin main
```

This pushes all commits made during the plan execution. Subsequent cloud routine runs will pick up the new wrappers + routine prompts.

---

## Self-Review

**Spec coverage:**
- Three trading-day Sheets writes — Task 8.
- `scripts/sheets.sh` with single `report` subcommand — Task 7.
- `scripts/perplexity.sh` replacing `openai.sh` — Tasks 2 + 3 + 4.
- `scripts/alpaca.sh snapshot SYM` — Task 1.
- Snapshot tab structure (account block + positions table) — Task 5 (`build_snapshot_grid`).
- History tab append-only with 9 columns — Task 5 + 6 (`build_history_row` + `_ensure_history_header`).
- Service-account auth — Task 6 (`_build_sheets_service`).
- Failure isolation: Sheets/Perplexity failure never blocks memory push — Tasks 7 + 8 (Telegram alert on non-zero exit, but routine markdown explicitly orders the call BEFORE commit/push and does not abort on its failure).
- Exit code map (3, 4, 5, 6) matches spec — Tasks 2, 6, 7.
- One-time setup checklist — Task 9.
- env.template + CLAUDE.md updates — Task 9.
- Out-of-scope items (charts, Telegram-image, intraday) — not built. ✓

**Placeholder scan:** none found.

**Type consistency:** function names (`parse_research_log`, `compute_day_pnl`, `compute_spy_change`, `build_snapshot_grid`, `build_history_row`, `_build_sheets_service`, `_alpaca`, `_read_sheet_id`, `_ensure_history_header`, `_retry`, `_now_pt_str`, `main`) are consistent across Tasks 5, 6, 7. Exit codes (2, 3, 4, 5, 6) are consistent between `sheets_report.py:main()`, `sheets.sh`, `perplexity.sh`, and the spec.
