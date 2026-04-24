# Poetry Examples

Real-world pyproject.toml configurations for common project types.

---

## 1. FastAPI Application (Poetry 2.x)

Modern async API with SQLAlchemy and testing.

```toml
[project]
name = "fastapi-app"
version = "1.0.0"
description = "Production-ready FastAPI application"
readme = "README.md"
requires-python = ">=3.11,<4.0"
license = "MIT"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["api", "fastapi", "async"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.115.0,<1.0.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy[asyncio]>=2.0.36",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "httpx>=0.28.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.scripts]
serve = "app.main:serve"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = true
packages = [{include = "app", from = "src"}]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-asyncio = "^0.24"
pytest-cov = "^6.0"
httpx = "^0.28"
mypy = "^1.13"
ruff = "^0.8"
pre-commit = "^4.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.6"
mkdocs-material = "^9.5"
mkdocstrings = {extras = ["python"], version = "^0.27"}

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM", "ASYNC"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src/app --cov-report=term-missing"

[tool.coverage.run]
source = ["src/app"]
omit = ["tests/*", "*/__init__.py"]
```

---

## 2. Django Application (Poetry 2.x)

Full Django setup with DRF and Celery.

```toml
[project]
name = "django-app"
version = "2.0.0"
description = "Django REST API with Celery"
readme = "README.md"
requires-python = ">=3.11,<4.0"
license = "MIT"
authors = [
    {name = "Your Team", email = "team@example.com"}
]
dependencies = [
    "django>=5.1,<6.0",
    "djangorestframework>=3.15.0",
    "django-cors-headers>=4.6.0",
    "django-filter>=24.3",
    "drf-spectacular>=0.28.0",
    "psycopg[binary]>=3.2.0",
    "redis>=5.2.0",
    "celery>=5.4.0",
    "django-celery-beat>=2.7.0",
    "gunicorn>=23.0.0",
    "whitenoise>=6.8.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
manage = "config.manage:main"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false  # Django projects typically don't need packaging

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-django = "^4.9"
pytest-cov = "^6.0"
factory-boy = "^3.3"
django-debug-toolbar = "^4.4"
mypy = "^1.13"
django-stubs = "^5.1"
djangorestframework-stubs = "^3.15"
ruff = "^0.8"

[tool.poetry.group.prod.dependencies]
sentry-sdk = "^2.19"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "DJ"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
plugins = ["mypy_django_plugin.main", "mypy_drf_plugin.main"]
strict = true

[tool.django-stubs]
django_settings_module = "config.settings"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
testpaths = ["tests"]
addopts = "-v --tb=short --reuse-db"
```

---

## 3. Python Library (Poetry 2.x)

Publishable library with full metadata.

```toml
[project]
name = "my-awesome-lib"
version = "1.2.3"
description = "A comprehensive Python library for awesome things"
readme = "README.md"
requires-python = ">=3.10,<4.0"
license = "Apache-2.0"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
maintainers = [
    {name = "Maintainer", email = "maintainer@example.com"}
]
keywords = ["library", "utility", "awesome"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.25",
]

[project.optional-dependencies]
async = ["aiohttp>=3.9"]
cli = ["typer>=0.13", "rich>=13.0"]
all = ["aiohttp>=3.9", "aiohttp>=3.9", "typer>=0.13", "rich>=13.0"]

[project.urls]
Homepage = "https://github.com/you/my-awesome-lib"
Documentation = "https://my-awesome-lib.readthedocs.io"
Repository = "https://github.com/you/my-awesome-lib.git"
Changelog = "https://github.com/you/my-awesome-lib/blob/main/CHANGELOG.md"

[project.scripts]
awesome-cli = "my_awesome_lib.cli:main"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = true
packages = [{include = "my_awesome_lib", from = "src"}]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-cov = "^6.0"
pytest-xdist = "^3.5"
mypy = "^1.13"
ruff = "^0.8"
pre-commit = "^4.0"
tox = "^4.21"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
sphinx = "^8.1"
sphinx-rtd-theme = "^3.0"
sphinx-autodoc-typehints = "^2.5"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM", "RUF"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src/my_awesome_lib --cov-report=xml"

[tool.coverage.run]
source = ["src/my_awesome_lib"]
branch = true

[tool.coverage.report]
fail_under = 90
```

---

## 4. CLI Application with Typer

Interactive CLI tool with rich output.

```toml
[project]
name = "my-cli"
version = "0.5.0"
description = "A powerful CLI tool"
readme = "README.md"
requires-python = ">=3.11,<4.0"
license = "MIT"
dependencies = [
    "typer>=0.13.0",
    "rich>=13.9.0",
    "httpx>=0.28.0",
    "pydantic>=2.10.0",
    "pyyaml>=6.0.0",
    "tomli>=2.0.0; python_version < '3.11'",
]

[project.scripts]
mycli = "my_cli.main:app"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
packages = [{include = "my_cli", from = "src"}]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-cov = "^6.0"
mypy = "^1.13"
ruff = "^0.8"

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
strict = true
```

---

## 5. Data Science Project

ML/Data project with Jupyter support.

```toml
[project]
name = "ml-project"
version = "0.1.0"
description = "Machine learning experiment"
readme = "README.md"
requires-python = ">=3.11,<4.0"
license = "MIT"
dependencies = [
    "numpy>=2.0",
    "pandas>=2.2",
    "scikit-learn>=1.5",
    "polars>=1.15",
    "matplotlib>=3.9",
    "seaborn>=0.13",
]

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false  # Non-package mode for experiments

[tool.poetry.group.dev.dependencies]
jupyter = "^1.1"
jupyterlab = "^4.3"
ipywidgets = "^8.1"
nbformat = "^5.10"
pytest = "^8.3"
mypy = "^1.13"
ruff = "^0.8"

[tool.poetry.group.ml.dependencies]
torch = "^2.5"
transformers = "^4.46"
datasets = "^3.1"

[tool.poetry.group.viz.dependencies]
plotly = "^5.24"
altair = "^5.4"

[tool.ruff]
line-length = 100  # Wider for notebooks

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
ignore = ["E501"]  # Allow long lines in data science

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true  # Many ML libs lack stubs
```

---

## 6. Monorepo with Shared Libraries

Workspace configuration with shared code.

### Root pyproject.toml

```toml
[project]
name = "monorepo-root"
version = "0.0.0"
requires-python = ">=3.11,<4.0"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false

# Shared dev dependencies
[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
mypy = "^1.13"
ruff = "^0.8"

# Path dependencies to workspace packages
[tool.poetry.group.packages.dependencies]
shared-lib = {path = "packages/shared-lib", develop = true}
service-api = {path = "services/api", develop = true}
service-worker = {path = "services/worker", develop = true}
```

### packages/shared-lib/pyproject.toml

```toml
[project]
name = "shared-lib"
version = "1.0.0"
requires-python = ">=3.11,<4.0"
dependencies = [
    "pydantic>=2.10",
]

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
packages = [{include = "shared_lib", from = "src"}]
```

### services/api/pyproject.toml

```toml
[project]
name = "service-api"
version = "1.0.0"
requires-python = ">=3.11,<4.0"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
]

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
packages = [{include = "api", from = "src"}]

[tool.poetry.dependencies]
shared-lib = {path = "../../packages/shared-lib", develop = true}
```

---

## 7. Minimal Non-Package Project

Scripts and tools without packaging.

```toml
[project]
name = "my-scripts"
version = "0.1.0"
requires-python = ">=3.11"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.32"
click = "^8.1"

[tool.poetry.group.dev.dependencies]
ruff = "^0.8"
```

---

## 8. Legacy Poetry 1.x (for reference)

Pre-PEP 621 format (still supported with deprecation warnings).

```toml
[tool.poetry]
name = "legacy-project"
version = "1.0.0"
description = "Legacy Poetry 1.x format"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
license = "MIT"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.32.0"}

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
mypy = "^1.13"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## Version Constraint Reference

| Constraint | Meaning | Example |
|------------|---------|---------|
| `^1.2.3` | Compatible releases (>=1.2.3, <2.0.0) | `^2.0` = >=2.0.0, <3.0.0 |
| `~1.2.3` | Approximately (>=1.2.3, <1.3.0) | `~2.0` = >=2.0.0, <2.1.0 |
| `>=1.2,<2.0` | Range | Explicit bounds |
| `==1.2.3` | Exact | Pinned version |
| `*` | Any | Latest compatible |

### PEP 508 vs Poetry Syntax

| Poetry 1.x | PEP 508 (Poetry 2.x) |
|------------|----------------------|
| `python = "^3.11"` | `requires-python = ">=3.11,<4.0"` |
| `fastapi = "^0.115"` | `"fastapi>=0.115.0,<0.116.0"` |
| `uvicorn = {extras = ["standard"], version = "^0.32"}` | `"uvicorn[standard]>=0.32.0"` |

---

*Last updated: 2026-01*
