# Stocks Momentum Bot

Python momentum-breakout trading bot for Alpaca paper account.
Spec: [docs/specs/2026-04-25-momentum-bot-design.md](docs/specs/2026-04-25-momentum-bot-design.md)
Plan: [docs/plans/2026-04-25-momentum-bot-plan.md](docs/plans/2026-04-25-momentum-bot-plan.md)

## Quick start (development, Windows)

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env  # then edit with real credentials
.venv\Scripts\pytest
```

## Run a scan (manual)

```bash
.venv/bin/python -m cli.run_scanner
```

## Run a backtest

```bash
.venv/bin/python -m cli.run_backtest --start 2025-01-01 --end 2026-04-01 --equity 100000
# Results land in backtest/results/<run_id>/
```

## Operator commands

```bash
.venv/bin/python -m cli.ops positions       # local + Alpaca side positions
.venv/bin/python -m cli.ops watchlist       # today's active watchlist
.venv/bin/python -m cli.ops halt "reason"   # halt new entries
.venv/bin/python -m cli.ops resume          # clear halt
.venv/bin/python -m cli.ops flatten AAPL    # market-sell one symbol
.venv/bin/python -m cli.ops flatten-all     # market-sell everything
```

## Deployment to the mini PC (Ubuntu, 192.168.1.111)

```bash
# 1. Clone + venv
ssh lui-tortuya@192.168.1.111
git clone <repo-url> ~/stocks_monitoring
cd ~/stocks_monitoring
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Copy .env (or symlink the shared one)
ln -s ~/.env .env

# 3. Refresh universe (one time)
.venv/bin/python -m cli.refresh_universe

# 4. Install systemd unit
mkdir -p ~/.config/systemd/user
cp ops/stocks-bot-trader.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable stocks-bot-trader.service
loginctl enable-linger lui-tortuya

# 5. Install crontab (preserves any existing entries)
crontab -l > /tmp/old.txt 2>/dev/null || true
cat /tmp/old.txt ops/crontab.txt | sort -u | crontab -

# 6. Verify
crontab -l | grep stocks_monitoring
systemctl --user status stocks-bot-trader.service
```

## Architecture

Three Python entrypoints orchestrated by cron + systemd:

- **`cli.run_scanner`** — daily 1:10 PM PT (4:10 PM ET). Scans NDX∪SPX, writes watchlist to SQLite.
- **`cli.run_trader`** — systemd-supervised daemon, started 6:25 AM PT and stopped 1:05 PM PT by cron. Polls watchlist symbols every 30s (15s during the first 90 min of session). Manages entries + exits.
- **`cli.run_backtest`** — manual, replays the strategy over historical data and writes a CSV trade log + JSON summary.

State lives in `data/state.sqlite`. Logs land in `data/logs/` (daily JSON-line files).

## Halt mechanisms

- `data/halt.flag` file present → no new entries (existing positions managed normally).
- `cli.ops halt "reason"` sets both the file AND a state-table entry.
- Daily drawdown ≥ 3% auto-sets the state halt.
- Reset with `cli.ops resume`.

## Key files

| Path | Role |
|---|---|
| `bot/config.py` | env + typed strategy constants — change thresholds here |
| `bot/scanner.py` | daily scan rules |
| `bot/entry.py` / `bot/exit.py` | trigger + exit logic |
| `bot/executor.py` | Alpaca order calls |
| `bot/state.py` | SQLite layer |
| `backtest/engine.py` | bar-replay backtester |
