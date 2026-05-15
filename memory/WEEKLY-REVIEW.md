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

## Week ending 2026-05-15

### Stats
| Metric | Value |
|--------|-------|
| Starting portfolio | $100,466.31 (Mon AM = Fri 5/8 close) |
| Ending portfolio | $99,921.33 |
| Week return | -$544.98 (-0.54%) |
| S&P 500 week | +0.30% (May 8 close 7,398.51 → May 15 close 7,420.62) |
| Bot vs S&P | -0.84% |
| Trades | 0 (W:0 / L:0 / open:3) |
| Win rate | N/A (no closed trades) |
| Best trade | XLP +1.56% (unrealized, $84.66 vs entry $83.36) |
| Worst trade | XLB -1.61% (unrealized, $50.24 vs entry $51.06) |
| Profit factor | N/A (no closed trades) |

### Closed Trades
| Ticker | Entry | Exit | P&L | Notes |
| — | — | — | — | None — zero trades all week (0/6 cap), 3 May 04 legs still open |

### Open Positions at Week End
| Ticker | Entry | Close | Unrealized | Stop |
| XLP | $83.36 (239 sh) | $84.66 | +$311.39 (+1.56%) | $77.022 (10% trail GTC, hwm $85.58 — 3 ratchets this wk) |
| XLB | $51.06 (390 sh) | $50.24 | -$320.75 (-1.61%) | $47.493 (10% trail GTC, hwm $52.77 — unchanged since 5/7) |
| XLI | $172.47 (87 sh) | $171.40 | -$92.71 (-0.62%) | $159.948 (10% trail GTC, hwm $177.72 — unchanged since 5/7) |

### What Worked
- Conditional-gate framework caught three real thesis-breaks cleanly: XLE-Wed skipped on hot PPI gate-1 fail (+1.4% MoM headline, ~3x cons), XLE-Thu skipped on the Trump-Xi Hormuz framework gate-3 fail (the exact gating event the conditional was authored to filter), and XLK-Fri skipped on hawkish-Warsh gate-1 fail ("no rush to cut" tone). Each skip was the right call in isolation — process A, not noise-rejection.
- XLE was correctly RETIRED Friday after two same-thesis skips, rather than being re-authored a third time on a now-fractured Hormuz case. That's the discipline week 1 and 2 reviews were calling for ("don't park ideas indefinitely" / "thesis-break vs tape-noise distinction").
- Trail-stop discipline intact: XLP ratcheted 3x this week ($84.80 → $85.02 → $85.255 → $85.58) lifting its stop $76.32 → $77.022; zero stop hits; zero -7% manual-cut candidates even on Friday's -2.77% XLB / -1.78% XLI drawdown.
- Env-var smoke-test workaround applied every day — saved feedback memory from May 06 (`alpaca.sh account` smoke-test vs. the `${!v:-}` shell loop) prevented a false-abort on all 5 sessions; zero pre-market disruptions this week.
- Macro reads were correctly framed and acted on in the right direction: CPI hot (3.8% YoY) absorbed constructively (basket +0.16% Day P&L Tue), PPI hot (+1.4% MoM) absorbed flat (basket -0.04% Wed), Trump-Xi framework correctly read as conditional-killer not Hormuz-resolution.

### What Didn't Work
- Third consecutive week with deployment stuck at ~55% vs. the 75-85% target band. Pattern: week 1 = 0% all week, week 2 = 55% from Monday on, week 3 = 55% all week with three conditional candidates authored and skipped. The gate framework is doing its job but producing zero deployment progress — correct skips compound into structural stagnation.
- Single risk-off Friday (-0.87% Day P&L) wiped the entire +0.85% phase peak built across days 11-12 and pushed Phase P&L back into the red (-0.08%) — clean illustration that a 3-leg XLP/XLB/XLI basket has no diversification on a broad-tape down day; effective correlation is ~1 when defensive premium and cyclical beta both compress together (XLP held up at -0.38% but XLB -2.77% and XLI -1.78% drove the loss).
- Zero AI/tech exposure during two consecutive AI-capex blowout AMC tapes (CSCO +19.84% AH Wed, AMAT GM 50% / 25-yr high Thu). The basket had no vehicle to participate; XLK was watch-only Mon-Thu and conditional-only Fri, and that conditional died on hawkish Warsh. The week's largest single-name moves were unowned.
- XLE conditional was carried watch-list-style from week 2 into week 3, fired twice on Wed/Thu, and was retired on Fri — net: a three-week dependency on one thesis that ultimately fractured. The pipeline-not-single-watch lesson from week 2's review was not operationalized; XLK became the next single watch-list dependency on Friday rather than one of several parallel candidates.
- Phase return turned NEGATIVE this week. Bot now -0.08% phase / 15 trading days vs. SPX phase +3.57% (Apr 24 close 7,165.08 → May 15 close 7,420.62) = -3.65% cumulative phase gap. The deployment gap is the entire gap — the basket itself is roughly tracking, but ~$45K of idle cash is dragging.
- XLB YTD source-discrepancy (3.4% / 7.5% / 17.2% across three sources this week) was flagged Thu and Fri pre-market with "Friday weekly review must reconcile" — and is being deferred AGAIN to next Monday. Same parking-the-watch pattern.

### Key Lessons
- Conditional-gate accuracy and deployment-floor adequacy are independent problems. Three weeks of correct skips have proven the gate framework is well-calibrated, but the FRAMEWORK ITSELF cannot solve a deployment gap because it only ever rejects setups; nothing in it generates the floor. The strategy needs a separate, additive mechanism (minimum-deployment-floor or default-broad-index core) to close the cash drag — proposed week 1, deferred week 2, still deferred this week.
- "Single watch-list candidate" is the structural failure mode. Week 1 had no watch list; week 2 had XLE alone; week 3 had XLE → XLK in sequence. In all cases a single thesis-break (Hormuz framework, hawkish Warsh) killed the week's only deployment path. Week 4's pre-market on Monday must author a 3-4-deep pipeline of independent-thesis candidates, not a single carry-over.
- "Right disposition" risk: the conditional framework reliably produces the locally-correct decision (skip on a hot PPI, skip on a Hormuz framework, skip on hawkish Warsh — all defensible), but a strategy that is locally-correct on every gate AND globally-stagnant on deployment is failing the mandate. The mandate is to beat SPY, not to defend cash perfectly. Need to weight the deployment-mandate side of the asymmetry more heavily.
- Friday's risk-off proves the basket lacks low-correlation legs. XLP/XLB/XLI are 3 names from the same "leadership cluster" thesis; when the tape risks-off, they sell together. A 4th leg needs to add a different beta (rate-sensitive XLU, tech XLK, broad-index SPY/RSP, or low-correlation defensive) — not another cyclical/defensive variant.
- Trail-stop ratcheting is working at the +1-2% range (XLP); the strategy has still not been stress-tested at the +15% / +20% tighten thresholds — 15 trading days in and no leg has approached them. The trail-tighten rules are not the active constraint.

### Adjustments for Next Week
- **Author a 3-4-deep pipeline Monday pre-market**, not a single carry-over. Each idea must be independently triggerable so a single thesis-break does not kill the week's deployment plan. Candidates to consider: XLU (rate-sensitive defensive), XLK (re-authored with non-Warsh gating), RSP/SPY (broad-index core, low single-thesis dependency), and one low-correlation single name OR sector that does NOT correlate to the existing XLP/XLB/XLI cluster.
- **Pilot the minimum-deployment-floor mechanism this week** (proposed week 1, deferred 2x). Concrete spec for pilot: if 0 single-name/sector setups pass gates by EOD Wednesday week 4, default to a 20-25% broad-index leg (SPY or RSP) with 10% trail. Don't ship to TRADING-STRATEGY.md yet — pilot one week, codify only if it produces a better risk-adjusted phase outcome than three weeks of conditional-skip stagnation.
- **Reconcile XLB YTD source-discrepancy Monday pre-market** (3.4% / 7.5% / 17.2% across sources). Either confirm leadership-cluster thesis with a clean number, or re-evaluate the position. No more "defer to next Friday".
- **Hard rule for the conditional pipeline**: if a single thesis is skipped twice on consecutive sessions for the same gating reason (XLE: PPI Wed + Hormuz framework Thu), it retires — do not re-author on session 3. Retirement triggers a forced new-thesis search, not another carry-over. Add this as a working rule for week 4 review.
- **Hold the line on existing rules**: no-options, max-20%-per-position, 10% trail, -7% manual cut, max 6 weekly / 3 daily — none of these were the active constraint this week. Deployment composition and pipeline depth are.
- **TRADING-STRATEGY.md unchanged** this Friday — the minimum-deployment-floor rule is still pre-pilot. Codify only if week 4's pilot produces evidence.

### Overall Grade: D
- D, not F: process discipline was again perfect (zero rule violations, zero stop hits, zero -7% cuts, three conditional skips each defensible on real thesis-break), and the XLE retirement Friday is a genuine adjustment from prior weeks' "park indefinitely" pattern. Trail-stop ratcheting on XLP is also working as designed.
- Not C or higher: phase return turned NEGATIVE this week (-0.08% vs. SPX +3.57% phase = -3.65% cumulative gap), the deployment gap is structural across 3 weeks with no codified fix, and Friday's risk-off wiped the entire +0.85% mid-week phase peak in one session — proof that the 3-leg basket offers no diversification. The conditional framework is locally-correct on every call AND globally-failing the mandate; that asymmetry needs the minimum-deployment-floor pilot in week 4 or the strategy will repeat the same outcome a fourth time.

