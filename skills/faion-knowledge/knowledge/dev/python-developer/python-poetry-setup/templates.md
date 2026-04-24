# Poetry Templates

Copy-paste ready configurations for common scenarios.

---

## pyproject.toml Templates

### Minimal Application (Poetry 2.x)

```toml
[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.11,<4.0"
dependencies = []

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false
```

### Standard Application

```toml
[project]
name = "my-app"
version = "0.1.0"
description = "Application description"
readme = "README.md"
requires-python = ">=3.11,<4.0"
license = "MIT"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = []

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
mypy = "^1.13"
ruff = "^0.8"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

### Publishable Library

```toml
[project]
name = "my-library"
version = "1.0.0"
description = "Library description"
readme = "README.md"
requires-python = ">=3.10,<4.0"
license = "MIT"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/you/my-library"
Documentation = "https://my-library.readthedocs.io"
Repository = "https://github.com/you/my-library.git"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
packages = [{include = "my_library", from = "src"}]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-cov = "^6.0"
mypy = "^1.13"
ruff = "^0.8"
pre-commit = "^4.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.6"
mkdocs-material = "^9.5"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src/my_library --cov-report=term-missing"

[tool.coverage.run]
source = ["src/my_library"]
branch = true

[tool.coverage.report]
fail_under = 80
```

---

## Dependency Group Templates

### Development Group

```toml
[tool.poetry.group.dev.dependencies]
# Testing
pytest = "^8.3"
pytest-cov = "^6.0"
pytest-mock = "^3.14"

# Type checking
mypy = "^1.13"

# Linting/Formatting
ruff = "^0.8"
pre-commit = "^4.0"

# Debugging
ipdb = "^0.13"
```

### Testing Group (Separate)

```toml
[tool.poetry.group.test.dependencies]
pytest = "^8.3"
pytest-asyncio = "^0.24"
pytest-cov = "^6.0"
pytest-mock = "^3.14"
pytest-xdist = "^3.5"
factory-boy = "^3.3"
faker = "^33.0"
httpx = "^0.28"
```

### Documentation Group (Optional)

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
# MkDocs
mkdocs = "^1.6"
mkdocs-material = "^9.5"
mkdocstrings = {extras = ["python"], version = "^0.27"}

# OR Sphinx
# sphinx = "^8.1"
# sphinx-rtd-theme = "^3.0"
# sphinx-autodoc-typehints = "^2.5"
```

### CI/Production Group

```toml
[tool.poetry.group.prod.dependencies]
sentry-sdk = "^2.19"
structlog = "^24.4"
prometheus-client = "^0.21"
```

---

## Tool Configuration Templates

### Ruff (Linter + Formatter)

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "migrations",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "W",      # pycodestyle warnings
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "ASYNC",  # flake8-async
]
ignore = [
    "E501",   # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["my_package"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
```

### MyPy (Type Checker)

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
warn_unreachable = true
show_error_codes = true
plugins = []

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = [
    "some_untyped_lib.*",
]
ignore_missing_imports = true
```

### MyPy with Django

```toml
[tool.mypy]
python_version = "3.11"
strict = true
plugins = [
    "mypy_django_plugin.main",
    "mypy_drf_plugin.main",
]

[tool.django-stubs]
django_settings_module = "config.settings"
```

### MyPy with Pydantic

```toml
[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

### Pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]
```

### Pytest with Async

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src"
```

### Pytest with Django

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
testpaths = ["tests"]
addopts = "-v --tb=short --reuse-db"
python_files = ["test_*.py", "*_test.py"]
```

### Coverage

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "tests/*",
    "*/__init__.py",
    "*/migrations/*",
]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@abstractmethod",
]
```

---

## CI/CD Templates

### GitHub Actions - Basic

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
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: "2.0.1"
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load cached venv
        uses: actions/cache@v4
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        run: poetry install --no-interaction

      - name: Run linting
        run: poetry run ruff check .

      - name: Run type checking
        run: poetry run mypy src/

      - name: Run tests
        run: poetry run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### GitHub Actions - Release

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
      id-token: write
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: "2.0.1"

      - name: Build package
        run: poetry build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - .venv/

test:
  stage: test
  image: python:3.12
  before_script:
    - pip install poetry
    - poetry config virtualenvs.in-project true
    - poetry install
  script:
    - poetry run ruff check .
    - poetry run mypy src/
    - poetry run pytest --cov

build:
  stage: build
  image: python:3.12
  before_script:
    - pip install poetry
  script:
    - poetry build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  image: python:3.12
  only:
    - tags
  before_script:
    - pip install poetry
  script:
    - poetry config pypi-token.pypi $PYPI_TOKEN
    - poetry publish
```

---

## Docker Templates

### Multi-stage Dockerfile

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install poetry==2.0.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Export requirements (faster than Poetry in production)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home appuser
USER appuser

# Run
CMD ["python", "-m", "src.main"]
```

### Development Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==2.0.1

# Configure Poetry
RUN poetry config virtualenvs.in-project true

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy application
COPY . .

# Install project
RUN poetry install

CMD ["poetry", "run", "python", "-m", "src.main"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## .gitignore Template

```gitignore
# Poetry
.venv/
poetry.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
coverage.xml
*.cover

# Type checking
.mypy_cache/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
*.local

# OS
.DS_Store
Thumbs.db
```

---

## Pre-commit Config

```yaml
# .pre-commit-config.yaml
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
        additional_dependencies:
          - pydantic>=2.0

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
```

---

## poetry.toml (Local Config)

```toml
# poetry.toml (project-local config, can be gitignored)
[virtualenvs]
in-project = true
create = true

[installer]
parallel = true
```

---

*Last updated: 2026-01*
