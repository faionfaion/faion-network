#!/usr/bin/env bash
# heuristic-precheck.sh — automated pre-check with axe-core + Lighthouse
# Covers heuristics: #1 (system status), #4 (consistency), #5 (error prevention), #9 (error recovery)
# Usage: bash heuristic-precheck.sh https://example.com
# Requires: @axe-core/cli (npm install -g @axe-core/cli), lighthouse (npm install -g lighthouse), jq

set -euo pipefail

URL="${1:?Usage: $0 <url>}"

echo "=== Accessibility checks (heuristics #5 Error Prevention, #9 Error Recovery) ==="
axe "$URL" --reporter=v2 2>/dev/null \
  | jq '[.violations[]
      | {
          rule: .id,
          impact: .impact,
          description: .description,
          count: (.nodes | length)
        }
    ] | sort_by(.impact)' 2>/dev/null \
  || echo "axe-core not available — install: npm install -g @axe-core/cli"

echo ""
echo "=== Performance + Best Practices (heuristic #1 Visibility of System Status) ==="
lighthouse "$URL" \
  --output=json \
  --chrome-flags="--headless --no-sandbox" \
  --quiet 2>/dev/null \
  | jq '{
      performance:    (.categories.performance.score * 100 | floor),
      accessibility:  (.categories.accessibility.score * 100 | floor),
      best_practices: (.categories["best-practices"].score * 100 | floor),
      failed_audits: [
        .audits | to_entries[]
        | select(.value.score != null and .value.score < 0.5)
        | {id: .key, score: (.value.score * 100 | floor), title: .value.title}
      ]
    }' 2>/dev/null \
  || echo "lighthouse not available — install: npm install -g lighthouse"

echo ""
echo "Manual checks still required for heuristics:"
echo "  #2 Match real world — language audit"
echo "  #3 User control — undo/exit path verification"
echo "  #6 Recognition vs recall — option visibility"
echo "  #7 Flexibility — keyboard shortcut and power-user feature review"
echo "  #8 Aesthetic minimalist — visual hierarchy assessment"
echo "  #10 Help and documentation — help availability check"
