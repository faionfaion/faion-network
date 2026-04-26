#!/bin/bash
# pre-push hook — XP "never break the build"
# Install: cp templates/pre-push-hook.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
set -e
echo "Running pre-push checks..."

# Run tests (fail fast on first failure)
pytest --tb=short -x -q

# Run linter + format check
ruff check . && ruff format --check .

echo "Pre-push checks passed."
