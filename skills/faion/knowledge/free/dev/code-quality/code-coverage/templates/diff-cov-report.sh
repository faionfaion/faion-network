#!/usr/bin/env bash
# diff-cov-report.sh — enforce diff-coverage and emit uncovered lines for agent.
# Usage: diff-cov-report.sh [base-branch] [target-percent]
# Example: diff-cov-report.sh origin/main 90
set -euo pipefail

BASE="${1:-origin/main}"
TARGET="${2:-90}"

# Run full test suite with branch coverage
pytest --cov=src --cov-branch --cov-report=xml -q

# Run diff-cover: fails if diff-coverage < TARGET
diff-cover coverage.xml \
  --compare-branch="$BASE" \
  --fail-under="$TARGET" \
  --markdown-report diff-cov.md \
  --json-report   diff-cov.json

echo ""
echo "## Agent-ready: uncovered changed lines per file"
jq -r '
  .src_stats | to_entries[]
  | select(.value.uncovered_lines | length > 0)
  | "FILE: \(.key)\nUNCOVERED_LINES: \(.value.uncovered_lines | join(","))\n"
' diff-cov.json
