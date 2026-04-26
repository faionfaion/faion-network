#!/usr/bin/env bash
# trend-snapshot-validate.sh <snapshot.json>
# Validates: 4 buckets, valid state, confidence in [0,1],
#            >=2 sources per bucket, no stale sources (>365 days).
set -euo pipefail

F="${1:?snapshot.json required}"
NOW=$(date -u +%s)

jq -e --argjson now "$NOW" '
  def stale(d): ($now - (d | fromdateiso8601)) > (365*86400);
  def valid_state: . as $s |
    ["accepted","contested","declining","emerging"] | index($s) != null;

  if (.buckets | length) != 4 then error("need exactly 4 buckets")
  else .buckets[] |
    if (.state | valid_state | not) then
      error("bad state in \(.name): \(.state)")
    elif (.confidence < 0 or .confidence > 1) then
      error("confidence out of range in \(.name)")
    elif ((.sources | length) < 2) then
      error("\(.name): need >=2 sources, got \(.sources | length)")
    elif (.confidence >= 0.6 and (.sources | length) < 2) then
      error("\(.name): confidence >=0.6 requires >=2 sources")
    elif any(.sources[]; stale(.published)) then
      error("\(.name): has stale source (>365 days old)")
    else .name
    end
  end
' "$F"

echo "OK: snapshot validation passed for $F"
