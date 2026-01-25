---
id: python-basics
name: "Python Project Setup"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Python Project Setup

## Poetry Setup

```bash
# New project
poetry new my-project
cd my-project

# Or existing project
cd existing-project
poetry init
```

## pyproject.toml Configuration

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = ["Author Name <author@example.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
djangorestframework = "^3.14"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-django = "^4.8"
pytest-cov = "^4.1"
mypy = "^1.8"
black = "^24.0"
isort = "^5.13"
flake8 = "^7.0"
django-stubs = "^4.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Dependency Management

```bash
# Add dependency
poetry add django fastapi

# Add dev dependency
poetry add --group dev pytest mypy

# Update dependencies
poetry update

# Lock dependencies
poetry lock

# Install from lock file
poetry install

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

## Virtual Environment

```bash
# Create and activate
poetry shell

# Or run command in venv
poetry run python manage.py migrate
poetry run pytest

# Show venv path
poetry env info --path
```

## pyenv for Python Versions

```bash
# Install pyenv (Linux)
curl https://pyenv.run | bash

# List available Python versions
pyenv install --list

# Install specific version
pyenv install 3.11.7

# Set local version for project
cd my-project
pyenv local 3.11.7

# Set global version
pyenv global 3.11.7

# Show current version
pyenv version
```

## pyenv + Poetry Integration

```bash
# Install Python version
pyenv install 3.11.7

# Set for project
cd my-project
pyenv local 3.11.7

# Initialize Poetry with this version
poetry env use $(pyenv which python)
poetry install
```

## Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only dependency files first (cache layer)
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . .

CMD ["python", "main.py"]
```

## Project Structure

```
project/
├── .venv/              # Virtual environment (gitignored)
├── .python-version     # pyenv local version
├── pyproject.toml      # Poetry config
├── poetry.lock         # Locked dependencies
├── requirements.txt    # Optional export
```

## .gitignore

```
.venv/
*.pyc
__pycache__/
.mypy_cache/
.pytest_cache/
```

## Sources

- [Poetry Documentation](https://python-poetry.org/docs/) - Official Poetry docs
- [pyenv GitHub](https://github.com/pyenv/pyenv) - Python version management
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/) - Project metadata standard
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html) - Built-in venv guide
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/) - Optimized Python images
