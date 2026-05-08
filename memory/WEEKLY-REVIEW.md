# Weekly Review

Friday reviews appended here. Newest at the bottom.

Template for each entry:

```
## Week ending YYYY-MM-DD

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $X |
| Ending portfolio | $X |
| Week return | ±$X (±X%) |
| S&P 500 week | ±X% |
| Bot vs S&P | ±X% |
| Trades | N (W:X / L:Y / open:Z) |
| Win rate | X% |
| Best trade | SYM +X% |
| Worst trade | SYM -X% |
| Profit factor | X.XX |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |

### What Worked
- ...

### What Didn't Work
- ...

### Key Lessons
- ...

### Adjustments for Next Week
- ...

### Overall Grade: X
```

## Week ending 2026-05-01

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $100,000.00 |
| Ending portfolio | $100,000.00 |
| Week return | $0.00 (0.00%) |
| S&P 500 week | +0.61% (Apr 24 close 7,165.08 → May 1 close 7,209.01) |
| Bot vs S&P | -0.61% |
| Trades | 0 (W:0 / L:0 / open:0) |
| Win rate | N/A (no closed trades) |
| Best trade | N/A |
| Worst trade | N/A |
| Profit factor | N/A |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |
| — | — | — | — | None — zero trades placed all week |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |
| — | — | — | — | None — 100% cash ($100,000) |

### What Worked
- Discipline held: every "skip" decision (FOMC week, mega-cap earnings cluster, Iran/Hormuz binary, capex-bear contagion) was correctly read as binary risk with no edge.
- Conditional-entry framework (Thu GOOGL + SMH) correctly killed both setups intraday on real gate failures (GOOGL gap fill / SMH MSFT-led tech red), so no forced entry during a hostile tape.
- No options, no leverage, no rule violations — risk controls are intact at the framework level.
- Pre-market research workflow ran every day and produced documented catalysts and sector reads, so the diagnosis below is data-backed rather than a guess.

### What Didn't Work
- 0/5 trading days deployed any capital — 100% cash all week vs. the 75–85% deployment target. The strategy cannot beat SPY from cash.
- The buy-side gate is correctly screening out trash, but the research output is producing zero candidates that pass — every idea in week 1 was filtered as "binary, defer." That is a research-output problem, not a gate problem.
- Catalyst calendar was unusually heavy (FOMC + 5 mega-cap prints + PCE + ISM + Iran tape stacked into 4 days), but the entry framework had no notion of a "wait-for-clean-tape" baseline trade — there was no "default deployment" idea (e.g., broad-index core position) that could deploy on day 1 while binary catalysts cleared.
- Conditional-entry gates were tightly coupled to single-name follow-through (MSFT not -1%, XLK net green, gap-hold rules) — a single mega-cap drag (MSFT -2.6%) killed the whole tech complex's eligibility. Gates may be over-fit to perfection.
- Lost the full week's compounding window vs. S&P (-0.61% relative) for an event-stack the strategy could have partially neutralized with a small core position.

### Key Lessons
- Patience > activity is not the same as 100% cash. The strategy needs a "minimum-deployment floor" concept so that capital is at least partially exposed to broad market beta when no high-conviction single-name setup is available, especially across event-stacked weeks.
- Single-week catalyst clustering is not rare — earnings-week + FOMC + PCE will recur every quarter. The framework needs a default playbook for "binary-stacked weeks" rather than re-defaulting to HOLD daily.
- Conditional-entry gates need to distinguish between "thesis broken" (e.g., AWS print bad) and "tape noise" (e.g., one-day MSFT drawdown on capex narrative). Current gates treat both as kill conditions.
- Documentation of every skip is valuable — the research log made this diagnosis possible. Keep that bar.

### Adjustments for Next Week
- Add a **minimum-deployment floor** rule (proposed): if 0 single-name setups pass the gate by EOD Wednesday of any week, default to a 20–30% broad-index position (SPY or RSP) with a 10% trail, until a higher-conviction single-name displaces it. Don't ship to TRADING-STRATEGY.md yet — pilot one week first, codify only if it produces a better risk-adjusted outcome than the cash week just observed.
- Pre-market workflow change: explicitly require **at least one "any-tape OK" idea** per session (a setup whose thesis does not depend on a same-day binary print clearing). If none can be authored, log why — that's a research-output failure to address, not a market problem.
- Conditional-entry gates: separate "thesis-break" gates (binding) from "tape-noise" gates (advisory). Re-test SMH-style setups with this distinction next week.
- Re-evaluate the catalyst-calendar overlay: avoid scheduling core deployment days in FOMC + mega-cap earnings weeks; pre-load broad-index exposure the prior Friday instead.
- Hold the line on no-options, max-20%-per-position, 10% trail, -7% manual cut — those rules were not the constraint this week.

### Overall Grade: D
- D, not F: process discipline was perfect, no rule was violated, no capital was lost, and every skip was defensible in isolation.
- Not C or higher: the *strategy-level outcome* was a full-week miss vs. SPY (-0.61%), 0/6 trade budget used, and zero compounding for week 1 of a finite challenge window. Discipline without deployment is not a winning posture; the framework needs the minimum-deployment-floor adjustment to avoid repeating this in week 2.

## Week ending 2026-05-08

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $100,000.00 |
| Ending portfolio | $100,493.05 |
| Week return | +$493.05 (+0.49%) |
| S&P 500 week | +1.78% (May 1 close 7,248.15 → May 8 close 7,376.25) |
| Bot vs S&P | -1.29% |
| Trades | 3 (W:0 / L:0 / open:3) |
| Win rate | N/A (no closed trades) |
| Best trade | XLB +1.05% (unrealized) |
| Worst trade | XLI +0.59% (unrealized, smallest gain — no losses) |
| Profit factor | N/A (no closed trades) |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |
| — | — | — | — | None — all 3 trades placed Mon are still open |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |
| XLP | $83.36 (239 sh) | $84.17 | +$194.28 (+0.97%) | $76.32 (10% trail GTC, hwm $84.80) |
| XLB | $51.06 (390 sh) | $51.60 | +$209.65 (+1.05%) | $47.493 (10% trail GTC, hwm $52.77) |
| XLI | $172.47 (87 sh) | $173.49 | +$89.12 (+0.59%) | $159.948 (10% trail GTC, hwm $177.72) |

### What Worked
- Capital actually deployed for the first time — Monday's 3 sector-ETF basket (XLP/XLB/XLI) executed cleanly at the open per pre-market plan, breaking the week-1 zero-deployment paralysis.
- Sector-rotation thesis is working at the basket level — all 3 legs sit in the YTD-leadership cluster (Cons Staples, Materials, Industrials) and finished the week green at +0.59% to +1.05% unrealized despite a binary-heavy macro week.
- Trail-stop discipline: 10% GTCs attached on every fill, hwms ratcheted upward through the week (XLP $84.35→$84.80, XLB $51.20→$52.77, XLI $173.21→$177.72), zero stop hits, zero -7% manual-cut candidates, no rule violations.
- Risk-management gates were correctly triggered on Tue and Thu — XLE conditional was killed midday Tue on Hormuz cease-fire (real thesis-break, not noise) and re-killed all week as oil leaked from $107 → $97; the framework correctly defended capital from chasing a deteriorating thesis.
- Saved feedback memory ("env-var loop check unreliable, smoke-test the wrapper") was applied successfully on Wed and Thu — rescued both pre-market sessions from false-abort that killed Mon May 6's first run.

### What Didn't Work
- Deployment stuck at ~55% all week vs. 75–85% target — the second consecutive week missing the deployment band. Pattern: 3 trades on day 1, then 4 idle days. Same shape as week 1 (zero days deployed), shifted right by one Monday.
- Bot underperformed SPY by -1.29% on the week (+0.49% vs. +1.78%), entirely because of the deployment gap — the basket itself returned ~+0.9% on its $54.8k notional, but the $45k cash drag held the portfolio back from matching SPY's 1.78%.
- The XLE 4th-leg slot was never filled — it was the deferred-Mon, midday-conditional Tue, then explicitly off-list Wed/Thu/Fri after the cease-fire. No replacement candidate was authored. The "candidate 4th leg" was a single-name dependency, not a pipeline.
- Pre-market env-var false-alarm killed two pre-market runs (Wed May 6 first run and Fri May 8) before the smoke-test workaround was applied; on Friday it was the NFP-day pre-market that was disrupted, the highest-stakes session of the week.
- The minimum-deployment-floor concept proposed in week 1's review was NOT codified into TRADING-STRATEGY.md, NOT piloted, and NOT referenced in the daily decision logic — week 2 played out without it as if week 1's lesson didn't exist.

### Key Lessons
- "3 trades on Monday, then HOLD all week" is week 2's failure mode. Week 1 was "HOLD all week"; week 2 is "front-load Monday, then HOLD." Both fail the deployment mandate. The fix is a *pipeline* of 4–6 candidate setups for the week, not a single Monday batch + a single 4th-leg-pending name.
- Conditional-entry framework is doing its job (correctly killed XLE midday Tue on Hormuz cease-fire — that was a real binary, not tape noise) but it produces zero new candidates after the kill. Need a "next-best replacement" mechanism, not a single-name watch-only.
- Trail-stop ratcheting is working as designed at the +1% range; the strategy hasn't yet been stress-tested at the +15% / +20% tighten thresholds — useful framing for next week if any leg breaks out.
- The env-var false-alarm pattern is now confirmed across 4+ sessions. Auto-memory caught it; the next step is fixing it at the routine level, not relying on Claude to remember the workaround every session.
- "Bot vs SPY" is the scoreboard. Week 1 -0.61%, week 2 -1.29% = phase running -1.90% behind SPY through 10 trading days. The cash drag is the entire gap; XLP/XLB/XLI is not the problem.

### Adjustments for Next Week
- **Codify the minimum-deployment floor** (week 1 proposal, now overdue): if 0 single-name setups pass the gate by EOD Wednesday, default the residual cash to a 20–25% broad-index leg (SPY or RSP) with 10% trail. Pilot week 3, codify into TRADING-STRATEGY.md if the math works (compounding floor > opportunity cost of cash). Not shipped to TRADING-STRATEGY.md this Friday — strategy doc kept stable until pilot data exists.
- **Author a 4–6-deep pipeline in Monday pre-market**, not a 3-Monday-batch + 1-conditional-watch. Each idea must be independently triggerable across the week so a single thesis-break (like XLE post-cease-fire) doesn't kill the week's deployment plan.
- **Fix the env-var routine bug at the harness, not in Claude's session memory.** Two NFP-day pre-market disruptions in two weeks is unacceptable. Operator action item: surface the missing-env condition in the cloud routine config so the loop check stops false-positiving.
- **Reassess XLU as 5th-leg candidate Monday** — has been watch-only for a week; either decide it's in or remove it from the watchlist to free attention. Don't park ideas indefinitely.
- **Hold the line on existing rules** — no-options, max-20%-per-position, 10% trail, -7% manual cut, max 6 weekly / 3 daily trades — these are not the constraint. Deployment composition is.

### Overall Grade: C-
- Up a notch from week 1 (D): capital was finally deployed, the basket finished green, no stop hits, no rule violations, the conditional-entry framework correctly defended against a real thesis break (Hormuz cease-fire), and the env-var workaround rescued two of three affected sessions.
- Not C or higher: the bot still trailed SPY by -1.29% — half of an aggressive challenge target gone in 2 weeks — and the deployment-stagnation problem flagged in week 1's review went unaddressed at the strategy-doc level. The minimum-deployment-floor proposal sat dormant for a full week while it would have closed most of the SPY gap. Process improved; outcome did not.

