#!/usr/bin/env bash
# Perplexity API wrapper for research routines.
# Usage: bash scripts/perplexity.sh "<prompt text>"
# Exit codes:
#   0  - success, response on stdout
#   2  - API error (after one retry)
#   3  - PERPLEXITY_API_KEY not set (caller falls back to native WebSearch)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "PERPLEXITY_API_KEY not set in environment" >&2
  exit 3
fi

PROMPT="${1:?usage: bash scripts/perplexity.sh \"<prompt text>\"}"
MODEL="${PERPLEXITY_MODEL:-sonar-pro}"

# Build JSON body via python to handle prompt escaping safely.
BODY=$(python3 -c '
import json, sys
prompt, model = sys.argv[1], sys.argv[2]
print(json.dumps({
  "model": model,
  "messages": [{"role": "user", "content": prompt}],
}))
' "$PROMPT" "$MODEL")

call_api() {
  curl -fsS --ssl-no-revoke --max-time 60 \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -X POST -d "$BODY" \
    "https://api.perplexity.ai/chat/completions"
}

RESPONSE="$(call_api 2>/dev/null)" || {
  sleep 3
  RESPONSE="$(call_api 2>/dev/null)" || {
    echo "Perplexity API failed after one retry" >&2
    exit 2
  }
}

# Extract content + citations.
python3 -c '
import json, sys
data = json.loads(sys.stdin.read())
content = data["choices"][0]["message"]["content"]
print(content)
citations = data.get("citations") or []
if citations:
    print()
    print("Sources:")
    for i, url in enumerate(citations, 1):
        print(f"  [{i}] {url}")
' <<< "$RESPONSE"
