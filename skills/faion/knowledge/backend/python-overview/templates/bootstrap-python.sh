#!/usr/bin/env bash
# purpose: Bootstrap routing decision for a new Python project
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# bootstrap-python.sh — create a modern Python project with uv + ruff + mypy + pytest.
# Usage: bash scripts/bootstrap-python.sh <project-name>
set -euo pipefail

P=${1:?Usage: bootstrap-python.sh <project-name>}

uv init "$P" --python 3.12
cd "$P"
uv add --dev ruff mypy pytest pytest-cov

# Append tool config to pyproject.toml
python - <<'PY'
import pathlib

extra = """
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "C4", "UP", "SIM", "T20"]

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
addopts = "-q --strict-markers --strict-config"
"""

p = pathlib.Path("pyproject.toml")
p.write_text(p.read_text() + extra)
print("pyproject.toml updated")
PY

mkdir -p src tests

cat > "src/__init__.py" <<'EOF'
def hello() -> str:
    return "world"
EOF

cat > "tests/test_hello.py" <<'EOF'
from src import hello

def test_hello() -> None:
    assert hello() == "world"
EOF

uv run ruff check src tests
uv run mypy src
uv run pytest -q
echo "Bootstrap complete: $P"
