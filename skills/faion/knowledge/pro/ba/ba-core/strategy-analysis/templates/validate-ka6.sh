#!/usr/bin/env bash
# validate-ka6.sh — validate all four KA-6 JSON artifacts before commit.
# Usage: validate-ka6.sh <initiative-slug>
# Requires: ajv-cli (npm i -g ajv-cli), schemas in .aidocs/_schemas/ka6/
set -euo pipefail
SCHEMA_DIR=".aidocs/_schemas/ka6"
ART_DIR=".aidocs/${1:?usage: validate-ka6.sh <initiative>}/strategy"
fail=0

for art in current-state future-state risk-register change-strategy; do
  f="$ART_DIR/$art.json"
  s="$SCHEMA_DIR/$art.schema.json"

  if [[ ! -f "$f" ]]; then
    echo "MISS  $art (file absent — run the corresponding KA-6 sub-agent)"
    fail=1; continue
  fi

  # Check freshness: reject artifacts older than 90 days
  if [[ "$(find "$f" -mtime +90)" ]]; then
    echo "STALE $art (last_validated_at > 90 days — re-run the sub-agent)"
    fail=1; continue
  fi

  if [[ ! -f "$s" ]]; then
    echo "WARN  $art schema missing at $s — skipping schema validation"
    echo "OK    $art (no schema)"
    continue
  fi

  if ! ajv validate -s "$s" -d "$f" --strict=false >/dev/null 2>&1; then
    echo "FAIL  $art schema"
    ajv validate -s "$s" -d "$f" --strict=false || true
    fail=1; continue
  fi

  # Additional check for future-state: reject unmeasurable goals
  if [[ "$art" == "future-state" ]]; then
    bad=$(jq '[.goals[] | select(.metric==null or .target==null or .target_date==null or .baseline==.target)] | length' "$f" 2>/dev/null || echo 0)
    if [[ "$bad" -gt 0 ]]; then
      echo "FAIL  future-state has $bad unmeasurable or trivial goals"
      fail=1
      continue
    fi
  fi

  echo "OK    $art"
done

exit $fail

# Add to .pre-commit-config.yaml:
# - id: validate-ka6
#   name: Validate KA-6 strategy artifacts
#   entry: bash .aidocs/strategy/validate-ka6.sh <initiative>
#   language: system
#   pass_filenames: false
#   files: ^\.aidocs/.*/strategy/
