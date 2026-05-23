#!/usr/bin/env bash
# purpose: Last-30-day DORA snapshot from git log + deploy.log
# consumes: deploy.log (one ISO 8601 UTC timestamp per line)
# produces: DF + Change Lead Time mean (stdout)
# depends-on: content/01-core-rules.xml#pair-dora-metrics, ai-pr-bot-split
# token-budget-impact: ~150 tokens when loaded as context
#
# Usage: ./dora-quick.sh [days=30]
set -euo pipefail

DAYS="${1:-30}"
SINCE="${DAYS} days ago"

# Deployment Frequency
DEPLOYS=$(awk -v cutoff="$(date -u -d "$SINCE" +%s 2>/dev/null || date -u -v-"${DAYS}"d +%s)" '
  { cmd="date -u -d \""$0"\" +%s 2>/dev/null || date -u -j -f \"%Y-%m-%dT%H:%M:%SZ\" \""$0"\" +%s"
    cmd | getline t; close(cmd)
    if (t > cutoff) c++ }
  END { print c+0 }' deploy.log 2>/dev/null || echo "0")

echo "Deployment Frequency: $(echo "scale=2; $DEPLOYS / $DAYS" | bc) /day (last ${DAYS}d)"

# Change Lead Time (commit ts → deploy ts, mean over matched commits)
LEAD_SECS=$(git log --since="$SINCE" --pretty=format:"%H %at" 2>/dev/null | \
  while read -r sha ts; do
    dep_ts=$(grep -m1 "$sha" deploy.log 2>/dev/null | \
             xargs -I{} date -u -d "{}" +%s 2>/dev/null || true)
    [ -n "$dep_ts" ] && echo "$((dep_ts - ts))"
  done | awk '{s+=$1; n++} END{ if(n) printf "%.0f\n", s/n }')

if [ -n "$LEAD_SECS" ] && [ "$LEAD_SECS" -gt 0 ]; then
  LEAD_H=$(echo "scale=1; $LEAD_SECS / 3600" | bc)
  echo "Change Lead Time (h, mean): ${LEAD_H}h"
else
  echo "Change Lead Time: n/a (no matched commits in deploy.log)"
fi

echo ""
echo "Note: CFR and MTTR require PagerDuty / incident log integration."
echo "Note: tag bot commits and report human/bot split before publishing DF."
