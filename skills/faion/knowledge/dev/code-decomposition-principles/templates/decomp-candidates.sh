# purpose: template for code-decomposition-principles (decomp-candidates.sh)
# consumes: code-decomposition-principles methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# decomp-candidates.sh — surface files that likely need splitting.
# Emits: oversize files, high-complexity functions, high-churn hotspots.
# Usage: decomp-candidates.sh [src-dir] [line-threshold] [complexity-threshold]
set -euo pipefail

ROOT="${1:-.}"
THRESHOLD_LINES="${2:-300}"
THRESHOLD_CCN="${3:-15}"

echo "## Oversize files (> ${THRESHOLD_LINES} lines)"
find "$ROOT" -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' \
  -o -name '*.js' -o -name '*.go' \) \
  | xargs wc -l 2>/dev/null \
  | awk -v t="$THRESHOLD_LINES" '$1 > t && $2 != "total" {printf "%6d  %s\n", $1, $2}' \
  | sort -rn | head -30

echo ""
echo "## High-complexity functions (CCN > ${THRESHOLD_CCN})"
if command -v lizard >/dev/null 2>&1; then
  lizard -C "$THRESHOLD_CCN" "$ROOT" 2>/dev/null | tail -n +3 | head -20
else
  echo "  lizard not installed: pip install lizard"
fi

echo ""
echo "## Hotspots (high churn × large file — last 6 months)"
git -C "$ROOT" log --since='6 months ago' --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|go)$' \
  | sort | uniq -c | sort -rn | head -15
