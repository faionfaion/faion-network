#!/usr/bin/env bash
# bootstrap.sh — One-shot modern Python project bootstrap (uv + ruff + mypy + pytest)
# Usage: bash bootstrap.sh <project-name> [python-version]
# Default Python version: 3.12

set -euo pipefail

PROJECT=${1:?Usage: bootstrap.sh <project-name> [python-version]}
PY_VERSION=${2:-3.12}

echo "==> Bootstrapping: $PROJECT (Python $PY_VERSION)"

# Create project
uv init "$PROJECT" --python "$PY_VERSION"
cd "$PROJECT"
uv python pin "$PY_VERSION"

# Dev dependencies
uv add --dev pytest pytest-asyncio pytest-cov ruff mypy pre-commit

# Project structure
mkdir -p src/"${PROJECT//-/_}" tests
touch src/"${PROJECT//-/_}"/__init__.py
touch tests/__init__.py

# conftest.py
cat > tests/conftest.py << 'CONFTEST'
"""Shared test fixtures."""
import pytest
CONFTEST

# ruff pre-commit hooks
cat > .pre-commit-config.yaml << 'PRECOMMIT'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
PRECOMMIT

uv run pre-commit install

echo ""
echo "==> Project ready. Next steps:"
echo "    uv run pytest              # Run tests"
echo "    uv run ruff check . --fix  # Lint + fix"
echo "    uv run mypy src/           # Type check"
