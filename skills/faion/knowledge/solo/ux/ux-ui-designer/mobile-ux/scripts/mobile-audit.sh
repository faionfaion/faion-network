#!/usr/bin/env bash
# mobile-audit.sh — Lighthouse mobile performance audit
# Usage: bash mobile-audit.sh https://example.com
# Requires: lighthouse (npm install -g lighthouse), jq
# Output: Core Web Vitals + failed audits sorted by score

set -euo pipefail

URL="${1:?Usage: $0 <url>}"
OUT="lighthouse-mobile-$(date +%Y%m%d-%H%M).json"

echo "Running Lighthouse mobile audit: $URL"
echo "Output file: $OUT"
echo ""

lighthouse "$URL" \
  --output=json \
  --output-path="$OUT" \
  --form-factor=mobile \
  --throttling-method=simulate \
  --preset=perf \
  --chrome-flags="--headless --no-sandbox" \
  --quiet

echo "=== Core Web Vitals ==="
jq '{
  LCP:   .audits["largest-contentful-paint"].displayValue,
  FID:   .audits["max-potential-fid"].displayValue,
  CLS:   .audits["cumulative-layout-shift"].displayValue,
  TTI:   .audits["interactive"].displayValue,
  score: (.categories.performance.score * 100 | floor | tostring) + "%"
}' "$OUT"

echo ""
echo "=== Failed Audits (score < 0.9) ==="
jq '[.audits | to_entries[]
  | select(.value.score != null and .value.score < 0.9)
  | {id: .key, title: .value.title, score: (.value.score * 100 | floor)}
] | sort_by(.score)' "$OUT"

echo ""
echo "Targets: LCP < 2.5s | CLS < 0.1 | TTI < 5s"
echo "Full report: $OUT"
