#!/usr/bin/env bash
# backlog-health.sh — weekly Linear backlog health check
# Usage: LINEAR_API_KEY=... TEAM_KEY=ENG bash backlog-health.sh
# Output: ~/backlog/YYYY-WNN/{issues.json,health.md,stale.txt}
# Requires: curl, jq, claude CLI

set -euo pipefail

TEAM_KEY=${TEAM_KEY:?set TEAM_KEY env var (e.g. ENG)}
WEEK=$(date +%Y-W%V)
OUT=~/backlog/"$WEEK"
mkdir -p "$OUT"

# 1. Pull all issues for team via Linear GraphQL
curl -s \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"{ issues(filter:{team:{key:{eq:\\\"$TEAM_KEY\\\"}}}) { nodes { id title state { name } updatedAt priority labels { nodes { name } } description } } }\"}" \
  https://api.linear.app/graphql > "$OUT/issues.json"

echo "Pulled $(jq '.data.issues.nodes | length' "$OUT/issues.json") issues"

# 2. Health metrics via jq
TOTAL=$(jq '.data.issues.nodes | length' "$OUT/issues.json")
STALE_CUTOFF=$(date -d '-180 days' -Iseconds 2>/dev/null || date -v-180d -Iseconds)

STALE=$(jq --arg cutoff "$STALE_CUTOFF" \
  '[.data.issues.nodes[] | select(.updatedAt < $cutoff)] | length' \
  "$OUT/issues.json")

echo "Total: $TOTAL | Stale (180d): $STALE | Stale%: $(( STALE * 100 / (TOTAL > 0 ? TOTAL : 1) ))%"

# 3. Generate stale candidate list
jq -r --arg cutoff "$STALE_CUTOFF" \
  '.data.issues.nodes[] | select(.updatedAt < $cutoff) |
   "\(.id) | \(.title) | last updated: \(.updatedAt)"' \
  "$OUT/issues.json" > "$OUT/stale.txt"

echo "Stale candidates → $OUT/stale.txt"

# 4. Claude health narrative (requires claude CLI)
if command -v claude &>/dev/null && [ -f ~/prompts/backlog-health.txt ]; then
  claude -p "$(cat ~/prompts/backlog-health.txt)" \
    --input-file "$OUT/issues.json" > "$OUT/health.md"
  echo "Health narrative → $OUT/health.md"
else
  echo "Skipping Claude narrative (no claude CLI or ~/prompts/backlog-health.txt)"
fi
