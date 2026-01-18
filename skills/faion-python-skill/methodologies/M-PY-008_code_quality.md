# M-PY-008: Code Quality

## Metadata
- **Category:** Development/Python
- **Difficulty:** Beginner
- **Tags:** #dev, #python, #quality, #methodology
- **Agent:** faion-code-agent

---

## Problem

Code quality degrades over time. Inconsistent formatting causes merge conflicts. Bugs slip through without linting. Technical debt accumulates silently. You need automated quality gates.

## Promise

After this methodology, your Python codebase will have consistent formatting, automated linting, and quality checks that catch issues before they become problems.

## Overview

Modern Python uses ruff for linting, black for formatting, and pre-commit for automation. These tools run fast and catch issues early.

---

## Framework

### Step 1: Install Tools

```bash
# Using poetry
poetry add --group dev ruff black isort mypy pre-commit

# Using pip
pip install ruff black isort mypy pre-commit
```

### Step 2: Configure Ruff

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "DTZ",  # flake8-datetimez
    "T10",  # flake8-debugger
    "EM",   # flake8-errmsg
    "ISC",  # flake8-implicit-str-concat
    "ICN",  # flake8-import-conventions
    "PIE",  # flake8-pie
    "PT",   # flake8-pytest-style
    "Q",    # flake8-quotes
    "RET",  # flake8-return
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
    "ARG",  # flake8-unused-arguments
    "PTH",  # flake8-use-pathlib
    "RUF",  # Ruff-specific
]
ignore = [
    "E501",   # Line too long (handled by formatter)
    "B008",   # Do not perform function call in argument defaults
    "RUF001", # Ambiguous unicode character
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG001", "S101"]
"__init__.py" = ["F401"]

[tool.ruff.lint.isort]
known-first-party = ["my_package"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Step 3: Configure Black

```toml
# pyproject.toml
[tool.black]
target-version = ["py311"]
line-length = 88
include = '\.pyi?$'
exclude = '''
/(
    \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
    | migrations
)/
'''
```

### Step 4: Configure mypy

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = ["external_library.*"]
ignore_missing_imports = true
```

### Step 5: Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - types-requests
```

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Step 6: Makefile Commands

```makefile
.PHONY: lint format check test all

lint:
	ruff check .

lint-fix:
	ruff check --fix .

format:
	ruff format .

check-format:
	ruff format --check .

type-check:
	mypy .

test:
	pytest

all: format lint type-check test
```

### Step 7: CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Check formatting
        run: poetry run ruff format --check .

      - name: Lint
        run: poetry run ruff check .

      - name: Type check
        run: poetry run mypy .

      - name: Test
        run: poetry run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Step 8: EditorConfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.{yaml,yml,json,toml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

---

## Templates

### Security Scanning

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main]
  schedule:
    - cron: "0 0 * * *"

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r src/ -c pyproject.toml

      - name: Run Safety
        run: |
          pip install safety
          safety check
```

```toml
# pyproject.toml
[tool.bandit]
exclude_dirs = ["tests", "venv"]
skips = ["B101"]  # Skip assert warnings
```

### Code Complexity

```toml
# pyproject.toml - Add to ruff config
[tool.ruff.lint]
select = [
    # ... existing rules ...
    "C90",  # mccabe complexity
]

[tool.ruff.lint.mccabe]
max-complexity = 10
```

---

## Examples

### Import Sorting

```python
# Before
from my_package import helper
import os
from typing import Optional
import sys
from django.db import models
import requests

# After (auto-sorted by ruff/isort)
import os
import sys
from typing import Optional

import requests
from django.db import models

from my_package import helper
```

### Auto-fixed Issues

```python
# Before
x = [1,2,3]
y = dict(a=1,b=2)
if x == []:
    pass
name = "hello"  + "world"
unused_var = 42

# After (ruff --fix)
x = [1, 2, 3]
y = {"a": 1, "b": 2}
if not x:
    pass
name = "hello" + "world"
# unused_var removed if flagged
```

### Type Ignore Comments

```python
# When you need to suppress warnings
result = some_untyped_library.function()  # type: ignore[no-untyped-call]

# More specific ignores
x: str = possibly_none  # type: ignore[assignment]
```

---

## Common Mistakes

1. **Ignoring pre-commit** - Always install and use pre-commit hooks
2. **Too many ignores** - Fix issues instead of ignoring them
3. **Inconsistent config** - Single source of truth in pyproject.toml
4. **No CI enforcement** - Quality checks must run in CI
5. **Outdated tools** - Keep ruff, black, mypy updated

---

## Checklist

- [ ] ruff configured for linting
- [ ] black or ruff-format for formatting
- [ ] mypy configured with strict mode
- [ ] pre-commit hooks installed
- [ ] CI pipeline runs all checks
- [ ] EditorConfig present
- [ ] Security scanning enabled
- [ ] Complexity limits set
- [ ] Team agrees on rules

---

## Next Steps

- M-PY-004: Pytest Testing
- M-DO-001: CI/CD GitHub Actions

---

*Methodology M-PY-008 v1.0*
