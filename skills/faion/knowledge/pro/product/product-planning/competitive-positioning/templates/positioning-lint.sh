#!/usr/bin/env bash
# positioning-lint.sh — flag comparative language and verify six-clause structure.
# Usage: ./positioning-lint.sh <positioning-statement.md>
# Wire into pre-commit on .aidocs/product_docs/positioning-statement.md
set -euo pipefail
FILE="${1:?usage: $0 <file.md>}"

# Banned: pure comparatives without a stated dimension and number.
BANNED='\b(better|easier|simpler|faster|cheaper|more powerful|most|best|leading|revolutionary|seamless)\b'
# Allowed pattern: a number + unit precedes or follows the comparative word ("5x faster", "30% cheaper at 10K subs")
ALLOWED_NUM='[0-9]+(x|%|\s*(min|hours|seats|subscribers|accounts))'

violations=$(grep -nEi "$BANNED" "$FILE" | grep -vE "$ALLOWED_NUM" || true)
if [ -n "$violations" ]; then
  echo "FAIL: comparative language without dimension+number:"
  echo "$violations"
  echo "-> rewrite as 'unlike X, we Y' with a concrete attribute."
  exit 1
fi

# Require structural skeleton: For/Who/Is/That/Unlike/We
missing=()
grep -qE "^For " "$FILE"    || missing+=("For")
grep -qE "^Who " "$FILE"    || missing+=("Who")
grep -qiE "\bis\b" "$FILE"  || missing+=("Is")
grep -qE "^That " "$FILE"   || missing+=("That")
grep -qE "^Unlike " "$FILE" || missing+=("Unlike")
grep -qE "^We " "$FILE"     || missing+=("We")

if [ ${#missing[@]} -gt 0 ]; then
  echo "FAIL: positioning statement missing clause(s): ${missing[*]}"
  echo "Required: For / Who / [Product] is / That / Unlike / We"
  exit 1
fi

echo "OK: positioning statement structurally sound."
