# Python Code Quality

**Black, isort, flake8, pre-commit hooks**

---

## Problem

Python code needs consistent formatting, import organization, and linting across the team.

## Framework

### Black Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
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

### isort Configuration

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip = [".venv", "migrations"]
known_first_party = ["apps", "config"]
known_third_party = ["django", "rest_framework", "fastapi"]
sections = [
    "FUTURE",
    "STDLIB",
    "THIRDPARTY",
    "FIRSTPARTY",
    "LOCALFOLDER",
]
```

### flake8 Configuration

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, E501, W503
exclude =
    .git,
    .venv,
    __pycache__,
    migrations,
    .mypy_cache,
per-file-ignores =
    __init__.py:F401
    tests/*:S101
```

### Running Tools

```bash
# Format with Black
black src/
black --check src/  # Check only

# Sort imports with isort
isort src/
isort --check-only src/  # Check only

# Lint with flake8
flake8 src/

# Run all (typical order)
isort src/ && black src/ && flake8 src/
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs
          - types-requests
```

### Install and Use Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### Makefile Integration

```makefile
.PHONY: format lint fix

format:
	isort src/ tests/
	black src/ tests/

lint:
	flake8 src/ tests/
	mypy src/

fix: format lint
```

## Templates

**Complete pyproject.toml tools section:**
```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
strict = true
```

## Sources

- [Black Documentation](https://black.readthedocs.io/) - Code formatter
- [isort Documentation](https://pycqa.github.io/isort/) - Import sorting
- [Flake8 Documentation](https://flake8.pycqa.org/) - Style guide enforcement
- [pre-commit Framework](https://pre-commit.com/) - Git hook management
- [mypy Configuration](https://mypy.readthedocs.io/en/stable/config_file.html) - Type checking setup

## Agent

Executed by: faion-code-agent, faion-devops-agent
