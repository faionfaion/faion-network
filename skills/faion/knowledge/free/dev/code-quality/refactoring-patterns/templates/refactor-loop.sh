#!/usr/bin/env bash
# refactor-loop.sh — apply one refactoring pattern, test, commit, repeat.
# Usage: refactor-loop.sh <target-file> <test-command> [max-iterations]
# Example: refactor-loop.sh src/payments.py "pytest tests/test_payments.py" 5
set -euo pipefail

TARGET="${1:?path required}"
TESTS="${2:?test command required}"
MAX="${3:-5}"

for i in $(seq 1 "$MAX"); do
  echo "=== Iteration $i ==="
  PLAN=$(claude -p "Pick exactly ONE refactoring pattern from this catalog: \
[extract-method, extract-class, replace-conditional-with-polymorphism, \
introduce-parameter-object, replace-magic-numbers, decompose-conditional, \
rename-for-clarity, move-method]. \
Apply it to: $(cat "$TARGET") \
Constraints: \
- Behavior preservation is mandatory. Cite which test(s) verify the affected code. \
- Output JSON: {\"pattern\": \"...\", \"justification\": \"...\", \"unified_diff\": \"...\", \"test_command\": \"...\"}. \
- If no catalog pattern fits cleanly, return {\"pattern\": null, \"reason\": \"...\"}.")

  PATTERN=$(echo "$PLAN" | jq -r '.pattern')
  [ "$PATTERN" = "null" ] && { echo "No more refactors available."; break; }

  echo "Applying: $PATTERN"
  echo "$PLAN" | jq -r '.unified_diff' | git apply --3way

  if eval "$TESTS"; then
    git add -A
    git commit -m "refactor: $PATTERN in $(basename "$TARGET")"
    echo "Committed: $PATTERN"
  else
    git checkout -- .
    echo "Reverted: $PATTERN broke tests"
    break
  fi
done
