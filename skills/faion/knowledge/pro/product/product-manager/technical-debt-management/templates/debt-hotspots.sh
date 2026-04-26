#!/usr/bin/env bash
# debt-hotspots.sh — find files most likely to be technical debt
# Usage: ./debt-hotspots.sh [since=6.months.ago] [top=20]
# Output: TSV table + JSONL file for scanner subagent consumption
set -euo pipefail

SINCE="${1:-6.months.ago}"
TOP="${2:-20}"
TMP="$(mktemp -d)"

# 1. churn: commits per file
git log --since="$SINCE" --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|rb)$' \
  | sort | uniq -c | sort -rn > "$TMP/churn.txt"

# 2. complexity proxy (lizard if available, else line count)
if command -v lizard >/dev/null; then
  lizard -l python -l javascript -l typescript -X -w 2>/dev/null \
    | awk -F, 'NR>1 {print $5"\t"$1}' | sort > "$TMP/cx.txt"
else
  awk '{ print FILENAME"\t"NR }' $(awk '{print $2}' "$TMP/churn.txt") 2>/dev/null \
    | awk '{a[$1]=$2} END{for (f in a) print a[f]"\t"f}' | sort > "$TMP/cx.txt"
fi

# 3. join and score: hotspot = churn * complexity
awk '{print $2"\t"$1}' "$TMP/churn.txt" | sort > "$TMP/churn_keyed.txt"
join -1 1 -2 2 "$TMP/churn_keyed.txt" "$TMP/cx.txt" 2>/dev/null \
  | awk '{print $1"\t"$2*$3"\t"$2"\t"$3}' \
  | sort -k2 -rn | head -n "$TOP" \
  | awk 'BEGIN{print "file\tscore\tchurn\tcomplexity"} {print}'

# 4. emit JSONL for scanner subagent
awk 'NR>1 {printf "{\"file\":\"%s\",\"score\":%s,\"churn\":%s,\"cx\":%s}\n",$1,$2,$3,$4}' \
  "$TMP/churn.txt" > "$TMP/hotspots.jsonl" 2>/dev/null || true
echo "--- hotspots.jsonl ---"
cat "$TMP/hotspots.jsonl"
