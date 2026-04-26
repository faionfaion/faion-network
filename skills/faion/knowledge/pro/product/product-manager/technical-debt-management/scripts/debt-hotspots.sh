#!/usr/bin/env bash
# debt-hotspots.sh — find files most likely to be technical debt
# Input:  current git repo
# Output: TSV table to stdout + hotspots.jsonl for scanner subagent seed
# Usage:  ./debt-hotspots.sh [since=6.months.ago] [top=20]
set -euo pipefail

SINCE="${1:-6.months.ago}"
TOP="${2:-20}"
TMP="$(mktemp -d)"

git log --since="$SINCE" --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|rb)$' \
  | sort | uniq -c | sort -rn > "$TMP/churn.txt"

if command -v lizard >/dev/null; then
  lizard -l python -l javascript -l typescript -X -w 2>/dev/null \
    | awk -F, 'NR>1 {print $5"\t"$1}' | sort > "$TMP/cx.txt"
else
  awk '{a[$2]++} END{for(f in a) print a[f]"\t"f}' "$TMP/churn.txt" | sort > "$TMP/cx.txt"
fi

awk '{print $2"\t"$1}' "$TMP/churn.txt" | sort > "$TMP/churn_keyed.txt"
join -1 1 -2 2 "$TMP/churn_keyed.txt" "$TMP/cx.txt" 2>/dev/null \
  | awk '{print $1"\t"$2*$3"\t"$2"\t"$3}' \
  | sort -k2 -rn | head -n "$TOP" \
  | awk 'BEGIN{print "file\tscore\tchurn\tcomplexity"} {print}'

awk 'NR>1 {printf "{\"file\":\"%s\",\"score\":%s,\"churn\":%s,\"cx\":%s}\n",$1,$2,$3,$4}' \
  "$TMP/churn_keyed.txt" > hotspots.jsonl 2>/dev/null || true
echo "Written: hotspots.jsonl"
