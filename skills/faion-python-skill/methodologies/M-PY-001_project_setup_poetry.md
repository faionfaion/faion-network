# M-PY-001: Python Project Setup with Poetry

## Metadata
- **Category:** Development/Python
- **Difficulty:** Beginner
- **Tags:** #dev, #python, #setup, #methodology
- **Agent:** faion-code-agent

---

## Problem

Setting up a Python project correctly takes time and expertise. Wrong setup leads to dependency hell, difficult deployment, and team friction. You need a standardized approach that works for any project size.

## Promise

After this methodology, you will have a professional Python project structure with dependency management, virtual environments, and best practices built in from day one.

## Overview

Poetry is the modern standard for Python project management. It handles dependencies, virtual environments, and packaging in one tool.

---

## Framework

### Step 1: Install Poetry

```bash
# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Verify installation
poetry --version
```

### Step 2: Create New Project

```bash
# New project from scratch
poetry new my-project

# Or initialize in existing directory
poetry init
```

**Project structure:**
```
my-project/
├── pyproject.toml      # Project config & dependencies
├── poetry.lock         # Locked dependency versions
├── README.md
├── my_project/
│   └── __init__.py
└── tests/
    └── __init__.py
```

### Step 3: Configure pyproject.toml

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "my_project"}]

[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^4.1"
black = "^24.0"
isort = "^5.13"
mypy = "^1.8"
ruff = "^0.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true
```

### Step 4: Manage Dependencies

```bash
# Add production dependency
poetry add django

# Add dev dependency
poetry add --group dev pytest

# Remove dependency
poetry remove django

# Update dependencies
poetry update

# Show installed packages
poetry show

# Show dependency tree
poetry show --tree
```

### Step 5: Use Virtual Environment

```bash
# Enter virtual environment
poetry shell

# Run command in venv without entering
poetry run python my_script.py

# Run tests
poetry run pytest

# Get venv path
poetry env info --path
```

### Step 6: Lock & Export

```bash
# Lock dependencies (auto on add/remove)
poetry lock

# Export to requirements.txt (for deployment)
poetry export -f requirements.txt --output requirements.txt

# Export with dev dependencies
poetry export -f requirements.txt --with dev --output requirements-dev.txt
```

---

## Templates

### Minimal pyproject.toml

```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Standard Project Structure

```
project-name/
├── pyproject.toml
├── poetry.lock
├── README.md
├── .gitignore
├── .env.example
├── Makefile
├── project_name/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
└── docs/
    └── README.md
```

### Makefile for Common Commands

```makefile
.PHONY: install test lint format

install:
	poetry install

test:
	poetry run pytest -v --cov=project_name

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run black .
	poetry run isort .

all: format lint test
```

---

## Examples

### Django Project

```bash
poetry new django-app
cd django-app
poetry add django djangorestframework
poetry add --group dev pytest-django
poetry run django-admin startproject config .
```

### FastAPI Project

```bash
poetry new fastapi-app
cd fastapi-app
poetry add fastapi uvicorn[standard]
poetry add --group dev pytest httpx
```

### CLI Tool

```toml
[tool.poetry.scripts]
mycli = "my_project.cli:main"
```

```python
# my_project/cli.py
def main():
    print("Hello from CLI!")
```

---

## Common Mistakes

1. **Not committing poetry.lock** - Always commit it for reproducible builds
2. **Global Python conflicts** - Use `poetry env use python3.11` to specify version
3. **Mixing pip and poetry** - Use poetry for all dependency management
4. **Forgetting dev groups** - Separate dev/test dependencies from production

---

## Checklist

- [ ] Poetry installed globally
- [ ] pyproject.toml configured
- [ ] Dev dependencies in separate group
- [ ] poetry.lock committed
- [ ] Virtual environment activated
- [ ] Makefile created for common commands
- [ ] .gitignore includes `__pycache__`, `.venv`

---

## Next Steps

- M-PY-004: Pytest Testing
- M-PY-006: Type Hints
- M-PY-008: Code Quality

---

*Methodology M-PY-001 v1.0*
