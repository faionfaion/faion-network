#!/usr/bin/env bash
# purpose: Generate weekly product-metric rollup from data warehouse
# consumes: DW SQL (configurable) + week ISO arg
# produces: .aidocs/process/weekly-rollup-<week>.md
# depends-on: psql or duckdb
# token-budget-impact: low
set -euo pipefail
WEEK="${1:-$(date +%G-W%V)}"
OUT=".aidocs/process/weekly-rollup-${WEEK}.md"
mkdir -p "$(dirname "$OUT")"
cat > "$OUT" <<EOF
# Weekly Rollup ${WEEK}
- north-star metric: {{value}}
- weekly delta: {{delta}}
- top-3 wins: {{wins}}
- top-3 risks: {{risks}}
- asks: {{asks}}
EOF
echo "wrote: $OUT"
