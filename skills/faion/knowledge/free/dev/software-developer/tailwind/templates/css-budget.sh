#!/usr/bin/env bash
# purpose: Check generated CSS bundle stays within budget
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# css-budget.sh — fail CI if prod CSS exceeds gzipped budget.
# Usage: css-budget.sh DIST_DIR MAX_KB
# Wire after pnpm build in CI.
set -euo pipefail

DIST="${1:?dist dir required}"
MAX_KB="${2:-50}"

shopt -s globstar
TOTAL=0
declare -a FILES=()

for f in "$DIST"/**/*.css; do
  [ -f "$f" ] || continue
  GZ=$(gzip -c "$f" | wc -c)
  KB=$(( (GZ + 1023) / 1024 ))
  TOTAL=$((TOTAL + KB))
  FILES+=("$KB KB  $f")
done

printf '%s\n' "${FILES[@]}"
echo "TOTAL: $TOTAL KB gzipped (budget: $MAX_KB KB)"

if (( TOTAL > MAX_KB )); then
  echo "FAIL — over budget by $((TOTAL - MAX_KB)) KB"
  echo "Investigate: rg -tcss '@apply' src/ ; rg --no-heading 'safelist' tailwind.config.*"
  exit 1
fi

echo "OK"
