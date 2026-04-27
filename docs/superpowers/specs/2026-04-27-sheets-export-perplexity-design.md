# Sheets Export + Perplexity Research — Design

Date: 2026-04-27
Status: approved (pending plan)

## Goal

1. Give the trader a glanceable visual: a Google Sheet that shows current account state and a running history of every trading-day routine run.
2. Replace OpenAI as the primary research source with Perplexity (sonar-pro), keeping native WebSearch as a fallback.

## Context

- Project root: `c:/Users/ltort/stocks monitoring/`
- Trading bot is "Claude-as-bot": stateless cloud routines fire on cron, clone the repo, read memory, call wrapper scripts, write memory, commit + push, destroy.
- Five routines today: `pre-market.md`, `market-open.md`, `midday.md`, `daily-summary.md`, `weekly-review.md` (cron times in `routines/README.md`, America/Chicago).
- Three of those run during the trading day: `market-open` (8:30 AM CT), `midday` (noon CT), `daily-summary` (3:00 PM CT). These are the three Sheets writes.
- Existing wrappers: `scripts/alpaca.sh`, `scripts/openai.sh`, `scripts/telegram.sh`. Each "exits 3 if its API key is unset" → routine falls back gracefully.

## Architecture

Two new wrapper scripts + three routine prompt updates. No changes to memory file format, alpaca.sh, telegram.sh, or the cron schedule.

- `scripts/sheets.sh report` — new. Service-account auth to Google Sheets API. Writes Snapshot tab (overwrite) and appends one row to History tab.
- `scripts/perplexity.sh "<prompt>"` — new. Replaces `scripts/openai.sh`. Same exit-3 fallback contract.
- `scripts/alpaca.sh snapshot <SYM>` — new subcommand. Wraps the Alpaca `/v2/stocks/{symbol}/snapshot` endpoint so the S&P 500 daily change can be computed. Single-line addition to the existing wrapper.
- `legacy/scripts/openai.sh` — old wrapper archived (matches existing `legacy/python-bot/` pattern). Not deleted, so it's recoverable without git archaeology if Perplexity disappoints.
- `routines/market-open.md`, `routines/midday.md`, `routines/daily-summary.md` — each gets a final step before commit/push: `bash scripts/sheets.sh report`. Pre-market and weekly-review do NOT write the sheet.
- All five routine prompts that mention `openai.sh` get find/replaced to `perplexity.sh`.

Failure isolation: a Sheets API failure sends a Telegram alert and exits non-zero, but the routine still proceeds to commit + push memory. The trading log is more important than the visual.

## Sheet structure

One Google Sheet titled `Trading Bot Dashboard`. Two tabs maintained by the bot, plus an optional manual `Charts` tab the user builds once.

### Snapshot tab (cleared + rewritten each run)

Top block — account state (rows 1–10, two columns: label, value):

| Label | Source |
|---|---|
| As of | timestamp PT, ISO-8601 |
| Equity | Alpaca account |
| Cash | Alpaca account |
| Day P&L | computed: `equity - last_equity` from `alpaca.sh account` |
| Day P&L % | computed: `(equity - last_equity) / last_equity * 100` |
| Open positions | count from `alpaca.sh positions` |
| S&P 500 today | computed from `alpaca.sh snapshot SPY` (% change vs prev close) |
| Last decision | tail of memory/RESEARCH-LOG.md |
| Last research headline | first line of latest research entry |
| Routine that wrote this | `$ROUTINE_NAME` env var |

Row 12: section header `Positions` (single cell, bold).

Rows 13+: positions table with columns:

`Ticker | Shares | Entry | Current | P&L $ | P&L % | Stop | Days held`

When there are no positions, write a single row "No open positions."

Range cleared each run: `Snapshot!A1:H100`.

### History tab (append-only)

Header in row 1 (created on first run if missing):

`Timestamp (PT) | Routine | Equity | Cash | Day P&L | Day P&L % | # Positions | Decision | Headline`

Each run appends one row.

### Charts tab

Built once by hand. Reads from History tab. Bot does not touch.

## Wrapper scripts

### scripts/sheets.sh

Single subcommand: `report`. Usage:

```
ROUTINE_NAME=market-open bash scripts/sheets.sh report
```

Reads:
- `data/dashboard-sheet-id.txt` — sheet ID (committed, not secret).
- `$GOOGLE_SERVICE_ACCOUNT_JSON` — full service account JSON, single-line, in env. No `.env` file in cloud per project convention.
- `$ROUTINE_NAME` — set in each routine prompt before the call.
- Alpaca account + positions (calls `scripts/alpaca.sh` for parity with existing wrapper conventions; no new auth path).
- `memory/RESEARCH-LOG.md` — tails to extract latest decision and headline.

Writes:
- Snapshot tab: clears `A1:H100`, then writes account block + positions table.
- History tab: appends one row.

Failure exit codes:
- 0 — success
- 4 — `GOOGLE_SERVICE_ACCOUNT_JSON` missing or unparseable
- 5 — `data/dashboard-sheet-id.txt` missing
- 6 — Sheets API failed after one retry (5s backoff)

On any non-zero exit, sends a Telegram alert: `🟥 sheets.sh failed (exit N): <short reason>`. Routine continues regardless — memory commit/push runs unconditionally.

Implementation language: Python. Uses `google-auth` and `google-api-python-client`. Justified by the recent commit `b9ba8ac` adding portable python detection — Python is already an expected runtime.

### scripts/perplexity.sh

Usage:

```
bash scripts/perplexity.sh "<prompt text>"
```

Prints plain-text response to stdout. Routines call this exactly where they used to call `openai.sh`.

Reads:
- `$PERPLEXITY_API_KEY` — required. Missing → exit 3.
- `$PERPLEXITY_MODEL` — optional. Defaults to `sonar-pro`.

Behavior:
- POSTs to `https://api.perplexity.ai/chat/completions` with the prompt as a single user message.
- Response format: response text, then a blank line, then `Sources:` followed by numbered citation URLs from the Perplexity response's `citations` array.
- Timeout: 60s. On timeout or 5xx → 1 retry with 3s backoff, then exit 2.

Exit codes match the existing wrapper convention:
- 0 — success
- 2 — real API error (non-retryable or retried-and-failed)
- 3 — `PERPLEXITY_API_KEY` unset → routine falls back to native WebSearch

## Routine prompt changes

For each of `market-open.md`, `midday.md`, `daily-summary.md`:
- Add `ROUTINE_NAME=<name>` export before the call.
- Add `bash scripts/sheets.sh report` as the second-to-last step (immediately before commit + push).

For all five routines:
- Find/replace `scripts/openai.sh` → `scripts/perplexity.sh`.
- Update any inline references to "OpenAI" in research-flow text.

## CLAUDE.md changes

In the project's CLAUDE.md "API Wrappers" section:
- Replace the `openai.sh` bullet with `perplexity.sh` (same exit-3 fallback note).
- Add `sheets.sh` bullet describing `report` subcommand and which routines call it.

In `routines/README.md`:
- Add `GOOGLE_SERVICE_ACCOUNT_JSON` and `PERPLEXITY_API_KEY` to the env vars list.
- Replace `OPENAI_API_KEY` and `OPENAI_MODEL` with `PERPLEXITY_API_KEY` and `PERPLEXITY_MODEL`.
- Add the one-time setup checklist (see below).

## One-time setup checklist

1. Create a Google Cloud project (free), enable Sheets API.
2. Create a service account, generate JSON key, download.
3. Create the Google Sheet titled `Trading Bot Dashboard` with `Snapshot` and `History` tabs.
4. Share the sheet with the service account's email (Editor permission).
5. Save the sheet ID to `data/dashboard-sheet-id.txt`. Commit.
6. Set `GOOGLE_SERVICE_ACCOUNT_JSON` env var on each of the three trading-day routines (single-line JSON value).
7. Sign up for Perplexity API access. Set `PERPLEXITY_API_KEY` env var on all five routines.
8. Run each trading-day routine once via "Run now" to verify the Sheets write.
9. (Optional, manual) Build the `Charts` tab in the sheet — equity curve, decision frequency, daily P&L distribution off the History tab.

## Risks and decisions baked in

- Sheets failure does not block memory persistence. Trading state is more important than the visual.
- Perplexity replacement is one-way but reversible: `legacy/scripts/openai.sh` retains the old wrapper, and the model can be tuned via `PERPLEXITY_MODEL` env var.
- Service account JSON in env var (~2KB) is the standard Google-recommended path for serverless/headless contexts. It avoids the OAuth refresh-token tangling that would couple this bot to the unrelated Breakwater project.
- No backfill from RESEARCH-LOG.md into History tab — the tab starts empty and grows from the next run forward. Markdown remains the source of truth for past decisions.

## Out of scope

- Equity curve as an image attached to a Telegram message.
- Intraday Sheet writes outside the three fixed routine times.
- Multi-account support (paper account only).
- Pre-market and weekly-review writing to the sheet.
- Migrating Perplexity model picks per routine (single default for now; per-routine override via env var if needed later).

## Costs

- Google Cloud / Sheets API: free for this volume (3 writes/day, well under 100 writes/min quota).
- Perplexity Pro API: ~$5/M tokens on `sonar-pro`, or $20/mo flat. User-managed.
- All other infra unchanged.
