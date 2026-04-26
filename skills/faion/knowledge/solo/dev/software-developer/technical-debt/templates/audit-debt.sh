#!/usr/bin/env bash
# Surfaces unresolved TODO/HACK/FIXME/TECH_DEBT with git blame metadata and age.
# Usage: ./audit-debt.sh [directory]
# Output: file:line <tab> author <tab> age_days <tab> comment
set -euo pipefail

DIR=${1:-.}
PATTERN='TODO|HACK|FIXME|XXX|TECH_DEBT'

git grep -nE "$PATTERN" -- \
  "$DIR"/'*.py' "$DIR"/'*.ts' "$DIR"/'*.tsx' \
  "$DIR"/'*.go' "$DIR"/'*.rs' \
  2>/dev/null \
| while IFS=: read -r file line rest; do
    author=$(git blame -L "$line,$line" --porcelain "$file" 2>/dev/null \
      | awk '/^author /{$1=""; print substr($0,2); exit}')
    ts=$(git blame -L "$line,$line" --porcelain "$file" 2>/dev/null \
      | awk '/^author-time /{print $2; exit}')
    age_days=0
    if [[ -n "$ts" ]]; then
      age_days=$(( ( $(date +%s) - ts ) / 86400 ))
    fi
    printf '%s:%s\t%-25s\t%4dd\t%s\n' \
      "$file" "$line" "${author:-unknown}" "$age_days" "$rest"
  done \
| sort -t$'\t' -k3 -rn \
| head -50
