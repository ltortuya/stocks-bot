---
description: Pre-market research workflow (local). Reads strategy + tail of logs, pulls account, runs research, writes today's RESEARCH-LOG entry. No commit.
---

You are running the pre-market research workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).

STEP 1 — Read memory for context:
- memory/TRADING-STRATEGY.md
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md

STEP 2 — Pull live account state:
    bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions
    bash scripts/alpaca.sh orders

STEP 3 — Research market context via OpenAI. Run
`bash scripts/openai.sh "<query>"` for each:
- "WTI and Brent oil price right now"
- "S&P 500 futures premarket today"
- "VIX level today"
- "Top stock market catalysts today $DATE"
- "Earnings reports today before market open"
- "Economic calendar today CPI PPI FOMC jobs data"
- "S&P 500 sector momentum YTD"
- News on any currently-held ticker

If openai.sh exits 3 (OPENAI_API_KEY missing), fall back to native WebSearch.

STEP 4 — Append a dated entry to memory/RESEARCH-LOG.md:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, today's releases)
- 2-3 actionable trade ideas WITH catalyst + entry/stop/target
- Risk factors for the day
- Decision: TRADE or HOLD (default HOLD — patience > activity)

STEP 5 — Notification: SILENT unless something is genuinely urgent.
If urgent: `bash scripts/telegram.sh "<one line>"`.

(No commit step in local mode — the user can commit manually if desired.)
