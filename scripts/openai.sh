#!/usr/bin/env bash
# Research wrapper. All market research goes through OpenAI's web-search-capable models.
# Usage: bash scripts/openai.sh "<query>"
# Exits with code 3 if OPENAI_API_KEY is unset so callers can fall back to native WebSearch.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

query="${1:-}"
if [[ -z "$query" ]]; then
  echo "usage: bash scripts/openai.sh \"<query>\"" >&2
  exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "WARNING: OPENAI_API_KEY not set. Fall back to WebSearch." >&2
  exit 3
fi

# Default to a model with built-in web browsing. Override via OPENAI_MODEL.
MODEL="${OPENAI_MODEL:-gpt-4o-search-preview}"

payload="$(python -c "
import json, sys
print(json.dumps({
    'model': sys.argv[1],
    'messages': [
        {'role': 'system', 'content': 'You are a precise financial research assistant. Use web search to verify every claim. Cite sources inline. Be concise — bullets, no fluff.'},
        {'role': 'user', 'content': sys.argv[2]},
    ],
}))
" "$MODEL" "$query")"

curl -fsS --ssl-no-revoke https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$payload"
echo
