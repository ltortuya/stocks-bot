# Conditional Midday Entries Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let pre-market author up to 3 conditional trade ideas per day; midday evaluates each free-form condition and fires the trade if true. Lift weekly trade cap from 3 to 6 with a new max-3-per-day cap.

**Architecture:** Pure prompt + strategy edits — no new wrapper scripts beyond a one-line `bars` subcommand on `alpaca.sh`. The "Conditional Entries" section is markdown in `RESEARCH-LOG.md`; midday reads it the same way it reads the rest of memory and judges each entry with quote / bars / Perplexity at its discretion.

**Tech Stack:** bash, markdown, Alpaca v2 data API.

**Reference spec:** [docs/superpowers/specs/2026-04-29-conditional-midday-entries-design.md](../specs/2026-04-29-conditional-midday-entries-design.md)

---

## File Map

**Create:** none.

**Modify:**
- `scripts/alpaca.sh` — add `bars` subcommand (1-min intraday bars endpoint). Needed by midday's evaluation toolkit.
- `memory/TRADING-STRATEGY.md` — Core Rule #8 (3/week → 6/week + 3/day) and Buy-side Gate (replace one line, add one line).
- `memory/RESEARCH-LOG.md` — extend the format template at the top with the new `Conditional Entries (midday-eligible)` block.
- `routines/pre-market.md` — extend STEP 4 to include conditional-entry authoring guidance, with a required format example. Default is zero entries.
- `routines/midday.md` — insert new STEP 5.5 (evaluate + fire conditionals); renumber subsequent steps.
- `routines/market-open.md` — STEP 3 hard-check: bump weekly cap to 6 and add per-day cap of 3.
- `CLAUDE.md` — Strategy Hard Rules quick reference: cap line.
- `README.md` — strategy summary line: cap.

**Tests:** no new tests. The existing `tests/test_sheets_report.py` covers the only Python in the project; everything edited here is markdown prompts and a one-line bash addition. Validation is a dry read-through (Task 8).

---

## Task 1: Add `bars` subcommand to alpaca.sh

**Files:**
- Modify: `scripts/alpaca.sh:43-46` (insert after `snapshot`), and the usage line `scripts/alpaca.sh:71`.

**Parallelizable with:** Tasks 2, 3, 4, 5 (independent edits).

- [ ] **Step 1: Add the new subcommand**

Edit `scripts/alpaca.sh`. Insert this case branch immediately after the existing `snapshot)` block (currently ending at line 46), before `orders)`:

```bash
  bars)
    sym="${1:?usage: bars SYM [timeframe] [limit]}"
    tf="${2:-5Min}"
    lim="${3:-78}"
    curl -fsS --ssl-no-revoke -H "$H_KEY" -H "$H_SEC" \
      "$DATA/stocks/$sym/bars?timeframe=$tf&limit=$lim&adjustment=raw"
    ;;
```

Defaults: `5Min` bars, 78 rows (full RTH session = 6.5h × 12 = 78 five-min bars). Both can be overridden positionally: `bash scripts/alpaca.sh bars NVDA 1Min 60`.

- [ ] **Step 2: Update the usage line**

Edit `scripts/alpaca.sh:71`. Change:

```bash
    echo "Usage: bash scripts/alpaca.sh <account|positions|position|quote|snapshot|orders|order|cancel|cancel-all|close|close-all> [args]" >&2
```

to:

```bash
    echo "Usage: bash scripts/alpaca.sh <account|positions|position|quote|snapshot|bars|orders|order|cancel|cancel-all|close|close-all> [args]" >&2
```

- [ ] **Step 3: Smoke test**

Run: `bash scripts/alpaca.sh bars SPY 5Min 6 | head -c 300`

Expected: a JSON blob containing `"bars":[{...},{...},...]`. If `ALPACA_API_KEY` isn't set locally, expected error: `ALPACA_API_KEY not set in environment` and exit 1.

Run with bad arg: `bash scripts/alpaca.sh bars`

Expected: `usage: bars SYM [timeframe] [limit]` and exit 1.

- [ ] **Step 4: Commit**

```bash
git add scripts/alpaca.sh
git commit -m "feat(alpaca): add bars subcommand for intraday evaluation"
```

---

## Task 2: Update TRADING-STRATEGY.md (cap + buy-side gate)

**Files:**
- Modify: `memory/TRADING-STRATEGY.md:20` (Core Rule #8) and `memory/TRADING-STRATEGY.md:27` (Buy-side Gate line).

**Parallelizable with:** Tasks 1, 3, 4, 5.

- [ ] **Step 1: Update Core Rule #8**

Edit `memory/TRADING-STRATEGY.md`. Replace:

```
8. Max 3 new trades per week
```

with:

```
8. Max 6 new trades per week, max 3 per day
```

- [ ] **Step 2: Update Buy-side Gate**

In the same file, replace this line:

```
- Total trades placed this week (including this one) ≤ 3
```

with these two lines:

```
- Total trades placed this week (including this one) ≤ 6
- Total trades placed today (including this one) ≤ 3
```

- [ ] **Step 3: Verify**

Run: `grep -n "Max .* trades" memory/TRADING-STRATEGY.md`

Expected: one match showing `8. Max 6 new trades per week, max 3 per day`.

Run: `grep -n "Total trades placed" memory/TRADING-STRATEGY.md`

Expected: two matches — `≤ 6` and `≤ 3` lines.

- [ ] **Step 4: Commit**

```bash
git add memory/TRADING-STRATEGY.md
git commit -m "feat(strategy): lift weekly cap to 6, add per-day cap of 3"
```

---

## Task 3: Update CLAUDE.md and README.md (cap mirror)

**Files:**
- Modify: `CLAUDE.md` (Strategy Hard Rules quick reference)
- Modify: `README.md` (strategy summary line)

**Parallelizable with:** Tasks 1, 2, 4, 5.

- [ ] **Step 1: Update CLAUDE.md**

Edit `CLAUDE.md`. Replace:

```
- Max 3 new trades per week.
```

with:

```
- Max 6 new trades per week, max 3 per day.
```

- [ ] **Step 2: Update README.md**

Edit `README.md`. Replace:

```
3 new trades/week.
```

with:

```
6 new trades/week (max 3/day).
```

(Context: this lives in the "Strategy (summary)" section's prose paragraph. The exact substring "3 new trades/week." is unique in the file.)

- [ ] **Step 3: Verify**

Run: `grep -n "trades per week\|trades/week" CLAUDE.md README.md`

Expected: two matches, both reflecting the new cap.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: mirror new weekly+daily trade cap"
```

---

## Task 4: Update market-open.md STEP 3 (hard-check)

**Files:**
- Modify: `routines/market-open.md:34-40` (STEP 3 bullet list)

**Parallelizable with:** Tasks 1, 2, 3, 5.

- [ ] **Step 1: Update the trades-this-week bullet and add a trades-today bullet**

Edit `routines/market-open.md`. Replace this block:

```
STEP 3 — Hard-check rules BEFORE every order. Skip any trade that fails
and log the reason:
- Total positions after trade <= 6
- Trades this week <= 3
- Position cost <= 20% of equity
- Catalyst documented in today's RESEARCH-LOG
- daytrade_count leaves room (PDT: 3/5 rolling business days as a defensive habit)
```

with:

```
STEP 3 — Hard-check rules BEFORE every order. Skip any trade that fails
and log the reason:
- Total positions after trade <= 6
- Trades this week <= 6
- Trades today <= 3
- Position cost <= 20% of equity
- Catalyst documented in today's RESEARCH-LOG
- daytrade_count leaves room (PDT: 3/5 rolling business days as a defensive habit)
```

- [ ] **Step 2: Verify**

Run: `grep -n "Trades this week\|Trades today" routines/market-open.md`

Expected: two matches — `<= 6` and `<= 3`.

- [ ] **Step 3: Commit**

```bash
git add routines/market-open.md
git commit -m "feat(market-open): enforce 6/week + 3/day trade caps"
```

---

## Task 5: Extend RESEARCH-LOG.md format template

**Files:**
- Modify: `memory/RESEARCH-LOG.md:5-34` (the format-block at the top of the file)

**Parallelizable with:** Tasks 1, 2, 3, 4. **Required before Task 6 and Task 7** (those reference the format).

- [ ] **Step 1: Insert Conditional Entries section into the format block**

Edit `memory/RESEARCH-LOG.md`. Find the format-template code block at the top (lines 7–34). Replace this segment:

```
### Trade Ideas
1. TICKER — catalyst, entry $X, stop $X, target $X, R:R X:1
2. ...

### Risk Factors
- ...
```

with:

```
### Trade Ideas
1. TICKER — catalyst, entry $X, stop $X, target $X, R:R X:1
2. ...

### Conditional Entries (midday-eligible) — up to 3
(Default zero. Only include if the setup needs intraday confirmation
rather than at-the-open execution. Required field format below.)
1. **TICKER** — allocation $X, stop 10% trail, target $Y, R:R Z:1
   Condition: <free-form prose — what midday should look for to confirm>
   Catalyst: <one line — why this is on the watchlist at all>
2. ...

### Risk Factors
- ...
```

Leave existing dated entries (lines 36+) untouched. They predate this format and aren't rewritten retroactively.

- [ ] **Step 2: Verify**

Run: `grep -n "Conditional Entries" memory/RESEARCH-LOG.md`

Expected: one match in the format block (around line 28-30 after the insert).

- [ ] **Step 3: Commit**

```bash
git add memory/RESEARCH-LOG.md
git commit -m "feat(memory): add Conditional Entries section to RESEARCH-LOG format"
```

---

## Task 6: Update pre-market.md (authoring guidance)

**Files:**
- Modify: `routines/pre-market.md:49-54` (STEP 4)

**Depends on:** Task 5 (format template must exist first so this step's instructions point to a real example).

- [ ] **Step 1: Replace STEP 4 with the extended version**

Edit `routines/pre-market.md`. Replace this block:

```
STEP 4 — Append a dated entry to memory/RESEARCH-LOG.md:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, today's releases)
- 2-3 actionable trade ideas WITH catalyst + entry/stop/target
- Risk factors for the day
- Decision: TRADE or HOLD (default HOLD — patience > activity)
```

with:

```
STEP 4 — Append a dated entry to memory/RESEARCH-LOG.md following the
format block at the top of that file. Required sections:
- Account snapshot (equity, cash, buying power, daytrade count)
- Market context (oil, indices, VIX, today's releases)
- 2-3 actionable trade ideas WITH catalyst + entry/stop/target
- Conditional Entries (midday-eligible) — OPTIONAL, up to 3. Default
  ZERO. Only author a conditional if the setup genuinely benefits from
  intraday confirmation rather than at-the-open execution. Each entry
  MUST include: ticker, allocation $ (≤ 20% of equity), stop (default
  "10% trail" — tighter allowed, looser not), target + R:R (≥ 2:1),
  free-form Condition prose (what midday should look for), one-line
  Catalyst. Format example is in the template at the top of
  RESEARCH-LOG.md.
- Risk factors for the day
- Decision: TRADE or HOLD (default HOLD — patience > activity)
```

- [ ] **Step 2: Verify**

Run: `grep -n "Conditional Entries" routines/pre-market.md`

Expected: one match inside STEP 4.

- [ ] **Step 3: Commit**

```bash
git add routines/pre-market.md
git commit -m "feat(pre-market): allow optional conditional-entry authoring"
```

---

## Task 7: Insert STEP 5.5 in midday.md (evaluate + fire)

**Files:**
- Modify: `routines/midday.md` — insert STEP 5.5 between current STEP 5 (thesis check) and current STEP 6 (optional intraday research). Renumber subsequent steps (6→7, 7→8, 8→9, 9→10).

**Depends on:** Task 1 (`bars` subcommand exists), Task 2 (gate text), Task 5 (format the agent reads).

- [ ] **Step 1: Insert STEP 5.5 after the existing STEP 5 thesis-check block**

Edit `routines/midday.md`. After the existing STEP 5 block (which ends with "Document reasoning in TRADE-LOG."), and before the existing STEP 6 (optional intraday research), insert this new step:

```

STEP 5.5 — Evaluate conditional entries authored by pre-market.

Read today's RESEARCH-LOG entry. If it has no "### Conditional Entries
(midday-eligible)" section, OR the section is empty, OR every entry is
already audit-marked from an earlier midday run: log "No conditionals
to evaluate." and proceed to STEP 6.

Otherwise, for each unmarked conditional entry IN AUTHOR ORDER:

(a) Buy-side gate FIRST. Skip with audit line "→ Skipped (HH:MM CT):
    gate — <which check>" if any of these fail. Do NOT fire.
    - Trades this week (incl. this fill) ≤ 6
    - Trades today (incl. this fill) ≤ 3
    - Open positions after fill ≤ 6
    - Allocation ≤ 20% of current equity
    - Allocation ≤ available cash
    - Daytrade count leaves PDT room (3/5 rolling)
    - Same ticker not already in book
    - Same ticker not already evaluated this session

(b) Pick toolkit based on the Condition prose:
    - ALWAYS: bash scripts/alpaca.sh quote TICKER
    - If prose mentions intraday momentum / level / volume / shape:
      bash scripts/alpaca.sh bars TICKER 5Min 78
    - If prose mentions news / headline / sentiment / qualitative:
      bash scripts/perplexity.sh "<focused query about TICKER+catalyst>"
      Fall back to native WebSearch if perplexity exits 3.

(c) Judge true / false / ambiguous. **DEFAULT-SKIP on ambiguous.** Only
    fire on a clear true.

(d) If false / skipped:
    Append audit line under the conditional in RESEARCH-LOG:
        → Skipped (HH:MM CT): <one-line reason>
    Continue to next conditional. No Telegram.

(e) If true → execute:
    1. Recompute shares: floor(allocation_dollars / latest_quote_price).
       If shares < 1 → audit "→ Skipped (HH:MM CT): insufficient cash".
    2. Place market buy, day TIF:
         bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy","type":"market","time_in_force":"day"}'
    3. Wait for fill confirmation.
    4. Place 10% trailing-stop GTC sell (or tighter if pre-market specified):
         bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"trailing_stop","trail_percent":"10","time_in_force":"gtc"}'
       If Alpaca rejects with PDT, fall back to fixed stop 10% below fill:
         bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"stop","stop_price":"X.XX","time_in_force":"gtc"}'
       If also blocked, queue in TRADE-LOG as "PDT-blocked, set tomorrow AM". Do NOT unwind the buy.
    5. Append audit line under the conditional in RESEARCH-LOG:
         → Fired (HH:MM CT) @ $<fill_price>, stop placed.
    6. Append a TRADE-LOG row in the existing format with a `[conditional]` tag:
         | TICKER | shares | entry | stop | thesis | target | R:R | [conditional]

Edge cases — skip with the listed audit reason:
    - quote stale / missing / zero  → "no quote"
    - allocation > available cash, shares < 1  → "insufficient cash"
    - news check needed but Perplexity AND WebSearch both fail  → "news check unavailable"
    - condition prose unparseable / ambiguous fields  → "format unparseable"
    - market closed (should never happen at noon CT weekday)  → "market closed"

```

- [ ] **Step 2: Renumber subsequent steps**

In the same file, the existing steps after the insert are STEP 6, 7, 8, 9 (intraday research, notification, sheets, commit). Renumber them to STEP 6, 7, 8, 9 as before — no renumbering needed because we used STEP 5.5 (decimal) rather than promoting. Verify by reading the file end-to-end and confirming step numbering remains: 1, 2, 3, 4, 5, **5.5**, 6, 7, 8, 9.

- [ ] **Step 3: Update STEP 7 (notification) trigger to include conditional fires**

In the same file, the existing STEP 7 reads:

```
STEP 7 — Notification: ONLY if action was taken.
    bash scripts/telegram.sh "<action summary>"
```

Replace with:

```
STEP 7 — Notification: ONLY if action was taken (cut / tighten / thesis exit / conditional fire). Skips and "no action" are silent.
    bash scripts/telegram.sh "<action summary>"
```

- [ ] **Step 4: Update STEP 9 (commit) to include the new audit edits**

The existing STEP 9 reads:

```
STEP 9 — COMMIT AND PUSH (if any memory files changed):
    git add memory/TRADE-LOG.md memory/RESEARCH-LOG.md
    git commit -m "midday scan $DATE"
    git push origin main
Skip commit if no-op. On push failure: rebase and retry. Never force-push.
```

The `git add memory/RESEARCH-LOG.md` already covers the new audit lines, so no change to the add line. But update the commit-message guidance to reflect the broader scope. Replace:

```
    git commit -m "midday scan $DATE"
```

with:

```
    git commit -m "midday scan $DATE"   # use "midday scan + N conditionals fired $DATE" if any fired
```

- [ ] **Step 5: Verify**

Run: `grep -n "STEP 5.5\|conditional" routines/midday.md`

Expected: at least one `STEP 5.5` match plus several `conditional` mentions inside the new step.

Read `routines/midday.md` end-to-end and confirm step numbering reads 1, 2, 3, 4, 5, 5.5, 6, 7, 8, 9 in order.

- [ ] **Step 6: Commit**

```bash
git add routines/midday.md
git commit -m "feat(midday): evaluate and fire conditional entries (STEP 5.5)"
```

---

## Task 8: End-to-end dry validation

**Files:** none modified. Read-only sanity check.

**Depends on:** Tasks 1–7.

- [ ] **Step 1: Re-read each touched file end-to-end**

Read each file and confirm internal consistency:

```
cat scripts/alpaca.sh
cat memory/TRADING-STRATEGY.md
cat memory/RESEARCH-LOG.md | head -40   # format block + first entry headers
cat routines/pre-market.md
cat routines/midday.md
cat routines/market-open.md
grep -n "trades" CLAUDE.md README.md
```

Confirm:
- The cap is `6 per week` and `3 per day` everywhere it appears (TRADING-STRATEGY.md, CLAUDE.md, README.md, market-open.md). No `3 per week` or `3/week` remnants.
- `routines/midday.md` step numbering is 1, 2, 3, 4, 5, 5.5, 6, 7, 8, 9.
- `routines/pre-market.md` STEP 4 mentions Conditional Entries.
- `memory/RESEARCH-LOG.md` format block contains the Conditional Entries example.
- `scripts/alpaca.sh` lists `bars` in its usage line.

- [ ] **Step 2: Cross-check against the spec**

Open the spec at `docs/superpowers/specs/2026-04-29-conditional-midday-entries-design.md` and walk its sections:

- Decisions table — every choice (D, A, C, 6/wk+3/day, B, A, D) is reflected in the edits above. ✓
- RESEARCH-LOG format addition — Task 5. ✓
- Midday evaluation flow steps (a)–(g) and edge cases — Task 7. ✓
- Strategy rule changes — Tasks 2, 3, 4. ✓
- Edge case table — every row is handled by an audit line in Task 7 step 1 part (e) or the explicit Edge cases section.
- Out-of-scope items: confirm `routines/intraday-check.md` is unchanged (`git status` shows it not modified) and `routines/daily-summary.md`, `routines/weekly-review.md`, all wrapper scripts other than `alpaca.sh` are unchanged.

Run: `git status`

Expected: working tree clean (everything committed via tasks 1–7), and `git log --oneline -10` shows commits from tasks 1, 2, 3, 4, 5, 6, 7 in that order.

- [ ] **Step 3: Local smoke (optional but recommended)**

If `.env` has working creds, run:

```
bash scripts/alpaca.sh bars SPY 5Min 6 | head -c 300
```

Expected: JSON with `"bars":[…]`. Confirms Task 1 didn't break the wrapper.

There is no automated way to dry-run the routines. The first real validation happens at the next midday cron fire on a day when pre-market has authored at least one conditional. Until then, no further action.

- [ ] **Step 4: Push**

```bash
git push origin main
```

If push fails: `git pull --rebase origin main`, then push again. Never force-push.

---

## Self-Review

**Spec coverage:**
- Decisions table (Q1–Q7): Q4 (cap) → Tasks 2, 3, 4. Q5 (sizing authority) + Q6 (format) + Q7 (toolkit) → Tasks 5, 7. Q1, Q2, Q3 (conditionals exist + midday-only + up to 3) → Task 6 + Task 7. ✓
- RESEARCH-LOG format addition → Task 5. ✓
- Midday evaluation flow (gate → toolkit → judge → execute / log) → Task 7 step 1. ✓
- Strategy rule changes (TRADING-STRATEGY, CLAUDE.md, README.md, market-open.md) → Tasks 2, 3, 4. ✓
- Edge cases (10 rows) → Task 7 step 1 part (e) + explicit edge-cases block. Spot-check: no-conditionals → covered (early-return at top of STEP 5.5). Stop fallback → covered (e.4). Quote stale → covered (edge cases). Same ticker in book → covered (gate check). ✓
- Out-of-scope items (intraday-check unchanged, no new wrappers, no schema changes) → Task 8 step 2 verification. ✓
- One spec assumption to flag: spec says "alpaca.sh bars" exists; it didn't. Task 1 adds it. ✓

**Placeholder scan:** No "TBD", "TODO", "etc.", "fill in details", or "similar to". Every step contains the exact text or command. ✓ The angle-bracket placeholders (`<which check>`, `<focused query>`, `<one-line reason>`) are runtime variables the agent fills at fire time, not author placeholders. ✓

**Type consistency:**
- Field names match across spec + tasks: `Condition`, `Catalyst`, `allocation`, `target`, `R:R`, `stop` (with default "10% trail").
- Audit-line format consistent: `→ Fired (HH:MM CT) @ $X, stop placed.` and `→ Skipped (HH:MM CT): <reason>`.
- Cap numbers consistent: 6/week, 3/day, in every file touched. ✓
- Tooling names consistent: `alpaca.sh`, `perplexity.sh`, `telegram.sh` — no typos. ✓
