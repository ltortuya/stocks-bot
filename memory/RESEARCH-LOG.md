# Research Log

Daily pre-market research entries are appended below. Newest at the bottom.

Format each entry:

```
## YYYY-MM-DD — Pre-market Research

### Account
- Equity: $X
- Cash: $X
- Buying power: $X
- Daytrade count: N

### Market Context
- WTI / Brent:
- S&P 500 futures:
- VIX:
- Today's catalysts:
- Earnings before open:
- Economic calendar:
- Sector momentum:

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

### Decision
TRADE or HOLD (default HOLD if no edge)
```

## 2026-04-26 — Pre-market Research

(Sunday — markets closed. Research/setup for Monday 2026-04-27 open. OpenAI key not set in local env; used native WebSearch fallback.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $199,624.72
- Daytrade count: 0
- Open orders: 1 stale TSLA market buy, 1 share, accepted, expires 2026-04-27 20:00 UTC (likely test order from 2026-04-25; flag — see risks)

### Market Context
- WTI / Brent: WTI ~$94/bbl, Brent ~$105/bbl (4/24 close); WTI up ~14% on the week on Iran/Mideast risk premium
- S&P 500 futures: no fresh quote (Sunday); week closed with risk-on tone on AI/peace-talk hopes
- VIX: 18.71 (4/24 close, -3.1%)
- Today's catalysts: none (Sunday)
- Earnings before open Mon 4/27: VZ, NUE, DPZ, ACMR, ARLP, BFST, DMRC, DEA, BMRC, PSA, AVB, CINF, VTR
- Economic calendar this week: ADP + Consumer Confidence Tue, FOMC Tue/Wed (rate decision Wed), durable orders + housing starts Wed, US GDP + PCE Thu, ISM Mfg Fri
- Mega-cap tech earnings Wed/Thu: MSFT, GOOG, META (Wed) and AAPL, AMZN (Thu) — index-mover concentration
- Sector momentum YTD: Energy +22–24% (leader), Materials +14%, Industrials +13%, Real Estate +11%; Tech / Comm Svcs / Cons Disc lagging YTD

### Trade Ideas
1. XLE (Energy ETF) — sector leader YTD on data-center power thesis; wait for FOMC + Iran headline clarity. Notional entry $X (next session quote), stop -10% trail, target +20%. Defer entry to Tue post-FOMC if oil holds and Iran tape doesn't break.
2. NUE — reports pre-mkt Mon; materials sector strong YTD. SKIP — earnings binary, no edge.
3. Mega-cap tech (MSFT/GOOG/META/AAPL/AMZN) — earnings Wed/Thu. SKIP pre-earnings; reassess Thu PM for post-print follow-through entries that meet 2:1 R:R with 10% trail.

### Risk Factors
- FOMC rate decision Wed → whole-week vol risk, avoid heavy deploys before
- Mega-cap tech earnings cluster Wed/Thu can swing index +/- several percent
- US-Iran peace talks: oil +14% week was geopolitical premium; collapse or breakthrough both binary
- US GDP + PCE Thu adds macro tape risk
- Stale TSLA buy order (1 share) from 2026-04-25 will likely fill at Monday open. Trivial $ but unauthorized exposure — recommend cancel at next session before open. Not cancelling now without explicit OK.

### Decision
HOLD. Sunday + FOMC + mega-cap-tech-earnings week = no edge for opening positions today. Patience > activity. Reassess at Monday pre-market and after FOMC Wed.

## 2026-04-27 — Pre-market Research

(Monday open. OPENAI_API_KEY not set in local env; used native WebSearch fallback.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Open orders: none (yesterday's stale TSLA 1-share buy is no longer on the book — expired or cleared overnight)

### Market Context
- WTI / Brent: WTI ~$95–96/bbl (intraday high $96.7), Brent ~$106 (intraday high ~$108) — Strait of Hormuz effectively closed, US-Iran talks stalled
- S&P 500 futures: ~flat premarket (S&P +0.03%, Dow -0.16%); Iran reportedly offered new Strait-reopen proposal, capping downside; 10Y 4.32%, 2Y 3.79%
- VIX: 18.71 (normal 15–20 band, well off March 31.05 peak)
- Today's catalysts: Iran / Strait of Hormuz tape, BMO earnings (VZ/NUE/DPZ/PSA), NVDA strength (+4.5% on next-gen chip demand reports)
- Earnings before open: VZ, NUE, DPZ, PSA (plus VTR, CINF, ARLP, DEA mid-day)
- Economic calendar: Tue Consumer Confidence + BoJ; Tue/Wed FOMC (Powell's last meeting, decision Wed); Thu PCE (no GDP this week per updated calendar)
- Sector momentum YTD: Energy +22% (leader), Real Estate / Consumer Staples at ATH, Industrials strong; Tech -3.8% YTD, Health Care + Cons Disc lagging; equal-weight S&P +7.1% vs cap-weight +0.7% — broad rotation out of mega-cap growth, small-cap value +10.9%

### Trade Ideas
1. XLE (Energy ETF) — sector leader YTD, but oil spike is geopolitical-binary (Iran headline can swing ±10% intraday). DEFER until post-FOMC Wed; don't enter into stalled-talks tape.
2. NUE / DPZ / VZ / PSA — earnings BMO. SKIP — earnings binary, no edge, violates 2:1 R:R discipline pre-print.
3. Mega-cap tech (MSFT/GOOG/META Wed, AAPL/AMZN Thu) — SKIP pre-print. Reassess Thu PM / Fri AM for post-print follow-through entries that meet 2:1 R:R with 10% trail and pass the buy-side gate.
4. Small-cap value / equal-weight rotation (RSP, IWN) — strong YTD breadth signal, but FOMC + tech-earnings cluster could swing the tape; defer to Thu post-PCE.

### Risk Factors
- FOMC Wed (Powell's last meeting) — rate-path / dot-plot risk, whole-week vol
- Mega-cap tech earnings cluster Wed (MSFT/GOOG/META) and Thu (AAPL/AMZN) can move S&P ±2–3% on prints
- US-Iran: Strait of Hormuz closed; any breakthrough or breakdown is a binary +/- on energy and broad indices
- PCE Thu — inflation print into FOMC fallout
- Premarket NVDA strength (+4.5%) on chip-demand headlines is single-stock noise, not a sector-momentum signal yet

### Decision
HOLD. Three binary catalysts (FOMC Wed, mega-cap earnings Wed/Thu, Iran tape) stacked into a 4-day window with VIX still in normal range = no risk-adjusted edge for opening today. Patience > activity. Reassess Wed afternoon post-FOMC, then Thu/Fri post-earnings for follow-through entries.

## 2026-04-28 — Pre-market Research

(Tuesday open. FOMC meeting Day 1 today, decision tomorrow Wed.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Positions: none
- Open orders: none

### Market Context
- WTI / Brent: WTI ~$98–101/bbl, Brent ~$105–110/bbl — Strait of Hormuz tension keeps oil elevated; geopolitical premium intact
- S&P 500 futures: ESM26 ~7,221.75 (-0.06%); cash S&P closed record 7,173.91 Mon (+0.12%); Dow -0.14%, Nasdaq -0.30% premarket; 10Y context unchanged
- VIX: 18.71 last print (Apr 24); no fresh tick yet — still in normal 15–20 band
- Today's catalysts: FOMC Day 1 (decision tomorrow), ADP private payrolls 12:15pm ET, NVDA/TSLA tape strength, Iran/Strait of Hormuz headlines
- Earnings before open: KO, UPS, SPGI, NVS, KMB, BRO, ALLE, INCY, AMT, CNC, GLW, SPOT — no mega-cap tech BMO today
- Economic calendar this week: ADP today; FOMC decision Wed (consensus hold 3.50–3.75%); MSFT/GOOG/META earnings Wed; AAPL/AMZN earnings Thu; PCE Thu
- Sector momentum YTD: Tech leading (AI/semis driving ~29.7% S&P YTD), Energy +22%, Materials +15%; Cons Disc -2%, Real Estate / Utilities / Industrials lagging recently — concentration risk in mega-cap tech remains elevated

### Trade Ideas
1. XLE (Energy ETF) — sector +22% YTD leader, but oil is geopolitical-binary on Iran/Hormuz tape. DEFER until post-FOMC clarity Wed PM.
2. XLK / SMH (Tech / Semis) — sector leader on AI demand, but mega-cap earnings cluster Wed/Thu is binary. SKIP pre-print; reassess Thu PM / Fri AM for post-earnings follow-through that meets 2:1 R:R with 10% trail.
3. KO / UPS / SPGI / NVS / KMB BMO earnings — SKIP, earnings binary, no edge, violates entry checklist.
4. Equal-weight / small-cap value (RSP, IWN) — broad-rotation thesis intact, but FOMC + tech earnings will dictate breadth this week. Defer to post-PCE Thu.

### Risk Factors
- FOMC Day 1 today, decision tomorrow Wed (Powell's last meeting per prior context) — rate-path / dot-plot binary
- ADP 12:15pm ET — pre-FOMC volatility kicker
- Mega-cap tech earnings cluster Wed (MSFT/GOOG/META) and Thu (AAPL/AMZN) — index-mover concentration
- PCE Thu — inflation tape into FOMC fallout, with oil-pushed energy CPI hot
- Iran / Strait of Hormuz: any breakthrough or breakdown is binary on energy + broad indices
- VIX 18.71 in normal band masks event-stacked tape this week

### Decision
HOLD. Same three binary catalysts as yesterday, now one day closer (FOMC Wed, mega-cap earnings Wed/Thu, Iran tape) plus ADP today as pre-FOMC vol kicker. No risk-adjusted edge for opening into this. Patience > activity. Reassess Wed PM post-FOMC, then Thu/Fri post-earnings for follow-through entries that pass the buy-side gate.

## 2026-04-29 — Pre-market Research

(Wednesday — FOMC decision day. MSFT/GOOG/META earnings AMC tonight.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Positions: none
- Open orders: none

### Market Context
- WTI / Brent: WTI ~$98–102/bbl (Apr 28 close $102.22, +2.95%); Brent spread ~$11 → ~$109–113. Oil remains elevated on Iran/Strait of Hormuz tape.
- S&P 500 futures: ESM26 modestly green premarket (~+0.10%); ES around 6,657–7,180 range references mixed across sources, but tape is flat-to-slightly-green into FOMC. Cash S&P closed near record 7,173 area Mon.
- VIX: 18.36 (Apr 28 close), down from 18.71 — still in normal 15–20 band, masking the binary event stack today.
- Today's catalysts: FOMC statement 2:00pm ET; Powell presser 2:30pm ET (no SEP/dot-plot this meeting); MSFT/GOOG/META earnings AMC; Iran/Hormuz tape ongoing.
- Earnings before open: none of size for our setup. Major prints AMC tonight: MSFT (FY26 Q3), GOOGL, META.
- Economic calendar: FOMC today (consensus hold 3.50–3.75%); Thu Apr 30 = Q1 GDP advance + March PCE + Q1 ECI cluster; AAPL/AMZN earnings AMC Thu.
- Sector momentum: YTD — Energy +22% leader, Materials +15%, Cons Staples +12%, Tech +small, Cons Disc -2%, Industrials +7%. April MTD reversal — Tech +2% MTD only outperformer; Energy -14% MTD as oil round-tripped. Rotation tape unsettled.

### Trade Ideas
1. XLK / SMH (Tech / Semis) — sector reasserting in April, but MSFT/GOOG/META print AMC tonight. SKIP pre-print. Reassess Thu AM for post-print follow-through that passes 2:1 R:R + 10% trail.
2. XLE (Energy ETF) — YTD leader but down 14% MTD on oil round-trip + Iran-tape binary. SKIP into FOMC; reassess Thu AM with PCE in hand.
3. RSP / IWN (equal-weight / small-cap value) — broad-rotation thesis still alive but FOMC + earnings cluster + PCE Thu = 3 binary events in 36 hours. DEFER to Fri AM after the dust clears.
4. KO / UPS / SPGI / NVS / KMB and others printing today — SKIP, earnings binary, no edge.

### Risk Factors
- FOMC decision 2pm + Powell 2:30pm ET — language/tone binary; hawkish on sticky core PCE 2.7% vs dovish on Q4 GDP 0.5% softness. No SEP this meeting → every word weighted.
- MSFT/GOOG/META AMC — Azure capex/AI revenue read-through dictates Thu AM gap on whole tech sector.
- Thu PCE + Q1 GDP advance + ECI cluster — inflation into FOMC fallout; hot PCE delays cuts.
- Iran / Strait of Hormuz: still closed; oil round-tripped from $102 to $96 area on talk-restart hopes — binary either way.
- VIX 18.36 in normal band understates 36-hour event stack.

### Decision
HOLD. Worst possible 24h to open new positions: FOMC at 2pm + 3 mega-cap earnings AMC + PCE/GDP cluster Thu morning. Three binary catalysts back-to-back-to-back. Patience > activity. Reassess Thu AM after FOMC + tech-print reaction; ideal entry window is Fri AM post-AAPL/AMZN + post-PCE for follow-through trades that pass the full buy-side gate.

## 2026-04-30 — Pre-market Research

(Thursday. FOMC done — held 3.50–3.75% with easing bias + 4 dissents. MSFT + GOOGL beat AMC; META -6.4% AH on capex. PCE/GDP/ECI/Jobless Claims at 8:30 ET. AAPL/AMZN print AMC tonight.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Positions: none
- Open orders: none

### Market Context
- WTI / Brent: WTI ~$108–111/bbl spot (Apr 29 session +3.4% to +6.95%, depending on source); Brent ~$11 spread → ~$119–122. Iran/Strait of Hormuz tape still hot.
- S&P 500 futures: ESM26 ~6,657 premarket, +0.10% (~+6.5pts). Cautious tone into 8:30 PCE/GDP cluster + after-hours tech-earnings split (MSFT/GOOGL up, META down).
- VIX: 17.83 (Apr 28 close); intraday Apr 29 high 18.81. Normal 15–20 band but underprices 8:30 binary print.
- Today's catalysts: 8:30 ET — Q1 GDP advance + March PCE + Q1 ECI + weekly Jobless Claims (4-print cluster, single moment of binary risk); 11:00 ET Trimmed Mean PCE; AAPL/AMZN earnings AMC tonight; FOMC follow-through tape from yesterday's hold.
- Earnings before open: Hippo Holdings (HIPO) only of note — not a trade candidate. Mega-cap reaction tape from MSFT/GOOGL/META AMC dominates the open.
- Economic calendar: 8:30 ET print cluster is the day. Tomorrow Fri 5/1 ISM Mfg + post-AAPL/AMZN reaction. Next FOMC June.
- Sector momentum YTD: Energy +38.3% (oil-driven leader), Materials +9.7%, Utilities +8.3%, Cons Staples +7.7%, Real Estate +2.8%. S&P breadth/level mixed across sources (one shows -4.3% YTD, others show 7,173 record). Tech +17% MTD April per one source — clear April rotation back into AI infra/semis. META capex miss may blunt that today; MSFT/GOOGL cloud beats support it.

### Trade Ideas
1. **GOOGL** — Cloud +28% YoY, double-beat ($181B rev vs $177B est, $2.78 EPS vs $1.64), +4% AH. Strongest single-name catalyst of the week. SKIP at-the-open execution into 8:30 PCE binary; author as a midday conditional (see below).
2. **XLK / SMH (AI infra / semis)** — MSFT + GOOGL cloud beats are bullish AI-capex demand. Counter: META -6.4% AH on its own capex is a capex-bears signal. Net: positive but mixed. SKIP at-the-open; conditional on post-PCE follow-through.
3. **XLE (Energy)** — +38% YTD leader, oil +7% session. Pure geopolitical-binary on Iran/Hormuz tape. Already extended; chasing into open is poor R:R. SKIP today.
4. **AAPL / AMZN** — print AMC. SKIP pre-print, no edge.

### Conditional Entries (midday-eligible) — up to 3
1. **GOOGL** — allocation $19,500 (≤19.5% of equity), stop 10% trail, target +25% from entry, R:R 2.5:1
   Condition: Post-PCE (after 9:00 ET digestion), GOOGL must (a) hold above its AH gap-up level of roughly $200+ (whatever opens as the AH-equivalent print), (b) show a 30-min consolidation above the open print without filling more than 50% of the gap, (c) S&P 500 not red >0.75% on PCE, and (d) VIX not spiking above 22. If all four, midday buys at market with 10% trail GTC attached.
   Catalyst: Cloud +28% YoY, double-beat earnings ($181B rev vs $177B), +4% AH — best single-name AI-infra read-through of the week.
2. **SMH (semis ETF)** — allocation $15,000 (15% of equity), stop 10% trail, target +20% from entry, R:R 2:1
   Condition: SMH must open green and hold a green print through the 8:30 PCE digestion (give it until ~10:00 ET). Require (a) MSFT not red >1% on its post-print follow-through, (b) META not dragging the cap-weight tech complex (XLK net green), (c) PCE core not above 0.4% m/m (hot-print kill switch). All three → midday entry with 10% trail GTC.
   Catalyst: MSFT + GOOGL cloud/AI capex beats reassert AI-infra demand thesis; tech +17% MTD April rotation already in motion.

### Risk Factors
- 8:30 ET binary: hot PCE re-prices Fed cuts further out, pressures tech valuations and breaks the rotation thesis. Hot Q1 GDP + hot PCE = stagflation tape.
- AAPL/AMZN AMC tonight is back-to-back binary; entries today carry overnight earnings exposure on the broad tape regardless of ticker chosen.
- META's -6.4% AH on capex concerns can spread: if cap-ex bears price-discover the rest of mega-cap tech today, GOOGL/MSFT bounce can fade.
- Oil at $108–111 with Iran/Hormuz still binary keeps Energy hot but un-chaseable. A breakthrough headline = -10% gap on XLE; a breakdown = +5% gap.
- Powell's last presser yesterday plus 4 dissents (most since 1992) leaves Fed reaction-function read murky — easing bias intact but 3 dissenters wanted hawkish wording.
- VIX 17.83 in normal band continues to underprice this stack of binaries.

### Decision
HOLD at the open. Two conditional midday entries authored (GOOGL, SMH) — both require post-PCE confirmation. Patience > activity. If 8:30 print is benign and tech holds, midday will execute up to 2 entries (~$34.5k notional, ~34.5% deployed). If PCE is hot or META capex contagion spreads, midday holds zero. Either way, no at-the-open buys today.

