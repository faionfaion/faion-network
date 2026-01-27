# Python Project Templates

Copy-paste templates for common Python project configurations.

---

## pyproject.toml Templates

### Modern Python Project (uv + ruff)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.12"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = []

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "pre-commit>=4.0.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]
exclude = [".git", ".ruff_cache", ".venv", "__pycache__"]

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
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-ra -q --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

### FastAPI Project

```toml
[project]
name = "fastapi-app"
version = "0.1.0"
description = "FastAPI application"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "httpx>=0.28.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.14.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "pre-commit>=4.0.0",
]

[project.scripts]
serve = "uvicorn app.main:app --reload"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "TCH", "PTH", "RUF"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

### Django Project

```toml
[project]
name = "django-app"
version = "0.1.0"
description = "Django application"
requires-python = ">=3.12"
dependencies = [
    "django>=5.1.0",
    "djangorestframework>=3.15.0",
    "django-cors-headers>=4.6.0",
    "psycopg[binary]>=3.2.0",
    "gunicorn>=23.0.0",
    "whitenoise>=6.8.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "django-stubs>=5.1.0",
    "djangorestframework-stubs>=3.15.0",
    "pytest>=8.0.0",
    "pytest-django>=4.9.0",
    "pytest-cov>=6.0.0",
    "factory-boy>=3.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "DJ"]  # DJ = flake8-django
ignore = ["E501"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = [
    "mypy_django_plugin.main",
    "mypy_drf_plugin.main",
]

[tool.django-stubs]
django_settings_module = "config.settings"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
testpaths = ["tests"]
addopts = "-ra -q"
```

### Data Science Project

```toml
[project]
name = "data-project"
version = "0.1.0"
description = "Data science project"
requires-python = ">=3.12"
dependencies = [
    "polars>=1.17.0",
    "pandas>=2.2.0",
    "numpy>=2.1.0",
    "scikit-learn>=1.6.0",
    "matplotlib>=3.9.0",
    "seaborn>=0.13.0",
    "plotly>=5.24.0",
    "jupyterlab>=4.3.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pandas-stubs>=2.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "NPY"]  # NPY = NumPy rules
ignore = ["E501"]
```

### ML/AI Project

```toml
[project]
name = "ml-project"
version = "0.1.0"
description = "Machine learning project"
requires-python = ">=3.12"
dependencies = [
    "torch>=2.5.0",
    "transformers>=4.46.0",
    "datasets>=3.1.0",
    "accelerate>=1.2.0",
    "peft>=0.14.0",
    "bitsandbytes>=0.45.0",
    "wandb>=0.19.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"
```

---

## Pre-commit Configuration

### .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
repos:
  # Ruff - linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # uv - lock file sync
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.5.0
    hooks:
      - id: uv-lock

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - pydantic

  # General checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: check-merge-conflict
      - id: detect-private-key

  # Security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]

ci:
  autofix_prs: true
  autoupdate_schedule: weekly
```

---

## GitHub Actions

### CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run linting
        run: uv run ruff check .

      - name: Run formatting check
        run: uv run ruff format --check .

      - name: Run type checking
        run: uv run mypy src/

      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Security audit
        run: |
          uv pip install pip-audit
          uv run pip-audit
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: dist/*
```

---

## Docker Templates

### Dockerfile (Production)

```dockerfile
# Dockerfile
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy source
COPY src/ src/

# Install project
RUN uv sync --frozen --no-dev


FROM python:3.12-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Copy virtual environment
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Set PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy application
COPY --from=builder --chown=app:app /app/src /app/src

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## Source Templates

### `__init__.py` with Version

```python
# src/my_package/__init__.py
"""My package description."""

__version__ = "0.1.0"

from my_package.main import MyClass, my_function

__all__ = ["MyClass", "my_function", "__version__"]
```

### Settings Module

```python
# src/app/config.py
"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "My App"
    debug: bool = False
    environment: str = Field(default="development", pattern="^(development|staging|production)$")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "sqlite:///./app.db"

    # Security
    secret_key: SecretStr = Field(default=...)
    allowed_hosts: list[str] = ["*"]

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

### Logging Configuration

```python
# src/app/logging.py
"""Logging configuration."""

import logging
import sys
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logging(
    level: LogLevel = "INFO",
    format_string: str | None = None,
) -> None:
    """Configure application logging."""
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Quiet noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
```

### Test Conftest

```python
# tests/conftest.py
"""Pytest configuration and fixtures."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Sample test data."""
    return {
        "name": "Test",
        "email": "test@example.com",
    }
```

---

## Makefile

```makefile
# Makefile
.PHONY: install dev test lint format typecheck clean

# Install production dependencies
install:
	uv sync --no-dev

# Install all dependencies including dev
dev:
	uv sync --all-extras --dev
	uv run pre-commit install

# Run tests
test:
	uv run pytest

# Run tests with coverage
coverage:
	uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Run linting
lint:
	uv run ruff check .

# Fix linting issues
lint-fix:
	uv run ruff check . --fix

# Run formatter
format:
	uv run ruff format .

# Check formatting
format-check:
	uv run ruff format --check .

# Run type checking
typecheck:
	uv run mypy src/

# Run all checks
check: lint format-check typecheck test

# Clean build artifacts
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

# Run development server
serve:
	uv run uvicorn app.main:app --reload --port 8000

# Build package
build:
	uv build

# Security audit
audit:
	uv run pip-audit
```

---

*Python Templates v1.0*
