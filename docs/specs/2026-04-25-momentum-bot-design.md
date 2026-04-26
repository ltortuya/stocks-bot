# Momentum Breakout Trading Bot — Design

**Date:** 2026-04-25
**Status:** Draft (awaiting user approval before implementation plan)
**Owner:** Lui Tortuya
**Account:** Alpaca paper (`PA32A9R0JNE6`), $100K starting equity

## 1. Goal

Build a Python trading bot that:

1. Scans NDX∪SPX daily for momentum breakout setups
2. Monitors qualifying setups intraday and executes entries on confirmed breakouts
3. Manages exits via fixed targets, stops, trailing stops, and time stops
4. Runs against Alpaca paper API; structured to flip to live with one config change later
5. Includes a backtester so the strategy can be validated on historical data before any capital risk

Runs on the existing Ubuntu mini PC (`192.168.1.111`) under cron + systemd.

## 2. Non-Goals (current phase)

- No live (real-money) trading
- No options, crypto, futures
- No machine learning or LLM-in-the-loop
- No portfolio optimization beyond max-3-positions
- No web UI; dashboards out of scope (CLI + Telegram only)

## 3. Strategy Specification

### 3.1 Universe

Per scan cycle, build the candidate universe:

- **Base:** S&P 500 ∪ NASDAQ 100 (deduped, ~530 names)
- **Source:** Static CSVs in `data/universe/sp500.csv` and `data/universe/ndx.csv`, refreshed monthly via `scripts/refresh_universe.py` (Wikipedia tables)
- **Filters applied each scan:**
  - `last_close > $10`
  - `30-day avg dollar volume > $25M` (`avg_close × avg_volume`)
  - Not in exclusion list (`data/universe/exclusions.csv`):
    - **Leveraged ETFs** (any 2x/3x — TQQQ, SQQQ, etc.) — none expected in NDX/SPX but defensive
    - **Inverse ETFs**
    - **ADRs**: identified via Alpaca `assets` endpoint where `country != "USA"` *or* hardcoded list of common ADR tickers (TSM, ASML, NVO, etc.). Refreshed monthly.

Result: ~400–450 names per scan.

### 3.2 Daily Scan (end-of-day, ~4:05 PM ET)

For each universe symbol, check **all five** conditions on the just-closed daily bar:

1. **Today's % change ≥ +4.0%** (`(close - prev_close) / prev_close >= 0.04`)
2. **Relative volume ≥ 1.8×** (today's daily volume / 20-day avg daily volume — see §3.4 for intraday version used at entry)
3. **Close > 20 SMA** AND **Close > 50 SMA** (simple moving averages of daily closes)
4. **20-day high break** OR **within 2% of 20-day high** — where "20-day high" = the highest daily high of the **prior 20 sessions** (excluding today). Pass if `today_close >= prior_20d_high * 0.98`.
5. **No earnings within next 5 trading days** (yfinance earnings calendar)

Every symbol that passes all 5 → added to next-day watchlist with the following stored fields:

```json
{
  "symbol": "AAPL",
  "scan_date": "2026-04-27",
  "signal_high": 215.42,
  "signal_low": 207.15,
  "signal_close": 213.80,
  "atr_14": 4.21,
  "rvol_eod": 2.31,
  "earnings_next": "2026-05-02",
  "is_active": true,
  "breakout_attempts": 0
}
```

### 3.3 Intraday Entry (next trading day)

For each watchlist symbol, on each polling cycle:

1. **Time gates:**
   - Skip during the first 5 min after market open (no entries before 9:35 AM ET)
   - No new entries after 2:30 PM ET (existing positions still managed)
2. **Gap check** (only on the first cycle of the day for that symbol): if `today_open >= signal_high * 1.08`, mark symbol **gapped — skip for the day**
3. **Trigger:** `last_trade_price > signal_high`
4. **Volume confirmation** (both must hold):
   - Current 5-min bar volume > prior 5-min bar volume
   - Current 5-min bar volume > 20-bar average 5-min volume (rolling, intraday)
5. **Position-cap check:** open positions < 3
6. **Order:** stop-limit
   - `stop = signal_high + $0.02`
   - `limit = stop × 1.003` (30 bps slippage allowance)
   - `time_in_force = day`
   - If unfilled by 3:55 PM ET → cancel
7. **On fill:** persist position, attach exit orders (§3.5), Telegram alert

### 3.4 Relative Volume — Two Modes

**Intraday RVOL (used at entry-confirmation time):**
- `today_cumulative_volume_at_T / avg_cumulative_volume_at_T_over_prior_20_sessions`
- Implementation: at scan time + first cycle of each trading day, fetch 1-min bars for prior 20 sessions for each watchlist symbol; build per-symbol "expected cumulative volume by minute-of-day" curve; cache in SQLite. At each polling cycle compute today's cumulative volume up to the current minute and divide.
- **Fallback** if compute is too slow: today's daily total / 20-day daily avg (the simpler version).

**EOD RVOL (used in scan):**
- Always the simple form: today's daily volume / 20-day avg daily volume.

### 3.5 Exits

After fill, attach managed exits. The bot owns the exit logic — initially a single OCO bracket, adjusted as conditions evolve:

- **Profit target:** sell 100% at `entry × 1.10` (limit order, GTC)
- **Hard stop:** sell 100% at `max(signal_low, entry × 0.95)` (stop-market, GTC) — i.e. whichever stop is tighter (closer to entry)
- **Trailing stop activation:** when `unrealized_gain >= 6%`, replace fixed stop with trailing stop. Distance = **5% below `highest_price_since_entry`** (assumption — user spec didn't specify trailing distance, this matches the hard-stop %), updated each polling cycle as `highest_price_since_entry` advances
- **Time stop:** at 3:50 PM ET on the 5th trading day of the trade (entry day counts as day 1), sell at market regardless of P&L. Mon entry → Fri 3:50 PM exit.
- **Earnings rule:** if a position has earnings within next 1 trading day:
  - If `unrealized_gain > 0` → hold through earnings
  - If `unrealized_gain <= 0` → sell at market by 3:55 PM ET on the day before earnings

Exit orders are tracked in state. Bot reconciles on every cycle: if Alpaca reports the position closed, remove from local state and log realized P&L.

### 3.6 Failed-Breakout Handling

A "failed breakout" = the entry triggered (order filled or attempted) but price falls back below `signal_high` within 30 minutes of trigger.

- On failed breakout: mark watchlist symbol `is_active = false` for the rest of the day
- **Reactivation (one shot):** if later in the same session the price re-crosses `signal_high` AND volume confirmation passes (both checks of §3.3 step 4), set `is_active = true` and increment `breakout_attempts`. Total max **2 attempts per symbol per day** (initial breakout + 1 reclaim). After the second failure, mark dead for the day. — This matches the user's "cancel watchlist symbol after one failed breakout unless it reclaims high with volume" rule.

### 3.7 Risk Rules

- **Per-trade risk:** 1.5% of current equity. `qty = floor(0.015 × equity / (entry - stop))`. If `qty < 1`, skip the trade.
- **Max open positions:** 3. New entries skipped if at cap.
- **Max daily new entries:** 5 — *defensive addition*, not in user spec. Prevents a runaway day where the scanner produces 20 setups and we burn margin on all of them. Adjust or remove on user feedback.
- **Daily drawdown halt:** if today's realized + unrealized P&L ≤ -3% of starting-day equity, set halt flag (no new entries; existing positions managed normally) — *defensive addition*, not in user spec.
- **Manual kill switch:** presence of `data/halt.flag` halts all new entries on next cycle (existing positions still managed); Telegram alert when triggered.

## 4. Architecture

### 4.1 Process Topology

Three Python entrypoints, all on the mini PC:

| Process | Schedule | Lifecycle |
|---|---|---|
| `run_scanner.py` | cron, 4:05 PM ET Mon–Fri | One-shot, ~30–60s runtime |
| `run_trader.py` | systemd service, started 9:25 AM ET, stopped 4:05 PM ET | Long-running daemon, polling loop |
| `run_backtest.py` | manual / cron-able | One-shot, minutes-to-hours depending on date range |

A small wrapper `scripts/start_trader.sh` and `scripts/stop_trader.sh` are invoked by cron to start/stop the systemd service at the right times. Systemd handles crash recovery during market hours.

### 4.2 Module Layout

```
stocks_monitoring/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── docs/
│   └── specs/
│       └── 2026-04-25-momentum-bot-design.md  (this file)
├── bot/
│   ├── __init__.py
│   ├── config.py            # env loading, constants, ET/UTC helpers
│   ├── universe.py          # build/cache eligible symbol list
│   ├── data/
│   │   ├── __init__.py
│   │   ├── base.py          # MarketDataProvider abstract interface
│   │   ├── alpaca_data.py   # concrete impl: REST + (later) WebSocket
│   │   └── earnings.py      # yfinance earnings wrapper
│   ├── indicators.py        # SMA, ATR, RVOL (intraday + EOD)
│   ├── scanner.py           # daily scan, writes watchlist to state
│   ├── entry.py             # entry trigger + volume confirmation
│   ├── exit.py              # TP / SL / trail / time-stop / earnings
│   ├── risk.py              # sizing, max-positions, halt checks
│   ├── executor.py          # AlpacaExecutor (place/cancel/replace orders)
│   ├── reconcile.py         # sync local state with Alpaca on startup + each cycle
│   ├── state.py             # SQLite persistence (positions, watchlist, fills, halts)
│   ├── alerts.py            # Telegram wrapper
│   └── logger.py            # structured JSON logs, daily rotation
├── cli/
│   ├── run_scanner.py
│   ├── run_trader.py
│   ├── run_backtest.py
│   ├── refresh_universe.py
│   └── ops.py               # admin: list-positions, force-flatten, set-halt
├── backtest/
│   ├── __init__.py
│   ├── engine.py            # historical replay (5-min bar walk)
│   ├── metrics.py           # CAGR, max DD, win rate, profit factor, Sharpe
│   └── report.py            # write trade log CSV + summary
├── data/
│   ├── universe/
│   │   ├── sp500.csv
│   │   ├── ndx.csv
│   │   └── exclusions.csv
│   ├── state.sqlite
│   ├── halt.flag            # presence = halt
│   └── logs/                # daily rotated *.jsonl
├── tests/
│   ├── test_indicators.py
│   ├── test_risk_sizing.py
│   ├── test_entry_logic.py
│   ├── test_exit_logic.py
│   ├── test_state.py
│   └── fixtures/            # canned bar data
└── ops/
    ├── stocks-bot-trader.service   # systemd unit
    └── crontab.txt                  # cron entries (scanner + start/stop trader)
```

**Modular data layer:** `bot/data/base.py` defines `MarketDataProvider` ABC (methods: `get_bars`, `get_last_trade`, `get_clock`, `subscribe(symbols)`). `alpaca_data.py` implements REST polling. Future WebSocket impl drops in without strategy code changes.

### 4.3 Trader Polling Loop

```
loop:
    if market_closed: sleep(60); continue
    cycle_start = now()
    try:
        clock = data.get_clock()
        if not clock.is_open: stop_trader(); break

        # 1. Reconcile open positions with Alpaca
        reconcile_positions()

        # 2. Manage existing positions (exits)
        for pos in open_positions:
            update_trailing_stop(pos)
            check_time_stop(pos)
            check_earnings_exit(pos)

        # 3. Look for new entries (only if not at max & not halted)
        if can_enter_new():
            for sym in active_watchlist:
                if entry.check_trigger(sym): place_entry_order(sym)

        # 4. Heartbeat
        log.heartbeat(cycle_start, open_positions, watchlist_size)
        consecutive_failures = 0
    except (NetworkError, ApiError) as e:
        consecutive_failures += 1
        log.warn(e)
        if consecutive_failures >= 3:
            alerts.send(f"3 consecutive cycle failures: {e}")
        sleep(backoff(consecutive_failures))  # 5s, 15s, 60s, 60s...
        continue

    elapsed = now() - cycle_start
    interval = 15 if first_90_min else 30
    sleep(max(0, interval - elapsed))
```

## 5. Data Sources

| Need | Source | Notes |
|---|---|---|
| Daily bars (scan) | Alpaca `/v2/stocks/{sym}/bars?timeframe=1Day` | Free with paper account |
| 5-min & 1-min bars (intraday + RVOL curve) | Alpaca bars API | IEX feed (free) — sufficient for our purposes |
| Last trade price | Alpaca `/v2/stocks/{sym}/trades/latest` | Free |
| Account/positions/orders | Alpaca `/v2/account`, `/v2/positions`, `/v2/orders` | Free |
| Earnings calendar | `yfinance` (`Ticker.calendar`) | Free; structure allows swap to paid source later |
| Universe constituents | Wikipedia tables (S&P 500, NASDAQ 100) → CSV | Refresh monthly via `refresh_universe.py` |
| ADR identification | Alpaca `assets` endpoint `country` field + hardcoded list | Refreshed in same monthly job |

## 6. State Persistence (SQLite)

`data/state.sqlite` schema:

```sql
CREATE TABLE watchlist (
  scan_date TEXT,
  symbol TEXT,
  signal_high REAL,
  signal_low REAL,
  signal_close REAL,
  atr_14 REAL,
  rvol_eod REAL,
  earnings_next TEXT,
  is_active INTEGER DEFAULT 1,
  breakout_attempts INTEGER DEFAULT 0,
  PRIMARY KEY (scan_date, symbol)
);

CREATE TABLE positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  symbol TEXT,
  entry_order_id TEXT,
  entry_time TEXT,
  entry_price REAL,
  qty INTEGER,
  signal_high REAL,
  signal_low REAL,
  initial_stop REAL,
  current_stop REAL,
  highest_price_since_entry REAL,
  trailing_active INTEGER DEFAULT 0,
  status TEXT,             -- open | closed
  exit_time TEXT,
  exit_price REAL,
  exit_reason TEXT,        -- target | stop | trail | time | earnings | manual
  realized_pnl REAL
);

CREATE TABLE fills (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  position_id INTEGER,
  alpaca_order_id TEXT,
  side TEXT, qty INTEGER, price REAL, filled_at TEXT
);

CREATE TABLE rvol_curves (
  symbol TEXT, minute_of_day INTEGER, avg_cum_volume REAL,
  computed_at TEXT, PRIMARY KEY (symbol, minute_of_day)
);

CREATE TABLE halts (
  triggered_at TEXT, reason TEXT, cleared_at TEXT
);

CREATE TABLE cycles (
  cycle_at TEXT PRIMARY KEY, duration_ms INTEGER,
  positions_open INTEGER, watchlist_size INTEGER
);
```

## 7. Order Lifecycle

1. **Entry order** (stop-limit): submitted when trigger fires. Stored with `position` row in `pending` state.
2. **On fill:** position promoted to `open`. Bracket exit orders submitted:
   - Take-profit: limit at `entry × 1.10`, GTC
   - Stop-loss: stop-market at `current_stop`, GTC
3. **Trailing stop transition:** when `last_price >= entry × 1.06`, cancel stop-loss and replace with new stop-market at `highest × 0.95`. Re-replace each cycle when `highest_price_since_entry` advances.
4. **Time stop:** at 3:50 PM ET on day-of-entry + 5 trading days, cancel TP+SL, market sell.
5. **Earnings exit:** at 3:55 PM ET day-before-earnings, if unprofitable: cancel TP+SL, market sell.

All cancel/replace operations must be **idempotent** — bot tolerates Alpaca returning "order not found" (already filled/cancelled) and reconciles state from `/v2/positions` source-of-truth.

## 8. Backtester

**Approach:** event-replay over historical 5-min bars from Alpaca.

For each `date` in backtest range:
1. **At simulated EOD:** run scanner using bars `<= date` only (strict no-lookahead)
2. **Build watchlist** for `date + 1`
3. **Walk through `date+1`'s 5-min bars** for each watchlist symbol:
   - Apply gap check on first bar
   - Check entry trigger + volume confirmation each bar
   - On trigger: assume fill at `signal_high + 1 cent` (conservative slippage model)
4. **For each open position**, walk subsequent 5-min bars:
   - Check stops (intra-bar high/low used to detect stop hits, fill at stop price + slippage)
   - Check trailing stop activation and updates
   - Check time stop on day 5
5. **Record every trade** to `backtest/results/<run_id>/trades.csv`
6. **Compute summary** to `backtest/results/<run_id>/summary.json`:
   - Total return, CAGR, max drawdown, win rate, avg win, avg loss, profit factor, Sharpe (assume 252 trading days, risk-free = 0)

CLI: `python -m cli.run_backtest --start 2024-01-01 --end 2026-04-01 --equity 100000`

**Note on data limits:** Alpaca historical 5-min bars require either IEX feed (free, lower volume) or SIP feed (paid). Spec assumes IEX is sufficient for development; we'll validate during implementation.

## 9. Logging & Alerts

### 9.1 Logging
- All modules use `bot/logger.py` (Python `logging` configured for JSON output)
- Daily-rotated files: `data/logs/trader-YYYY-MM-DD.jsonl`, `data/logs/scanner-YYYY-MM-DD.jsonl`
- Log levels: DEBUG (cycle minutiae), INFO (signals, orders, fills), WARN (retries, partial failures), ERROR (uncaught)
- Heartbeat record per cycle includes: `cycle_at`, `duration_ms`, `positions_open`, `watchlist_size`, `consecutive_failures`

### 9.2 Telegram Alerts
Reuse `TELEGRAM_TOKEN` + `TELEGRAM_CHAT_ID` from `C:/Users/ltort/.env`. Send on:
- Trader start / stop
- Watchlist generated (count + top 5 by RVOL)
- Entry signal triggered (symbol, qty, entry price, stop, target)
- Position closed (symbol, P&L, reason)
- Halt activated (with reason)
- 3 consecutive cycle failures
- Any uncaught exception (with stack trace, then process exits — systemd restarts)

## 10. Configuration

`bot/config.py` reads from `C:/Users/ltort/.env` (existing) and exposes typed constants:

```python
ALPACA_API_KEY: str
ALPACA_API_SECRET: str
ALPACA_BASE_URL: str        # paper-api.alpaca.markets/v2
TELEGRAM_TOKEN: str
TELEGRAM_CHAT_ID: str

POLL_INTERVAL_SEC: int = 30
POLL_INTERVAL_FAST_SEC: int = 15
FAST_POLL_END_MIN: int = 90       # first 90 min of session

MIN_PRICE: float = 10.0
MIN_DOLLAR_VOL: float = 25_000_000
PCT_CHANGE_MIN: float = 0.04
RVOL_MIN: float = 1.8
NEAR_BREAKOUT_PCT: float = 0.02
LOOKBACK_BREAKOUT: int = 20

PER_TRADE_RISK_PCT: float = 0.015
MAX_OPEN_POSITIONS: int = 3
MAX_DAILY_NEW_ENTRIES: int = 5
DAILY_DRAWDOWN_HALT_PCT: float = -0.03

PROFIT_TARGET_PCT: float = 0.10
HARD_STOP_PCT: float = 0.05
TRAIL_ACTIVATION_PCT: float = 0.06
TRAIL_DISTANCE_PCT: float = 0.05
TIME_STOP_DAYS: int = 5
GAP_SKIP_PCT: float = 0.08

NO_ENTRY_FIRST_MIN: int = 5
NO_NEW_ENTRY_AFTER: str = "14:30"   # ET
TRADER_END_TIME: str = "15:55"      # ET (cancel unfilled, last management cycle)

EXCHANGE_TZ: str = "America/New_York"
```

All thresholds editable in one place; no magic numbers in strategy modules.

## 11. Testing Strategy

`pytest` covers the deterministic core:
- `test_indicators.py`: SMA / ATR / RVOL math against canned fixtures
- `test_risk_sizing.py`: position sizing with edge cases (entry near stop → qty 0 skip)
- `test_entry_logic.py`: trigger + volume-confirmation truth table
- `test_exit_logic.py`: each exit path (TP, SL, trail activation, trail update, time stop, earnings)
- `test_state.py`: SQLite migrations, position open/close round-trip
- `test_reconcile.py`: bot state vs. Alpaca state divergence cases (filled-while-offline, externally-cancelled, etc.)

Mock Alpaca client (`tests/fakes/fake_alpaca.py`) used in unit tests + as the data layer for backtest dry-runs. CI not in scope yet — `pytest` runs locally and on the mini PC pre-deploy.

## 12. Deployment

**Mini PC** (`192.168.1.111`, Ubuntu, existing breakwater automation host):

```
~/stocks_monitoring/                  # repo clone
~/stocks_monitoring/.venv/            # python venv
```

**Cron** (added to existing `crontab -e`):
```
# Stocks bot
5  16 * * 1-5  cd ~/stocks_monitoring && .venv/bin/python -m cli.run_scanner    >> data/logs/scanner.log 2>&1
25  9 * * 1-5  systemctl --user start stocks-bot-trader
5  16 * * 1-5  systemctl --user stop  stocks-bot-trader
0   3 1 * *    cd ~/stocks_monitoring && .venv/bin/python -m cli.refresh_universe >> data/logs/universe.log 2>&1
```

**Systemd unit** (`~/.config/systemd/user/stocks-bot-trader.service`):
```ini
[Unit]
Description=Stocks momentum trader
After=network-online.target

[Service]
WorkingDirectory=/home/lui-tortuya/stocks_monitoring
ExecStart=/home/lui-tortuya/stocks_monitoring/.venv/bin/python -m cli.run_trader
Restart=on-failure
RestartSec=10
StandardOutput=append:/home/lui-tortuya/stocks_monitoring/data/logs/trader-systemd.log
StandardError=inherit

[Install]
WantedBy=default.target
```

`.env` mirrored from main rig OR a dedicated paper-only `.env` on the mini PC (cleaner separation).

## 13. Open Questions / Future Work

- **Universe refresh source**: Wikipedia is convenient but has been known to break. If/when it does, switch to a paid maintained source (e.g. iShares constituent files for SPY/QQQ).
- **Intraday RVOL curve compute cost**: with ~20 watchlist symbols × 20 sessions × 390 minutes, that's ~156K data points. Should fit in <2s with batched Alpaca calls but TBD; fallback to simple form is acceptable.
- **Earnings data accuracy**: yfinance pulls from Yahoo, which has occasional gaps for less-followed names. NDX/SPX coverage is generally complete. Worth adding a sanity check at scan time.
- **Slippage model in backtest**: currently +1¢ on stop fills. Real slippage on momentum breakouts is often worse. Phase 2: estimate from realized fills vs trigger price during paper-trading and back-fit a more conservative model.
- **No alpha decay analysis yet**: spec doesn't include strategy parameter sweep. Once backtester works, run a sweep over `RVOL_MIN`, `PCT_CHANGE_MIN`, `PROFIT_TARGET_PCT` to see whether current values are robust or over-fit.

## 14. Rollout Phases

1. **Phase 1 (this spec)**: build everything, run backtest on 2024–early 2026 data, review results
2. **Phase 2**: deploy to mini PC, paper trade for 4 weeks, compare paper P&L vs backtest expectations
3. **Phase 3**: tune parameters based on Phase 2 evidence (or kill the strategy if it doesn't hold up)
4. **Phase 4 (future)**: consider live trading at small size if Phase 2/3 results justify it
