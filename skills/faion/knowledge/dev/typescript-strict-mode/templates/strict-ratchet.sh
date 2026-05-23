#!/usr/bin/env bash
# purpose: Detect ratcheting of TS strict-mode flags
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# strict-ratchet.sh — fail CI if strict error count increases vs stored baseline.
# Wire as a required CI check on PRs.
# Commit .strict-baseline decreases as a sign of progress.
set -euo pipefail

BASE=".strict-baseline"
COUNT=$(npx tsc --noEmit --pretty false 2>&1 | grep -c "error TS" || true)
echo "current strict errors: $COUNT"

if [ ! -f "$BASE" ]; then
  echo "$COUNT" > "$BASE"
  echo "baseline written"
  exit 0
fi

PREV=$(cat "$BASE")
if (( COUNT > PREV )); then
  echo "FAIL — strict errors increased ($PREV -> $COUNT)"
  npx tsc --noEmit --pretty false 2>&1 | grep "error TS" | head -50
  exit 1
fi

if (( COUNT < PREV )); then
  echo "$COUNT" > "$BASE"
  echo "ratchet tightened ($PREV -> $COUNT) — commit .strict-baseline"
fi

echo "OK"
