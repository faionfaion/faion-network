#!/usr/bin/env bash
# purpose: Lint positioning statement for missing elements
# consumes: positioning-canvas.md path
# produces: exit 0 if clean; exit 1 with violations
# depends-on: grep
# token-budget-impact: low
set -euo pipefail
F="${1:?path}"
v=0
grep -qi '## 1. Competitive Alternatives' "$F" || { echo "VIOLATION: missing alternatives section"; v=1; }
grep -qi 'do nothing\|spreadsheet' "$F" || { echo "VIOLATION: missing 'do nothing'/'spreadsheet' alternative"; v=1; }
grep -qi 'Quantified Value' "$F" || { echo "VIOLATION: missing quantified value translation"; v=1; }
grep -qi 'Trigger event' "$F" || { echo "VIOLATION: missing trigger event in best-fit"; v=1; }
grep -qi 'Positioning Statement' "$F" || { echo "VIOLATION: missing positioning statement"; v=1; }
exit "$v"
