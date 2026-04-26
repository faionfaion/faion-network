#!/usr/bin/env bash
# bootstrap.sh — One-shot Python 3.12+ project bootstrap using uv
# Usage: bash bootstrap.sh <project-name>
# Requires: uv installed (curl -LsSf https://astral.sh/uv/install.sh | sh)

set -euo pipefail

PROJECT=${1:?Usage: bootstrap.sh <project-name>}

echo "==> Creating project: $PROJECT"
uv init "$PROJECT" --python 3.12
cd "$PROJECT"

echo "==> Pinning Python version"
uv python pin 3.12

echo "==> Adding dev dependencies"
uv add --dev pytest pytest-cov ruff mypy

echo "==> Creating project structure"
mkdir -p src/"${PROJECT//-/_}" tests

cat > src/"${PROJECT//-/_}"/__init__.py << 'EOF'
"""Package root."""
EOF

cat > tests/__init__.py << 'EOF'
EOF

cat > tests/conftest.py << 'EOF'
"""Shared test fixtures."""
import pytest
EOF

echo "==> Writing pyproject.toml tool config"
# (copy from templates/pyproject.toml and adjust project name)

echo "==> Installing pre-commit hooks"
uv add --dev pre-commit
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF
uv run pre-commit install

echo "==> Done. Run: uv run pytest"
