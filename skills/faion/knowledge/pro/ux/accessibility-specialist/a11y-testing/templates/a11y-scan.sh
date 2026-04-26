#!/usr/bin/env bash
# a11y-scan.sh <URL> [--ci]
# Runs axe + Pa11y + Lighthouse; outputs reports/<host>/{axe.json,pa11y.json,lighthouse.json,summary.md}
# Requires: @axe-core/cli, pa11y, lighthouse (all global npm installs)
set -euo pipefail

URL="${1:?Usage: a11y-scan.sh <url> [--ci]}"
HOST=$(echo "$URL" | awk -F/ '{print $3}')
OUT="reports/$HOST"
mkdir -p "$OUT"

echo "Scanning: $URL"

# 1. axe-core scan (WCAG 2.1 + 2.2 AA tags)
axe "$URL" --tags wcag2aa,wcag21aa,wcag22aa --stdout > "$OUT/axe.json" || true

# 2. Pa11y scan (WCAG2AA standard)
pa11y --standard WCAG2AA --reporter json "$URL" > "$OUT/pa11y.json" || true

# 3. Lighthouse accessibility audit
lighthouse "$URL" \
  --only-categories=accessibility \
  --output=json \
  --output-path="$OUT/lighthouse.json" \
  --quiet \
  --chrome-flags="--headless"

# 4. Summary
node -e '
  const fs = require("fs"), p = process.argv[1];
  const ax = JSON.parse(fs.readFileSync(p + "/axe.json")).violations || [];
  const pa = JSON.parse(fs.readFileSync(p + "/pa11y.json")).issues || [];
  const lh = JSON.parse(fs.readFileSync(p + "/lighthouse.json")).categories.accessibility.score;
  const incomplete = JSON.parse(fs.readFileSync(p + "/axe.json")).incomplete || [];
  console.log([
    "# A11y Summary",
    "- Lighthouse score: " + ((lh * 100) | 0) + "/100",
    "- axe violations: " + ax.length,
    "- axe incomplete (not tested): " + incomplete.length,
    "- Pa11y issues: " + pa.length,
    "",
    "## axe Violations",
    ax.map(v => "- [" + v.impact + "] " + v.id + ": " + v.nodes.length + " instance(s)").join("\n"),
  ].join("\n"));
' "$OUT" > "$OUT/summary.md"

echo "Report: $OUT/summary.md"

# CI mode: exit 1 if any critical violations
if [[ "${2:-}" == "--ci" ]]; then
  CRITICAL=$(node -e '
    const ax = require("./'$OUT'/axe.json").violations || [];
    console.log(ax.filter(v => v.impact === "critical").length);
  ')
  if [[ "$CRITICAL" -gt 0 ]]; then
    echo "FAIL: $CRITICAL critical axe violations found."
    exit 1
  fi
fi
