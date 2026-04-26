# Trading Strategy

## Mission
Beat the S&P 500 over the challenge window. Stocks only — no options, ever.

## Capital & Constraints
- Starting capital: ~$100,000 (paper account `PA32A9R0JNE6`)
- Platform: Alpaca paper trading
- Instruments: Stocks ONLY
- PDT limit: 3 day trades per 5 rolling days (account < $25k threshold doesn't apply at $100k, but be defensive anyway)

## Core Rules
1. **NO OPTIONS** — ever
2. 75–85% deployed
3. 5–6 positions at a time, max 20% each (~$20,000)
4. 10% trailing stop on every position as a real GTC order
5. Cut losers at -7% manually
6. Tighten trail: 7% at +15%, 5% at +20%
7. Never within 3% of current price; never move a stop down
8. Max 3 new trades per week
9. Follow sector momentum
10. Exit a sector after 2 consecutive failed trades
11. Patience > activity

## Buy-side Gate (every check must pass)
- Total positions after this fill ≤ 6
- Total trades placed this week (including this one) ≤ 3
- Position cost ≤ 20% of account equity
- Position cost ≤ available cash
- Daytrade count leaves room (PDT: 3/5 rolling business days as a defensive habit)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The instrument is a stock (not an option, not anything else)

## Sell-side Rules
- If unrealized loss is -7% or worse → close immediately
- If thesis breaks (catalyst invalidated, sector rolling over, news event) → close, even if not at -7% yet
- If position is up +20% or more → tighten trailing stop to 5%
- If position is up +15% or more → tighten trailing stop to 7%
- If a sector has two consecutive failed trades → exit all positions in that sector

## Entry Checklist (document all four before placing)
- What is the specific catalyst today?
- Is the sector in momentum?
- What is the stop level (7–10% below entry)?
- What is the target (minimum 2:1 risk/reward)?
