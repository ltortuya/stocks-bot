#!/usr/bin/env bash
# Run a stocks-bot routine non-interactively via Claude Code CLI.
# Wired by cron on the mini PC. Usage: scripts/run-routine.sh <routine-name>
# e.g. scripts/run-routine.sh pre-market

set -euo pipefail

ROUTINE="${1:?usage: scripts/run-routine.sh <routine-name>}"
ROOT="/home/lui-tortuya/stocks_monitoring"
LOG_DIR="$ROOT/data/logs"
LOG="$LOG_DIR/routine-${ROUTINE}-$(date +%Y-%m-%d).log"
mkdir -p "$LOG_DIR"

{
  echo
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') — running ${ROUTINE} ==="

  cd "$ROOT"

  # Pull latest strategy/code; warn-but-continue on failure.
  if ! git pull --rebase origin main; then
    echo "[warn] git pull failed; continuing with local copy"
  fi

  # Make claude visible to this subshell.
  export PATH="$HOME/.local/bin:$PATH"

  # Run the routine.
  claude --print \
    --allowed-tools Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch \
    --permission-mode bypassPermissions \
    "Read CLAUDE.md, then read routines/${ROUTINE}.md, then execute the workflow defined there exactly as written. The repo is your working directory. End with a git commit + push to main per the routine's commit step (skip the commit if the routine says to skip on no-op)."

  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') — ${ROUTINE} done ==="
} >> "$LOG" 2>&1
