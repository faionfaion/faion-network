#!/usr/bin/env bash
# no-new-any.sh — Pre-commit script: fail if a touched .py file introduces a new Any annotation.
# Usage: add as a pre-commit hook (see pre-commit config below)
# Requires: mypy installed in the project venv

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
