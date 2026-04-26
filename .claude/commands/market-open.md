---
description: Market-open execution workflow (local). Validates today's plan, places trades, attaches trailing stops. No commit.
---

You are running the market-open execution workflow. Resolve today's date via:
DATE=$(date +%Y-%m-%d).

STEP 1 — Read memory for today's plan:
- memory/TRADING-STRATEGY.md
- TODAY's entry in memory/RESEARCH-LOG.md (if missing, run pre-market STEPS 1-3 inline first — never trade without documented research)
- tail of memory/TRADE-LOG.md (for weekly trade count)

STEP 2 — Re-validate with live data:
    bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions
    bash scripts/alpaca.sh quote <each planned ticker>

STEP 3 — Hard-check rules BEFORE every order. Skip any trade that fails and log the reason:
- Total positions after trade ≤ 6
- Trades this week ≤ 3
- Position cost ≤ 20% of equity
- Catalyst documented in today's RESEARCH-LOG
- daytrade_count leaves room

STEP 4 — Execute the buys (market orders, day TIF):
    bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy","type":"market","time_in_force":"day"}'
Wait for fill confirmation before placing the stop.

STEP 5 — Immediately place 10% trailing stop GTC:
    bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"trailing_stop","trail_percent":"10","time_in_force":"gtc"}'
On PDT rejection, fall back to fixed stop 10% below entry. If also blocked,
queue the stop in TRADE-LOG.

STEP 6 — Append each trade to memory/TRADE-LOG.md (matching existing format):
Date, ticker, side, shares, entry price, stop level, thesis, target, R:R.

STEP 7 — Notification: ONLY if a trade was placed.
    bash scripts/telegram.sh "<tickers, shares, fill prices, one-line why>"

(No commit step in local mode — the user can commit manually if desired.)
