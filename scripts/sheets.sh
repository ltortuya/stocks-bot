#!/usr/bin/env bash
# Google Sheets dashboard writer.
# Usage: ROUTINE_NAME=<name> bash scripts/sheets.sh report
# Exit codes:
#   0 - success
#   2 - bad usage
#   4 - GOOGLE_SERVICE_ACCOUNT_JSON missing/unparseable
#   5 - data/dashboard-sheet-id.txt missing
#   6 - Sheets API failed after retry

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

cmd="${1:-}"
case "$cmd" in
  report)
    PY="$(command -v python3 || command -v python)"
    if [[ -z "$PY" ]]; then
      echo "python3/python not found on PATH" >&2
      exit 2
    fi

    set +e
    "$PY" "$ROOT/scripts/sheets_report.py"
    rc=$?
    set -e

    if [[ "$rc" -ne 0 ]]; then
      # Best-effort Telegram alert. Never let the alert itself fail the script.
      if [[ -x "$ROOT/scripts/telegram.sh" ]]; then
        bash "$ROOT/scripts/telegram.sh" \
          "🟥 sheets.sh failed (exit $rc) for routine ${ROUTINE_NAME:-unknown}" \
          >/dev/null 2>&1 || true
      fi
      exit "$rc"
    fi
    ;;
  *)
    echo "Usage: ROUTINE_NAME=<name> bash scripts/sheets.sh report" >&2
    exit 2
    ;;
esac
