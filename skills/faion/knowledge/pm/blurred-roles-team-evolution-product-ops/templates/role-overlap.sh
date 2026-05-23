#!/usr/bin/env bash
# purpose: Emit per-author file-area distribution from git history
# consumes: git log
# produces: stdout: per-author file-area summary
# depends-on: git
# token-budget-impact: low
set -euo pipefail
SINCE="${1:-3 months ago}"
git log --since="$SINCE" --pretty=format: --name-only \
  | awk 'NF' \
  | sed 's|/.*||' \
  | sort | uniq -c | sort -rn \
  | head -20
echo "---"
echo "by author (top 5 dirs each):"
for a in $(git log --since="$SINCE" --format="%ae" | sort -u | head -10); do
  echo "== $a =="
  git log --since="$SINCE" --author="$a" --pretty=format: --name-only \
    | awk 'NF' | sed 's|/.*||' \
    | sort | uniq -c | sort -rn | head -5
done
