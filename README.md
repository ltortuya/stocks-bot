# Stocks Trading Bot — Claude as the Bot

Autonomous trading agent built on Claude Code. Each scheduled run is a fresh
stateless container that clones this repo, reads markdown memory, decides on
action, places orders via Alpaca, writes new memory, commits back to `main`,
and notifies via Telegram.

There is no separate Python bot process. **Claude IS the bot.**

## Architecture at a glance

- **scripts/** — three thin bash wrappers: `alpaca.sh` (trading), `openai.sh`
  (research), `telegram.sh` (chat notifications).
- **memory/** — five markdown files committed to git. The agent's only state
  between runs.
- **routines/** — five cloud routine prompts (production path). Each runs on a
  cron and is paste-verbatim into the Claude Code cloud routine UI.
- **.claude/commands/** — local-mode slash commands for ad-hoc + manual runs.
- **CLAUDE.md** — agent rulebook auto-loaded every session.

## Strategy (summary)

Swing trading, stocks only, no options. Max 5–6 positions, 20% per position,
6 new trades/week (max 3/day). 10% trailing stop on every position as a real GTC order.
Cut losers at -7%. Tighten trail to 7% at +15%, 5% at +20%. Patience > activity.

Full rules in [memory/TRADING-STRATEGY.md](memory/TRADING-STRATEGY.md).

## Local mode (development + ad-hoc)

```bash
cp env.template .env  # then fill in real credentials
chmod +x scripts/*.sh

# Smoke test
bash scripts/alpaca.sh account
bash scripts/telegram.sh "test message"

# In Claude Code, run the slash commands:
/portfolio
/pre-market
/market-open
/midday
/daily-summary
/weekly-review
/trade AAPL 10 buy
```

## Cloud mode (production)

Five cron-fired routines, configured in the Claude Code cloud UI. See
[routines/README.md](routines/README.md) for setup.

| Routine        | Cron                  | When (America/Chicago) |
|----------------|-----------------------|------------------------|
| Pre-market     | `0 6 * * 1-5`         | 6:00 AM weekdays       |
| Market-open    | `30 8 * * 1-5`        | 8:30 AM weekdays       |
| Midday         | `0 12 * * 1-5`        | Noon weekdays          |
| Daily-summary  | `0 15 * * 1-5`        | 3:00 PM weekdays       |
| Weekly-review  | `0 16 * * 5`          | 4:00 PM Fridays only   |

## Legacy

The previous Python-bot architecture (intraday momentum scanner + polling
trader + backtest engine) is preserved in `legacy/python-bot/` for reference.
Not used by the new system.

## Credit

Architecture follows the *Opus 4.7 Trading Bot — Setup Guide* by Nate Herk
(AIS+), with substitutions: Telegram for ClickUp, OpenAI web-search for
Perplexity.
