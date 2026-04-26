#!/usr/bin/env bash
# scripts/typecheck-touched.sh
# Run mypy --strict only on Python files changed vs base branch.
# Usage: bash scripts/typecheck-touched.sh [base-ref]
# Exits 0 if no files changed or all pass.
set -euo pipefail

BASE_REF="${1:-origin/main}"

mapfile -t files < <(
  git diff --name-only --diff-filter=AM "$BASE_REF" -- '*.py' \
    | grep -v -E '^(migrations/|tests/fixtures/|conftest\.py$)'
)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No Python files changed."
  exit 0
fi

echo "Typechecking ${#files[@]} file(s) with mypy --strict..."
mypy --strict "${files[@]}"
