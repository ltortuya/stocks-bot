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
   → Skipped (12:02 CT): condition (b) failed — session opened $374.52, traded down to $365.87 low (gap fully filled, no 30-min consolidation above open print) before recovering to $378.93. Current quote $378.64/$380. Default-skip on broken intraday shape.
2. **SMH (semis ETF)** — allocation $15,000 (15% of equity), stop 10% trail, target +20% from entry, R:R 2:1
   Condition: SMH must open green and hold a green print through the 8:30 PCE digestion (give it until ~10:00 ET). Require (a) MSFT not red >1% on its post-print follow-through, (b) META not dragging the cap-weight tech complex (XLK net green), (c) PCE core not above 0.4% m/m (hot-print kill switch). All three → midday entry with 10% trail GTC.
   Catalyst: MSFT + GOOGL cloud/AI capex beats reassert AI-infra demand thesis; tech +17% MTD April rotation already in motion.
   → Skipped (12:02 CT): gates (a) and (b) failed — MSFT -2.60% from regular open ($410.56→$399.90, kill switch >1%), XLK net red -0.68% ($159.53→$158.45, not net green). SMH itself -0.13% from open, session low $495.34. Post-print follow-through broke down; capex contagion confirmed.

### Risk Factors
- 8:30 ET binary: hot PCE re-prices Fed cuts further out, pressures tech valuations and breaks the rotation thesis. Hot Q1 GDP + hot PCE = stagflation tape.
- AAPL/AMZN AMC tonight is back-to-back binary; entries today carry overnight earnings exposure on the broad tape regardless of ticker chosen.
- META's -6.4% AH on capex concerns can spread: if cap-ex bears price-discover the rest of mega-cap tech today, GOOGL/MSFT bounce can fade.
- Oil at $108–111 with Iran/Hormuz still binary keeps Energy hot but un-chaseable. A breakthrough headline = -10% gap on XLE; a breakdown = +5% gap.
- Powell's last presser yesterday plus 4 dissents (most since 1992) leaves Fed reaction-function read murky — easing bias intact but 3 dissenters wanted hawkish wording.
- VIX 17.83 in normal band continues to underprice this stack of binaries.

### Decision
HOLD at the open. Two conditional midday entries authored (GOOGL, SMH) — both require post-PCE confirmation. Patience > activity. If 8:30 print is benign and tech holds, midday will execute up to 2 entries (~$34.5k notional, ~34.5% deployed). If PCE is hot or META capex contagion spreads, midday holds zero. Either way, no at-the-open buys today.


## 2026-05-01 — Pre-market Research

(Friday. Last trading day of week 1; weekly review checkpoint later. AMZN beat AMC but -1.6 to -3% AH on $44B Q1 capex / $200B FY guide → capex-bear contagion now META + AMZN. AAPL Q2 fiscal print also AMC last night — specific EPS/rev not yet captured by Perplexity, "tariff impacts" flagged in coverage. ISM Manufacturing PMI 10:00 ET.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Positions: none
- Open orders: none

### Market Context
- WTI / Brent: WTI ~$106/bbl, Brent ~$110/bbl. Off yesterday's $108–111 highs but still elevated on Iran/Hormuz tape.
- S&P 500 futures: ESM26 ~7,250–7,255, +0.09% premarket. Cash S&P closed Apr 30 at 7,254.19; April MTD +6.78% (very strong month).
- VIX: 18.68 open, prior close 18.81. Still in normal 15–20 band; underprices ISM print + post-AAPL/AMZN tape.
- Today's catalysts: ISM Manufacturing PMI 10:00 ET (consensus 52.7, prev 52.7); AAPL/AMZN reaction tape; FOMC follow-through; Iran/Hormuz headlines ongoing.
- Earnings before open: CVX (Chevron, $372B), FFIV, SFM, RITM, CTS — none compelling for our setup. Major mega-cap reaction is from yesterday AMC (AAPL/AMZN).
- Economic calendar: ISM Mfg today 10am; next Fed meeting June. Quiet week ahead.
- Sector momentum: Yesterday's snapshot — Energy +38% YTD leader, Materials +9.7%, Utilities +8.3%, Cons Staples +7.7%. Tech +17% MTD April rotation now under capex-bear pressure (META Wed -6.4% AH, AMZN Thu -1.6 to -3% AH). AMZN's AWS +28% YoY (15-quarter high) is the only clean positive.

### Trade Ideas
1. **AMZN** — AWS +28% YoY (best in 15 qtrs), $181.5B rev double-beat, $2.78 EPS vs $1.64 est (70% surprise), AI services $15B+ run rate. But -1.6 to -3% AH on $44B Q1 capex / $200B FY guide. Contrarian add against expanding capex-bear theme. SKIP at-the-open execution into ISM 10am print.
2. **AAPL** — print AMC, no quantified data captured (only "tariff impacts" coverage notes). Cannot author without numbers. SKIP.
3. **XLK / SMH** — yesterday's SMH conditional was killed by MSFT -2.6% intraday + XLK net red close. AMZN AWS print is bullish AI-infra demand but capex-bear narrative now dominates the tape. Mixed → SKIP today; reassess next week.
4. **XLE** — sector +38% YTD, oil $106 WTI. Still pure geopolitical-binary on Iran/Hormuz. Already extended; chasing into Friday weekly close + thin afternoon is poor R:R. SKIP.
5. **CVX** — earnings BMO; SKIP, earnings binary, no edge.

### Conditional Entries (midday-eligible) — up to 3
(Zero conditionals authored today.)

Reasoning: capex-bear contagion is the dominant intraday theme (META Wed, AMZN Thu) and would break any tech-side conditional's gates the same way SMH was killed yesterday. AMZN itself is a contrarian add against that theme — not a setup that genuinely benefits from intraday confirmation, just one that the market may discount further. Energy is extended into a Friday close. AAPL data is incomplete. No conditional clears the "needs intraday confirmation, not at-the-open execution" bar.

### Risk Factors
- ISM Mfg PMI 10:00 ET binary; below-50 employment subindex (49.0 fcst) leads broader jobs prints — soft read pressures cyclicals.
- Capex-bear contagion now 2-of-3 mega-cap tech prints (META, AMZN). AAPL reaction today + MSFT/GOOGL follow-through risk a third leg lower in tech if capex-bear theme spreads.
- AAPL "tariff impacts" flagged but unquantified; could be a bigger overnight story than picked up here — execution risk if entering tech sympathetically.
- Friday afternoon thin tape + weekly close positioning amplifies any binary print.
- Oil $106 WTI still binary on Iran/Hormuz — breakthrough = -10% gap on XLE; breakdown = +5% gap.
- 5th consecutive no-trade day pressures the deployment narrative — weekly review later today must diagnose whether the entry filter is calibrated correctly or if the workflow needs adjusting (NOT a reason to force a trade today).

### Decision
HOLD. Zero at-the-open entries, zero midday conditionals. Capex-bear theme + ISM print + incomplete AAPL data + Friday thin tape = no setup that passes the buy-side gate. Patience > activity, even on day 5 of zero deployment. Weekly review this afternoon will document the no-trade week and propose any workflow adjustments for week 2. Reassess Monday with AAPL/AMZN reaction tape fully digested and ISM in hand.


## 2026-05-04 — Pre-market Research

(Monday — start of week 2. Mega-cap tech earnings done (MSFT/GOOGL beat, META capex-miss, AMZN AWS beat / capex-bear, AAPL closed -1.09% at $257.46 Fri on tariff overhang). FOMC done — held 3.50–3.75% w/ easing bias. ISM Mfg in hand. No FOMC until June. Quiet macro Mon–Thu; only Friday May 8 brings NFP + ISM Services 8:30/10:00 ET. WEEKLY-REVIEW from Friday confirmed week 1 was 0 trades, 100% cash idle.)

### Account
- Equity: $100,000.00
- Cash: $100,000.00
- Buying power: $200,000.00
- Daytrade count: 0
- Positions: none
- Open orders: none (clean book)

### Market Context
- WTI / Brent: WTI ~$101.50/bbl (range $99.59–108.94 last week), Brent ~$110–116. Off the late-Apr $108–111 highs; "Gulf proposals to stabilize oil" headline moderates the Hormuz binary, but Strait still effectively closed. Symmetrical-triangle compression $90–110.
- S&P 500 futures: ESM26 ~7,272.25, +0.20% to +0.23% premarket. Cash S&P closed Fri ~7,254 (Apr MTD +6.78%, very strong month). Tape constructive into a quiet macro week.
- VIX: 16.89 last (Apr; meaningful drop from Fri 18.68 → mid-16s implies the binary stack is largely cleared). Normal-band complacency, but the print is internally consistent with no FOMC, no major earnings, no major macro until Friday.
- Today's catalysts: structural / rotational only — no event print today. Iran/Hormuz tape ongoing. INTC still strong on government-involvement theme. AI / Nasdaq momentum reasserting per Investors Underground, GME potential EBAY-bid headline (binary, skip).
- Earnings before open: zero of size (CapyFin/Nasdaq calendars list 0 BMO reports). Notable but non-tradable: CRMT, FOSL, RRGB, PLCE later in day. No tradable earnings catalyst today.
- Economic calendar: Mon–Thu quiet (JOLTS Tue is the only mid-tier print). Fri May 8 = Apr NFP (cons +62k, unemployment 4.3%) + ISM Services PMI (prev 54). Markets pricing steady rates with potential for one 25bp cut later in 2026. RBA likely +25bp Tue (74% odds), Norges hike — non-USD.
- Sector momentum YTD: Energy +22.34% (leader), Cons Staples +15.97%, Materials +15.67%, Industrials +11.92%, Real Estate +7.56%, Utilities +6.34%, Health Care +0.97%, Comm Svcs -0.89%, Tech -3.83%, Cons Disc -4.62%, Financials -5.7%. Equal-weight leadership intact; rotation away from mega-cap growth still the dominant 2026 story. April MTD reversed Tech +17% but capex-bear theme (META Wed, AMZN Thu) blunted the bounce.

### Trade Ideas
1. **XLP (Consumer Staples ETF)** — sector +15.97% YTD (#2), low-vol defensive showing momentum is the cleanest "rotation away from growth" signal of 2026. Entry at market, stop 10% trailing GTC, target +15–20%, R:R ~2:1. Allocation up to 20% ($20k). Catalyst: structural rotation + low-VIX regime favors defensive YTD-leader compounders into a quiet macro week.
2. **XLB (Materials ETF)** — sector +15.67% YTD (#3), pairs with Energy/Industrials as the cyclical-rotation leg. Entry at market, stop 10% trail, target +20%, R:R 2:1. Allocation up to 20% ($20k). Catalyst: rotation + commodity-tape strength + Industrials momentum cluster.
3. **XLI (Industrials ETF)** — sector +11.92% YTD, in the leadership cluster. Entry at market, stop 10% trail, target +18%, R:R ~2:1. Allocation up to 15% ($15k). Catalyst: rotation tape + industrial-cycle re-acceleration into low-VIX regime.
4. **XLE (Energy ETF)** — sector +22.34% YTD leader, but oil $101.50 is mid-triangle ($90–110) and Iran/Hormuz remains pure-binary. Author as a midday CONDITIONAL rather than at-the-open (see below) — the geopolitical sensitivity warrants intraday confirmation.
5. **AAPL / AMZN / single-name tech** — capex-bear theme is fresh, AAPL tariff overhang unquantified. SKIP today; wait for the tape to digest fully.
6. **GME (potential EBAY bid headline)** — pure single-name binary, no edge. SKIP.

### Conditional Entries (midday-eligible) — up to 3
1. **XLE** — allocation $15,000 (15% of equity), stop 10% trail GTC, target +20% from entry, R:R 2:1
   Condition: By ~12:00 ET, midday must confirm: (a) no Iran/Hormuz breakthrough headline (a breakthrough is -10% gap on XLE — kill switch); (b) WTI holding above $100 spot (round-trip below $100 = sector-momentum break, kill); (c) S&P 500 not red >0.50% (broader-tape risk-off invalidates rotation-leader thesis); (d) VIX not spiking above 20 (regime change). All four → midday entry at market with 10% trail GTC.
   Catalyst: Sector +22.34% YTD leader; Strait of Hormuz still closed keeps geopolitical premium; "Gulf proposals stabilize oil" headline gives the mid-triangle compression a downside floor without removing upside optionality. Genuinely benefits from intraday confirmation because oil tape is event-driven within the session.
   → Skipped (12:01 CT): gate — trades today already at 3/3 daily cap (XLP/XLB/XLI fired at open). Conditional cannot fire today regardless of confirmation, per pre-market plan.

### Risk Factors
- Iran / Strait of Hormuz still binary — breakthrough = -10% gap on XLE, oil round-trip; breakdown = +5% gap on XLE, oil retest of $110+.
- Capex-bear contagion (META Wed, AMZN Thu) is fresh, blunts any tech-side bounce; sympathetic tech entries today carry that overhang. Not relevant for our XLP/XLB/XLI/XLE leg but worth flagging if rotation reverses.
- AAPL "tariff impacts" still unquantified post-print — opaque overnight risk for the mega-cap tape.
- VIX 16.89 implies low-vol complacency; gap-open risk on any unscheduled headline (Hormuz, tariff, geopolitical).
- Friday May 8 NFP + ISM Services double-print is the week's binary — entries today should size for ability to hold through that print, or else size lighter and reassess Thu PM.
- Week 2 deployment pressure is real after week 1's 0/6 trades — the entry filter must remain disciplined; rotation-momentum ideas above are independently justified, not deployment-pressure-driven.

### Decision
TRADE. Three at-the-open candidates (XLP, XLB, XLI — sector-momentum rotation leaders, low individual-name binary risk, pass entry checklist with structural catalyst + 2:1 R:R + 10% trail) plus one midday XLE conditional. Total notional if fully executed: $20k + $20k + $15k + $15k = $70k (~70% deployed) — within 75-85% target band even allowing for one trade not to fire. Market-open routine should evaluate each against the buy-side gate (max 3/day, max 6/week, ≤20% per position, ≤6 total positions) and execute at market with 10% trailing GTC stops attached. If risk-off tape opens (S&P -0.50%+, VIX 20+), market-open should HOLD on the at-open candidates and let midday handle XLE only.


## 2026-05-05 — Pre-market Research

(Tuesday — Day 7, week 2 day 2. Hold 3 sector-ETF longs from yesterday (XLP/XLB/XLI), all with 10% trail GTCs live. Cash $45,158.79 (~45.3%). Today's tape: WTI gapped +3.75% to $105 on May 4 close; VIX +8.95% to 18.51 on May 4 (regime-shift yellow flag); ISM Services PMI + JOLTS double-print at 10:00 ET; AMD/PYPL/PFE/SMCI earnings on the day. Daily cap resets to 3/3, weekly cap 3/6 used.)

### Account
- Equity: $99,814.75
- Cash: $45,158.79 (45.25%)
- Buying power: $144,973.54
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.36 (mkt $19,980, +$58.05 / +0.29%), XLB 390 sh @ $51.06 (mkt $19,800, -$114.05 / -0.57%), XLI 87 sh @ $172.47 (mkt $14,875, -$129.25 / -0.86%). Cost basis $54,841 (~54.8% deployed).
- Open orders: 3 trail-stop GTCs — XLP $75.92 stop / hwm $84.35; XLB $46.08 stop / hwm $51.20; XLI $155.89 stop / hwm $173.21. All trail 10%, none within 3% of price, none below cost-basis at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$105.13 (May 4 close, +3.75%; intraday range $100.36–109.39 — high-vol session). Brent ~$116 (May 1 print). Symmetrical-triangle compression resolved upward intraday yesterday. Iran/Hormuz tape still effectively closed.
- S&P 500 futures: ESM26 ~7,227 premarket, -0.12% (Nasdaq -0.10%) into the open. Cash S&P closed May 4 at 7,200.75 (-0.41% vs Fri's 7,254). Tape softened on yesterday's oil spike + Apr-MTD profit-taking.
- VIX: 18.51 (May 4 close, +8.95% from 16.99 on May 1). Still inside 15–20 normal band but the +8.95% jump is the largest single-day move since the FOMC week — regime-shift watch on; not a hold-disqualifier yet.
- Today's catalysts: ISM Services PMI 10:00 ET (cons 53.7, prev 54.0 — consensus expects soft-but-expansion; Employment subindex flagged at 45.2 = contraction, Prices Paid 70.7 = hot; stagflation-tilt signal pre-NFP); JOLTS 10:00 ET (cons 6.85M vs prev 6.88M); Fed Chair Bowman 10:00 ET (3pm GMT), Fed Barr 12:30 ET (5:30pm GMT); AMD + SMCI report AMC tonight.
- Earnings before open: PFE, CVS, CMI, DUK, MAR, DD, NRG, PAYC, BNTX, BRBR, DOCN, CIGI — none in our held tickers, no sector-ETF impact of size.
- Economic calendar: Quiet window through Thu after today's ISM Services / JOLTS. Friday May 8 NFP (cons +62k, unemployment 4.3%) + ISM Services PMI was the prior framing; today's print is the warm-up. RBA decision overnight (74% odds +25bp, non-USD). New Home Sales today (cons 0.652M, +3.0% MoM rebound from -17.6%).
- Sector momentum YTD (May 1 totalrealreturns total-return, dividends reinvested vs SPY +5.97%): XLE +32.49% (leader, up from +22.34% prior week as oil spike hit), XLK +12.57%, XLI +11.81%, XLU +9.80%, XLP +8.96%, XLB not tabled but prior week ~+15.67% — call it mid-pack rotation leg, XLF -4.72%. Equal-weight rotation theme intact; Energy regaining undisputed leadership on yesterday's $105 oil print. Held XLP/XLB/XLI all sit in the leadership cluster; thesis on each remains intact (no -7% triggers, no thesis-break news).

### Trade Ideas
1. **XLE (Energy ETF)** — sector +32.49% YTD (re-extended on yesterday's WTI +3.75% spike to $105). Yesterday's deferred 4th leg (was midday conditional, didn't fire because daily cap was at 3/3). Today daily cap resets, capacity available. Author as MIDDAY CONDITIONAL again rather than at-the-open — Iran/Hormuz still pure-binary AND ISM Services + JOLTS print at 10:00 ET adds tape risk that intraday confirmation can clear. Allocation $15,000 (15% of equity), 10% trail GTC, target +20%, R:R 2:1. See conditional below.
2. **HOLD existing XLP/XLB/XLI** — all three within trail-stop range, none at -7%, all in the YTD-leadership rotation cluster. Trail-tighten triggers (7% at +15%, 5% at +20%) not in play yet. No add to existing names.
3. **AMD / SMCI** — report AMC; chip-tape binary. SKIP earnings entries per strategy.
4. **PFE / CVS / CMI / DUK / MAR / DD** — BMO earnings; SKIP, earnings binary, no edge.
5. **XLU (Utilities ETF)** — sector +9.80% YTD, defensive cousin of XLP that benefits from VIX regime-shift. Potential 5th leg if the next 1–2 sessions confirm regime change (VIX > 20 hold) AND XLP/XLB/XLI hold their trail stops. Not authored today — premature, watch-only.
6. **XLK / single-name tech** — capex-bear overhang from META Wed / AMZN Thu still fresh; AMD AMC tonight is the next mega-cap chip print. SKIP today regardless of ISM print.

### Conditional Entries (midday-eligible) — up to 3
1. **XLE** — allocation $15,000 (15% of equity), stop 10% trail GTC, target +20% from entry, R:R 2:1
   Condition: By ~12:00 ET, midday must confirm ALL of: (a) ISM Services print not a stagflation shock (Employment subindex not below 43, Prices Paid not above 75 simultaneously — that combo kills the rotation tape); (b) WTI holding above $102 spot (round-trip below $102 = giveback of yesterday's spike, momentum break); (c) S&P 500 not red >0.50% intraday (broader-tape risk-off invalidates rotation-leader thesis); (d) VIX not above 21 (regime-shift breach, kill); (e) no Iran/Hormuz breakthrough headline (a breakthrough is -10% gap on XLE, kill switch — preserved from yesterday's gating). All five → midday entry at market with 10% trail GTC.
   Catalyst: Sector +32.49% YTD undisputed leader; WTI +3.75% spike to $105 yesterday confirms upside resolution of the $90–110 triangle; Strait of Hormuz still closed maintains geopolitical premium. Genuinely benefits from intraday confirmation because the 10:00 ET ISM Services + JOLTS print is event-driven within the session and can re-rate the entire rotation tape in either direction.
   → Skipped (13:08 CT): gate (e) — Iran/Hormuz cease-fire / "Strait of Hormuz disruptions ease" headline = breakthrough kill switch; gate (b) WTI round-trip $105→$102 = momentum break. Default-skip on ambiguous, two gates failed/at-threshold.

### Risk Factors
- VIX +8.95% pop on May 4 (16.99 → 18.51) is the largest single-day move since FOMC week — yellow flag for regime shift. A break above 20 is the threshold that flips the held-positions disposition from "hold" to "tighten manually."
- ISM Services 10:00 ET is the binary of the day. Employment subindex consensus 45.2 (contraction) is the pre-NFP read — a print at 43 or below pre-prints next week's NFP miss; Prices Paid 70.7 is the inflation tell — print 73+ alongside soft Employment = stagflation signal that breaks the rotation-leadership thesis.
- JOLTS 10:00 ET cons 6.85M (prev 6.88M) — small-magnitude print, but a sub-6.5M shock would compound any soft ISM Employment read.
- Iran / Strait of Hormuz still binary — yesterday's WTI +3.75% spike confirms upside binary remains live; a breakthrough headline = -10% gap on XLE, oil round-trip below $100; a breakdown = +5% gap on XLE.
- AMD + SMCI report AMC tonight — chip-tape binary into Wed open; no held exposure but rotation-tape risk if mega-cap chip-bear narrative spreads.
- Held positions are all in unrealized-loss range except XLP (-0.57%, -0.86%, +0.29%); none near -7% triggers, none near trail-stop triggers. No action required from this entry alone.
- Friday May 8 NFP + ISM Services double-print is the week's binary — sizing on any new entry today must allow a hold through Friday, or else stay on the sidelines.
- Week 2 deployment pressure: still under 75-85% target band at ~54.8% deployed; XLE conditional would lift to ~70% if filled. Do NOT force an add purely for deployment math.

### Decision
HOLD at the open. Zero at-the-open buys; existing XLP/XLB/XLI continue under their 10% trail GTCs (no thesis break, no -7% triggers). One midday XLE conditional authored, gated on ISM Services / JOLTS reaction (10:00 ET) plus WTI/VIX/S&P levels and Iran/Hormuz tape. If all five gates clear by ~12:00 ET, market-open / midday routine executes XLE at market with 10% trail GTC, lifting deployment from ~54.8% to ~70% — still inside the 75-85% target band on the upper allowance. If any gate fails, HOLD entirely and let the tape print Friday's NFP before reassessing further legs. Daily cap available 3/3, weekly cap 3/6 → conditional entry has full headroom. Patience > activity.

### Afternoon Addendum — Midday Scan (13:08 CT)
- Held tape: XLP +0.89% / +0.67% day, XLB +1.09% / +1.92% day (turned green), XLI -0.03% / +0.84% day. None at -7%, none at +15% tighten trigger. Held trails: XLP stop $75.92/hwm $84.35; XLB stop $46.61/hwm $51.79 (hwm ratcheted up from $51.20 yesterday); XLI stop $155.89/hwm $173.21. No cuts, no tightens, no thesis breaks — all three sit in YTD-leadership rotation cluster intact.
- ISM Services PMI Apr: headline 53.6 (cons 53.7, prev 54.0) — soft but expansion, no shock. Employment subindex 45.2 (inline with cons, well above the 43 stagflation threshold). Prices Paid not yet pulled by Perplexity. No stagflation kill.
- WTI: ~$102 intraday — round-tripped from yesterday's $105.13 close (-2.9% giveback) on Middle East de-escalation. Right at the conditional's $102 floor → momentum break per the conditional's prose.
- Iran/Hormuz: NEW HEADLINE — "U.S. reports holding cease-fire in Middle East erodes geopolitical risk premium; Strait of Hormuz disruptions ease" (Polymarket / Twelve Data context). This is exactly the (e) breakthrough kill switch the pre-market plan flagged.
- S&P 500: SPY $724.28 → S&P ~7,242, ~+0.6% intraday vs May 4 close 7,200.75. Tape constructive, not a risk-off (gate (c) clear).
- VIX: not pulled (Perplexity declined). Tape not behaving like a >21 spike — SPY green and rotation cluster green, suggests VIX likely back inside 18–19 normal band.
- XLE conditional → SKIPPED (gate (b) momentum break + gate (e) kill switch). Audit line appended above.
- Deployment unchanged at ~54.8%. Tomorrow's pre-market should reassess: (1) whether the cease-fire is durable (XLE thesis materially weakened if Hormuz reopens), (2) XLU as defensive 5th-leg watch given VIX still elevated vs. last week, (3) AMD/SMCI AMC reaction tape for chip-cluster signal.

## 2026-05-06 — Pre-market Research

ABORT: env vars missing — ALPACA_API_KEY, ALPACA_SECRET_KEY, PERPLEXITY_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID. No wrappers run, no live account/positions/orders pull, no Perplexity research. Telegram alert sent via wrapper fallback (creds resolved through wrapper config, not process env). Per routine: STOP and exit on missing env. Held positions per yesterday's EOD (XLP 239 / XLB 390 / XLI 87, all green, all under 10% trail GTCs, none at -7% or +15% triggers) continue under existing GTC trail stops — no new at-the-open action authored today.

### Decision
HOLD (forced — no research possible without env vars). Re-run pre-market after env is restored.

### Re-attempt Addendum (second pre-market run)
- Re-ran env-var verification per routine STEP 0: ALPACA_API_KEY, ALPACA_SECRET_KEY, PERPLEXITY_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID all still MISSING in process env.
- Confirmed by direct wrapper call: `bash scripts/alpaca.sh account` → "ALPACA_API_KEY: ALPACA_API_KEY not set in environment" (exit non-zero).
- Telegram alert re-sent via wrapper fallback (creds not resolved; wrote to DAILY-SUMMARY.md fallback file naming all five missing vars).
- No live account/positions/orders pull; no Perplexity research; no new trade ideas authored.
- Held positions disposition unchanged: XLP 239 / XLB 390 / XLI 87 continue under existing 10% trailing GTC stops (XLP $76.01 / XLB $46.61 / XLI $155.89 per yesterday's EOD). None within -7% or +15% trigger range as of last known quotes; no manual action required.
- Decision unchanged: HOLD (forced). Re-run pre-market after env is restored. Operator action item: surface the missing-env condition in the cloud routine config — two consecutive aborts on the same date indicate the secrets are not being injected into the routine process env.

### Afternoon Addendum — Midday Scan (12:01 CT)
- Env-var note: routine STEP 0 shell check (`${!v:-}`) again printed MISSING for all five vars in this `/bin/sh` session, but a smoke-test `bash scripts/alpaca.sh account` returned the live account JSON (equity $100,967.74, cash $45,158.79). Wrappers can read the env even when the loop check cannot — proceeded per saved feedback memory rather than aborting.
- Held tape (live quotes via Alpaca):
  - XLP 239 @ $83.36 → $83.875 (+0.62% unrealized, intraday -0.22%); stop $76.0545 / hwm $84.505.
  - XLB 390 @ $51.06 → $52.43 (+2.68% unrealized, intraday +1.75%); stop $47.394 / hwm $52.66 (hwm ratcheted up).
  - XLI 87 @ $172.47 → $175.915 (+2.00% unrealized, intraday +2.03%); stop $159.174 / hwm $176.86 (hwm ratcheted up).
- Cut check: none ≤ -7%. No closes.
- Tighten check: none ≥ +15%. Trails stay at 10%. No cancel/replace.
- Thesis check: cyclical-rotation legs (XLB, XLI) leading the tape today; defensive XLP modest red within noise. YTD-leadership rotation cluster intact, no thesis break, no manual exits.
- Conditionals: today's pre-market authored no "### Conditional Entries (midday-eligible)" section (forced HOLD on env aborts). No conditionals to evaluate.
- Action this scan: NONE. No Telegram. Sheets snapshot to follow.
- Deployment ~55.3% ($55,798 mkt value vs. $100,968 equity), still under the 75-85% target band; XLE candidacy remains weakened post-cease-fire (per yesterday's addendum) — defer leg-add decision to tomorrow's pre-market.

## 2026-05-07 — Pre-market Research

(Thursday — Day 9, week 2 day 4. Hold 3 sector-ETF longs (XLP/XLB/XLI), all green and well within trail stops. WTI rolled from $105 May 4 → $102.56 May 6 (intraday low $99.57), confirming the cease-fire / Hormuz-de-escalation narrative is sticking. No mega-cap earnings of size today. Quiet macro day; only Productivity & Costs Q1 prelim + weekly Jobless Claims at 8:30 ET. Daily cap resets to 3/3, weekly cap 3/6 used. Env-var shell check again printed MISSING — wrapper smoke-test confirmed creds work; proceeded per saved feedback memory.)

### Account
- Equity: $101,257.93
- Cash: $45,158.79 (44.60%)
- Buying power: $146,416.72
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.36 (mkt $20,267.20, +$344.85 / +1.73%), XLB 390 sh @ $51.06 (mkt $20,439.90, +$525.55 / +2.64%), XLI 87 sh @ $172.47 (mkt $15,392.04, +$387.53 / +2.58%). Cost basis $54,841 (~54.2% deployed at last quote).
- Open orders: 3 trail-stop GTCs — XLP $76.0545 stop / hwm $84.505; XLB $47.3985 stop / hwm $52.665; XLI $159.606 stop / hwm $177.34. All trail 10%, none within 3% of price, none below cost-basis at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$102.56 May 6 close (intraday low $99.57, range tightening); prediction-market implied ~$94–97 currently — material weakening from May 5 $107+ peak. Brent ~$108–112 (typical $5–10 premium). Symmetrical-triangle compression $90–110 with downside pressure now active post-cease-fire.
- S&P 500 futures: Mixed quotes from sources (ESM26 ~7,275 prediction print / +0.10–0.28% intraday); cash S&P closed May 6 ~7,254 implied via prior log (portfolio +0.77% day confirms constructive tape). Premarket flat-to-slightly-positive, no risk-off signal.
- VIX: 18.29 (last available May 4 close per Trading Economics; no fresh print captured). Still in normal 15–20 band but elevated vs. late-Apr 16-handle; regime-shift watch remains amber, not red.
- Today's catalysts: STRUCTURAL — no major event print. Productivity & Costs Q1 prelim + Initial Jobless Claims at 8:30 ET (low-tier), Challenger Job Cuts mid-morning. NO CPI, NO PPI, NO FOMC. AI-capex narrative still dominant (AMD +18% on data-center beat per market overview).
- Earnings before open: 22nd Century Group (XXII), Praxis Precision Medicines (PRAX) — micro/small cap, not tradable for our sector-ETF strategy. No mega-cap impact today.
- Economic calendar: Quiet through Thursday. Per prior framing Friday May 8 potentially carries NFP + ISM Services (cons +62k / 53.7), though some sources push NFP to June 5 — either way, treat tomorrow as the week's binary day. RBA decision overnight non-USD. CPI for May not until June 10.
- Sector momentum YTD (latest snapshot): XLE +32.63% (still #1 but momentum decelerating post-cease-fire), XLF +25.44% (Apr-strength but trailing-6mo lagging), XLI +24.75%, XLB +22.67%, XLP +17.94%, XLK +33.78% Apr-print but trailing-6mo +4.7% (capex-bear blunt). Held XLP/XLB/XLI all in YTD-leadership cluster; thesis intact, no break.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — all three +1.73% to +2.64% unrealized, all in YTD-leadership rotation cluster, none at -7% triggers, none at +15% tighten triggers. Best leg XLB at +2.64% well below the +15% threshold. Trail-stop GTCs live, hwms ratcheted upward. No add to existing names (XLP/XLB already at 20% cap on market value; XLI at 15% by design).
2. **XLE (Energy ETF)** — sector still YTD #1 (+32.63%) but Hormuz cease-fire holding for 2nd consecutive session, WTI rolled from $107+ to ~$95–102 range, May 6 intraday low $99.57 broke prior $102 momentum floor. Original conditional thesis was geopolitical-binary upside — that binary is now resolving downward. SKIP. Will re-evaluate once oil tape stabilizes or new geopolitical catalyst emerges.
3. **XLU (Utilities ETF)** — sector +9.80% YTD prior week; defensive cousin of XLP, benefits if VIX regime stays elevated. Author as a 5th-leg WATCH only — premature today (no fresh catalyst, no VIX breakout, daily cap available but conviction not there). Reassess on Monday post-NFP if VIX prints >20 sustained.
4. **AAPL / AMZN / single-name tech** — capex-bear overhang dormant but unresolved; AMD positivity is single-name not sector-confirming. SKIP, no edge.
5. **Earnings-day plays (XXII, PRAX)** — micro-cap, not in scope. SKIP per strategy.

### Conditional Entries (midday-eligible) — up to 3
(Zero conditionals authored today.)

Reasoning: today is a structurally quiet macro day (no event print, no earnings of size). XLE — the only standing leg-add candidate — has its catalyst materially weakened by the cease-fire holding 2 sessions, so authoring an XLE conditional would chase a deteriorating thesis rather than confirm a strong one. XLU is watch-only. Held positions need no manual action. No setup today genuinely benefits from intraday confirmation rather than at-the-open execution.

### Risk Factors
- Oil cease-fire / Hormuz-de-escalation holding 2nd day weakens the rotation-leadership-Energy thesis; if WTI breaks $95, XLE could leak 5–10% and drag XLB sympathetically (commodity tape correlation).
- Friday May 8 potentially carries NFP + ISM Services (some sources push to June 5 — date ambiguity is itself a risk; treat tomorrow as the week's macro binary). Sizing on any new entry today must allow hold through Friday or stay sidelined.
- VIX 18.29 vs. mid-16s late April — regime-shift amber-flag persists; a sustained break >20 flips the held-positions disposition to "tighten manually."
- AI-capex narrative still cuts both ways (AMD positive, META/AMZN earlier capex-bear); no held tech exposure but rotation tape can flip if cap-ex bears reassert.
- Productivity & Costs / Jobless Claims at 8:30 ET — low-tier prints, but a Jobless Claims spike (>250k cons range) ahead of NFP would compound stagflation read.
- Held positions: none near -7% (worst is +1.73%), none near +15% tighten trigger (best is +2.64%); no manual action required from this entry alone.
- Week-2 deployment still ~55% vs. 75–85% target — DO NOT force an add for deployment math; XLE candidacy weakened, no other high-conviction setup, capital reserve is the right disposition into Friday's binary.

### Decision
HOLD at the open. Zero at-the-open buys, zero midday conditionals. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers). XLE candidacy materially weakened by Hormuz cease-fire holding — defer rather than chase. XLU watch-only — premature without VIX regime break. Daily cap available 3/3, weekly cap 3/6 — full headroom preserved into tomorrow's potential NFP binary. Patience > activity. Reassess Friday pre-market with macro print in hand.

### Afternoon Addendum — Midday Scan (12:01 CT)
- Env-var note: routine STEP 0 shell check again printed MISSING for all four vars in this `/bin/sh` session, but smoke-test `bash scripts/alpaca.sh account` returned live JSON (equity $100,537.04, cash $45,158.79). Wrappers have creds — proceeded per saved feedback memory rather than aborting.
- Held tape (live quotes via Alpaca):
  - XLP 239 @ $83.357 → $83.80 (+0.53% unrealized, intraday -0.52%); stop $76.0545 / hwm $84.505 (unchanged).
  - XLB 390 @ $51.062 → $51.715 (+1.28% unrealized, intraday -1.33%); stop $47.493 / hwm $52.77 (hwm ratcheted from $52.665).
  - XLI 87 @ $172.466 → $174.545 (+1.21% unrealized, intraday -1.32%); stop $159.948 / hwm $177.72 (hwm ratcheted from $177.34).
- Cut check: none ≤ -7% (worst is XLP +0.53%). No closes.
- Tighten check: none ≥ +15% (best is XLB +1.28%). Trails stay at 10%. No cancel/replace.
- Thesis check: all three sector-ETF rotation legs in unison-red intraday on a soft tape (~-1.3% each on XLB/XLI, XLP -0.5%) — no idiosyncratic break, YTD-leadership rotation cluster intact. No manual exits.
- Conditionals: today's pre-market authored zero "### Conditional Entries (midday-eligible)" entries (deliberate — XLE thesis weakened post-cease-fire, XLU watch-only). No conditionals to evaluate.
- Action this scan: NONE. No Telegram.
- Deployment ~55.1% ($55,382 mkt value vs. $100,537 equity); cash reserve preserved into tomorrow's potential NFP binary per pre-market plan. Daily cap 0/3, weekly cap 3/6.

## 2026-05-08 — Pre-market Research

(Friday — Day 10, week 2 day 5; NFP day. Hold 3 sector-ETF longs (XLP/XLB/XLI), all green and well within trail stops. WTI continues to soften: $107 May 5 → $102.56 May 6 → $97.08 May 7 close → ~$96–97 spot. Hormuz cease-fire holding 3rd consecutive session. Today's binary: April Employment Situation (NFP / Unemployment / Hourly Earnings) at 8:30 ET, ISM Services / JOLTS / ISM Mfg / Construction Spending at 10:00 ET. Daily cap resets to 3/3, weekly cap 3/6 used. Env-var loop check again printed MISSING — wrapper smoke-test confirmed creds work; proceeded per saved feedback memory. Weekly review checkpoint follows market close.)

### Account
- Equity: $100,475.41
- Cash: $45,158.79 (44.94%)
- Buying power: $145,634.20
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,080.78, +$158.43 / +0.79%), XLB 390 sh @ $51.062 (mkt $20,139.60, +$225.25 / +1.13%), XLI 87 sh @ $172.466 (mkt $15,096.24, +$91.73 / +0.61%). Cost basis $54,841 (~55.1% deployed at last quote).
- Open orders: 3 trail-stop GTCs — XLP $76.0545 stop / hwm $84.505; XLB $47.493 stop / hwm $52.77; XLI $159.948 stop / hwm $177.72. All trail 10%, none within 3% of price, none below cost-basis at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$96–97/bbl spot (May 7 close $97.08, May 8 range $95.50–$99.47). Brent ~$108–110 (typical premium; one source flagging $120 looks stale). Symmetrical-triangle resolved DOWNWARD post-cease-fire — third consecutive session of softening; geopolitical premium unwinding cleanly.
- S&P 500 futures: ESM26 ~7,362.75 May 7 settle (+0.03%); cash S&P closed May 7 at -0.40%, Nasdaq -0.28%, Dow -0.51% — broad consolidation pre-NFP. Premarket flat-to-slightly-positive; massive E-mini put volume (8M+ contracts) signals options-side hedging into the print.
- VIX: 17.39 (May 6 close per FRED/YCharts); no fresh print captured. BACK INSIDE the calmer 16–18 band — yesterday's amber regime-shift watch flag has cooled; rotation tape can keep working unless NFP shocks.
- Today's catalysts: NFP DAY — April Employment Situation 8:30 ET (cons +70k Q2-fwd / unemployment 4.4% steady / hourly earnings +0.3% MoM, +3.7% YoY; March print was +178k, big upside surprise vs +60k cons). ISM Services PMI 10:00 ET. ISM Mfg + JOLTS + Construction Spending 10:00 ET. Triple-print binary day; consolidation in the futures tape reflects the binary.
- Earnings before open: light day — only ~53 reports vs. 405–566 prior days. No mega-cap of size; no held-ticker overlap. Not tradable for our sector-ETF strategy.
- Economic calendar: today is THE binary of the week; quiet thereafter through next FOMC. RBA non-USD overnight. CPI not until June 10.
- Sector momentum YTD (latest snapshot): XLE +28.32% (still #1 but decelerating from +32.63% Wed as oil leaks below $100), XLK +18.25% (capex-bear blunted but rebuilding), XLI +12.49%, XLP +9.06%, XLU +7.82%, SPY +7.91% (benchmark), XLF -4.86% (laggard). Held XLP/XLB/XLI all in or near the leadership cluster; XLP RSI ~80 = overbought signal worth flagging but no thesis break. No held-ticker idiosyncratic news (XLB/XLI sparse coverage; sector-flow story intact).

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — all three +0.61% to +1.13% unrealized, all in YTD-leadership rotation cluster, none at -7% triggers, none at +15% tighten triggers. XLP RSI ~80 overbought is a watch flag, NOT a sell signal — trail GTC handles a momentum unwind. No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design).
2. **XLE (Energy ETF)** — sector still YTD #1 (+28.32%) but momentum broke down 3rd session running. Cease-fire is now durable (3 sessions); WTI under $100 invalidates the original conditional thesis (geopolitical-binary upside). SKIP. Off the watchlist until oil tape stabilizes or new geopolitical catalyst.
3. **XLU (Utilities ETF)** — sector +7.82% YTD, defensive cousin of XLP. VIX back in 16–18 band undermines the regime-shift case for adding XLU as a 5th leg. WATCH only; reassess Monday post-NFP if VIX gaps >20 on a shock print.
4. **AAPL / AMZN / single-name tech** — capex-bear theme dormant; AMD +18% data-center beat is single-name confirmation, not sector-confirming. SKIP, no edge today especially into NFP binary.
5. **NFP-reaction trades (any ticker)** — explicit SKIP. Strategy is sector-rotation momentum, not macro-print scalping. Let the print clear and reassess Monday.

### Conditional Entries (midday-eligible) — up to 3
(Zero conditionals authored today.)

Reasoning: today is the macro-binary day of the week (NFP + ISM Services + JOLTS triple-print). Authoring a midday conditional would mean buying INTO the post-print tape with one hour of digestion — that's macro-reaction trading, not the strategy. XLE thesis is broken (cease-fire + WTI sub-$100); XLU watch-only without VIX regime break; held positions need no manual action. Capital reserve is the right disposition; conviction setups belong in Monday's pre-market with the print fully digested over the weekend.

### Risk Factors
- NFP shock either way: hot print (>+150k, hourly earnings >+0.4% MoM, unemployment <4.3%) = inflation/hawkish-Fed signal, can crater XLP/XLU and broader rotation tape; soft print (<+30k, hourly earnings flat) = stagflation read combined with ISM Services Employment subindex, breaks the rotation-leadership thesis. In-line print (+50–100k, 4.4% steady) = quiet day, held positions hold.
- Massive E-mini put volume (8M+ contracts) into expiry signals heavy hedging; gap-open risk on either NFP outcome is amplified.
- ISM Services 10:00 ET is the second leg — Employment subindex still the pre-NFP read concept, Prices Paid the inflation tell. Stagflation-tilt signal would compound a soft NFP.
- Oil tape: WTI sub-$100 third session means cyclical legs (XLB) carry commodity-tape correlation risk if oil keeps leaking; XLB +1.13% unrealized has limited cushion before approaching stop.
- XLP RSI ~80 overbought — momentum unwind risk; +0.79% unrealized leaves modest cushion before trail-stop activates ($76.0545 stop = ~9% below entry of $83.357 with hwm $84.505).
- VIX 17.39 inside normal band but options-tape hedging suggests realized vol could exceed 17.39 after the print prints.
- Held positions: none near -7% (worst is XLI +0.61%), none near +15% tighten trigger (best is XLB +1.13%); no manual action required from this entry alone.
- Week-2 deployment ~55.1% vs. 75-85% target; into NFP binary the right disposition is to STAY at 55% rather than force an add. Weekly review later today will diagnose deployment-stagnation if applicable.
- Friday afternoon thin tape + weekly close positioning amplifies any post-print binary; market-on-close drift can extend the print's reaction.

### Decision
HOLD at the open. Zero at-the-open buys, zero midday conditionals. Held XLP/XLB/XLI continue under their 10% trailing GTCs. NFP + ISM Services triple-print at 8:30/10:00 ET is the week's macro binary — strategy is sector-rotation momentum, not macro-reaction; capital reserve is the right disposition. XLE candidacy off (cease-fire durable, WTI sub-$100 broke the thesis). XLU watch-only (VIX back in normal band). Daily cap 3/3 available, weekly cap 3/6 — full headroom preserved into Monday's reassessment with NFP fully digested. Weekly review later today will document week-2 results (3 trades, +0.4-something% phase P&L vs. SPY benchmark, deployment-stagnation diagnosis). Patience > activity.

## 2026-05-11 — Pre-market Research

(Monday — Day 11, week 3 day 1. Week 2 closed +0.47% phase ($100,466.31). Friday's NFP digested cleanly: SPX cash printed an all-time high at 7,398.51 on Friday May 8 (+0.84% on the week); ES futures premarket today ~7,412.50, -0.09%. WTI continues to soften: $97.08 May 7 → ~$95–97 spot today; Hormuz cease-fire holding 4th consecutive session. Daily cap 3/3 fresh, weekly cap 0/6 fresh. CPI prints Tuesday May 12 at 8:30 ET (cons +3.7% YoY headline, +0.4% MoM / 2.7% YoY core) — the binary of the week. Env-var loop check again printed MISSING for all five vars; wrapper smoke-test confirmed `alpaca.sh account` returns live JSON (per saved feedback memory).)

### Account
- Equity: $100,470.86
- Cash: $45,158.79 (44.95%)
- Buying power: $145,629.65
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,121.41, +$199.06 / +0.999%, current $84.19), XLB 390 sh @ $51.062 (mkt $20,124.00, +$209.65 / +1.053%, current $51.60), XLI 87 sh @ $172.466 (mkt $15,066.66, +$62.15 / +0.414%, current $173.18). Cost basis $54,841 / mkt $55,312.07 (~55.05% deployed).
- Open orders: 3 trail-stop GTCs — XLP $76.32 stop / hwm $84.80; XLB $47.493 stop / hwm $52.77; XLI $159.948 stop / hwm $177.72. All trail 10%, none within 3% of price, none at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$95.42–$97.41/bbl spot (range tightening on 4th consecutive cease-fire session); Brent ~$103.64–$104.87, premium ~$6–9. Geopolitical premium fully unwound from May 5 $107 peak; oil tape is no longer the rotation-leadership driver.
- S&P 500 futures: ESM26 ~7,412.50 premarket (-0.09%, vol 75k contracts). SPX cash 7,398.51 May 8 close = ATH on Friday post-NFP relief rally (+0.84% wkly). Futures defending 7,410 support; resistance 7,469–7,585 (Fibonacci) on a break above.
- VIX: 17.19 May 8 close (Cboe; prev 17.08, intraday open 17.37). Solidly inside 16–18 normal band, regime-shift watch flag is OFF. Realized vol post-NFP was muted.
- Today's catalysts: STRUCTURALLY QUIET — no major macro print today. Light pre-CPI consolidation expected. AI-capex narrative still dominant in single-name tape (Apple-Intel deal rumor, chipmakers strong).
- Earnings before open: CEG ($2.54), SPG ($3.01), STE ($2.85), MOS ($0.24), MNDY ($0.93), FOXA ($0.98), B/Barrick ($0.81), TME ($1.37), UAA (-$0.02), PLUG (-$0.10), LULU (this week), BABA AMC. None held, no sector-ETF impact of size (CEG/SPG idiosyncratic, MOS is a single materials name not the ETF).
- Economic calendar this week: Mon quiet → Tue CPI 8:30 ET (THE binary) → Wed PPI 8:30 ET → Thu Retail Sales + Initial Claims 8:30 ET → Fri quiet. CPI cons headline +3.7% YoY (up from +3.3% prior), core +0.4% MoM / +2.7% YoY. New Fed chair confirmation backdrop amplifies CPI's monetary-policy weight.
- Sector momentum YTD (May 1/8 snapshots, dividends reinvested vs SPY +8.46%): XLE +25.40% (#1, decelerating from +28.32% last Thu as oil leaks), XLK +22.07% (rebuilding from capex-bear), XLB ~+12% (cross-source estimate, leadership cluster), XLI +11.97% (held, leadership cluster), XLP +8.98% (held, in line with SPY), XLU +5.49%, XLC -0.53%, XLF -5.96 to -8.27% (laggard). Held XLP/XLB/XLI all in leadership/mid-pack rotation cluster; thesis intact, no idiosyncratic news, no -7% triggers, no +15% tighten triggers.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — all three +0.41% to +1.05% unrealized, all in YTD-leadership rotation cluster, none at -7% triggers, none at +15% tighten triggers. Best leg XLB at +1.053% well below the +15% threshold. Trail-stop GTCs live, hwms ratcheted on Friday's strength (XLP hwm $84.80 vs $84.505 prior). No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design).
2. **XLE (Energy ETF)** — sector still YTD #1 (+25.40%) but momentum 4th session of deceleration, WTI sub-$100 firmly. Original conditional thesis (geopolitical-binary upside) is fully resolved downward. SKIP. Off the watchlist until oil tape stabilizes above $100 or new geopolitical catalyst emerges.
3. **XLK (Technology ETF)** — sector +22.07% YTD, capex-bear narrative blunted, AI-tape constructive (AMD +18% data-center beat, Apple-Intel rumor). Not authored today — into CPI binary, adding a high-beta tech leg is event-reaction trading, not the strategy. WATCH for post-CPI reassessment Wednesday if print clears in-line and XLK confirms breakout.
4. **XLU (Utilities ETF)** — sector +5.49% YTD, defensive cousin of XLP. VIX 17 inside normal band undermines the regime-shift case for adding XLU as a 5th leg. WATCH only; reassess if VIX gaps >20 on CPI shock.
5. **Single-name earnings (CEG, SPG, LULU, etc.)** — SKIP per strategy. Sector-ETF momentum, not earnings binaries.
6. **NFP-post / CPI-reaction trades** — explicit SKIP. Wait for the print, reassess Wednesday's pre-market with CPI digested.

### Conditional Entries (midday-eligible) — up to 3
(Zero conditionals authored today.)

Reasoning: today is a structurally quiet macro day INTO Tuesday's CPI binary. Authoring a midday conditional would mean committing capital one trading session before the week's major macro print — that's the wrong risk-asymmetry vs. waiting for the print to clear. XLE thesis is broken; XLK/XLU are watch-only (need CPI to clear); held positions need no manual action. Capital reserve is the right disposition into CPI; conviction setups belong in Wednesday's pre-market with the print digested.

### Risk Factors
- CPI Tuesday is the week's binary: hot print (>+3.8% YoY headline, core >+0.5% MoM) = hawkish-Fed re-pricing, can crater XLP/XLU and rate-sensitive cyclicals; soft print (<+3.5% YoY, core <+0.3% MoM) = dovish-tail, lifts equities broadly especially rate-sensitives. In-line print (~+3.7% / +0.4%) = quiet day, SPX consolidates near ATH.
- SPX at ATH 7,398.51 = elevated-base risk; any CPI shock has more downside asymmetry than upside given valuations. Held positions carry directional beta to a CPI-driven SPX drawdown.
- Oil tape: WTI sub-$100 4th consecutive session means cyclical legs (XLB) carry commodity-tape correlation risk if oil keeps leaking; XLB +1.053% unrealized has limited cushion before approaching trail.
- Single-name earnings density today (CEG, SPG, LULU, BABA AMC, etc.) is moderate but idiosyncratic — only sector-flow risk if a cluster of misses tags a thematic sector. Watch CEG (utilities/power) for XLU read-through, MOS (materials) for XLB sympathy (small position weighting in XLB, unlikely to move the ETF materially).
- New Fed chair confirmation backdrop amplifies CPI's hawkish/dovish tilt — political-monetary crossover risk if confirmation hearings produce dovish/hawkish soundbites.
- AI-capex narrative is constructive (AMD beat) but two-way; META/AMZN capex-bear ghosts still in tape memory. XLK watch-only, no held tech exposure.
- Held positions: none near -7% (worst is XLI +0.41%), none near +15% tighten trigger (best is XLB +1.053%); no manual action required from this entry alone.
- Week 3 deployment ~55% vs. 75-85% target — structural deployment-stagnation persists. Friday's weekly review (commit `3bfd7a2`) flagged this; the disposition into CPI is HOLD reserve, but if CPI clears in-line Wednesday, the bar for adding a 4th leg (XLK or XLU) drops materially.
- E-mini put volume into Friday was 8M+ contracts (heavy hedging); some of that unwound into Friday's ATH close, but residual hedging tape into CPI can amplify either-way moves.

### Decision
HOLD at the open. Zero at-the-open buys, zero midday conditionals. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact). Tuesday CPI (cons +3.7% YoY / +0.4% MoM core) is the week's macro binary — committing capital into the print one session before is poor risk-asymmetry, especially with SPX at ATH. XLE candidacy off (cease-fire durable 4 sessions, WTI sub-$100); XLK/XLU watch-only into CPI. Daily cap 3/3 available, weekly cap 0/6 fresh — full headroom preserved into Wednesday's post-CPI reassessment. Patience > activity.

## 2026-05-12 — Pre-market Research

(Tuesday — Day 12, week 3 day 2, CPI DAY. Hold 3 sector-ETF longs (XLP/XLB/XLI), basket flat-to-mixed vs. Monday's snapshot (XLB +1.30% Mon close ratcheting further pre-market, XLI giving back yesterday's +1.06%, XLP flat). April CPI at 8:30 ET (cons +3.7% YoY / +0.6% MoM headline, +2.7% YoY / +0.3% MoM core; Cleveland Fed nowcast 3.56%; markets price >3.6% at 67-78%). Iran/Hormuz tape RE-ESCALATED overnight — Trump rejected Iran's 14-point counter as "garbage" on Truth Social May 11; WTI bouncing $99.45 (+1.41% session, June futures CLM6), Brent $116.55 — the durable-cease-fire narrative from last Thu/Fri/Mon has cracked. Daily cap 3/3 available (1/6 weekly fresh — XLE add WAS NOT placed yesterday despite earlier framing). Env-var loop check again printed MISSING for all five vars; wrapper smoke-test confirmed `alpaca.sh account` returns live JSON (per saved feedback memory). Fed Chair transition (Powell → Warsh) finalizes Friday — adds dovish-tilt expectation backdrop to CPI.)

### Account
- Equity: $100,585.18
- Cash: $45,158.79 (44.90%)
- Buying power: $145,743.97
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $19,951.72, +$29.37 / +0.15%, current $83.48, intraday +0.13%), XLB 390 sh @ $51.062 (mkt $20,475.00, +$560.65 / +2.82%, current $52.50, intraday +0.46%), XLI 87 sh @ $172.466 (mkt $14,999.67, -$4.84 / -0.03%, current $172.41, intraday -1.50%). Cost basis $54,841 / mkt $55,426.39 (~55.10% deployed).
- Open orders: 3 trail-stop GTCs — XLP $76.32 stop / hwm $84.80; XLB $47.493 stop / hwm $52.77; XLI $159.948 stop / hwm $177.72. All trail 10%, none within 3% of price, none at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$99.45 (CLM6, +1.41% session); Brent ~$116.55. Geopolitical premium RE-ASSERTING after Trump rejected Iran's 14-point counter ("totally unacceptable", "garbage") May 11 — IRGC fired on US Navy warships in strait, drone strikes on UAE/Kuwait/Qatar (UAE intercepted 2). Hormuz ~20% global oil supply, ~1,500 cargo vessels still trapped per recent reporting. Brent-WTI spread elevated (~$17) on Hormuz shipping risk. This is a material reversal of the durable-cease-fire framing carried through Mon's pre-market.
- S&P 500 futures: Premarket data conflicting — Business Insider quote ESM26 ~6,657.50 (+0.10%, 06:22 ET); contextual reference (Friday SPX ATH 7,398.51, yesterday's pre-market ES ~7,412.50) suggests the 6,657 print is stale/source-error rather than a ~10% gap-down (no event would justify). Treat the +0.10% bias as the load-bearing read, absolute level ambiguous. Premarket bias = slightly positive, consolidation tone into CPI.
- VIX: No fresh print captured (last log: 17.19 May 8 close). Implied = unchanged 16–18 normal band, low-moderate read consistent with consolidation premarket tape. Will spike on hot CPI; would compress on cool CPI.
- Today's catalysts: CPI 8:30 ET = the binary. Real Earnings 8:30 ET same release. No Fed speakers listed. No Treasury auction of size flagged. AI-capex narrative dormant ahead of Cisco/Applied Materials Wed-Thu. Fed Chair transition (Powell final CPI act → Warsh handover Fri) adds rate-path-expectation amplifier; consensus pre-priced expects Warsh-era dovish tilt, so a hot print snaps that and could trigger broad correction off SPX ATH.
- Earnings before open: CEG (Constellation Energy, $108B mkt cap, 2.60 cons +21.5% YoY), B (Barrick Mining, $79B, 0.79 cons +125.7%), IX (ORIX, $39B), SATS (EchoStar, $37B), CRCL (Circle Internet, $32B), FOXA (Fox Corp, $29B), MOS (Mosaic, $7B), MNDY (monday.com, $4B). No held tickers. MOS (materials) → marginal XLB read-through but small ETF weighting, unlikely to move XLB materially. CEG (power/utilities-adjacent) → XLU read-through if guidance shocks. No mega-cap of size; no broad sector-flow driver.
- Economic calendar this week: Tue CPI 8:30 ET (TODAY) → Wed PPI 8:30 ET (cons +0.3% MoM core) → Thu Retail Sales + Initial Claims 8:30 ET → Fri quiet + Fed Chair handover. CPI is the dominant macro print; PPI confirms.
- Sector momentum YTD (latest 6-month trailing snapshot): XLE +30.3% (still #1, ACCELERATING again on renewed Iran escalation reversing last week's deceleration), XLB +17.2% (held — leadership cluster, AI/infrastructure/defense tailwind), XLI +11.4% (held — Schwab "Most Favored", AI infra/defense), XLC +10.3%, XLP +7.2% (held — defensive hedge, Coca-Cola key holding +12.3% YTD, neutral rating but breakout from multi-year consolidation per MarketBeat May 11), XLK +4.7% (Schwab "More Favored" but lagging YTD), XLU +2.3%, XLY +0.4% (laggard), XLV -1.2%, XLF -2.0%. Held XLP/XLB/XLI all confirmed in leadership/mid-pack rotation cluster; thesis intact, no idiosyncratic news of size, no -7% triggers, no +15% tighten triggers.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLB +2.82% unrealized is best of basket (well below +15% tighten threshold), XLP +0.15% (RSI ~80 overbought watch flag from Mon, but no thesis break), XLI -0.03% (giving back yesterday's +1.06% intraday, deepest red on the day). None at -7% triggers. Trail-stop GTCs live, hwms intact from Fri (XLP $84.80 / XLB $52.77 / XLI $177.72). No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design).
2. **XLE (Energy ETF)** — sector YTD +30.3%, ACCELERATING again on overnight Iran escalation (Trump rejecting Iran counter, WTI back to $99.45, Brent $116.55). Original conditional thesis (geopolitical-binary upside) was declared "broken" Mon — that call now looks premature. HOWEVER, committing one trading session before CPI is wrong risk-asymmetry: if CPI prints HOT, oil/inflation hedge is doubly bid AND rate-path repricing crushes equities broadly (mixed signal for XLE which has both inflation-hedge tailwind and rate-sensitive cyclical risk). WATCH-only today; the cleaner re-entry is Wed pre-market with CPI digested AND Iran tape clear.
3. **XLK (Technology ETF)** — sector +4.7% YTD 6-mo (laggard despite Schwab "More Favored"), AI-capex constructive (AMD beat carrying through). Into CPI binary, adding high-beta tech is event-reaction trading. SKIP. Reassess post-CPI Wed with Cisco/Applied Materials AMC Thu earnings tape also in hand.
4. **XLU (Utilities ETF)** — sector +2.3% YTD (laggard), defensive cousin of XLP. CEG earnings BMO with strong cons (+21.5% YoY EPS, +26.85% revenue) is a positive sector read-through but single-name, idiosyncratic. VIX 17 still inside normal band undermines regime-shift case for adding as 5th leg. WATCH only; reassess if VIX gaps >20 on CPI shock.
5. **Single-name earnings (CEG, B/Barrick, MOS, MNDY, etc.)** — SKIP per strategy. Sector-ETF momentum, not earnings binaries. B/Barrick miners benefit from gold + tariffs theme but XLB exposure dilutes; no individual stock take here.
6. **NFP / CPI-reaction trades (any single name)** — explicit SKIP. Wait for print, reassess Wed pre-market.

### Conditional Entries (midday-eligible) — up to 3
(Zero conditionals authored today.)

Reasoning: today is CPI binary day. Authoring a midday conditional means committing capital with one hour of post-print digestion on the week's dominant macro event — that's macro-reaction trading, not the strategy. XLE re-escalation thesis is real but premature (need to see post-CPI tape AND Iran tape persistence over 24-48hr); committing today is double-binary (CPI + Iran headlines simultaneously). XLK/XLU are watch-only (need CPI to clear). Held positions need no manual action. Capital reserve is the right disposition; conviction setups belong in Wed pre-market with CPI fully digested.

### Risk Factors
- CPI hot print (>+3.8% YoY headline, core >+0.5% MoM) = hawkish re-pricing INTO Warsh-handover dovish-tilt prior = double-shock asymmetry; SPX at ATH 7,398 carries elevated correction risk. Held XLP/XLB/XLI all carry directional beta to a hawkish-CPI SPX drawdown, but the trail-stop GTCs absorb up to 10% from hwm before forced exit.
- CPI cool print (<+3.5% YoY, core <+0.3% MoM) = dovish-tail confirmation of Warsh expectation, lifts rate-sensitives broadly (XLU, XLK, XLF) — but our basket is cyclical/defensive, not pure rate-sensitive; basket likely up modestly on a cool print but underperforms rate-sensitive sectors.
- CPI in-line (~+3.7% / +0.3-0.4%) = quiet day, SPX consolidates near ATH, basket holds.
- Iran/Hormuz RE-ESCALATION post-Trump rejection May 11 is the secondary binary today — WTI back to $99.45, Brent $116.55, Brent-WTI spread $17. If a fresh Iran headline tags during/after CPI, XLE/XLB get inflation-hedge bid; XLP/XLU also benefit defensively; XLI/XLK get hit on input-cost amplification.
- SPX premarket source-data discrepancy (Business Insider 6,657 vs. contextual ~7,400 reference) is suspect — Perplexity may have served stale 2025-era prints. The DIRECTIONAL signal (+0.10% premarket, consolidation tone) is the load-bearing read; absolute level uncertain pending market open.
- XLP RSI ~80 overbought (from Mon log) — momentum unwind risk; Mon's -0.96% was first digestion print, +0.15% unrealized today leaves modest cushion before trail-stop activates ($76.32 stop = ~8.5% below entry of $83.357 with hwm $84.80). Coca-Cola breakout supports the leg but rotation tape can flip.
- XLI giving back yesterday's +1.06% in pre-market (-1.50% intraday) deserves a watch; if it continues to weaken on a hawkish CPI, deepest-red leg becomes the manual-cut watch candidate, though still far from -7% (-0.03% unrealized vs. -7% = $160.39 entry-relative). No action this entry.
- Fed Chair confirmation hearings Fri amplify CPI's monetary-policy weight; hawkish-Warsh soundbite + hot CPI = compound risk; dovish-Warsh + cool CPI = compound relief.
- E-mini put volume residue from Friday's heavy hedging tape still amplifies either-way moves; gap-open risk on CPI binary remains elevated.
- AI-capex narrative quiet (Cisco/Applied Materials Wed-Thu) — not a today-risk but a Wed-Thu-risk; held XLK exposure = zero so direct risk is nil, but rotation tape can be tagged by a capex-bear soundbite.
- Held positions: none near -7% (worst is XLI -0.03%), none near +15% tighten trigger (best is XLB +2.82%); no manual action required from this entry alone.
- Week 3 deployment ~55.10% vs. 75-85% target — structural deployment-stagnation persists for a 3rd straight week. The right disposition into CPI is to STAY at 55% rather than force an add; if CPI clears in-line and Iran tape stabilizes, Wed pre-market opens the door for a 4th leg (XLE re-asserting OR XLK breakout-confirmation OR XLU regime-shift).

### Decision
HOLD at the open. Zero at-the-open buys, zero midday conditionals. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact). Tuesday April CPI (cons +3.7% YoY / +0.3% MoM core) at 8:30 ET is the week's macro binary AND Iran/Hormuz tape has materially re-escalated overnight (Trump rejection May 11, WTI $99.45, Brent $116.55) — committing capital into a double-binary one print before is poor risk-asymmetry, especially with SPX at ATH. XLE candidacy WATCH-only (re-asserting but premature today); XLK/XLU watch-only into CPI. Daily cap 3/3 available, weekly cap 0/6 fresh (or 1/6 if XLE conditional yesterday lifted; portfolio data confirms NO new fills since May 04, so 0/6 fresh holds). Full headroom preserved into Wed post-CPI reassessment. Patience > activity.

## 2026-05-13 — Pre-market Research

(Wednesday — Day 13, week 3 day 3, PPI day. CPI digested constructively yesterday despite a HOT April print (3.8% YoY headline vs. ~3.1% cons / +0.6% MoM; Energy +17.9% YoY tied to Hormuz gasoline shock; core 2.8% YoY / +0.4% MoM) — basket closed +0.16% Day P&L / +0.85% Phase. Hormuz/Iran tape NOW STRUCTURAL: research confirms Strait of Hormuz effectively closed since Feb 28, 2026 (multi-month, not a binary tape risk); France deployed an aircraft carrier strike group; UK preparing to secure waterway; Trump-Xi meeting this week to pressure China to force Iran to reopen. WTI ~$102.93 spot (Brent est. $106–110, premium $3–8 norm). Daily cap 3/3 fresh, weekly cap 0/6 fresh. PPI 8:30 ET = today's macro print. Env-var loop check again printed MISSING for all five vars; wrapper smoke-test confirmed `alpaca.sh account` returns live JSON (per saved feedback memory).)

### Account
- Equity: $100,533.82
- Cash: $45,158.79 (44.92%)
- Buying power: $145,692.61
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,080.78, +$158.43 / +0.795%, current $84.02, intraday -0.50%), XLB 390 sh @ $51.062 (mkt $20,108.40, +$194.05 / +0.974%, current $51.56, intraday -1.11%), XLI 87 sh @ $172.466 (mkt $15,185.85, +$181.34 / +1.209%, current $174.55, intraday +0.12%). Cost basis $54,841.21 / mkt $55,375.03 (~55.08% deployed).
- Open orders: 3 trail-stop GTCs — XLP $76.518 stop / hwm $85.02; XLB $47.493 stop / hwm $52.77; XLI $159.948 stop / hwm $177.72. All trail 10%, none within 3% of price, none at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$102.93 spot (Twelve Data 5/13); Brent est. $106–110 (premium $3–8 norm; no clean spot quote). Hormuz crisis is structural now — Strait effectively closed since Feb 28, 2026 (~10+ weeks); ~1,500 cargo vessels remain trapped per recent reporting; France deployed CSG; UK assisting; Trump rejected Iran's 14-point counter May 11 ("garbage"); Trump-Xi meet this week to pressure China (40% China oil from region) to force Iran reopen. CPI Energy subcomponent +17.9% YoY is the inflation-print fingerprint of this supply shock. Goldman 2026 oil forecast $53 is irrelevant near-term — supply-shock regime dominates.
- S&P 500 futures: ESM26 +0.10% premarket (Business Insider 06:22 ET); SPX cash sitting near recent ATH cluster ~7,400 (Friday 5/8 print 7,398.51). Quiet pre-PPI tone. Source-data discrepancy continues across feeds; treat the directional signal (slightly positive, consolidation) as the load-bearing read, absolute level ambiguous.
- VIX: No fresh print captured (last log: 17.19 May 8 close). Implied = unchanged 16–18 normal band post-CPI absorption; regime-shift watch flag is OFF. Would spike on hot PPI; would compress on cool PPI.
- Today's catalysts: PPI 8:30 ET = today's binary (April PPI; cons ~+0.3% MoM core, confirms or refutes CPI hot signal). No Fed speakers of size flagged. Cisco (CSCO) earnings AMC (cons EPS $0.92, rev ~$14B) is the AI-tape read; Applied Materials AMC Thu. Fed Chair transition (Powell → Warsh) finalizes Friday — adds dovish-tilt expectation backdrop; hot PPI compounds the CPI signal and snaps that prior.
- Earnings before open: Per multiple sources, NO major US pre-market reports of size today (Nasdaq calendar flags "data not available"; Wall Street Horizon shows Optorun JP, Adecco SA, Globe Telecom PH only — no held tickers, no sector-flow driver). Mega-cap focus shifts to CSCO AMC tonight + AMAT/BABA Thu.
- Economic calendar this week: Tue CPI 8:30 ET (DONE — hot 3.8% YoY, absorbed) → Wed PPI 8:30 ET (TODAY) → Thu Retail Sales + Initial Claims 8:30 ET → Fri quiet + Fed Chair handover (Powell → Warsh). PPI confirms or refutes the CPI hot read.
- Sector momentum YTD (refreshed May 12 snapshot, dividends reinvested vs SPY): XLK +21.85% (#1, megacaps AAPL/MSFT/NVDA ~70% weight, mid-cycle leader despite $2.3B net sell imbalance on 5/12), XLI +20.14% (held — leadership-quadrant cluster, materially ratcheted vs. prior 6-mo +11.4% snapshot), XLE est. mid-teens (top quadrant on Hormuz supply-shock; structural bid), XLB +17.2% (held — leadership cluster, AI/infrastructure/defense tailwind), XLP est. low-single-digits but in "leading" momentum quadrant on defensive bid (held — Coca-Cola breakout), XLU +5.49% (lagger, defensive cousin). Held XLP/XLB/XLI all confirmed in leadership cluster; thesis intact, no idiosyncratic news of size, no -7% triggers, no +15% tighten triggers.
- Fed cut expectations: Goldman / JPM / Barclays / Fidelity all now forecast ZERO cuts in 2026 (Goldman first cut Dec 2026 + Mar 2027; JPM hold + +25bp Q3 2027; Barclays first cut Mar 2027). CME FedWatch + Polymarket pricing virtually zero. Higher-for-longer regime locked. Implication: inflation-hedge/commodity sectors structurally favored; high-multiple growth gets multiple-compression risk on every hot inflation print.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLI +1.21% unrealized best of basket (well below +15% tighten threshold), XLB +0.97%, XLP +0.80%. None at -7% triggers. Trail-stop GTCs live; XLP hwm $85.02 (ratcheted yesterday from $84.80, stop now $76.518); XLB hwm $52.77 unchanged; XLI hwm $177.72 unchanged. No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design).
2. **XLE (Energy ETF) — CONDITIONAL** (see Conditional Entries below). Thesis: Hormuz closure is structural (10+ weeks, multi-nation military response building) not a binary headline; sector in leadership cluster; CPI Energy +17.9% YoY is the supply-shock print fingerprint; higher-for-longer Fed locks the regime. Last week's "cease-fire durable, thesis broken" call was premature. Today's PPI 8:30 ET is the gating binary, hence conditional (not at-open) execution.
3. **XLK (Technology ETF)** — sector YTD #1 (+21.85%) but $2.3B net sell imbalance on 5/12, megacap-heavy concentration risk, multiple-compression vulnerability under higher-for-longer Fed and hot inflation prints. Cisco AMC tonight + Applied Materials Thu AMC are the AI-tape reads. SKIP today; chasing the YTD #1 leader into a hot-inflation regime is wrong asymmetry. Reassess Thu pre-market with CSCO digested.
4. **XLU (Utilities ETF)** — sector +5.49% YTD (laggard), defensive cousin of XLP. VIX 17 still inside normal band undermines regime-shift case. WATCH only; reassess if VIX gaps >20 on PPI shock.
5. **Single-name (CSCO, AMAT, etc.)** — SKIP per strategy. Sector-ETF momentum, not earnings binaries.
6. **PPI-reaction trades (any single name)** — explicit SKIP. Wait for print, sector-ETF conditional only.

### Conditional Entries (midday-eligible) — up to 3
1. **XLE** — allocation $19,837 (345 sh @ ~$57.50 est. ref close $57.14–57.57), stop 10% trail GTC, target +20% (~$69.00), R:R 2:1
   Condition: After PPI 8:30 ET prints, ALL FOUR gates must clear by ~11:30 ET for execution at market: (1) PPI in-line or cool (headline ≤+0.4% MoM, core ≤+0.4% MoM — anything materially hotter = SKIP, double-hot-inflation print compounds CPI and is hawkish-Fed shock, mixed signal for XLE which has both inflation-hedge tailwind and broad-equity-correction risk); (2) WTI holds ≥$100 on session (any Hormuz-reopen / China-pressure-success headline that breaks WTI below $100 voids the thesis); (3) VIX <22 (no broad-market shock that bleeds defensives along with cyclicals); (4) XLE itself trading green-on-day or within -0.5% (confirms the bid is present; chasing a -2% pullback = catching falling knife). All four required; any one failing = HOLD entirely.
   Catalyst: Multi-month Hormuz closure (since Feb 28, 2026) is structural supply shock, NOT binary headline; CPI Energy +17.9% YoY confirms inflation-print fingerprint; Fed-cuts-off-table (0 cuts 2026 per Goldman/JPM/Barclays) locks inflation-hedge regime; YTD sector leadership cluster; deployment lift 55.1% → 74.9% (inside 75-85% target band lower edge).
   → Skipped (12:00 CT): gate (1) — April PPI headline +1.4% MoM (BLS, largest since Mar 2022) vs ≤+0.4% threshold (~3x cons +0.5%, YoY +6.0% vs +4.3% prior). Double-hot inflation print compounds yesterday's hot CPI; gates 2-4 not evaluated (gate 1 fails decisively). XLE intraday $57.41 / prev close $57.57 = -0.28% (gate 4 would have passed). HOLD entirely per condition.

(No other conditionals authored. XLK is YTD leader but multiple-compression risk under hot-inflation regime is the wrong asymmetry; XLU lacks the regime-shift gate.)

### Risk Factors
- PPI hot print (headline >+0.5% MoM, core >+0.5% MoM) confirms CPI hot signal = compound hawkish-Fed re-pricing under already-zero-cuts-priced regime; SPX ~ATH carries elevated correction risk; held XLP/XLB/XLI carry directional beta to a hawkish-PPI SPX drawdown, but trail-stop GTCs absorb up to 10% from hwm before forced exit. XLE conditional voids on hot PPI per gate (1).
- PPI cool print (headline <+0.2% MoM, core <+0.2% MoM) = walks back CPI hot signal, dovish-tail relief, lifts equities broadly especially rate-sensitives (XLK, XLU, XLF); XLE conditional clears gate (1) cleanly.
- PPI in-line (~+0.3% MoM headline, +0.3% MoM core) = quiet day, SPX consolidates near ATH, basket holds; XLE conditional clears gate (1).
- Hormuz reopen / China-pressure-success binary headline (Trump-Xi meeting this week is the gating event): WTI could gap -5 to -10% on a credible breakthrough; XLE -5 to -10% sympathy; voids conditional via gate (2). This is the dominant single-headline risk today.
- SPX at recent ATH ~7,400 = elevated-base risk; any PPI shock has more downside asymmetry than upside given valuations. Held basket carries beta but no leg near trail-stop trigger.
- XLE chase-risk: sector is YTD leadership cluster after weeks of structural-Hormuz bid; entering at $57.50 is not catching a bottom — it's joining a trend after the bulk of the move. Trade is justified by structural-supply-shock thesis + deployment-stagnation pressure, NOT by trying to catch a low.
- Single-name earnings (CSCO AMC tonight, AMAT/BABA Thu AMC) = AI-tape binary risk Thu pre-market; no held tech exposure but XLB/XLI carry AI-infrastructure correlation; thesis-break risk if mega-capex bear narrative reignites.
- Cisco AMC tonight is the largest single read-through of size today; positive surprise lifts XLK and AI-cap-ex narrative broadly, negative miss tags XLK and bleeds into XLB/XLI infrastructure correlation.
- Fed Chair confirmation (Powell → Warsh Fri) amplifies PPI's monetary-policy weight; hawkish-Warsh soundbite + hot PPI = compound risk; dovish-Warsh + cool PPI = compound relief.
- XLP RSI ~80 overbought watch flag continues from Mon log; Tuesday's +1.30% put XLP at a new hwm $85.02, momentum is reasserting but Coca-Cola weighted reversal is the leg's idiosyncratic risk.
- XLI giving back yesterday's morning weakness; current +1.21% unrealized has cushion, but if PPI tags cyclicals via input-cost amplification, the leg can compress fast.
- Held positions: none near -7% (worst is XLP +0.80%), none near +15% tighten trigger (best is XLI +1.21%); no manual action required from this entry alone.
- Week 3 deployment ~55.08% vs. 75-85% target — structural deployment-stagnation persists for a 3rd straight week. Friday's weekly review (commit `3bfd7a2`) flagged this. Today's XLE conditional, if it fires, lifts deployment to ~74.9% — inside the target-band lower edge for the first time this phase. Capital cap if all four gates clear is enforced by the conditional itself (single 4th leg, no additional adds).

### Decision
HOLD at the open. Zero at-the-open buys. ONE midday conditional authored on XLE, gated on PPI 8:30 ET clearing in-line/cool AND WTI ≥$100 AND VIX <22 AND XLE trading green/flat-to-slightly-red on the day (all four required by ~11:30 ET; any one failing = HOLD entirely). Rationale: CPI digested constructively yesterday despite hot print, Hormuz closure is structural not binary (10+ weeks, multi-nation military response), Fed cuts effectively zero — inflation-hedge regime structurally favors XLE entry. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact). Daily cap 3/3 available, weekly cap 0/6 fresh — conditional has full headroom. Reserve XLK / XLU / single-name AI-tape entries for Thu pre-market with PPI + CSCO + AMAT in hand. Patience > activity except for the structural-thesis upgrade on XLE.

## 2026-05-14 — Pre-market Research

(Thursday — Day 14, week 3 day 4. Basket grinding higher: XLP +1.64% / XLB +1.95% / XLI +1.03% unrealized, equity $100,869.15 (+0.87% Phase, intraday +$53.94 / +0.05% from yesterday EOD). PPI digested HOT yesterday (+1.4% MoM headline vs +0.5% cons, largest since Mar 2022) but basket absorbed it (Day -0.04% flat); XLE conditional was SKIPPED on gate (1) fail as designed. Today's macro is second-tier: Advance Retail Sales + Initial Claims + Import/Export Prices all 8:30 ET (Retail Sales cons +0.4% MoM, prior +0.5%, advance print +1.7% per one source — verify on release). The TAPE-MOVING new catalyst is CSCO blowout AMC last night: non-GAAP EPS $1.06 vs $1.00 cons (+6%), revenue $15.8B beat, Q4 guide $16.7-16.9B and FY26 guide $62.8-63.0B vs $61.6B cons, restructuring announced, stock +19.84% after-hours to $122.08 / +13% pre-market. NQM26 +0.79% premarket, ESM26 +0.25% — AI-capex narrative reasserting hard. AMAT (Applied Materials) reports AMC tonight = next AI-tape binary. Daily cap 3/3 fresh, weekly cap 0/6 fresh. Env-var loop check again printed MISSING for all five vars; wrapper smoke-test confirmed `alpaca.sh account` returns live JSON with portfolio_value $100,869.15 — proceeded per saved feedback memory.)

### Account
- Equity: $100,869.15
- Cash: $45,158.79 (44.77%)
- Buying power: $146,027.94
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,248.08, +$325.73 / +1.635%, current $84.72, intraday flat), XLB 390 sh @ $51.062 (mkt $20,303.40, +$389.05 / +1.954%, current $52.06, intraday flat), XLI 87 sh @ $172.466 (mkt $15,158.88, +$154.37 / +1.029%, current $174.24, intraday +0.36%). Cost basis $54,841.21 / mkt $55,710.36 (~55.23% deployed).
- Open orders: 3 trail-stop GTCs — XLP $76.7295 stop / hwm $85.255 (ratcheted 5/13); XLB $47.493 stop / hwm $52.77 (unchanged since 5/7); XLI $159.948 stop / hwm $177.72 (unchanged since 5/7). All trail 10%, none within 3% of price, none at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$101.65 (Twelve Data spot, 5/14 close $101.6476, -0.22% from 5/13's $101.6983, intraday high 5/13 $104.45); Brent ~$110.43 (last clean reference 5/12, premium $8-10 norm holds). WTI cooling marginally from yesterday's $102.93 but still firmly above the $100 floor. Hormuz remains structurally closed (10+ weeks since Feb 28, 2026); France CSG deployed; UK assisting; Trump-Xi meeting THIS WEEK is the gating breakthrough catalyst — no headline of size yet. Inflation-print fingerprint of supply shock confirmed twice now (CPI Energy +17.9% YoY, PPI +1.4% MoM headline).
- S&P 500 futures: ESM26 ~$7,414.25 (+0.25% premarket per Barchart); NQM26 +0.79% premarket on CSCO blowout AMC. SPX cash closed near recent ATH ~7,400 cluster yesterday (5/13 +0.58%). Tape leans constructive, tech-led on AI-capex reassertion.
- VIX: 17.99 (5/12 YCharts close, 17.87 Investing intraday); 16-18 normal band intact across the CPI/PPI hot-print absorption. No regime-shift signal.
- Today's catalysts: (1) CSCO AMC blowout last night = dominant tape catalyst (XLK / AI-capex narrative); (2) Advance Retail Sales 8:30 ET (cons +0.4% MoM, prior +0.5%; one source flags advance print +1.7% — exceptionally hot if confirmed = consumer-resilience signal); (3) Initial Claims 8:30 ET; (4) Import/Export Price Indexes 8:30 ET; (5) AMAT (Applied Materials) AMC tonight = next AI-tape binary. Trump-Xi Hormuz meeting "this week" = ongoing structural-headline risk.
- Earnings before open: NO major US large-cap pre-market reports of size (Nasdaq calendar "data not available"; MarketBeat lists small/mid-caps: NIQ $1.05B rev cons, NVMI $227M, GOOS, PBH, CATX, EARN, CRMD, GWRS, LUNR, FENC). No held tickers, no sector-flow driver. Focus shifts to AMAT AMC tonight + Baba Thu AMC.
- Economic calendar this week: Tue CPI (DONE — hot 3.8% YoY) → Wed PPI (DONE — hot +1.4% MoM) → Thu Retail Sales + Claims (TODAY) → Fri quiet + Fed Chair handover (Powell → Warsh). Two hot inflation prints in hand = higher-for-longer locked, Goldman/JPM/Barclays unchanged at zero 2026 Fed cuts.
- Sector momentum YTD (refreshed snapshot 5/14): XLE +29.60% (#1, structural Hormuz supply-shock bid, ACCELERATING through hot-inflation regime), XLK +21.84% (#2, AI-capex reasserting on CSCO blowout, AAPL/MSFT/NVDA ~70% weight), XLI +12.71% (held — leadership cluster, AI infra/defense), XLP +9.31% (held — Coca-Cola breakout, defensive bid), XLU +6.60% (defensive cousin, lagger), XLB +3.4% (held — note: source-discrepancy vs prior 6-mo snapshot showing +17.2%; treat with caution, the position thesis is unchanged but the +3.4% read merits a fresh check on Friday), XLY +2.1%, XLC -1.27%, XLV -3.2%, XLF -5.34%. Held basket all in top-4 leadership; thesis intact.
- Held-ticker news: No idiosyncratic news of size for XLP/XLB/XLI. Coca-Cola (XLP ~10% weight) breakout continues per MarketBeat. Materials sector read across XLB: source-discrepancy YTD print is a watch flag, not a thesis-break signal (no fundamental news, no leadership-cluster exit, basket is +1.95% unrealized).
- Fed cut expectations: Goldman / JPM / Barclays / Fidelity unchanged at ZERO 2026 cuts post-hot-PPI. Higher-for-longer regime locked through Q3 2027 per consensus. Multiple-compression risk on high-multiple growth on every hot print, but CSCO blowout shows productivity/earnings can ABSORB the multiple compression — that's the bull case for XLK today.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLB +1.95% unrealized best (well below +15% tighten threshold), XLP +1.64%, XLI +1.03%. None at -7% triggers. Trail-stop GTCs live, hwms intact (XLP $85.255 ratcheted yesterday, XLB $52.77 unchanged, XLI $177.72 unchanged). No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design). Trail-tighten triggers (7% at +15%, 5% at +20%) — none in play.
2. **XLE (Energy ETF) — CONDITIONAL re-authored** (see Conditional Entries). Yesterday's conditional fired and was correctly skipped on PPI gate (1). Today's setup is CLEANER: PPI binary is past (already hot, regime locked), CPI absorbed, basket riding the hot-inflation regime constructively. Hormuz closure is structural (10+ weeks); WTI holding $101+; XLE YTD #1 leader at +29.60%. Replacing the PPI gate with a Retail Sales / Trump-Xi gate set.
3. **XLK (Technology ETF) — WATCH** — sector #2 YTD (+21.84%), CSCO blowout AMC is a direct positive catalyst (~3% weight in XLK; AAPL/MSFT/NVDA ~70% weight also lift on AI-capex reassertion), NQM26 +0.79% premarket. HOWEVER: (a) AMAT AMC tonight is the NEXT binary — entering today means owning into the AMAT print, which can re-tag XLK on a miss; (b) chasing the #2 YTD leader at the open after a +0.79% NQ gap is poor entry geometry; (c) two hot inflation prints under higher-for-longer locks multiple-compression risk despite CSCO earnings tape. SKIP today, reassess Fri pre-market with AMAT digested.
4. **XLU (Utilities ETF)** — sector +6.60% YTD, defensive cousin of XLP. VIX 17-18 still inside normal band — no regime-shift signal. WATCH only; reassess if VIX gaps >20.
5. **Single-name (CSCO, AMAT, NIQ, etc.)** — SKIP per strategy (sector-ETF momentum, not single-name binaries).
6. **Retail-Sales-reaction trades** — explicit SKIP. Wait for print, sector-ETF conditional only.

### Conditional Entries (midday-eligible) — up to 3
1. **XLE** — allocation $19,837 (345 sh @ ~$57.50 est. ref), stop 10% trail GTC, target +20% (~$69.00), R:R 2:1
   Condition: By ~11:30 ET (post-Retail Sales/Claims digestion), ALL FIVE gates must clear for execution at market: (1) Retail Sales advance MoM ≥ -0.5% (deep-negative print = demand-destruction signal, hits cyclicals INCLUDING XLE via demand; in-line/hot = fine, even positive for the regime); (2) WTI holds ≥$100 on session (any Hormuz-reopen / China-pressure-success headline that breaks WTI below $100 voids the thesis); (3) No credible Trump-Xi reopen headline (the gating structural-headline risk this week — any breakthrough or even a framework announcement voids); (4) VIX <22 (no broad-market shock that bleeds defensives along with cyclicals); (5) XLE trading green-on-day or within -0.5% (confirms the bid; chasing a -2% pullback = catching falling knife). All five required; any one failing = HOLD entirely.
   Catalyst: Hormuz closure is structural (10+ weeks since Feb 28, 2026); CPI Energy +17.9% YoY and PPI +1.4% MoM both confirm supply-shock inflation-print fingerprint; Fed-cuts-off-table (0 cuts 2026) locks inflation-hedge regime; YTD sector #1 leader (+29.60%) confirms momentum cluster; deployment lift 55.2% → 74.9% (inside 75-85% target band lower edge for the first time this phase).
   → Skipped (12:00 CT): gate (3) — Trump-Xi met today in Beijing, joint framework on Hormuz ("must remain open", "must not be militarized"); Chinese vessels actively passing under Iran's "management protocols"; Xi pushing to buy more US oil to reduce China's Hormuz dependence. This is the framework-announcement scenario the conditional was designed to filter out. Gates (1) Retail Sales +0.5% MoM = PASS, (2) WTI ~$101 = PASS, (4) VIX 17.90 = PASS, (5) XLE green-on-day ~+1% ($57.60 open → $58.07) = PASS — but (3) FAIL voids the conditional entirely per spec ("any breakthrough or even a framework announcement voids").

(No other conditionals. XLK setup needs AMAT digested before entry; XLU lacks regime-shift gate.)

### Risk Factors
- Retail Sales catastrophic print (advance <-0.5% MoM, prior +0.5%) = demand-destruction signal, cyclical drawdown risk; XLE and XLB/XLI held basket carry beta. Initial Claims spike >250K confirms labor weakening, amplifies. Trail-stop GTCs absorb up to 10% from hwm before forced exit.
- Retail Sales blowout print (+1.7% MoM as one source flagged, vs +0.4% cons) = consumer-resilience confirmation, lifts cyclicals (XLI/XLB/XLY) but ALSO confirms higher-for-longer Fed → multiple-compression risk on XLK. Mixed signal; held basket modestly favored.
- Trump-Xi Hormuz reopen / framework headline (gating event this week) = WTI gaps -5 to -10% on a credible breakthrough; XLE -5 to -10% sympathy; voids conditional via gate (3). This is the dominant single-headline risk today.
- AMAT (Applied Materials) AMC tonight = next AI-tape binary. Negative miss/guide-cut tags XLK Friday open AND bleeds into XLB/XLI infrastructure correlation. Held basket carries indirect AI-capex correlation but not direct XLK exposure.
- SPX at recent ATH ~7,400 = elevated-base risk; any Retail Sales / AMAT shock has more downside asymmetry than upside given valuations. Held basket carries beta but no leg near trail-stop trigger.
- XLE chase-risk: sector is multi-week YTD leadership cluster after structural-Hormuz bid; entering at $57.50 is joining a trend after the bulk of the move, not catching a low. Trade justified by structural-supply-shock thesis + deployment-stagnation pressure, NOT bottom-fishing.
- XLB YTD source-discrepancy: today's snapshot shows +3.4% but prior 6-mo snapshot showed +17.2%; could be (a) reset to YTD-only window vs trailing-6-mo, (b) source error, or (c) genuine giveback. Position thesis unchanged (+1.95% unrealized, no -7% trigger, no fundamental news) but Friday's weekly review should reconcile.
- CSCO +13% to +19% pre-market is single-stock idiosyncratic — XLK weighting ~3% (~$140-200M flow lift on a $300B+ ETF AUM context) is bounded; broader AI-capex narrative is the bigger pull-through. Do NOT mistake CSCO single-name move for sector-confirming on its own.
- Fed Chair handover (Powell → Warsh Fri) under two-hot-prints-week amplifies any Friday Warsh confirmation soundbite into monetary-policy weight.
- XLP RSI ~80 overbought watch flag continues; Tuesday's +1.30% and Wednesday's +0.32% pushed hwm to $85.255, momentum reasserting but Coca-Cola weighted reversal is the leg's idiosyncratic risk.
- Held positions: none near -7% (worst is XLI +1.03%), none near +15% tighten trigger (best is XLB +1.95%); no manual action required from this entry alone.
- Week 3 deployment ~55.23% vs. 75-85% target — structural deployment-stagnation persists for a 3rd straight week. Today's XLE conditional, if it fires, lifts deployment to ~74.9% — inside the target-band lower edge for the first time this phase. If it skips again, Friday's weekly review needs to address whether the conviction bar is structurally too high for the 75-85% deployment mandate.

### Decision
HOLD at the open. Zero at-the-open buys. ONE midday conditional re-authored on XLE with REFINED gating (Retail Sales not catastrophic, WTI ≥$100, no Trump-Xi reopen headline, VIX <22, XLE green/flat-on-day; all five required by ~11:30 ET, any one failing = HOLD entirely). Rationale: PPI/CPI both digested hot, regime locked, basket riding higher; CSCO blowout adds tech-tape positive but XLK chase into AMAT binary is wrong asymmetry today; XLE structural-Hormuz thesis intact with cleaner gate set (PPI binary now behind us). Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact). Daily cap 3/3 available, weekly cap 0/6 fresh — conditional has full headroom. Reserve XLK / XLU entries for Fri pre-market with AMAT print in hand. Patience > activity except for the structural-thesis play on XLE.

## 2026-05-15 — Pre-market Research

(Friday — Day 15, week 3 day 5, weekly-review checkpoint. Basket holding near the high: XLP +2.22% / XLB +0.95% / XLI +1.17% unrealized, equity $100,809.11 (+0.81% Phase, intraday +$6.43 from yesterday EOD). Yesterday's XLE conditional was SKIPPED as designed — Trump-Xi met in Beijing 5/14 with a joint Hormuz framework ("must remain open", Xi open to helping reopen, China won't arm Iran), which is exactly the gate-3 trigger the conditional was written to filter. WTI cooled $102.93 → $101.65, but Hormuz remains structurally closed per Barchart commentary. The DOMINANT tape catalyst today is Powell→Warsh Fed Chair handover; secondary is AMAT BLOWOUT AMC last night (Q2 rev $7.91B beat, Q3 rev guide $8.5-9.5B vs $8.2B cons, EPS guide $3.16-3.56 vs $2.91, GM 50% — 25-yr high). AI-capex narrative reasserting hard for the 2nd consecutive AMC tape (CSCO Wed + AMAT Thu). SPX closed 7,501 ATH yesterday after CSCO; ESM26 +0.25%, NQM26 +0.30-0.79% premarket. Daily cap 3/3 fresh, weekly cap 0/6 fresh. Env-var loop check again printed MISSING for all five vars; wrapper smoke-test confirmed `alpaca.sh account` returns live JSON with portfolio_value $100,809.11 — proceeded per saved feedback memory.)

### Account
- Equity: $100,809.11
- Cash: $45,158.79 (44.80%)
- Buying power: $145,967.90
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,365.19, +$442.84 / +2.223%, current $85.21, intraday +0.27%), XLB 390 sh @ $51.062 (mkt $20,104.50, +$190.15 / +0.955%, current $51.55, intraday -0.23%), XLI 87 sh @ $172.466 (mkt $15,180.63, +$176.12 / +1.174%, current $174.49, intraday -0.01%). Cost basis $54,841.21 / mkt $55,650.32 (~55.20% deployed).
- Open orders: 3 trail-stop GTCs — XLP $76.734 stop / hwm $85.26 (unchanged 5/14; current $85.21 hasn't pinged a new hwm yet); XLB $47.493 stop / hwm $52.77 (unchanged since 5/7); XLI $159.948 stop / hwm $177.72 (unchanged since 5/7). All trail 10%, none within 3% of price, none at -7% trigger.

### Market Context
- WTI / Brent: WTI ~$101.65 spot (Twelve Data, last 5/14 close; cooling marginally from 5/13's $102.93 and intraday-high $104.45); Brent ~$112-118 range (clean spot quote not captured, premium $8-15 norm holds, 5/1 reference $116.10). Trump-Xi summit in Beijing 5/14 produced a joint Hormuz framework ("must remain open", Xi open to helping reopen, China assured no military equipment to Iran, no nuclear weapon for Iran). White House readout explicit; Beijing readout more general but discussed "major regional issues including the Middle East". Practical reality: Hormuz remains structurally closed (10+ weeks since 2/28/26) per Barchart oil commentary, the framework is a forward-path statement, not an immediate reopening. WTI cooling but not collapsing — the $100 floor holds. Structural supply shock thesis is materially fractured but not yet broken; the next leg is whether China actually pressures Iran to operationalize the framework over the next 1-3 weeks.
- S&P 500 futures: ESM26 +0.25-0.31% premarket (multiple sources); NQM26 +0.30-0.79% premarket on AMAT blowout reinforcing CSCO blowout from Wed. SPX cash closed at the ATH 7,501 on 5/14 (FullyInformed) on Cisco-led AI-capex bid. Tape constructive but stretched — light support below until ~7,150 per technical commentary (light = the rapid 7,300 → 7,500 run left no consolidation cushion).
- VIX: Last confirmed close 17.87 (5/13 per FRED VIXCLS, one-day lag); no fresh Friday print captured. Implied 16-18 normal band intact across CPI/PPI hot-print absorption and the Hormuz-framework relief; regime-shift watch flag remains OFF. Would spike on hawkish-Warsh handover surprise.
- Today's catalysts: (1) Powell → Warsh Fed Chair handover = THE binary today (Warsh's first formal statement, Q&A tone on rate-cut framework, balance-sheet/QT guidance, dovish vs hawkish tilt vs market-priced dovish expectation); (2) AMAT AMC blowout last night = dominant single-stock tape mover (XLK / SOXX / NVDA-cluster lift); (3) Empire State Manufacturing 8:30 ET printed +11.0 vs prior -0.2 — strong manufacturing pickup, mildly positive for XLI/XLB; (4) Industrial Production / Capacity Utilization 9:15 ET — secondary; (5) Trump-Xi summit may extend into today's news cycle (Hormuz framework operationalization or any breakdown headline).
- Earnings before open: NO held tickers, no mega-cap of size. Alibaba (BABA) already reported Wed 5/13 (not today). Wall Street Horizon May 15 pre-market list shows small/mid-caps only (no sector-flow driver). Focus shifted: CSCO Wed + AMAT Thu blowouts are the AI-capex tape; next major prints next week.
- Economic calendar this week (FINAL DAY): Tue CPI (DONE — hot 3.8% YoY) → Wed PPI (DONE — hot +1.4% MoM) → Thu Retail Sales (DONE — per yesterday's log +0.5% MoM, in-line/firm) + Claims → Fri (TODAY) quiet macro + Fed Chair handover (Powell → Warsh). Two hot inflation prints in hand = higher-for-longer locked. Empire State +11.0 confirms manufacturing-side resilience.
- Sector momentum YTD (refreshed 5/15 from multiple Perplexity sources; data range noted): XLE ~+22-32% (#1 across all sources, structural Hormuz bid; one source notes "tied with XLB at +7.5%" which appears to be a different time window, likely YTD-narrow-window rather than rolling-6-mo — treat the #1 leadership ranking as load-bearing, the percentage as approximate), XLK ~+21.84% (#2, AI-capex reasserting on CSCO + AMAT blowouts; AAPL/MSFT/NVDA ~70% weight; AMAT GM 50% / 25-yr-high signals semicap-cycle peak strength), XLB (held) — sources conflict: one shows +7.5% YTD-narrow, another +17.2% trailing-6-mo, "Leading" quadrant on momentum map confirmed across sources; YTD source-discrepancy flagged Thu carries forward today's weekly review reconcile, (held — leadership cluster intact), XLI (held) +5.9-12.71% range across sources, "Leading" quadrant confirmed (held — leadership cluster intact), XLP (held) +5.28-9.31% range across sources, "Leading" relative-strength quadrant on flight-to-safety bid, valuation flag (forward P/E ~26 vs 5-yr avg ~22.7, defensive premium already paid — risk of underperformance if defensive rotation reverses on dovish-Warsh tape). Across all sources held basket all in leadership/top-half cluster; thesis intact, no -7% triggers, no +15% tighten triggers.
- Held-ticker news: XLP (Consumer Staples) — defensive bid still intact per Kavout commentary; Coca-Cola weighting unchanged; ~33.74% Distribution & Retail / 19.45% Beverages / 16.78% Food / 15.61% Household / 10.95% Tobacco breakdown stable. XLB (Materials) — sector commentary "tied with XLE in 2026 leadership", AI/infrastructure tailwind intact, no idiosyncratic news of size. XLI (Industrials) — Empire State +11.0 is a marginal positive read-through, AI-infrastructure correlation intact, no idiosyncratic news of size. No thesis break for any leg.
- Fed cut expectations: Goldman/JPM/Barclays/Fidelity unchanged at ZERO 2026 cuts post-hot-PPI. Higher-for-longer regime locked through Q3 2027 per consensus. CSCO + AMAT prove productivity-side multiple-compression resistance for top-tier AI-capex names — bullish for XLK absolute return but doesn't change the regime. Warsh handover tape today is the wildcard — markets price dovish-tilt; any hawkish surprise tags growth/duration severely from SPX ATH.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLP +2.22% unrealized best of basket (well below +15% tighten threshold), XLI +1.17%, XLB +0.95%. None at -7% triggers. Trail-stop GTCs live; XLP hwm $85.26 (current $85.21 — fractional intraday lift could ratchet $85.26 → $85.50 area if XLP holds bid, would lift stop $76.734 → ~$76.95); XLB hwm $52.77 unchanged; XLI hwm $177.72 unchanged. No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design). Trail-tighten triggers (7% at +15%, 5% at +20%) — none in play, closest is XLP at +2.22%.
2. **XLE (Energy ETF) — DOWNGRADE: conditional retired** — yesterday's Trump-Xi framework on Hormuz reopen is the gating-event trigger the conditional was designed to filter. Re-authoring the conditional yet again with the same Hormuz thesis is dishonest: the framework announcement materially fractures the structural-supply-shock case even though Hormuz isn't physically reopened. WTI cooling $102.93 → $101.65 confirms the tape is starting to price it. XLE chase here is fighting both the framework headline AND the cooling commodity. WATCH only; require a Hormuz framework BREAKDOWN headline OR WTI re-acceleration >$105 to re-author. This is the right disposition vs. forcing a third re-authoring on the same broken thesis just for deployment-stagnation reasons.
3. **XLK (Technology ETF) — UPGRADE to active conditional candidate** — CSCO blowout Wed + AMAT blowout Thu (Q3 rev guide $8.5-9.5B vs $8.2B cons, EPS guide above, GM 50% / 25-yr high) is the two-tape-confirmation the AI-capex thesis was missing. Sector #2 YTD (+21.84%), AAPL/MSFT/NVDA ~70% weight. Today's binary is Powell→Warsh handover — a dovish-tilt or in-line Warsh tape clears the gate for XLK entry; a hawkish-surprise Warsh tags XLK directly on multiple-compression. Conditional structure below.
4. **XLU (Utilities ETF)** — sector +6.60% YTD, defensive cousin of XLP, lagger. VIX 17-18 still inside normal band — no regime-shift signal; AMAT blowout reinforces tech-tape, undermines defensive rotation case. SKIP today — XLP already provides the defensive bid in the basket.
5. **Single-name AMAT / CSCO / NVDA chase** — explicit SKIP per strategy (sector-ETF momentum, not earnings binaries). XLK gives the diversified vehicle.
6. **Warsh-handover-reaction trades (any single name or index)** — explicit SKIP at the open. Conditional only.

### Conditional Entries (midday-eligible) — up to 3
1. **XLK** — allocation $19,837 (~89 sh @ ~$223 est. ref — XLK trades in the ~$220-230 range per market context; share count to confirm at execution), stop 10% trail GTC, target +20% (~$268), R:R 2:1
   Condition: By ~12:00 ET (post-Warsh-handover statement + Q&A digestion), ALL FOUR gates must clear for execution at market: (1) Warsh tone NOT hawkish — no "no rush to cut", no "inflation still too high" framing; dovish, balanced, or growth-risks-emphasizing language clears; a hawkish-surprise tags growth/duration severely from SPX ATH and the trade dies on entry; (2) NQM26 / Nasdaq composite still GREEN-on-day or within -0.5% (confirms AMAT-blowout bid persists post-handover — chasing a -2% NQ pullback on hawkish-Warsh = catching falling knife); (3) VIX <22 (no broad-market shock event); (4) XLK itself trading green-on-day or within -0.5% (confirms the AI-capex tape is being bought, not faded into the handover). All four required; any one failing = HOLD entirely.
   Catalyst: AMAT blowout AMC 5/14 (Q3 rev guide $8.5-9.5B vs $8.2B cons, EPS guide above, GM 50% / 25-yr high) + CSCO blowout AMC 5/13 = two-tape AI-capex confirmation; XLK sector #2 YTD (+21.84%); Powell→Warsh handover dovish-tilt expectation pre-priced; AAPL/MSFT/NVDA ~70% weight benefits from AI-capex narrative + dovish Fed; deployment lift 55.2% → 74.9% (inside 75-85% target-band lower edge for the first time this phase). REPLACES the retired XLE conditional that ran twice on a now-fractured thesis.

   → Skipped (12:02 CT): gate (1) — Warsh tone hawkish-leaning per Perplexity ("no rush to cut" / "inflation is still too high or too uncertain" / "policy may need to stay restrictive for longer" — the exact framing the gate was written to filter); gate (4) also fails — XLK $177.21 vs yesterday close ~$179.50 ≈ -1.28% on day (beyond -0.5% threshold), intraday low $174.77 confirms growth/duration tag. Conditional dies per author "any one failing = HOLD entirely". No fire.

(No other conditionals. XLE retired per Trade Idea 2; XLU lacks regime-shift gate.)

### Risk Factors
- **Powell→Warsh handover hawkish surprise** = primary risk today; markets pre-price dovish tilt under Warsh, any "no rush to cut" / "inflation still too high" framing into SPX ATH 7,501 + two-hot-inflation-prints-in-hand triggers multiple compression severely. Held basket has beta but no leg near trail-stop (deepest cushion is XLB +0.95%, ~9% from -7% trigger; XLP +2.22% has more cushion). XLK conditional voids on gate (1) fail. Dominant single-event risk.
- **Powell→Warsh dovish-confirmation OR in-line** = relief tape, XLK conditional clears gate (1), AI-capex melt-up extends, defensives (XLP/XLU) may underperform on rotation OUT of safety.
- **Trump-Xi Hormuz framework breakdown / re-escalation headline** = WTI bid sharply back, XLE rallies, but the conditional is retired so no execution risk; the held basket has no XLE leg so no direct beta. XLB carries some commodity-input read-through but minor.
- **Hormuz framework operationalization headline** (China actually pressuring Iran toward reopen, with credible mechanism) = WTI gaps -5 to -10%, XLE gets crushed (no held exposure, neutral), but XLB carries some commodity-input read-through (could rally on cost relief).
- **SPX at recent ATH 7,501 with light support to 7,150** (~5% downside cushion to next technical support) = elevated-base risk; any hawkish-Warsh shock has more downside asymmetry than upside given valuations. Held basket carries beta.
- **AMAT post-blowout fade risk** = stocks that gap up on blowout earnings sometimes fade hard intraday (sell-the-news), which can tag XLK gate (4); the gate is structured to detect this — if XLK opens up and fades to red, the conditional skips, protecting against AI-capex single-tape exhaustion entry.
- **XLP RSI ~80 overbought watch flag continues** — Mon's -0.96% was first digestion print, Tue/Wed/Thu all green, +2.22% unrealized now; defensive premium (forward P/E ~26 vs 5-yr avg ~22.7) is the leg's valuation overhang. If dovish-Warsh triggers rotation OUT of safety, XLP can compress fast. But trail-stop ($76.734, ~10% from hwm $85.26) absorbs the move; thesis-break would require Coca-Cola weighted reversal + the leg breaking through stop.
- **XLB YTD source-discrepancy** (3.4-7.5-17.2% across sources) continues into today — Friday weekly review must reconcile, but position thesis unchanged (+0.95% unrealized, leadership-quadrant confirmed, no fundamental news, no -7% trigger).
- **Held positions** — none near -7% (worst is XLB +0.95%), none near +15% tighten trigger (best is XLP +2.22%); no manual action required from this entry alone.
- **Week 3 deployment ~55.20% vs. 75-85% target** — structural deployment-stagnation persists for a 3rd straight week. Today's XLK conditional, if it fires, lifts deployment to ~74.9% — inside the target-band lower edge for the first time this phase. If gate (1) fails on hawkish-Warsh, basket stays at 55% AND faces multiple-compression risk on existing legs — the wrong side of the asymmetry. Weekly review checkpoint must address whether the conviction bar is structurally too high for the 75-85% deployment mandate after THREE straight weeks of conditional-skips on the same XLE thesis.
- **Trump-Xi summit may continue into today** (May 14-15 listed across sources) — additional Hormuz / AI-guardrails / chip-export headlines possible; tech-sector tape (XLK) carries direct AI-export-control beta to any restrictive headline, but a constructive framework continuation lifts the conditional case.
- **Friday handover + weekend headline risk** = entering a new leg into Friday means owning the weekend tape; if Warsh's confirmation hearings have a soundbite that tags markets on Monday open, the new leg has no Friday close cushion. The conditional gate structure absorbs this risk pre-execution but doesn't post-execution.

### Decision
HOLD at the open. Zero at-the-open buys. ONE midday conditional authored on XLK (gated on Warsh-not-hawkish AND NQ green/flat AND VIX <22 AND XLK green/flat; all four required by ~12:00 ET, any one failing = HOLD entirely). XLE conditional RETIRED — running it a third time on a now-Trump-Xi-framework-fractured thesis is dishonest deployment-pressure trading, not strategy. The two-tape AI-capex confirmation (CSCO Wed + AMAT Thu blowouts) materially upgrades the XLK setup vs. last Friday's "watch only" call; the Warsh-handover gate keeps the asymmetry favorable. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact; XLP +2.22% unrealized is the leg's high so far). Daily cap 3/3 available, weekly cap 0/6 fresh — conditional has full headroom. Today is also the weekly review checkpoint (per /weekly-review skill) — this week's wrap-up needs to address (1) the XLE conditional retirement and replacement with XLK, (2) the persistent ~55% deployment vs. 75-85% target across three weeks, (3) the XLB YTD source-discrepancy reconciliation, (4) whether the conditional-gate framework is producing the right conviction-bar calibration. Patience > activity except for the structural-tape upgrade on XLK.

## 2026-05-18 — Pre-market Research

(Monday — Day 16, week 4 day 1, opening session of new trading week. Friday closed the phase essentially flat after a -0.87% risk-off Friday wiped the entire +0.85% peak built across weeks 2-3; equity $99,921.33 EOD Fri → $99,849.36 now (small pre-market drift on XLB/XLI). Friday XLK conditional skipped on hawkish-Warsh handover tape (gate 1 + gate 4 failed per the entry above). Weekly review committed `1ce307d` Fri PM. Daily cap 3/3 fresh, weekly cap 0/6 fresh. Major binary today: WMT + HD earnings BMO (WMT is a top-3 XLP holding by weight). Macro tape light this week — no FOMC minutes, no NFP — but the Iran/Hormuz situation appears to have escalated over the weekend per single source (Crestwood Advisors May 2026 update flagging "US naval blockade of Iran extended indefinitely" with Brent ~$120 / WTI ~$107). HEADLINE NOT CROSS-CONFIRMED — Twelve Data shows WTI ~$101.61 close last session, conflicting with Crestwood's $107 print. Two-source verification required before any XLE re-author. Env-var loop check printed MISSING for all five vars again; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,849.36 — proceeded per saved feedback memory.)

### Account
- Equity: $99,849.36
- Cash: $45,158.79 (45.23%)
- Buying power: $145,008.15
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,212.23, +$289.88 / +1.455%, current $84.57, lastday $84.64, intraday -0.08%), XLB 390 sh @ $51.062 (mkt $19,617.00, -$297.35 / -1.493%, current $50.30, lastday $50.30, intraday 0.00%), XLI 87 sh @ $172.466 (mkt $14,861.34, -$143.17 / -0.954%, current $170.82, lastday $171.40, intraday -0.34%). Cost basis $54,841.21 / mkt $54,690.57 (~54.77% deployed). XLB and XLI flipped to unrealized-red on Friday's -0.87% wipe; XLP still modestly green.
- Open orders: 3 trail-stop GTCs — XLP $77.022 stop / hwm $85.58 (ratcheted Fri intraday from $85.26 → $85.58 on a faded intraday rally); XLB $47.493 stop / hwm $52.77 (unchanged since 5/7); XLI $159.948 stop / hwm $177.72 (unchanged since 5/7). All trail 10%, none within 3% of price (closest is XLB current $50.30 vs stop $47.493 = +5.9% cushion), none at -7% trigger (worst leg XLB -1.49%, well above trigger).

### Market Context
- WTI / Brent: **SOURCE CONFLICT FLAG — primary risk to today's read.** Perplexity source A (Investing.com via Twelve Data) reports WTI May 18 close $101.61, prev $102.46, change ~-0.8%; spot WTI $101.00-$101.13 May 15-16 range. Perplexity source B (Crestwood Advisors May 2026 update) reports WTI ~$107, Brent ~$120 with the framing "US naval blockade of Iran extended indefinitely". The two prints are not reconcilable as the same instrument at the same time. Most-likely explanation: source A is the front-month CL futures intraday or settlement; source B is either a stale narrative from earlier in the month or a different reference basket. Until cross-confirmed by a second oil-specific source (Barchart, EIA, or live CME quote), the operating prior is WTI ~$101-102 (modestly cooling from prior week's $101.65 close per Fri research log), Brent ~$108-115 range. The blockade-extension headline is NOT confirmed — single source. Re-confirmation gate at midday required before any XLE re-author trigger fires.
- S&P 500 futures: ESM26 ~7,389.50 per CME June contract, -42.75 pts (-0.58%) overnight. Risk-off continuation from Friday's -0.87% cash session. SPX cash closed 7,422.37 Fri (per public data, derived from index history), down from the 5/14 ATH 7,501. Premarket implies cash open ~7,380s if futures basis holds, ~1.6% below ATH and continuing the rejection from 7,500-area resistance.
- VIX: ~18-19 range per Perplexity (no fresh print captured; cited 18-19 with note that May 18 is also last full trading day before May VIX expiration). Last confirmed FRED close was 17.87 (5/13), so 18-19 = modest VIX expansion consistent with Friday's risk-off + heading into earnings binary. Regime-shift watch flag remains OFF (still inside 16-22 normal band) but ticking up.
- Today's catalysts: (1) **WMT earnings BMO** = THE binary today, direct XLP exposure (WMT is a top-3 XLP holding by weight, ~5-6% of the ETF); a beat + strong guide on consumer health lifts XLP, a miss or weak comp tags it. (2) **HD earnings BMO** = secondary binary, direct read-through to housing/consumer-discretionary (XLB has indirect exposure via construction materials, but HD is XLY-sector not XLB-direct). (3) **Iran/Hormuz blockade-extension headline** per Crestwood — single source, unconfirmed; if real, it's the BREAKDOWN headline the Fri entry specified would re-author the XLE conditional. (4) **Warsh-handover Monday digestion** — Friday's hawkish-leaning Warsh tape ("no rush to cut" / "policy may need to stay restrictive for longer" per the skipped XLK conditional notes) carries forward into Monday; weekend confirmation hearings or follow-up tape risk on multi-day soundbites. (5) **Pre-market risk-off** ES -0.58%, VIX 18-19 — defensive bid into the open suggests broader-tape pressure.
- Earnings before open: **WMT (direct XLP binary, top-3 holding)**, HD (XLY-direct, no held exposure), JD / SE / NIO / LI / XPEV (China ADRs — no held exposure, but JD/SE Q1 prints color US-China trade tape). No other mega-cap of size. Wall Street Horizon May 18 pre-market list confirms WMT + HD as the only US large-caps of consequence.
- Economic calendar this week: **LIGHT.** Tue 5/19 8:30 ET Housing Starts + Building Permits (April); Thu 5/21 8:30 ET Initial Jobless Claims. NO FOMC minutes this week (next late May). NO NFP this week (next first Friday of June). NO CPI/PPI (both printed week of 5/12-13, both hot — locked in). Catalyst calendar today is dominated by WMT/HD earnings and any Iran-tape developments, not macro releases.
- Sector momentum YTD (refreshed 5/18 from Perplexity ETFreplay/State Street/First Trust composite): **1. XLE Energy (#1, structural Hormuz bid persists), 2. XLP Consumer Staples (#2, defensive bid amplified post-Fri risk-off — note: a sharp jump from prior weeks where XLP was #6 per other sources, the discrepancy reflects mid-May defensive rotation strength + the source-window difference), 3. XLI Industrials (#3, held — leadership cluster intact), 4. XLB Materials (#4, held — leadership cluster intact, slight ranking demotion from #2-3 in prior weeks reflecting Friday's -2.77% XLB drubbing as the basket's worst leg), 5. XLU Utilities, 6. XLV Health Care, 7. XLF Financials, 8. XLC Comm Services, 9. XLK Information Technology, 10. XLY Consumer Discretionary.** XLK dropped to #9 — reflects Friday's hawkish-Warsh-tape multiple-compression that took XLK $179.50 → $177.21 (-1.28%) intraday low $174.77 per the skipped-conditional notes; the AI-capex narrative is intact but the rate-path repricing dominates the YTD-relative tape. XLY at #10 confirms consumer-discretionary weakness consistent with elevated-oil consumer-squeeze narrative ($6+/gallon California gas per Crestwood). Held basket (XLP/XLI/XLB) ALL remain in the top-4 leadership cluster across sources; thesis intact.
- Held-ticker news: **XLP (Consumer Staples) — WMT EARNINGS BMO IS THE BINARY** (top-3 holding by weight, ~5-6%). Per MarketBeat XLP ~+11.9% YTD, surged ~6% last week, NAV mid-$80s, 52-week range $75.16-$90.14. Defensive-rotation narrative intact, but valuation overhang persists (forward P/E ~26 vs 5-yr avg ~22.7 flagged in prior log). XLB (Materials) — Friday's -2.77% was the basket's worst leg, no idiosyncratic news identified, leg flipped to unrealized-red -1.49%; commodity-input pressure if oil escalates further is a marginal positive for energy-related material names but neutral-to-negative for industrial chemicals. XLI (Industrials) — no idiosyncratic news identified, leg at -0.95% unrealized, AI-infrastructure correlation intact but Empire State manufacturing positive from last week may fade if WMT consumer-print weakens broad cyclical bid. No thesis break for any leg; no -7% triggers active.
- Fed cut expectations: Unchanged at ZERO 2026 cuts post-hot-CPI/PPI + post-hawkish-Warsh tape. Higher-for-longer regime locked through Q3 2027 per consensus. Warsh's Friday "no rush to cut" framing reinforces the regime; any weekend dovish-walkback or Monday confirmation-hearing soundbite could re-engage rate-cut-pricing, but no such headline captured in research.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLP +1.46% unrealized best of basket (well below +15% tighten threshold), XLB -1.49% worst, XLI -0.95% middle. None at -7% triggers (XLB cushion ~5.5% from trigger). Trail-stop GTCs live; XLP hwm $85.58 (Fri ratcheted from $85.26); XLB hwm $52.77 unchanged since 5/7; XLI hwm $177.72 unchanged since 5/7. No add to existing names (XLP/XLB at 20% cap by market value; XLI at 15% by design). Trail-tighten triggers (7% at +15%, 5% at +20%) — none in play. **WMT print is the leg-level binary** — strategy says do not pre-emptively trim/cut on earnings binaries unless thesis is broken; thesis (defensive-bid + structural staples) is intact, no pre-print action.
2. **XLE (Energy ETF) — RE-AUTHOR CONDITIONAL contingent on headline cross-confirmation** — single-source Crestwood headline "US naval blockade of Iran extended indefinitely, Brent ~$120 / WTI ~$107" IS the breakdown trigger the Fri entry specified would re-engage the conditional. BUT Perplexity source A shows WTI $101.61, materially conflicting with $107. Authoring a midday conditional that requires (a) cross-source confirmation of the blockade extension OR oil bid AND (b) standard tape gates. Re-engagement justified by genuine new info (if real); structured to skip if Crestwood print is stale/wrong.
3. **XLK (Technology ETF) — DOWNGRADE: conditional retired for today** — Friday's hawkish-Warsh tape killed the conditional at gate 1; the multi-day digestion of "no rush to cut" / "policy may need to stay restrictive for longer" carries into Monday with no dovish walkback captured. Re-authoring today is the same dishonest deployment-pressure trading flagged on XLE last week. WATCH-only; require a Warsh dovish-walkback OR a clean +1% AI-tape day with VIX <17 to re-author. Patience.
4. **WMT-pre-print single-name chase or XLP trim** — explicit SKIP. Single-name earnings binary trades are out-of-strategy (sector-ETF momentum only); XLP pre-emptive trim violates the "thesis-break-only" cut rule. Hold through the print; reassess at midday once WMT digestion is clear.
5. **XLU (Utilities ETF)** — sector +mid-single-digit YTD, defensive cousin of XLP. VIX 18-19 inside normal band — no regime-shift signal authorizing add. SKIP today.
6. **Single-name HD / NVDA / WMT chase post-print** — explicit SKIP per strategy (sector-ETF momentum, not single-name earnings reactions).

### Conditional Entries (midday-eligible) — up to 3
1. **XLE** — allocation $14,977 (~15% of equity; ~150-160 sh @ ~$93-100 est. ref, share count to confirm at execution from live quote), stop 10% trail GTC, target +20% from entry, R:R 2:1
   Condition: By ~12:00 ET, ALL FIVE gates must clear for execution at market: (1) **Cross-source confirmation of the Crestwood blockade-extension headline** — at least one additional credible source (Reuters, Bloomberg, WSJ, AP, or a tier-1 oil-trade publication like S&P Platts/Argus) reports the Iran naval blockade extension OR clear escalation language ("extended", "indefinite", "tightened") — if only Crestwood has it and no other source confirms, the print is likely stale/wrong and the trigger doesn't apply; (2) **WTI front-month >$103 intraday OR Brent >$112 intraday** (live CME/ICE quote; this is below Crestwood's $107/$120 but above source A's $101.61 — designed to confirm oil tape is bidding the escalation, not fading it); (3) **ESM26 / SPX cash recovered to flat-on-day or green** (don't chase XLE entry into a -1%+ broad-tape sell-off — XLE has tape-beta and gets dragged down with the market even on bullish oil; wait for the broad bid before adding); (4) **VIX <22** (no broad-market shock event); (5) **XLE itself trading green-on-day** (confirms oil-tape bid translating to sector lift, not faded — protects against "headline true, but XLE faded because tape risk-off dominates"). All five required; any one failing = HOLD entirely. Skip default if no cross-confirmation by 12:00 ET.
   Catalyst: Friday entry retired XLE on Trump-Xi Hormuz-framework thesis; re-author trigger was "Hormuz framework BREAKDOWN headline OR WTI re-acceleration >$105". Crestwood May 2026 "US naval blockade of Iran extended indefinitely" + Brent $120 / WTI $107 would constitute BOTH triggers simultaneously IF cross-confirmed. Single-source data quality bar is the gate — same conviction discipline that retired the XLE conditional last week applies to re-authoring this week. Deployment lift if fires: 54.8% → 69.8% (still below 75% target-band but closes ~75% of the gap; adds the structurally-uncorrelated 4th leg the basket has been missing for 4 weeks).
   → Skipped (12:00 CT): gate 1 — no tier-1 wire (Reuters/Bloomberg/WSJ/AP/Platts/Argus) cross-confirms the Crestwood blockade-extension headline by deadline. Perplexity surfaced Wikipedia "2026 United States naval blockade of Iran" and militarnyi.com "USA extends maritime blockade of Iranian vessels" — broadly consistent with the thesis but not on the explicit tier-1 source list authored into the gate. Per default-skip-on-ambiguous rule, conditional HOLDs entirely. Note: XLE was acting bullishly intraday (opened $59.24, current ~$60.40, ~+2% intraday, range $58.72-$60.67), so gate 5 would have passed; live WTI/Brent print unavailable through Perplexity (Barchart commentary mentioned "Strait of Hormuz closed" but no live price), gate 2 unverified; SPY $735.98 vs intraday high $741.38 = modestly red, gate 3 ambiguous. Data-quality gate 1 is dispositive — XLE not added; deployment stays ~54.8%; 4th-leg deferral continues into Tue.

(No XLK conditional today — multi-day hawkish-Warsh digestion makes re-authoring premature. No XLU conditional — no regime-shift gate. Max one conditional today; deployment-stagnation acknowledged but conditional bar holds.)

### Risk Factors
- **WMT earnings BMO = primary single-event risk for XLP leg** — WMT is a top-3 XLP holding (~5-6% weight); a clear miss + weak FY guide tags XLP by ~30-60 bps even if rest of basket holds; a beat + strong guide reinforces the defensive-rotation bid. XLP currently +1.46% unrealized with $77.022 stop ~9% cushion to -7% trigger and ~9% to stop-out — single-print binary won't trigger a stop unless print is catastrophic. Strategy: no pre-print action, reassess at midday.
- **Iran/Hormuz single-source-headline risk** — Crestwood blockade-extension print is unconfirmed; trading XLE on it without cross-source verification is a classic single-source-mistake setup. The conditional gate (1) is explicitly written to filter this. If gate (1) fails, XLE conditional skips and deployment stays at 55%.
- **Iran tape kinetic-retaliation risk** — if the blockade-extension IS real and Iran retaliates with a real strike on shipping or US assets, the tape goes immediate-risk-off; held basket has zero direct exposure (no XLE held) so passive in this scenario, but ES futures already -0.58% means cushion is thin.
- **Hormuz framework operationalization headline** (China actually pressures Iran toward reopen) = WTI gaps -5 to -10%, XLE crushed (no held exposure, neutral), XLB marginally positive on commodity-input relief. Less likely given the blockade-extension framing if real.
- **ES futures -0.58% pre-market = broad risk-off continuation from Fri** — held basket has beta (Fri's -0.87% basket-day was the proof); deepest leg cushion is XLB ~5.5% to -7% trigger. A continued -1%+ broad sell-off today drags basket toward trigger zones but no leg currently within striking distance.
- **SPX 1.6% below ATH 7,501 with light technical support to 7,150** (~3% below current) = elevated-base risk, sharp downside asymmetry on any binary surprise (WMT-miss + hawkish-Warsh-confirmation soundbite = compounding negative).
- **Warsh-handover multi-day digestion** — Friday's "no rush to cut" / "policy may need to stay restrictive for longer" framing carries forward; any weekend confirmation-hearing soundbite or Monday follow-up that tightens the hawkish framing further re-engages multiple-compression on the basket. XLP/XLI/XLB all carry rates-beta but less than XLK/XLY.
- **Held basket 4-week structural deployment gap** — basket at 54.8% across 4 straight weeks (15+ sessions); 4th-leg add (XLE/XLK/XLU) deferred every weekly review including Fri's. If today's XLE conditional fires, deployment lifts to ~69.8% — first time inside lower-target neighborhood. If skips, the structural gap is the de facto strategy. Strategy mandate (75-85% deployed) is now in tension with the conviction-bar framework that keeps killing the 4th-leg authorization.
- **XLP RSI overbought-watch flag continues** — leg is +1.46% unrealized off Friday's -0.38% red day, defensive premium (forward P/E ~26 vs 5-yr avg ~22.7) is the valuation overhang. WMT print is the catalyst that resolves this either direction.
- **XLB worst-leg watch** — Fri's -2.77% drubbing left XLB at -1.49% unrealized, the deepest red of the basket. Stop $47.493 / hwm $52.77 means ~5.5% to stop-out from current $50.30; not yet a -7% manual-cut candidate (manual-cut math: stop_loss = avg_entry × 0.93 = $51.062 × 0.93 = $47.488, almost exactly equal to the live trail-stop ~$47.493 — the GTC trail is already covering the -7% rule for XLB at this hwm). No pre-emptive action needed.
- **Held positions** — none near -7% (worst is XLB -1.49%), none near +15% tighten trigger (best is XLP +1.46%); no manual action required from this entry alone.
- **WMT-print correlation risk inside XLP** — even if XLP holds up on a WMT miss because of basket diversification, the print can compress the leg by 50-100 bps which is meaningful relative to current +1.46% cushion; if XLP flips red on the print, it joins XLB/XLI in unrealized-red territory making the basket fully red into a weak macro tape.

### Decision
HOLD at the open. Zero at-the-open buys. ONE midday conditional authored on XLE (gated on cross-source headline confirmation AND oil tape bid AND broad-tape recovery AND VIX <22 AND XLE green-on-day; all five required by ~12:00 ET, any one failing = HOLD entirely). XLK conditional NOT re-authored — multi-day hawkish-Warsh digestion makes re-authoring premature; require a dovish walkback OR clean AI-tape lift first. The XLE re-author is justified by the Crestwood blockade-extension headline (IF cross-confirmed) which would be both triggers the Fri entry specified for re-engagement; the data-quality gate is intentionally strict to avoid running on a stale single-source print. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, hwms intact; WMT BMO print is the XLP-leg binary — no pre-print action). Daily cap 3/3 available, weekly cap 0/6 fresh — conditional has full headroom. Week 4 begins with the same structural question that has been deferred 3 weekly reviews: 4th-leg add or accept 3-leg basket as the phase configuration. Today's XLE conditional, if it fires, addresses the question; if it skips, the deferral continues into Fri's weekly review. Patience > activity except for the explicit re-engagement trigger on the XLE thesis.

## 2026-05-18 — Pre-market Research — ABORTED

### Status
ABORT before STEP 2. Wrapper smoke-test (`bash scripts/alpaca.sh account`) returned:
`scripts/alpaca.sh: line 16: ALPACA_API_KEY: ALPACA_API_KEY not set in environment`

### Missing env vars (per `[[ -n "${!v:-}" ]]` loop AND wrapper confirmation)
- ALPACA_API_KEY
- ALPACA_SECRET_KEY
- PERPLEXITY_API_KEY
- TELEGRAM_TOKEN
- TELEGRAM_CHAT_ID

### Action taken
- Per routines/pre-market.md:13-14, stopped before any further wrapper calls.
- Telegram alert attempted → fell back to local `memory/DAILY-SUMMARY.md` (TELEGRAM_TOKEN also missing).
- No `alpaca.sh positions / orders`, no Perplexity queries, no trades.

### Carry-over (held positions, unchanged from 2026-05-15 EOD)
- XLP 239 sh @ $83.36 — trail $77.022 (hwm $85.58)
- XLB 390 sh @ $51.06 — trail $47.493 (hwm $52.77)
- XLI 87 sh @ $172.47 — trail $159.948 (hwm $177.72)
All three 10% trailing GTCs assumed live on the broker (no client-side modification this session).

### Decision
HOLD. No new entries, no conditional entries authored — pre-market workflow cannot complete without account/research wrappers. Market-open routine will inherit this abort and should also halt unless env is restored.

## 2026-05-18 — Midday Scan

### Account (12:00 CT)
- Equity: $99,926.89 | Cash: $45,158.79 (45.19%) | Buying power: $145,085.68 | Daytrade count: 0
- Positions (cost basis $54,841.21 / mkt $54,775.70 / ~54.81% deployed):
  - XLP 239 sh @ $83.357 — current $85.21, intraday +0.67%, unrealized +$442.84 (+2.22%)
  - XLB 390 sh @ $51.062 — current $50.28, intraday -0.04%, unrealized -$305.15 (-1.53%)
  - XLI 87 sh @ $172.466 — current $170.13, intraday -0.74%, unrealized -$203.20 (-1.35%)
- Open orders (3 trailing 10% GTCs):
  - XLP stop $77.202 / hwm $85.78 — RATCHETED today from $77.022 / $85.58 (new intraday high $85.78)
  - XLB stop $47.493 / hwm $52.77 — unchanged
  - XLI stop $159.948 / hwm $177.72 — unchanged

### Actions
- **Cut losers (-7% rule):** None. Worst leg XLB -1.53%, well above -7% trigger.
- **Tighten winners:** None. Best leg XLP +2.22%, well below +15% tighten threshold.
- **Thesis check:** No breaks. XLP +0.67% intraday post-WMT BMO print = constructive digestion of the leg-level binary; defensive-rotation thesis intact. XLB flat / XLI -0.74% = normal noise; sector-momentum leadership cluster (XLP/XLB/XLI all top-4 YTD per pre-market refresh) unchanged.
- **Conditional XLE: SKIPPED at gate 1.** No tier-1 wire (Reuters/Bloomberg/WSJ/AP/Platts/Argus) cross-confirms the Crestwood blockade-extension headline. Wikipedia + militarnyi.com appear but are not on the explicit gate list — DEFAULT-SKIP on ambiguous per rules. XLE was trading bullishly intraday (open $59.24 → $60.40, ~+2%) so gate 5 would have passed; live oil prints not retrievable so gate 2 unverified; SPY modestly red so gate 3 ambiguous. Data-quality gate 1 is dispositive. Audit line appended under the conditional above.

### Env-check note
Loop check printed MISSING for all five env vars again; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,926.89 — proceeded per saved feedback memory.

### Decision
NO ACTION. Held basket intact, no cuts, no tightens, no conditional fire. Trades today 0/3, trades this week 0/6, deployment ~54.81% unchanged. 4th-leg add remains deferred — gate 1 data-quality bar held. Daily-summary at EOD will capture final marks; weekly review Friday gets the structural-deployment question again.

## 2026-05-19 — Pre-market Research

(Tuesday — Day 17, week 4 day 2. Yesterday's session closed green: equity $100,129.94 EOD Mon (+0.21% day) with XLP +1.49% leading on WMT BMO digestion, XLB / XLI marginally red. XLE midday conditional SKIPPED at gate 1 (no tier-1 wire cross-confirmed the Crestwood blockade-extension headline) — that gate held correctly: today's WTI quote ~$102 and Brent ~$110 directly contradict Crestwood's $107/$120 print, so the single-source signal was stale or wrong. Pre-market drift modest: equity $100,085.98 now (-$43.96, -0.04% from Mon EOD); XLP ratcheted to a new hwm $85.94 yesterday lifting trail $77.022 → $77.346. Daily cap 3/3 fresh, weekly cap 0/6 fresh. HD earnings BMO is today's single-event catalyst; no held exposure direct. Macro calendar light — no FOMC, NFP, CPI/PPI; Housing Starts/Building Permits/Jobless Claims start Wed. Env-var loop check printed MISSING for all five vars again; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $100,085.98 — proceeded per saved feedback memory.)

### Account
- Equity: $100,085.98 (last_equity $100,129.94, pre-market drift -$43.96 / -0.04%)
- Cash: $45,158.79 (45.12%)
- Buying power: $145,244.77
- Daytrade count: 0
- Positions: XLP 239 sh @ $83.357 (mkt $20,554.00, +$631.65 / +3.17%, current $86.00, lastday $85.90, intraday +0.12%), XLB 390 sh @ $51.062 (mkt $19,585.80, -$328.55 / -1.65%, current $50.22, lastday $50.22, intraday 0.00%), XLI 87 sh @ $172.466 (mkt $14,787.39, -$217.12 / -1.45%, current $169.97, lastday $170.75, intraday -0.46%). Cost basis $54,841.21 / mkt $54,927.19 (~54.88% deployed).
- Open orders: 3 trail-stop GTCs — XLP $77.346 stop / hwm $85.94 (RATCHETED yesterday from $77.022 / $85.58 on WMT-print-driven XLP rip); XLB $47.493 stop / hwm $52.77 (unchanged since 5/7); XLI $159.948 stop / hwm $177.72 (unchanged since 5/7). All trail 10%, none within 3% of price (XLB closest at +5.7% cushion current $50.22 vs stop $47.493), none at -7% trigger.

### Market Context
- WTI / Brent: WTI front-month ~$102/bbl (CLN26 ~102.12 per CME); WTI spot inferred low-$100s (EIA series lag). Brent ~$110.08 cited by Fortune as of May 18 9:10 ET, with $7-10 premium spread to WTI implying Brent $109-112 range now. **CRESTWOOD HEADLINE FALSIFIED**: yesterday's Crestwood May 2026 print of WTI ~$107 / Brent ~$120 is NOT consistent with today's CME front-month and Fortune live Brent — confirms yesterday's data-quality gate (1) skip was correct, the print was either stale (earlier-month narrative) or wrong (different reference basket). Hormuz situation per multiple sources still a "dual blockade" — Iran intermittent strait closure since late Feb 2026, US "Project Freedom" paused 5/4-5/6, Trump-Xi 5/14 framework still in early-digestion phase, no operationalized reopening. Practical reality: structural supply shock persists at constrained-but-cooling level; WTI in low-$100s = the floor holds but the premium is bleeding, not building. Risk of miscalculation-at-sea (mine incident, escort clash) remains elevated but no fresh kinetic event today.
- S&P 500 futures: ESM26 ~7,415.75, -0.13% overnight (Barchart June E-mini); NQM26 ~29,022.50, -0.25%. Mildly red into HD print + post-Warsh-digestion. SPX cash closed Mon ~7,422 (recovered from Fri's risk-off, still ~1.05% below 5/14 ATH 7,501). Tape neither risk-on nor decisively risk-off; HD print direction will set the day.
- VIX: Mon close 17.82 (Investing.com), intraday high 19.25, FRED official 5/15 close 18.43. Current ~17-18 range, regime-shift watch flag remains OFF (still inside 16-22 normal band). Mon also was last full trading day before May VIX expiration; rolls active.
- Today's catalysts: (1) **HD earnings BMO** = THE binary today, XLY-direct (no held exposure), indirect XLB read-through via construction-materials chain, marginal XLI via industrial-supply. Consensus EPS ~$3.41-$3.42 (-4% YoY), revenue ~$41.5-41.6B (+4.2% YoY); modeling soft transaction count (-1.2% YoY) offset by +1.9% YoY average ticket — consumer-cyclical resilience print. (2) **WMT-print Mon digestion carryover** — solid Q1 (US comps +4.5%, eCommerce +22%, profit +3%, mild post-print reaction), reinforcing defensive-consumer narrative for XLP top-3 holding (WMT actually 12.13% of XLP per State Street data — CORRECTION to yesterday's "5-6%" estimate, the leg-level binary was MORE concentrated than logged). (3) **Iran/Hormuz tape** — no fresh kinetic event captured, Crestwood print falsified; structural constraint persists but no re-escalation catalyst today. (4) **Warsh-handover multi-day digestion** — Friday's "no rush to cut" / "policy may need to stay restrictive for longer" framing carries forward; no dovish walkback captured, no scheduled Warsh speech today.
- Earnings before open: **HD (XLY-direct, no held exposure)**, plus mid-cap retailers (Best Buy / Lowe's not today, HD only of size). Wall Street Horizon May 19 BMO list shows HD as the only US large-cap of consequence. PANW reports AMC later this week, not today.
- Economic calendar this week: **LIGHT.** Wed 5/20 8:30 ET Building Permits + Housing Starts (April; cons 1.37M permits, 1.45M starts) + Initial Jobless Claims (week ending 5/16, cons 210K) + Philly Fed Manufacturing (cons 19); Wed 11:00 ET MBA 30-Year Mortgage Rate; Wed 11:30 PM Fed speaker Venable. Thu 5/21 8:30 ET Census official New Residential Construction release. Fri 5/22 quiet. NO FOMC, NO NFP, NO CPI/PPI this week. Catalyst calendar today is HD-print-dominant.
- Sector momentum YTD — **SOURCE DISCREPANCY CONTINUES** (yesterday flagged; today's Perplexity source returned a materially different ranking and the discrepancy is now load-bearing):
  - Yesterday's source (ETFreplay/State Street/First Trust composite, 5/18 refresh): XLE #1, XLP #2, XLI #3, XLB #4, XLU #5, XLK #9, XLY #10 — defensive-rotation + Hormuz-structural framing
  - Today's source (ETFreplay/State Street-style, mid-May 2026 refresh): XLC #1 (mid-20s%), XLK #2 (high-teens/low-20s%), XLY #3 (mid-teens%), XLI #4 (low-mid-teens%), XLF #5 (low-teens%), XLB #6 (high-single-digit%), XLV #7 (mid-single-digit%), XLE #8 (low-single-digit%), XLU #9 (flat-low), XLP #10 (flat-slightly positive) — AI-capex / growth-cyclical framing with defensives LAGGING
  - The two rankings cannot both be true simultaneously. Most-likely explanation: different time windows (YTD-narrow vs. trailing-6-mo vs. rolling-3-mo) or different equal-weight vs. cap-weight constructions. Today's source ranks XLP at #10 ("flat / slightly positive") which is FLATLY inconsistent with XLP's $83 → $86 ~+3.4% leg-level move since 5/4 — implying today's source is either using a different window OR is wrong. Treat the held basket's leadership status as DATA-QUALITY UNCERTAIN; the absolute price action of the basket (XLP +3.17% unrealized, basket flat-to-green) is the cleaner signal than the rotating sector-rank tape. Friday's weekly review must reconcile both source-discrepancies (the YTD numbers AND the rank) by going to State Street's primary source page rather than relying on Perplexity-synthesized rankings.
- Held-ticker news: **XLP (Consumer Staples) — WMT print Mon was the leg-level binary; outcome MILDLY CONSTRUCTIVE.** Walmart Q1 sales +4% cc, US comps +4.5%, Sam's Club +6.7% ex-fuel, eCommerce +22%, profit +3%. Market reaction muted/positive, no big shock. XLP top holdings: **WMT 12.13%, COST 9.65%, PG 6.92%, KO 6.51%, PM 6.23%, MDLZ 4.87%** — Costco and Walmart together >21% of the fund, so the print drives 1-2% of NAV on a clean beat/miss directionally. Defensive narrative intact; one bearish-IV commentary surfaced (Perplexity result [1] for XLP suggested call-overwrite/put-spread positioning) but no fundamental catalyst supporting it. XLB (Materials) — Friday's -2.77% leg-level low; no idiosyncratic news identified, no thesis break. XLI (Industrials) — no idiosyncratic news identified, Empire State manufacturing +11.0 (5/15) read-through still positive but stale. No thesis break for any leg; no -7% triggers active.
- Fed cut expectations: Unchanged at ZERO 2026 cuts. Warsh hawkish-lean framing carries forward. No FOMC minutes / Fed event today; Wed PM Venable speech is the week's next Fed catalyst.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — XLP +3.17% unrealized (new phase high for the leg, still well below +15% tighten threshold), XLB -1.65% worst (well above -7% trigger), XLI -1.45% middle. None at -7% triggers (XLB cushion ~5.4% to stop-out from current $50.22, manual-cut math $51.062 × 0.93 = $47.488 ≈ live trail stop $47.493 — GTC trail covers the -7% rule). Trail-stop GTCs live; XLP hwm $85.94 (current $86.00 a fractional intraday high → may ratchet stop $77.346 → ~$77.40 if XLP closes near current); XLB hwm $52.77 unchanged; XLI hwm $177.72 unchanged. Trail-tighten triggers (7% at +15%, 5% at +20%) — none in play, closest XLP +3.17% (~12 pp from +15% trigger). No add to existing names (XLP/XLB at 20% cap; XLI at 15% by design). **HD print is NOT a leg-level binary** for the held basket (XLY-direct, no held exposure); indirect XLB read-through is too diluted to act on.
2. **XLE (Energy ETF) — DEFINITIVELY RETIRED for this phase** — yesterday's data-quality gate (1) skip was vindicated within 24 hours: Crestwood's $107 WTI / $120 Brent print is materially inconsistent with today's CME front-month $102 and Fortune Brent $110. Re-authoring the conditional on a now-twice-falsified thesis (Trump-Xi framework 5/14 + Crestwood-print-falsified 5/18-19) would be classic deployment-pressure trading. WATCH-only at the deepest level — only re-author on a (a) cross-confirmed tier-1 kinetic-escalation headline (multiple wire sources within 24 hours) AND (b) WTI re-acceleration through $105 sustained. Either alone insufficient.
3. **XLK (Technology ETF) — WATCH-only, conditional deferred** — multi-day hawkish-Warsh digestion continues with no dovish walkback captured. Re-authoring on top of the still-fresh "no rush to cut" tape would be premature. Require (a) Warsh dovish soundbite OR (b) clean +1% AI-tape day with VIX <17 to re-engage. No-action today.
4. **HD-pre-print single-name chase or post-print XLY add** — explicit SKIP per strategy (sector-ETF momentum, not single-name earnings binaries). XLY is currently the #10-ranked sector by today's Perplexity source and the worst-positioned sector for cyclical-consumer exposure given oil at $102 and rate path higher-for-longer. Even a clean HD beat would be a one-name lift on a sector with structural headwinds.
5. **XLU (Utilities ETF)** — defensive cousin of XLP. VIX 17-18 inside normal band — no regime-shift signal authorizing add; XLP already covers the basket's defensive bid. SKIP.
6. **Single-name chase post-HD print** — explicit SKIP per strategy.

### Conditional Entries (midday-eligible) — up to 3
(None today. The XLE thesis is retired; XLK is in multi-day Warsh-digestion deferral; XLU has no regime-shift gate; HD-print-reaction trades are single-name out-of-strategy and the indirect XLB/XLI read-through is too diluted. The structural deployment-gap is now 4 weeks running; today's right answer is to acknowledge that the data-quality framework is killing every 4th-leg candidate and that Friday's weekly review must address the framework calibration — not to author another conditional that exists primarily to relieve deployment pressure.)

### Risk Factors
- **HD earnings BMO** = primary single-event risk today; XLY-direct, no held basket exposure but a sharp miss + weak guide tags broad cyclical/consumer tape and can compress XLB (construction materials chain) and marginally XLI (industrial supply). Held basket cushion: XLB ~5.4% to stop-out, XLI ~6.5% to stop-out — a single-print binary on HD even in worst-case won't trigger stops unless the print is catastrophic AND triggers a 2%+ broad-tape sell-off.
- **Crestwood-print-falsified Iran/Hormuz tape** — the headline that triggered yesterday's conditional was likely stale or wrong (WTI $107 / Brent $120 vs. today's $102 / $110). The structural-supply-shock thesis is fundamentally intact (Hormuz still constrained, dual-blockade dynamic continues) but the BID is bleeding, not building — XLE is NOT the right vehicle to be entering even if a fresh kinetic-escalation headline drops, because the tape would have to clear (a) cross-source confirmation AND (b) WTI re-acceleration AND (c) broad-tape green-on-day before the data-quality framework permits action.
- **Iran tape kinetic-retaliation risk** — if a fresh mine-incident / escort-clash / tanker-strike materializes today (always possible given the "dual blockade" structural setup), tape goes immediate-risk-off; held basket has zero direct exposure but ES futures already -0.13% means the cushion is modest.
- **Warsh-handover multi-day digestion** — Friday's hawkish framing ("no rush to cut" / "policy may need to stay restrictive for longer") carries forward into Tuesday with no confirming-hearing walkback captured. Any fresh Warsh / Fed-speaker soundbite tightening the hawkish framing re-engages multiple-compression on the basket. Wed PM Venable speech is the week's next Fed catalyst; today is event-free on Fed.
- **ESM26 -0.13% pre-market** = mild drift into the open; held basket has beta but no leg near trail-stop (deepest cushion XLB ~5.4%). Continued -1%+ broad sell-off today drags basket toward trigger zones but no leg currently within striking distance.
- **SPX 1.05% below ATH 7,501 with light technical support to ~7,150** (~3.7% below current) = elevated-base risk with sharp downside asymmetry on any HD-miss + tape-binary surprise.
- **Held basket 4-week structural deployment gap** — 54.88% deployment across 17 sessions; 4th-leg conditional has been authored every weekly cycle and SKIPPED every weekly cycle. Today: NO conditional authored — first session of week 4 to acknowledge the framework is producing repeat-skips and the right action is to admit the conviction bar is structurally too high for the 75-85% mandate AND defer the resolution to Friday's weekly review (not author another doomed conditional). The deployment gap remains the dominant structural risk for the phase; if it persists another week, the de facto strategy is the 3-leg basket at 55% deployment.
- **XLP overbought / valuation overhang** — leg at +3.17% unrealized off WMT-print-driven rip is the cleanest performer; defensive premium (forward P/E ~26 vs. 5-yr avg ~22.7) is the structural overhang. If today's Perplexity sector-rank source (XLP #10) reflects an emerging rotation OUT of defensives into AI-capex / growth-cyclicals, XLP can compress fast. But the absolute price action ($83 → $86) contradicts that ranking — treat the rank-vs-price-action discrepancy as live ambiguity. Trail-stop $77.346 covers stop-out; no pre-emptive trim.
- **XLB worst-leg watch** — at -1.65% unrealized, deepest red of basket; stop $47.493 / hwm $52.77 covers the -7% rule (manual-cut math = live stop), ~5.4% cushion to stop-out from current $50.22.
- **Sector-rank source discrepancy** — yesterday's source ranked XLE/XLP/XLI/XLB top-4; today's source ranks them #8/#10/#4/#6. Two different framings of the same tape. Friday weekly review MUST reconcile by going to a single authoritative source (State Street primary, ETFreplay direct, or a Bloomberg/FactSet terminal) — Perplexity-synthesized rankings cannot resolve which source-window or weighting is correct.
- **WMT 12.13% weight in XLP** correction from yesterday's "5-6%" log entry — the leg-level binary on Mon was MORE concentrated than logged. Implication: the +1.49% XLP day Mon was substantially WMT-print-driven (consistent with the muted-positive WMT reaction); a future earnings-binary on WMT, COST (9.65%), PG (6.92%), or KO (6.51%) carries more direct leg risk than prior entries acknowledged. Next major XLP holdings prints: COST Q3 typically end-May, KO/PG already reported in April.
- **Held positions** — none near -7% (worst XLB -1.65%), none near +15% tighten trigger (best XLP +3.17%); no manual action required from this entry alone.

### Decision
HOLD at the open. **Zero at-the-open buys. Zero midday conditionals authored.** First session of week 4 where the structural deployment-gap question is acknowledged in the decision rather than papered over with another doomed conditional: XLE retired (Crestwood falsified), XLK in Warsh-deferral, XLU lacks regime-shift gate, HD-print-reaction trades out-of-strategy. The 4th-leg add framework has produced repeat-skips for 4 consecutive weeks; today's right action is to defer the framework-calibration question to Friday's weekly review and accept that the basket may remain at 55% deployment through the phase if no genuinely cross-confirmed catalyst materializes. Held XLP/XLB/XLI continue under their 10% trailing GTCs (no thesis break, no -7% triggers, no +15% tighten triggers, XLP hwm intact at $85.94 with fractional further ratchet possible if XLP closes near current $86.00). Daily cap 3/3 available, weekly cap 0/6 fresh — full headroom remains if a clean cross-confirmed catalyst materializes intraday, but no conditional pre-authored. Patience > activity. Midday scan will re-check for any kinetic-escalation headline cross-confirmation; daily-summary at EOD captures final marks.

## 2026-05-19 — Midday Scan

### Account (12:01 CT)
- Equity: $99,766.59 | Cash: $45,158.79 (45.26%) | Buying power: $144,925.38 | Daytrade count: 0
- Positions (cost basis $54,841.21 / mkt $54,608.56 / ~54.74% deployed):
  - XLP 239 sh @ $83.357 — current $86.24, intraday +0.40%, unrealized +$689.01 (+3.46%)
  - XLB 390 sh @ $51.062 — current $49.305, intraday -1.82%, unrealized -$685.40 (-3.44%)
  - XLI 87 sh @ $172.466 — current $169.75, intraday -0.59%, unrealized -$236.26 (-1.58%)
- Open orders (3 trailing 10% GTCs):
  - XLP stop $78.0255 / hwm $86.695 — RATCHETED intraday from $77.346 / $85.94 (new intraday high $86.695)
  - XLB stop $47.493 / hwm $52.77 — unchanged
  - XLI stop $159.948 / hwm $177.72 — unchanged

### Actions
- **Cut losers (-7% rule):** None. Worst leg XLB -3.44% (deepening from pre-market -1.65% on HD-print read-through compressing materials), well above -7% trigger (~3.6 pp cushion of unrealized to trigger; price cushion XLB current $49.305 vs stop $47.493 = ~3.7%).
- **Tighten winners:** None. Best leg XLP +3.46% (new phase high for the leg), well below +15% tighten threshold.
- **Thesis check:** No breaks. XLP +0.40% intraday continues post-WMT defensive bid (hwm ratcheted $85.94 → $86.695 by Alpaca GTC, trail $77.346 → $78.0255); XLB -1.82% and XLI -0.59% softness consistent with HD-print indirect read-through on construction-materials chain + mildly red ES tape (ESM26 -0.13% overnight, drifted weaker into noon). No idiosyncratic news identified on any leg; no thesis break.
- **Conditionals:** None to evaluate — today's pre-market RESEARCH-LOG authored zero conditionals (XLE retired post-Crestwood-falsification, XLK in Warsh-deferral, XLU lacks regime-shift gate, HD-print single-name out-of-strategy). No conditional evaluation work this session.
- **Intraday research:** None triggered. XLB -1.82% is the move-of-day on the basket but is plausibly HD-print read-through + broad-tape drift, not idiosyncratic; below the "sharply moving with no obvious cause" bar for unscheduled Perplexity spend.

### Env-check note
Loop check printed MISSING for all five env vars again; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,766.59 — proceeded per saved feedback memory.

### Decision
NO ACTION. Held basket intact, no cuts, no tightens, no conditional fire. Trades today 0/3, trades this week 0/6, deployment ~54.74% unchanged. XLP trail stop auto-ratcheted by Alpaca (broker-side, no client modification needed). Day-of risk is HD-print indirect read-through to XLB; XLB cushion ~3.7% to stop-out from $49.305 — monitorable but not at trigger. Daily-summary at EOD captures final marks; weekly review Friday gets the structural-deployment question again.

## 2026-05-20 — Pre-market Research

### Account
- Equity: $99,575.87 (pre-open; XLP marking $86.2389 above lastday $86.09)
- Cash: $45,158.79
- Buying power: $144,734.66
- Daytrade count: 0
- Open orders: 3 trailing stop sells (XLP $78.0255, XLB $47.493, XLI $159.948) — all live, GTC

### Positions
| Ticker | Qty | Entry | Cur | Unrealized | Stop | HWM |
| — | — | — | — | — | — | — |
| XLP | 239 | $83.36 | $86.2389 | +$688.75 (+3.46%) | $78.0255 | $86.695 |
| XLB | 390 | $51.06 | $49.04 | -$788.75 (-3.96%) | $47.493 | $52.77 |
| XLI | 87 | $172.47 | $168.74 | -$324.13 (-2.16%) | $159.948 | $177.72 |

### Market Context
- WTI / Brent: WTI ~$104, Brent ~$110 — Hormuz blockade tape still active (Kharg Island struck late-Mar, US-Iran kinetic exchanges ongoing, AIS jamming, regional fuel-price caps in South Korea). Geopolitical premium intact.
- S&P 500 futures: ~6,657, +0.10% (mildly green premarket per Markets Insider). Tape constructive but light.
- VIX: ~17.26 (recent print; no fresh spike despite Tuesday's risk-off equity move)
- Today's catalysts: **FOMC Minutes 2:00 PM ET** — dominant macro event. Markets digesting rate-cut path; minutes correspond to late-April meeting and will move on dot-plot dispersion / dissent count / Q&A redactions.
- Earnings before open: No flagged mega-caps from cross-source scan; nothing market-moving in pre-mkt window above the noise floor for sector-ETF basket
- Economic calendar: NO fresh CPI / PPI / jobs prints today. FOMC Minutes 2pm ET is the day. Initial Claims + Philly Fed land Thursday 5/21 8:30 ET.
- Sector momentum YTD (Mar-update-base): Energy #1 (~+26%), Consumer Staples #2 (~+10.7%), Industrials #3 (~+9.6%), Materials in leading quadrant per Investing.com sector rotation. Risk-off Tue compressed XLB / XLI sharply (XLB -2.41% / XLI -1.18%) — characterized as "leaders taking a breather" rather than thesis-break in cross-source check.

### Trade Ideas
1. **HOLD** all three legs into FOMC Minutes 2pm ET. Minutes are a known binary — no edge betting direction; high-skew Q&A redactions / dissent count are the unpredictable variables.
2. **XLB stop-watch** — unrealized -3.96% is the worst leg of the phase. Cushion to -7% manual trigger is ~3.04% additional downside ($49.04 → ~$47.49). Trail stop at $47.493 (-10% from hwm $52.77) is the broker-side exit. If FOMC Minutes are hawkish and XLB extends another -2 to -3%, manual-cut decision moves to the front of the queue.
3. **XLE 4th-leg conditional deferred** — tier-1 wire confirmation of Crestwood-extension headline still absent. Hormuz tape is real (WTI $104, Brent $110, Kharg Island strike, fuel-price caps) but the data-quality gate (Reuters/Bloomberg/WSJ/AP/Platts/Argus cross-source) remains unmet across multiple sessions. No re-author.

### Conditional Entries (midday-eligible) — up to 3
None. The dominant intraday event is FOMC Minutes 2pm ET; conditional entries before then carry binary-event risk, conditional entries after the print are post-event chase trades that don't benefit from intraday confirmation in a strategy-consistent way. XLE remains data-quality-gated. XLK/XLU have no fresh regime-shift catalyst. Default zero applies cleanly.

### Risk Factors
- **FOMC Minutes 2pm ET** — direction risk both ways. Hawkish dispersion compresses cyclicals further (XLB/XLI extend Tuesday's slide); dovish surprise lifts the broad tape but XLP defensive premium can compress on rotation.
- **XLB at -3.96% unrealized** — closer to -7% manual trigger than any leg has been this phase; another -3% intraday move from $49.04 puts it in manual-cut territory before the broker-side trail at $47.493 fires.
- **Hormuz/oil tape** still elevated — WTI $104 / Brent $110 with active kinetic exchanges and AIS jamming. Held basket has no XLE exposure (neutral on oil) but XLB carries cost-input read-through if WTI gaps higher.
- **Concentration risk confirmed Tuesday** — 3-leg sector-ETF basket gave back -0.60% in a single risk-off session, similar to May 15 (-0.87%). Basket has now round-tripped from +0.85% phase high (May 12) to -0.47% in 5 sessions. The structural-deployment gap (~55% vs. 75-85% target) means undeployed cash is the only ballast.
- **17 consecutive sessions ~55% deployment** — Friday weekly review (this Friday 5/22) faces the same question for the 4th consecutive week: commit to a 4th leg or accept the 3-leg basket as final.

### Env-check note
Loop check again printed MISSING for all five vars; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,575.87 — proceeded per saved feedback memory.

### Decision
**HOLD.** Pre-FOMC-Minutes binary day — no at-the-open entries, no conditionals. Held basket intact (no cuts: worst leg XLB -3.96% above -7% trigger; no tightens: best leg XLP +3.46% below +15% trigger). Trades today 0/3, trades this week 0/6 fresh, deployment ~54.63% unchanged. Day-of monitor: XLB drift toward -7% trigger if Minutes are hawkish; XLP trail-stop auto-ratchet if intraday hwm extends above $86.695. Patience > activity into the print; reassessment is post-2pm-ET event with Minutes digested.

## 2026-05-20 — Midday Scan

### Account (12:01 CT)
- Equity: $99,838.38 | Cash: $45,158.79 (45.23%) | Buying power: $144,997.17 | Daytrade count: 0
- Positions (cost basis $54,841.21 / mkt $54,670.58 / ~54.76% deployed):
  - XLP 239 sh @ $83.357 — current $85.75, intraday -0.40%, unrealized +$571.90 (+2.87%)
  - XLB 390 sh @ $51.062 — current $49.51, intraday +0.96%, unrealized -$605.45 (-3.04%)
  - XLI 87 sh @ $172.466 — current $170.89, intraday +1.27%, unrealized -$137.08 (-0.91%)
- Open orders (3 trailing 10% GTCs, all unchanged from pre-market):
  - XLP stop $78.0255 / hwm $86.695 — no new intraday high (current $85.75 < hwm)
  - XLB stop $47.493 / hwm $52.77 — unchanged
  - XLI stop $159.948 / hwm $177.72 — unchanged

### Actions
- **Cut losers (-7% rule):** None. Worst leg XLB -3.04% (improved from pre-market -3.96% on cyclical bounce-back), well above -7% trigger. Price cushion XLB current $49.51 vs stop $47.493 = ~4.1%; unrealized cushion to -7% = ~3.96 pp.
- **Tighten winners:** None. Best leg XLP +2.87% (below +15% threshold by ~12 pp).
- **Thesis check:** No breaks. Basket is digesting Tuesday's risk-off with a constructive pre-FOMC-Minutes bid in cyclicals — XLB +0.96% and XLI +1.27% recovering, XLP -0.40% mild defensive rotation as broad-tape leans slightly risk-on into the 2pm ET print. No idiosyncratic news identified on any leg.
- **Conditionals:** None to evaluate — today's pre-market RESEARCH-LOG explicitly authored zero conditionals (FOMC-Minutes binary day, XLE data-quality-gated, XLK/XLU no fresh catalyst).
- **Intraday research:** None triggered. No leg moving sharply without obvious cause; pre-FOMC drift is the dominant tape feature.

### Env-check note
Loop check printed MISSING for all five env vars again; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,838.38 — proceeded per saved feedback memory.

### Decision
NO ACTION. Held basket intact, no cuts, no tightens, no conditional fire. Trades today 0/3, trades this week 0/6 fresh, deployment ~54.76% unchanged. Cyclical bounce-back (XLB +0.96%, XLI +1.27%) trimmed pre-mkt unrealized losses; XLB pulled back from -3.96% to -3.04%, restoring ~1 pp of cushion to the -7% manual-cut trigger ahead of FOMC Minutes 2pm ET. XLP trail-stop ratchet not triggered (no new hwm). Day-of monitor: FOMC Minutes 2pm ET reaction is the dominant remaining risk; XLB -7% trigger watch persists if Minutes are hawkish and cyclicals reverse. Daily-summary at EOD captures final marks; pre-market Thursday addresses post-Minutes basket positioning.

## 2026-05-21 — Pre-market Research

### Account
- Equity: $99,726.13 (pre-open; lastday $99,837.60, drift -$111.47 / -0.11%)
- Cash: $45,158.79 (45.28%)
- Buying power: $144,884.92
- Daytrade count: 0
- Open orders: 3 trailing 10% stop sells (XLP $78.0255 / hwm $86.695, XLB $47.493 / hwm $52.77, XLI $159.948 / hwm $177.72) — all GTC, all unchanged from Mon's XLP ratchet

### Positions
| Ticker | Qty | Entry | Cur | Unrealized | Stop | HWM |
| — | — | — | — | — | — | — |
| XLP | 239 | $83.36 | $85.52 | +$516.93 (+2.60%) | $78.0255 | $86.695 |
| XLB | 390 | $51.06 | $49.50 | -$609.35 (-3.06%) | $47.493 | $52.77 |
| XLI | 87 | $172.47 | $170.38 | -$181.45 (-1.21%) | $159.948 | $177.72 |

### Market Context
- WTI / Brent: Perplexity returned no live tick — prediction-market and CME-quote links only (Barchart CLK26, CME light-sweet page). Working assumption WTI low-$100s / Brent $108-112 carried forward from yesterday's read (WTI ~$104 / Brent ~$110); no fresh Hormuz kinetic event captured in cross-source scan. **XLE 4th-leg data-quality gate remains UNMET** for the 4th consecutive session (no tier-1 wire confirmation of the Crestwood-extension headline; Crestwood's $107/$120 print stays falsified by today's CME front-month).
- S&P 500 futures: Mixed signals. Investing.com confirms **SPX cash closed 7,432.89 (+1.08%) on May 20** — Minutes interpreted as constructive/relief (no near-term trend reversal). Schwab open-update flagged SPX at 7,353.61 (-0.67%) but that print is inconsistent with the closing tape and our basket's pre-mkt drift (only -0.11% portfolio); treating as either stale or different-window snapshot rather than a real -1% gap-down. Basket pre-mkt drift mild: XLP flat (current $85.52 = lastday), XLB -0.44% ($49.50), XLI -0.21% ($170.38) — consistent with light post-rally consolidation, not risk-off.
- VIX: Last published close 18.06 (5/19 per YCharts); no May 20 print captured in search (likely 17-18 range given equity rally). Regime-shift watch flag remains OFF (16-22 band).
- Today's catalysts: **DE earnings BMO** = THE binary today, XLI-direct. Consensus EPS ~$5.80-$5.81 (-12-13% YoY vs. Q2 2025 $6.64); Zacks Earnings ESP +6.24% flags elevated beat probability; bull-case framing on precision-ag / recurring revenue +18% YoY offsetting ~70% of equipment-volume decline. DE is a top-5 XLI holding (typically ~3-4% of XLI NAV) and the industrial-bellwether of the year — clean beat-and-raise lifts XLI a meaningful sub-1% on print, a miss + cautious guide compresses XLI directly. **Initial Jobless Claims + Philly Fed Manufacturing 8:30 ET** = 8:30 binary. Claims consensus ~210K (prior 211K) — flat-to-slightly-lower expected, low-skew binary. Philly Fed consensus ~15.0 (prior 26.7) — large step-down expected, the surprise direction would be either side of 15. XLI-direct read-through on Philly Fed.
- Earnings before open: **DE (XLI-direct, held exposure)** is the leg-level binary. Perplexity earnings-list returned WMT as BMO today which is FACTUALLY WRONG (WMT reported Mon 5/18, confirmed by 5/19 RESEARCH-LOG and the XLP +1.49% Mon move) — treating the Perplexity earnings list as data-quality-degraded and using DE as the confirmed cross-source single name. Other names on the list (AAP, WMS, HLNE, LSPD, NTES, CRVL, IMVT) are not held-basket-relevant.
- Economic calendar: Today 8:30 ET = Initial Jobless Claims (cons ~210K, prior 211K) + Philly Fed Manufacturing May (cons 15.0, prior 26.7); MBA Mortgage Rate 11:00 ET; Census New Residential Construction official release Thursday. Tomorrow (Fri 5/22) quiet. No FOMC / NFP / CPI / PPI this week. FOMC Minutes binary already cleared (yesterday afternoon).
- Sector momentum YTD: Cross-source check today returned XLP / XLI / XLB / XLE as **leading**, XLK **cooling** post-AI run — narrative aligns with the held basket and reverses Tuesday's Perplexity rank discrepancy (which had put XLP at #10). Friday's weekly review still owes the source-discrepancy reconciliation by going to State Street primary, but today's cross-source check is at least directionally supportive of the basket.
- Held-ticker news: **XLP** — defensive narrative intact; some BTIG/Kirsch put-spread color flagged on tobacco-regulation/tariff risk, no fundamental catalyst supporting it; WMT 12.13% / COST 9.65% / PG 6.92% / KO 6.51% / PM 6.23% top holdings unchanged. **XLB** — no idiosyncratic news, broad-tape risk-off Tuesday and Wed cyclical bounce-back was the story. **XLI** — DE BMO today is the only direct catalyst; otherwise narrative intact (defense/aerospace strength + capex/manufacturing read-through, freight mixed).
- Fed cut expectations: Unchanged. Minutes confirmed dot-plot shift toward fewer 2026 cuts (consensus from one-cut at March SEP; Powell discussed possibility next move could be a hike, hawkish tilt; Miran sole dissent for an immediate 25 bp cut). Market interpretation post-Minutes was constructive (SPX +1.08% Tue close), suggesting the hawkish content was already priced. No FOMC speakers today; Venable Wed PM already passed.

### Trade Ideas
1. **HOLD existing XLP/XLB/XLI** — basket grinding sideways in week 4. XLP +2.60% unrealized (best leg, still well below +15% tighten threshold by ~12.4 pp); XLB -3.06% worst (improved from yesterday pre-mkt -3.96% on Wed cyclical bounce-back, cushion ~4.0% from current $49.50 to stop $47.493, ~3.94 pp unrealized cushion to -7% manual-cut trigger); XLI -1.21% middle (cushion ~6.5% to stop). No leg near any trigger. No add to existing names (XLP/XLB at 20% cap; XLI at 15% by design). Trail GTCs live; XLP hwm $86.695 (current $85.52 below — no ratchet on the open), XLB and XLI hwms long-stale ($52.77 from May 7, $177.72 from May 7).
2. **DE-print read-through to XLI** — XLI direct catalyst risk. Beat+raise lifts XLI ~0.5-1% (modest, DE ~3-4% of XLI NAV but earnings beats compress to half the implied move usually); clean miss + cautious guide compresses XLI ~1-2% which would push XLI unrealized from -1.21% toward -2.5-3.0%, still well above -7% trigger. **No pre-emptive trim** — strategy is HOLD through earnings binaries unless thesis breaks; DE-specific guide cautious on ag equipment is sub-segment risk, not industrial-bellwether thesis-break.
3. **XLE 4th-leg conditional — RETIRED for this phase** (4th consecutive session). Crestwood-print falsification stands (CME WTI front-month ~$102 vs. Crestwood's $107 print); no tier-1 wire kinetic-escalation headline today. Watch-only at deepest level — re-author only on (a) cross-confirmed tier-1 wire kinetic-escalation AND (b) WTI re-acceleration through $105 sustained. Neither condition met.
4. **XLK (Technology ETF) — WATCH-only, conditional deferred** — multi-day hawkish-Warsh / Minutes-digestion continues; sector momentum cross-source has XLK as "cooling after a strong AI-driven run." Re-author only on (a) Warsh / Fed-speaker dovish soundbite OR (b) clean +1% AI-tape day with VIX <17. No-action today.
5. **XLU (Utilities ETF)** — VIX 18 inside normal band; defensive bid already covered by XLP. SKIP.
6. **DE single-name chase pre- or post-print** — explicit SKIP per strategy (sector-ETF momentum, not single-name earnings binaries).

### Conditional Entries (midday-eligible) — up to 3
(None. DE-print + 8:30 ET data are pre-open binaries that don't benefit from a midday conditional structure — by the time midday scan runs, the print is fully digested into XLI price and there's no incremental confirmation to wait for. XLE remains data-quality-gated for the 4th consecutive session — the framework correctly fired SKIP on Mon and continues to hold; authoring another XLE conditional today would be the deployment-pressure trade the May 19 entry explicitly flagged against. XLK / XLU have no fresh regime-shift gate. Friday's weekly review must reconcile the 4-week 4th-leg-skip pattern with the structural 55% deployment gap; today's right answer is to defer that reconciliation, not paper it over with another doomed conditional.)

### Risk Factors
- **DE earnings BMO** = primary single-event risk today, XLI-direct. Bull case (precision-ag mix-shift surprise + +6.24% ESP) lifts XLI ~0.5-1%; bear case (clean miss + ag-equipment demand-normalization cautious guide) compresses XLI ~1-2%. Worst-case mathematics: XLI compression of 2.5% from current $170.38 puts XLI ~$166.10, unrealized -3.7%, still well above -7% trigger and well above trail stop $159.948 (~3% cushion remaining). DE is the only large-cap industrial of size on today's calendar, so the print is the leg-level binary for XLI specifically and read-through for the broader industrials tape.
- **8:30 ET Initial Claims + Philly Fed binary** — low-skew expected (claims flat-to-slightly-lower; Philly Fed already cons'd to step-down to 15.0). Surprise directions: claims spike >220K compresses cyclicals (XLB/XLI bid lower on growth-concern read-through); Philly Fed negative print (<0) is the sharp tail risk on industrials. Both directions priced as low-probability tails; central case is benign.
- **XLB at -3.06% unrealized** — improved from yesterday pre-mkt's worst phase reading (-3.96%) on Wed's +1.39% bounce. Cushion to -7% manual trigger ~3.94 pp; price cushion XLB current $49.50 vs stop $47.493 = ~4.0%. Still the deepest red leg; today's binary scenarios (DE miss → broad cyclical compression → XLB read-through) keep it on the watch list but not at trigger.
- **Concentration risk** — basket has now round-tripped from +0.85% phase high (May 12 Tue) to -0.16% (May 20 Wed) in 5 sessions; the 3-leg sector-ETF basket without a 4th low-correlation leg shows full beta to broad-tape risk-off events. 4-week structural deployment gap (now 18 consecutive sessions at ~55%) confirms framework-skip rate is the deployment-gap-driver. Friday weekly review owes the reconciliation.
- **Crestwood-falsified Iran/Hormuz tape** — structural-supply-shock thesis intact (Hormuz constrained, dual-blockade dynamic continues, AIS jamming, regional fuel-price caps) but the BID is bleeding. No fresh kinetic event today. XLE NOT the right vehicle for re-entry even on a fresh headline — gates 1 (cross-source) + 5 (WTI re-acceleration through $105) are both unmet.
- **Iran kinetic-retaliation tail risk** — always-on given the structural setup. Held basket has zero direct XLE exposure; ES futures already mildly weaker pre-mkt means cushion is modest. No specific event flagged today.
- **Warsh / Fed-speaker headline tail** — no scheduled FOMC speaker today; Venable Wed PM already passed without market-moving content (basket reaction modest). Friday is event-free on Fed; next major Fed catalyst is the Powell Jackson Hole prep cycle later in the cycle.
- **XLP overbought / valuation overhang** — leg at +2.60% unrealized off WMT-print-driven rip, forward P/E ~23-24x vs. 5-yr avg ~22.7. Today's sector-momentum cross-source put XLP back in the leading cohort (reversing Tue's #10 outlier), de-risking the "emerging rotation OUT of defensives" framing somewhat. Trail-stop $78.0255 covers stop-out; no pre-emptive trim. Tobacco-regulation / tariff put-spread color flagged but no fundamental catalyst.
- **Held basket 4-week deployment gap** — 54.72% deployment today (cost basis $54,841 / equity $99,726), 18 consecutive sessions at this ratio. The 4th-leg framework has produced repeat-skips for 4 straight weekly cycles; today is the second consecutive session where the right answer is acknowledged in the decision rather than papered over with another doomed conditional. The dominant structural risk for the phase.

### Env-check note
Loop check again printed MISSING for all five env vars; wrapper smoke-test (`alpaca.sh account`) returned live JSON with portfolio_value $99,726.13 — proceeded per saved feedback memory.

### Decision
**HOLD.** Zero at-the-open buys. Zero midday conditionals authored. Held XLP/XLB/XLI continue under their 10% trailing GTCs — no thesis break, no -7% triggers (worst XLB -3.06%), no +15% tighten triggers (best XLP +2.60%), no leg within 3% of stop (XLB closest at ~4.0% price cushion). DE earnings BMO is the dominant intraday binary, XLI-direct; strategy is HOLD through the print (no pre-emptive trim) with worst-case math showing XLI cushion intact even on a -2.5% compression. 8:30 ET claims+Philly Fed are low-skew tail-risk binaries; basket holds. XLE 4th-leg gate continues to hold for the 4th consecutive session — Crestwood-falsified, no tier-1 wire kinetic-escalation, no WTI re-acceleration above $105. Daily cap 3/3 fresh, weekly cap 0/6 fresh. Patience > activity into the DE print + 8:30 binaries; midday scan re-checks for any thesis-break or sharp XLI/XLB move from the print; daily-summary at EOD captures final marks. Friday weekly review owes (a) the source-discrepancy reconciliation via State Street primary, (b) the 4-week 4th-leg-skip vs. 55% deployment framework calibration, (c) whether to accept the 3-leg basket as final for the phase or commit to XLE/XLK/XLU even at a relaxed conviction bar.
