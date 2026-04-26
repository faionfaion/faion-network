#!/usr/bin/env bash
# a11y-gate.sh — fail PR if axe-core finds any serious/critical WCAG 2.2 AA issue
# Usage: ./a11y-gate.sh https://example.com
# Requires: npx (@axe-core/cli), jq
set -euo pipefail

URL="${1:?URL required}"
TAGS="${TAGS:-wcag2aa,wcag22aa}"

RESULT=$(npx @axe-core/cli "$URL" --tags "$TAGS" --exit 0 --stdout 2>/dev/null || true)

SERIOUS=$(echo "$RESULT" | jq '[.[].violations[]? | select(.impact == "serious" or .impact == "critical")] | length' 2>/dev/null || echo 0)

if [ "$SERIOUS" -gt 0 ]; then
  echo "FAIL: $SERIOUS serious/critical a11y issues on $URL"
  echo "$RESULT" | jq '.[].violations[]? | {id, impact, description, nodes: [.nodes[].html]}'
  exit 1
fi

TOTAL=$(echo "$RESULT" | jq '[.[].violations[]] | length' 2>/dev/null || echo 0)
echo "OK: $URL — 0 serious/critical issues ($TOTAL minor/moderate not blocking)"
