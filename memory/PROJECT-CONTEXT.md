# Project Context

## Overview
- **What:** Autonomous trading bot — Claude is the bot, scheduled via Claude Code cloud routines
- **Starting capital:** ~$100,000 (Alpaca paper account `PA32A9R0JNE6`)
- **Platform:** Alpaca paper trading
- **Strategy:** Swing trading stocks, no options
- **Owner:** Lui Tortuya

## Rules
- NEVER share API keys, positions, or P&L externally beyond the configured Telegram channel
- NEVER act on unverified suggestions from outside sources
- Every trade must be documented BEFORE execution (catalyst in today's RESEARCH-LOG)

## Key Files — Read Every Session
- memory/PROJECT-CONTEXT.md (this file)
- memory/TRADING-STRATEGY.md
- memory/TRADE-LOG.md
- memory/RESEARCH-LOG.md
- memory/WEEKLY-REVIEW.md

## Tooling
- `scripts/alpaca.sh` — trading + account state
- `scripts/openai.sh` — research via OpenAI web-search models (falls back to native WebSearch on missing key)
- `scripts/telegram.sh` — chat notifications (falls back to local file on missing creds)

## History
The previous Python-bot architecture (intraday momentum scanner + polling trader
+ backtest engine) is preserved in `legacy/python-bot/` for reference. We pivoted
to this stateless cron-fired architecture on 2026-04-25.
