#!/bin/bash
# Audit a Figma Sites published URL for accessibility and performance.
# Usage: ./audit-figma-sites.sh https://your-figma-site.figma.site
# Requires: Lighthouse CLI (npm i -g lighthouse), axe-cli (npm i -g axe-cli)

URL="$1"
REPORT_DIR="figma-sites-audit"
mkdir -p "$REPORT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "Running Lighthouse audit on $URL..."
npx lighthouse "$URL" \
  --output json,html \
  --output-path "$REPORT_DIR/lighthouse-$TIMESTAMP" \
  --chrome-flags="--headless" \
  --only-categories=accessibility,performance,best-practices

echo "Running axe accessibility scan..."
axe "$URL" --reporter json > "$REPORT_DIR/axe-$TIMESTAMP.json"

echo "Audit complete."
echo "Lighthouse: $REPORT_DIR/lighthouse-$TIMESTAMP.report.html"
echo "Axe: $REPORT_DIR/axe-$TIMESTAMP.json"
