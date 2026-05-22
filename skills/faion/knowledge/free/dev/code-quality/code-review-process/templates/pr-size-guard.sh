# purpose: template for code-review-process (pr-size-guard.sh)
# consumes: code-review-process methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# pr-size-guard.sh — Warn above 400 lines, block above 1500 lines.
# Outputs GitHub Actions annotations: ::warning and ::error.
# Run: bash pr-size-guard.sh  (uses origin/main as base by default)

set -euo pipefail

BASE="${BASE:-origin/main}"
git fetch -q origin "${BASE#origin/}"

LINES=$(git diff --shortstat "$BASE"...HEAD | awk '{n=$4+$6} END{print n+0}')
WARN=400
FAIL=1500

echo "PR adds/removes $LINES lines total."

if [ "$LINES" -ge "$FAIL" ]; then
  echo "::error::PR too large ($LINES lines). Split into smaller PRs before merging."
  exit 1
fi

if [ "$LINES" -ge "$WARN" ]; then
  echo "::warning::PR is large ($LINES lines). Agent review quality drops above $WARN lines. Consider splitting."
fi

exit 0
