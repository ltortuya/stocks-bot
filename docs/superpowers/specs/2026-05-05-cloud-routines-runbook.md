# Cloud Routines & Local Cron — Runbook

Date: 2026-05-05
Status: canonical (retrospective from 2026-05-05 key-rotation incident)

## Goal

Document the actual production topology of the trading bot's scheduled jobs and the runbook for any change that touches credentials or routine config. `routines/README.md` describes the *intended* cloud setup but assumes a single execution surface; in reality the bot runs on **two parallel systems** that both need synchronized credentials. This doc captures that.

## What happened on 2026-05-05

- 06:58 AM PT — user reported a Telegram alert about missing API keys.
- Investigation found two cloud `pre-market` routines on the same cron: one working (hardcoded keys baked into prompt as a `.env` heredoc), one broken (clean prompt expecting environment-variable secrets that were never wired). The broken duplicate had been firing alongside the working one daily, and today it alerted.
- Diagnosis showed an incomplete migration started 2026-04-27 (likely when Opus 4.7 dropped) that aimed to replace the hardcoded-keys workaround with the canonical environment-variable setup documented in `routines/README.md`. The new routine config was created, but env secrets were never set on the routine and the prompt was never written past `"scan the market"`.
- Migration completed in-session: rotated keys (Alpaca paper + Telegram bot), set env secrets on the cloud routine, rewrote prompt to read CLAUDE.md → routines/pre-market.md, bumped model to `claude-opus-4-7[1m]`.
- Mid-session, the **mini PC midday routine** aborted with Alpaca 401 because its local `.env` still had the old keys. Mini PC `.env` was updated and midday re-fired cleanly. **This was the gotcha:** rotating keys requires updating *all three* surfaces, not just the cloud routine.

## Production topology

The bot has three credential-bearing surfaces. Any rotation must hit all three.

| Surface | Location | What runs there | Credentials live in |
|---|---|---|---|
| **Cloud routine** | `claude.ai/code/routines` (env `env_01RJmXKgu2agUu87A4iKUxvb`) | `pre-market` (4 AM PT weekdays) | Routine UI env-vars panel |
| **Mini PC cron** | `lui-tortuya@192.168.1.111:~/stocks_monitoring/` | `market-open`, `midday`, `daily-summary`, `weekly-review`, `intraday-check` (×2/day) | `~/stocks_monitoring/.env` |
| **Local Windows** | `c:/Users/ltort/stocks monitoring/` | Interactive `/pre-market`, `/midday`, `/trade`, `/portfolio` slash commands | `c:/Users/ltort/stocks monitoring/.env` |

The mini PC and Windows surfaces each have a full clone of the repo and their own `.env`. The cloud routine has the repo cloned per-run and reads secrets from the routine env-var panel — never from a `.env` file.

## Cloud routine canonical config

When creating or updating a cloud routine, this is the shape that matches `routines/README.md`:

```json
{
  "name": "Stocks bot — <routine>",
  "cron_expression": "<UTC cron>",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "env_01RJmXKgu2agUu87A4iKUxvb",
      "events": [{
        "data": {
          "uuid": "<fresh v4 uuid>",
          "session_id": "",
          "type": "user",
          "parent_tool_use_id": null,
          "message": {
            "content": "You are running today's <ROUTINE> routine for the stocks-monitoring trading bot.\n\nRead CLAUDE.md, then read routines/<ROUTINE>.md, then execute the workflow exactly as documented — STEP 1 through STEP N, including the mandatory git add + commit + push to main.\n\nEnv vars (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_ENDPOINT, ALPACA_DATA_ENDPOINT, PERPLEXITY_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID) are pre-set on this routine. Do NOT create or source a .env file. If any wrapper reports \"KEY not set in environment\", send one Telegram alert naming the missing var and exit.",
            "role": "user"
          }
        }
      }],
      "session_context": {
        "model": "claude-opus-4-7[1m]",
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch"],
        "sources": [{
          "git_repository": {
            "url": "https://github.com/ltortuya/stocks-bot",
            "allow_unrestricted_git_push": true
          }
        }]
      }
    }
  }
}
```

Anti-patterns to refuse:
- `.env` heredoc embedded in the prompt (leaks creds via routine config and contradicts CLAUDE.md "no .env in cloud" rule).
- `outcomes` block with auto-generated branch (`claude/*`) — pushes go to a stray branch instead of `main`, so the work is invisible from the user's working tree.
- Bare `"scan the market"` style prompts — the routine must read CLAUDE.md and the relevant `routines/*.md` so behavior stays sourced from version control, not the routine config.

## Key rotation runbook

When rotating Alpaca paper keys, Telegram bot token, Perplexity, or Google service-account JSON:

1. **Rotate the key at the source** (Alpaca dashboard / @BotFather / Perplexity / GCP).
2. **Update mini PC `.env`**:
   ```bash
   ssh lui-tortuya@192.168.1.111
   sed -i 's|^KEY_NAME=.*$|KEY_NAME=NEWVALUE|' ~/stocks_monitoring/.env
   cd ~/stocks_monitoring && bash scripts/alpaca.sh account   # 200 OK = good
   ```
3. **Update local Windows `.env`** (`c:/Users/ltort/stocks monitoring/.env`) — same key/value.
4. **Update cloud routine env-var panel** at `claude.ai/code/routines/<trigger_id>` — paste the new value, save.
5. **Verify all three:**
   - Local: `bash scripts/alpaca.sh account` (or `telegram.sh "test"` etc.)
   - Mini PC: same, via SSH.
   - Cloud: trigger the routine via "Run Now" and watch for a successful commit on `main` within ~5 min.

Rotation order matters: rotating before any surface is updated will cause every in-flight run to fail. Either accept that one fire-cycle dies, or stage updates fast enough to land between cron firings.

## Verification checklist before declaring a routine "deployed"

A routine is not deployed until all of these pass:

- [ ] Prompt reads `CLAUDE.md` and the relevant `routines/*.md` — does **not** hardcode workflow logic in the prompt.
- [ ] Env-var secrets are set on the routine (not in a `.env` heredoc in the prompt).
- [ ] `sources` block includes `allow_unrestricted_git_push: true` and the correct repo URL.
- [ ] No `outcomes` block (so commits go to `main`, not a feature branch).
- [ ] Cron expression converted from CT (the original guide's tz) → UTC (what the cloud expects).
- [ ] One successful "Run Now" producing a commit on `main` and no error Telegram.
- [ ] No duplicate routine on the same cron — check `RemoteTrigger {action: "list"}` for collisions.

## Drift detection

Drift between the three credential surfaces is invisible until something fires and fails. A periodic sanity check could catch it earlier — possible follow-ups:

- **Daily-summary routine extension:** at the end of `daily-summary.md`, fire a tiny check that hits Alpaca `account` from each available surface and Telegrams a one-liner if any return non-200. This catches stale credentials before they cause a missed trading-day signal.
- **Routine inventory script:** local helper that lists all cloud routines + their cron expressions and flags duplicates or missing env-vars. Can be a wrapper around `RemoteTrigger {action: "list"}` plus a hand-maintained allowlist of expected routines.

Neither is implemented today — flagged for future consideration.

## Files touched in this incident

- `c:/Users/ltort/stocks monitoring/.env` — Alpaca keys updated.
- `lui-tortuya@192.168.1.111:~/stocks_monitoring/.env` — Alpaca keys updated.
- Cloud routine `trig_01WAvRr2jq1Tak15zRhLuUmQ` (`Stocks bot — pre-market`) — prompt rewritten, model bumped to Opus 4.7 (1M ctx), `sources` added.
- Cloud routine `trig_013iN9v7MUgVegJYo837DcLK` (`pre-market` orphan) — disabled. Pending user deletion at https://claude.ai/code/routines.

No code changes — this was a config + credentials operation only.
