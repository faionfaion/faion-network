# TASK_000: Project Setup (Python)

<!-- SUMMARY: Initialize {project_name} Python project with full development infrastructure -->

## Complexity: normal
## Created: {YYYY-MM-DD}
## Project: {project_name}
## Depends on: none

---

## Description

Bootstrap Python project with:
- Poetry package management
- Directory structure
- Ruff (linter + formatter)
- mypy (type checking)
- pytest (testing)
- pre-commit hooks
- GitHub Actions CI

---

## Context

- **Constitution:** `aidocs/sdd/{project_name}/constitution.md`
- **Python Version:** 3.12+
- **Package Manager:** Poetry
- **Target Directory:** `{project_path}/`

---

## Goals

1. Initialize Poetry project
2. Create src layout directory structure
3. Configure Ruff for linting and formatting
4. Set up mypy for type checking
5. Configure pytest with coverage
6. Set up pre-commit hooks
7. Create GitHub Actions workflow
8. Create README with getting started

---

## Acceptance Criteria

- [ ] `poetry install` succeeds
- [ ] `make lint` (ruff check) passes
- [ ] `make format` (ruff format) passes
- [ ] `make typecheck` (mypy) passes
- [ ] `make test` (pytest) runs
- [ ] pre-commit hooks work
- [ ] CI pipeline is green
- [ ] README has getting started

---

## Technical Notes

```
pyproject.toml - Single config for all tools
src/{project_name}/ - Source code
tests/ - Test files
.github/workflows/ci.yml - CI pipeline
Makefile - Developer commands
```

---

## Out of Scope

- Application code
- Database setup
- Deployment config
- API documentation

---

## Subtasks

- [ ] 01. Create project directory
- [ ] 02. Initialize Poetry:
  ```bash
  poetry init --name {project_name} --python "^3.12" --no-interaction
  ```
- [ ] 03. Install dev dependencies:
  ```bash
  poetry add --group dev ruff mypy pytest pytest-cov pre-commit
  ```
- [ ] 04. Create directory structure:
  ```
  {project_name}/
  ├── src/{project_name}/
  │   ├── __init__.py
  │   └── py.typed
  ├── tests/
  │   ├── __init__.py
  │   └── conftest.py
  └── docs/
  ```
- [ ] 05. Configure Ruff in pyproject.toml:
  ```toml
  [tool.ruff]
  line-length = 100
  target-version = "py312"

  [tool.ruff.lint]
  select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]

  [tool.ruff.format]
  quote-style = "double"
  ```
- [ ] 06. Configure mypy in pyproject.toml:
  ```toml
  [tool.mypy]
  python_version = "3.12"
  strict = true
  warn_return_any = true
  warn_unused_configs = true
  ```
- [ ] 07. Configure pytest in pyproject.toml:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  addopts = "-v --cov=src --cov-report=term-missing"
  ```
- [ ] 08. Create .pre-commit-config.yaml:
  ```yaml
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.8.0
      hooks:
        - id: ruff
          args: [--fix]
        - id: ruff-format
    - repo: https://github.com/pre-commit/mirrors-mypy
      rev: v1.13.0
      hooks:
        - id: mypy
          additional_dependencies: []
  ```
- [ ] 09. Create .gitignore (Python template)
- [ ] 10. Create Makefile:
  ```makefile
  .PHONY: install lint format typecheck test all

  install:
  	poetry install

  lint:
  	poetry run ruff check .

  format:
  	poetry run ruff format .

  typecheck:
  	poetry run mypy src

  test:
  	poetry run pytest

  all: format lint typecheck test
  ```
- [ ] 11. Create .github/workflows/ci.yml:
  ```yaml
  name: CI
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: "3.12"
        - run: pip install poetry
        - run: poetry install
        - run: make all
  ```
- [ ] 12. Create README.md
- [ ] 13. Initialize pre-commit:
  ```bash
  poetry run pre-commit install
  ```
- [ ] 14. Initial commit

---

## Implementation

<!-- To be filled by executor -->

---

## Summary

<!-- To be filled after completion -->
