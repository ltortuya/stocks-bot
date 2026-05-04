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
