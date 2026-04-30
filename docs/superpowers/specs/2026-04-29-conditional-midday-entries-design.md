# Conditional Midday Entries — Design

Date: 2026-04-29
Status: pending user review

## Goal

Let pre-market author up to 3 conditional trade ideas per day that midday is allowed to fire if the trigger condition is met. Captures intraday opportunities (gap follow-through, news confirmation, level-hold setups) without granting midday open-ended discretion to research and pick new tickers.

## Context

- Project root: `c:/Users/ltort/stocks monitoring/`
- Trading bot is "Claude-as-bot": stateless cloud routines fire on cron, clone repo, read memory, call wrapper scripts, write memory, commit + push.
- Today's routines: pre-market 6:00 AM CT (research only), market-open 8:30 AM CT (only routine that opens new positions), intraday-check 8:00 AM + 11:30 AM CT (risk-only, explicit "no new entries" rule), midday 12:00 PM CT (risk + thesis check today; no entry authority), daily-summary 3:00 PM CT, weekly-review Fri 4:00 PM CT.
- Existing buy-side gate (TRADING-STRATEGY.md): max 6 positions, max 20% per position, max 3 new trades per week, ≤ available cash, PDT room, catalyst documented in today's RESEARCH-LOG.
- Today the bot has no way to act on intraday confirmation — a gap-up that holds until noon must wait for tomorrow's pre-market, by which time the move is often priced in.

## Decisions (from brainstorm)

| # | Question | Choice |
|---|----------|--------|
| 1 | Trigger type | D — free-form prose, agent-judged |
| 2 | Firing routine(s) | A — midday only |
| 3 | Authoring count | C — up to 3 per day |
| 4 | Weekly cap with this feature | 6/week, max 3/day (lifted from 3/week) |
| 5 | Authority at fire time | B — pre-market specs ticker/$/stop/target; midday recomputes shares from fresh quote, no other discretion |
| 6 | Format / location | A — new section in RESEARCH-LOG.md |
| 7 | Evaluation toolkit | D — agent-chosen (quote / bars / Perplexity per condition) |

## Architecture

No new wrapper scripts. No new memory files. No cron changes. The feature is two routine-prompt edits, two strategy-rule edits, and one new RESEARCH-LOG section format.

Files touched:
- `routines/pre-market.md` — instructs the agent how to author the new section, when to author (default zero), and the required field format.
- `routines/midday.md` — new STEP 5.5 inserts the evaluation + execution flow before the existing optional intraday research step. Subsequent steps renumber.
- `memory/TRADING-STRATEGY.md` — Core Rule #8 lifted from 3/week to 6/week + 3/day. Buy-side Gate gains a per-day check.
- `memory/RESEARCH-LOG.md` — format template at the top gets the new section block (Conditional Entries) between Trade Ideas and Risk Factors.
- `CLAUDE.md` — Strategy Hard Rules quick reference updated to match.
- `README.md` — strategy summary line updated to match.
- `routines/market-open.md` STEP 3 — `Trades this week ≤ 3` becomes `≤ 6`, plus new line `Trades today ≤ 3`.

`routines/intraday-check.md` is **not** touched — it stays explicitly risk-only.
`routines/daily-summary.md`, `routines/weekly-review.md`, all wrapper scripts, all sheets dashboard logic — unchanged.

## RESEARCH-LOG format addition

New section between **Trade Ideas** and **Risk Factors** in each daily entry:

```
### Conditional Entries (midday-eligible) — up to 3
1. **TICKER** — allocation $X, stop 10% trail, target $Y, R:R Z:1
   Condition: <free-form prose: what midday should look for to confirm>
   Catalyst: <one line — why this is on the watchlist at all>
2. ...
```

Required fields per entry:
- **Ticker** — single stock; same instrument rules as elsewhere (no options, no crypto, etc.).
- **Allocation in dollars** — must be ≤ 20% of equity at author time.
- **Stop** — defaults to "10% trail GTC". Pre-market may specify tighter (e.g., "8% trail") but never looser.
- **Target + R:R** — minimum 2:1, same as existing entry checklist.
- **Condition** — free-form prose. Agent-judged at fire time.
- **Catalyst** — one line. Satisfies the existing hard-rule "catalyst documented in today's RESEARCH-LOG".

If the section is absent, empty, or all entries already audit-marked: midday is risk-only, identical to today's behavior.

Authoring discipline (text in pre-market.md): "Fewer is better. Default to zero. Only author a conditional if you have a real setup that benefits from intraday confirmation rather than at-the-open execution."

## Midday evaluation flow (new STEP 5.5)

Inserted in `routines/midday.md` after the existing thesis-check step on open positions, before the optional intraday research step. Steps renumber accordingly.

Flow per conditional entry, in author order:

1. **Read the entry** — ticker, allocation $, stop, target, condition prose, catalyst.
2. **Buy-side gate check first**, in this order. If any fails, mark `Skipped: gate — <which check>`:
   - Trades this week (incl. this fill) ≤ 6
   - Trades today (incl. this fill) ≤ 3
   - Open positions after fill ≤ 6
   - Allocation ≤ 20% of current equity
   - Allocation ≤ available cash
   - Daytrade count leaves PDT room
   - Same ticker not already in book (no averaging-in via this path)
   - Same ticker not already evaluated this session (dedupe within the day)
3. **Pick toolkit** based on condition prose:
   - Always: `alpaca.sh quote TICKER` for current price.
   - If condition references intraday momentum, levels, volume, or shape: `alpaca.sh bars TICKER` for intraday bars since the open.
   - If condition references news, headline, sentiment, or anything qualitative: `perplexity.sh "<focused query>"`. Fall back to native WebSearch if perplexity exits 3.
4. **Judge** — true / false / ambiguous.
   - **Default-skip on ambiguous.** Only fire on a clear true. Bias is toward inaction.
5. **If true → execute**:
   - Recompute shares = `floor(allocation / quote)`.
   - If `shares < 1` → skip with `Skipped: insufficient cash`.
   - Place market buy, day TIF, via `alpaca.sh order`.
   - Wait for fill confirmation.
   - Place 10% trailing-stop GTC sell. If Alpaca rejects with PDT, fall back to fixed stop 10% below fill. If also blocked, queue in TRADE-LOG as `PDT-blocked, set tomorrow AM`. Same fallback chain as market-open.
6. **If false / skipped → log only.** Append a one-line audit entry to today's RESEARCH-LOG entry, **inline under the conditional**:

```
1. **NVDA** — allocation $20,000, stop 10% trail, target $X, R:R 2.5:1
   Condition: hold ≥ $850 with bars showing volume continuation after the chip-demand headline
   Catalyst: 4.5% premarket pop on next-gen chip demand reports
   → Skipped (12:04 CT): condition false — bars show no momentum follow-through, declining volume into noon
```

7. **TRADE-LOG entry on fire** uses the existing format plus a `[conditional]` tag in the row so it's distinguishable from market-open trades.

Telegram on fires only. Skips are silent (matches existing midday convention).

## Strategy rule changes

`memory/TRADING-STRATEGY.md`:
- Core Rule #8: `Max 3 new trades per week` → `Max 6 new trades per week, max 3 per day`
- Buy-side Gate: replace `Total trades placed this week (including this one) ≤ 3` with `Total trades placed this week (including this one) ≤ 6` and add new line `Total trades placed today (including this one) ≤ 3`

`CLAUDE.md` (Strategy Hard Rules quick reference):
- `Max 3 new trades per week.` → `Max 6 new trades per week, max 3 per day.`

`README.md`:
- `3 new trades/week` → `6 new trades/week (max 3/day)`

`routines/market-open.md` STEP 3:
- `Trades this week <= 3` → `Trades this week <= 6`
- New bullet: `Trades today <= 3`

## Edge cases

| Case | Handling |
|---|---|
| No conditionals authored | Midday logs `No conditionals to evaluate.` and continues. Risk-only behavior preserved. |
| Buy-side gate fails after condition true | `Skipped: gate — <which check>`. Silent. No Telegram. |
| Trailing stop placement fails post-fill | Fallback chain: trailing → fixed-stop 10% below entry → queue in TRADE-LOG as `PDT-blocked, set tomorrow AM`. Don't unwind the buy. |
| Quote stale, missing, or implausible | `Skipped: no quote`. Don't size off bar-close fallback. |
| Allocation > available cash at fill time | Recompute shares against actual cash; if `< 1`, `Skipped: insufficient cash`. |
| Same ticker already in book | `Skipped: position already open`. Preserves max-20%-per-position rule. |
| Same ticker queued in two conditionals | Fire only the first that evaluates true; later duplicates `Skipped: ticker already evaluated this session`. |
| Ambiguous condition prose | `Skipped: condition ambiguous`. Default-skip is the design bias. |
| Perplexity unavailable / exits 3 | Fall back to native WebSearch (existing pattern). If both fail and the condition needs news, `Skipped: news check unavailable`. |
| Conditional was already audit-marked earlier in the day | Skip — never re-evaluate a fired or skipped conditional in the same session. |
| Market closed when midday fires | Should never happen at 12:00 CT on weekdays, but if it does, skip with `Skipped: market closed`. |

## Out of scope

- `intraday-check` continues to be strictly risk-only. No conditional-fire authority is granted there.
- `market-open` does not look at the Conditional Entries section. Conditionals only fire at midday.
- No new bash wrappers. `alpaca.sh`, `perplexity.sh`, `sheets.sh`, `telegram.sh` already cover everything needed.
- No backtest of the historical 3/week → 6/week change. The cap lift is a forward-looking design choice.
- No automated parser. Midday reads the markdown section as text, the same way it reads the rest of memory today.
- Sheets dashboard — no schema changes. The history row counts trades agnostically; conditional fires show up as ordinary trades with the `[conditional]` tag visible only in TRADE-LOG.

## Risks & open questions

- **Risk: format drift.** Midday parses markdown by reading. If pre-market drifts from the field format, midday could mis-size or skip incorrectly. Mitigation: pre-market.md states the exact required format with an example, and midday.md instructs the agent to skip with `Skipped: format unparseable` rather than guess.
- **Risk: gate budget exhaustion.** With 6/week + 3/day, a single Monday could fully consume the week's budget if pre-market authors three conditionals that all fire. This is the intended behavior under the lifted cap, but worth flagging.
- **Risk: ambiguity gradient.** "Default-skip on ambiguous" depends on the agent's calibration. Bias toward conservatism is the design intent; we accept some missed fires as the cost of safety.
- **Open question (deferred):** Should weekly-review include a section on conditional-fire vs market-open hit-rate? Out of scope for this spec; can be added later if the data warrants it.
