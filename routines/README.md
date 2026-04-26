# Cloud Routines

Five Claude Code cloud routines fire on cron. Each is a stateless container:
clone → read memory → call wrappers → write memory → commit + push → destroy.

## Cron schedules (America/Chicago)

| File                        | Cron             | When                |
|-----------------------------|------------------|---------------------|
| `pre-market.md`             | `0 6 * * 1-5`    | 6:00 AM weekdays    |
| `market-open.md`            | `30 8 * * 1-5`   | 8:30 AM weekdays    |
| `midday.md`                 | `0 12 * * 1-5`   | Noon weekdays       |
| `daily-summary.md`          | `0 15 * * 1-5`   | 3:00 PM weekdays    |
| `weekly-review.md`          | `0 16 * * 5`     | 4:00 PM Fridays     |

## Setup checklist (one-time per routine)

1. **Install the Claude GitHub App** on this repo (least-privilege, single-repo).
2. **Enable "Allow unrestricted branch pushes"** in the routine environment.
   Without this, `git push origin main` silently fails.
3. **Set environment variables on the routine** (NOT in a `.env` file):
   - `ALPACA_API_KEY` (required)
   - `ALPACA_SECRET_KEY` (required)
   - `ALPACA_ENDPOINT` (optional; defaults to paper)
   - `ALPACA_DATA_ENDPOINT` (optional)
   - `OPENAI_API_KEY` (required for research)
   - `OPENAI_MODEL` (optional; defaults to `gpt-4o-search-preview`)
   - `TELEGRAM_TOKEN` (required for notifications)
   - `TELEGRAM_CHAT_ID` (required for notifications)
4. **Paste the routine prompt verbatim** from the corresponding file. Do NOT paraphrase.
5. **Set the cron schedule** per the table above.
6. **Click "Run now"** once to verify before waiting for the cron.

## The mental model

The cloud runner is **stateless**. Git is the memory. If it's not pushed to
`main`, it didn't happen. Every routine ends with a mandatory commit + push.
