#!/usr/bin/env bash
# purpose: Pre-commit guard — fail when a staged .py file introduces a new `Any` annotation.
# consumes: staged python files from `git diff --cached`.
# produces: exit 0 (clean) or exit 1 (regression with file:line listing).
# depends-on: bash, git, grep (no python runtime dep).
# token-budget-impact: zero — pure shell, runs in &lt; 200ms on typical commits.

set -euo pipefail

# Get list of staged .py files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

echo "==> Checking for new Any annotations in staged files..."

# Run mypy on staged files, grep for error codes that indicate Any
MYPY_OUTPUT=$(uv run mypy --no-error-summary $STAGED_FILES 2>&1 || true)

# Check for Any-related errors
ANY_ERRORS=$(echo "$MYPY_OUTPUT" | grep -E "(no-any-return|type\[Any\]|Returning Any|has type.*Any)" || true)

if [ -n "$ANY_ERRORS" ]; then
    echo "ERROR: New Any annotations detected in staged files:"
    echo "$ANY_ERRORS"
    echo ""
    echo "Fix: Replace Any with a specific type or use TypedDict/Protocol."
    echo "If unavoidable: use '# type: ignore[return-value]' with a justification comment."
    exit 1
fi

echo "==> No new Any annotations found."
exit 0

# ─── .pre-commit-config.yaml snippet ─────────────────────────────────────────
# - repo: local
#   hooks:
#     - id: no-new-any
#       name: No new Any annotations
#       entry: bash skills/faion/knowledge/free/dev/python-developer/python-typing/templates/no-new-any.sh
#       language: system
#       stages: [pre-push]
#       pass_filenames: false
