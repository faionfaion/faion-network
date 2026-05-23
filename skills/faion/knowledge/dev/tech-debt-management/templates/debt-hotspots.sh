#!/usr/bin/env bash
# debt-hotspots.sh — files most frequently changed AND most complex.
# Requires: git, lizard (pip install lizard)
# Usage: ./debt-hotspots.sh [repo-path]
# Output: rank by (churn, complexity) — top 20 highest-leverage debt targets
set -euo pipefail
cd "${1:-.}"

# Top-50 most-churned files in last 12 months
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -50 \
  > /tmp/churn.txt

echo "rank  churn  complexity  file"
echo "----  -----  ----------  ----"

while read -r count file; do
  if [[ -f "$file" ]]; then
    cmplx=$(lizard "$file" 2>/dev/null | awk '/^[0-9]+/ {sum+=$2} END {print sum+0}')
    printf "%4s  %5s  %10s  %s\n" "-" "$count" "$cmplx" "$file"
  fi
done < /tmp/churn.txt | sort -k2,2 -rn -k3,3 -rn | head -20 | nl -w4 -s"  "
