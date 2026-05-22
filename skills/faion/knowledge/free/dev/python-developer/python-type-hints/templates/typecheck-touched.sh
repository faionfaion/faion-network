#!/usr/bin/env bash
# purpose: Run mypy on changed files only
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# typecheck-touched.sh — Strict mypy on files changed vs main branch.
# Use as pre-push hook: runs only on files touched in the current branch.
# Requires: mypy + django-stubs installed in venv (uv run)

set -euo pipefail

BASE_BRANCH=${BASE_BRANCH:-main}

# Find .py files changed vs base branch
CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH"...HEAD -- '*.py' | grep -v migrations || true)

if [ -z "$CHANGED_FILES" ]; then
    echo "==> No Python files changed. Skipping type check."
    exit 0
fi

echo "==> Running mypy --strict on changed files:"
echo "$CHANGED_FILES" | sed 's/^/    /'

# Run mypy with strict overrides for touched files
# --no-error-summary: cleaner output
# --show-column-numbers: precise error location
uv run mypy \
    --strict \
    --no-error-summary \
    --show-column-numbers \
    $CHANGED_FILES

echo "==> mypy passed on all changed files."
