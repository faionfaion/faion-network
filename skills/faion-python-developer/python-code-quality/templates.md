# Python Code Quality Templates

Copy-paste configurations for Ruff, mypy, pre-commit, and CI/CD pipelines.

---

## pyproject.toml - Complete Configuration

### Minimal Setup (New Projects)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.11"
strict = true
```

### Standard Setup (Most Projects)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.14.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pre-commit>=4.0.0",
]

# ============================================================================
# RUFF CONFIGURATION
# ============================================================================

[tool.ruff]
target-version = "py311"
line-length = 88
exclude = [
    ".git",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    "migrations",
    "node_modules",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # Pylint
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default argument (FastAPI Depends)
    "PLR0913", # too many arguments
]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports in __init__
"tests/*" = ["S101", "ARG001", "PLR2004"]  # assert, unused args, magic values

[tool.ruff.lint.isort]
known-first-party = ["src", "app", "apps"]
section-order = [
    "future",
    "standard-library",
    "third-party",
    "first-party",
    "local-folder",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = true

# ============================================================================
# MYPY CONFIGURATION
# ============================================================================

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true
show_error_codes = true
show_column_numbers = true

# Per-module overrides
[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = ["migrations.*"]
ignore_errors = true

# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/migrations/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
fail_under = 80
show_missing = true
```

### Django Project Setup

```toml
[project]
name = "my-django-project"
version = "0.1.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.14.0",
    "django-stubs>=5.0.0",
    "djangorestframework-stubs>=3.15.0",
    "pytest>=8.0.0",
    "pytest-django>=4.9.0",
    "pytest-cov>=6.0.0",
    "pre-commit>=4.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88
exclude = [
    "migrations",
    "*/migrations/*",
    ".venv",
    "manage.py",
    "settings.py",  # Often has long lines
]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "DJ"]  # DJ = flake8-django
ignore = ["E501", "B008"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101", "ARG001"]
"conftest.py" = ["ARG001"]

[tool.ruff.lint.isort]
known-first-party = ["apps", "config"]
known-third-party = ["django", "rest_framework"]

[tool.mypy]
python_version = "3.11"
plugins = [
    "mypy_django_plugin.main",
    "mypy_drf_plugin.main",
]
strict = true

[[tool.mypy.overrides]]
module = ["*.migrations.*"]
ignore_errors = true

[tool.django-stubs]
django_settings_module = "config.settings"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = ["-v", "--tb=short", "--reuse-db"]
```

### FastAPI Project Setup

```toml
[project]
name = "my-fastapi-project"
version = "0.1.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.14.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "httpx>=0.28.0",
    "pre-commit>=4.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ASYNC"]  # ASYNC for async rules
ignore = ["E501", "B008"]  # B008: function call in default (FastAPI Depends)

[tool.ruff.lint.isort]
known-first-party = ["app", "src"]
known-third-party = ["fastapi", "pydantic", "sqlalchemy"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = ["-v", "--tb=short"]
```

---

## Pre-commit Configuration

### Standard .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
# Run: pre-commit install
# Update: pre-commit autoupdate

default_language_version:
  python: python3.11

repos:
  # ==========================================================================
  # General hooks
  # ==========================================================================
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
        args: [--unsafe]  # Allow custom tags
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-merge-conflict
      - id: debug-statements
      - id: detect-private-key
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master]

  # ==========================================================================
  # Python - Ruff (linting + formatting)
  # ==========================================================================
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      # Linter
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      # Formatter
      - id: ruff-format

  # ==========================================================================
  # Python - Type checking
  # ==========================================================================
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-PyYAML
        args: [--ignore-missing-imports]

  # ==========================================================================
  # Security
  # ==========================================================================
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
```

### Django Pre-commit Configuration

```yaml
# .pre-commit-config.yaml for Django projects

default_language_version:
  python: python3.11

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: debug-statements
      - id: no-commit-to-branch

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs>=5.0.0
          - djangorestframework-stubs>=3.15.0
          - types-requests
        args: [--config-file=pyproject.toml]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-c, pyproject.toml, -r, apps/]
        additional_dependencies: ["bandit[toml]"]
```

### Minimal Pre-commit (Fast Feedback)

```yaml
# .pre-commit-config.yaml - minimal, fast setup

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: no-commit-to-branch
```

---

## GitHub Actions Workflows

### Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run Ruff linter
        run: uv run ruff check .

      - name: Run Ruff formatter
        run: uv run ruff format --check .

      - name: Run mypy
        run: uv run mypy src/

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests with coverage
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: true
```

### Matrix Testing (Multiple Python Versions)

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest -v

  coverage:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests with coverage
        run: uv run pytest --cov=src --cov-report=xml --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### Complete CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"

jobs:
  # ==========================================================================
  # Quality Gates
  # ==========================================================================
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Ruff lint
        run: uv run ruff check . --output-format=github

      - name: Ruff format
        run: uv run ruff format --check .

  type-check:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: mypy
        run: uv run mypy src/

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Bandit
        run: uv run bandit -r src/ -c pyproject.toml

      - name: Safety check
        run: uv run pip-audit

  # ==========================================================================
  # Tests
  # ==========================================================================
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: [lint, type-check]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml --cov-report=term-missing

      - name: Check coverage threshold
        run: uv run coverage report --fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: true

      - name: Coverage comment
        if: github.event_name == 'pull_request'
        uses: py-cov-action/python-coverage-comment-action@v3
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # ==========================================================================
  # Pre-commit (catch-all)
  # ==========================================================================
  pre-commit:
    name: Pre-commit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Run pre-commit
        uses: pre-commit/action@v3.0.1
```

---

## Makefile

### Standard Makefile

```makefile
.PHONY: help install dev lint format type-check test coverage clean

PYTHON := python3.11
UV := uv

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	$(UV) sync

dev:  ## Install dev dependencies
	$(UV) sync --dev
	pre-commit install

lint:  ## Run linter
	$(UV) run ruff check .

format:  ## Format code
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

type-check:  ## Run type checker
	$(UV) run mypy src/

test:  ## Run tests
	$(UV) run pytest

coverage:  ## Run tests with coverage
	$(UV) run pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

check: lint type-check test  ## Run all checks

clean:  ## Clean build artifacts
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## VS Code Settings

### .vscode/settings.json

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "python.analysis.typeCheckingMode": "standard",
  "python.analysis.autoImportCompletions": true,
  "ruff.lint.args": ["--config=pyproject.toml"],
  "ruff.format.args": ["--config=pyproject.toml"],
  "mypy-type-checker.args": ["--config-file=pyproject.toml"],
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

### .vscode/extensions.json

```json
{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.mypy-type-checker",
    "tamasfe.even-better-toml"
  ]
}
```

---

## Bandit Configuration

### pyproject.toml (Bandit section)

```toml
[tool.bandit]
exclude_dirs = ["tests", "migrations", ".venv"]
skips = ["B101"]  # Skip assert_used (we use it in tests)

[tool.bandit.assert_used]
skips = ["*_test.py", "test_*.py", "conftest.py"]
```

---

## EditorConfig

### .editorconfig

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
max_line_length = 88

[*.{json,yaml,yml,toml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

---

## Installation Commands

### Using uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init my-project
cd my-project

# Add dev dependencies
uv add --dev ruff mypy pytest pytest-cov pre-commit bandit

# Install pre-commit hooks
uv run pre-commit install

# Run checks
uv run ruff check .
uv run ruff format .
uv run mypy src/
uv run pytest
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dev dependencies
pip install ruff mypy pytest pytest-cov pre-commit bandit

# Install pre-commit hooks
pre-commit install

# Run checks
ruff check .
ruff format .
mypy src/
pytest
```
