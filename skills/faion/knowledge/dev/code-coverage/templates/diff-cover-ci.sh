#!/usr/bin/env bash
# purpose: CI step: produce coverage.xml then run diff-cover --fail-under=90.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Call from CI workflow.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
# scripts/diff-cover-ci.sh
# Run pytest with branch coverage, then gate new-code coverage via diff-cover.
# Usage: bash scripts/diff-cover-ci.sh [base-branch]
# Exits non-zero if new-code coverage is below 90%.
set -euo pipefail

BASE_BRANCH="${1:-origin/main}"

echo "==> Running pytest with coverage..."
pytest --cov=src --cov-branch --cov-report=xml --cov-report=term-missing

echo "==> Running diff-cover against ${BASE_BRANCH}..."
diff-cover coverage.xml \
  --compare-branch="${BASE_BRANCH}" \
  --fail-under=90 \
  --html-report diff-coverage.html

echo "==> diff-coverage report: diff-coverage.html"
