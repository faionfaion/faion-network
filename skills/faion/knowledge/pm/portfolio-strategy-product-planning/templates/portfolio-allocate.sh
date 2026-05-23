#!/usr/bin/env bash
# purpose: Compute allocation across H1/H2/H3 horizons from bet list
# consumes: bets.csv: id,horizon,effort_pd
# produces: stdout: allocation pct per horizon
# depends-on: awk
# token-budget-impact: low
set -euo pipefail
CSV="${1:?path to bets.csv}"
awk -F, 'NR>1 {sum[$2]+=$3; total+=$3} END {
  for (h in sum) printf "%s: %.1f%%\n", h, sum[h]*100/total
}' "$CSV"
