# Python Ecosystem

## Summary

Patterns for the full Python development stack: Poetry for dependency management, Django
models/views/services/admin, FastAPI routes/dependencies/schemas, pytest fixtures/mocking/parametrize,
type hints with `mypy --strict`, Black + isort + flake8 formatting, venv/pyenv, and asyncio
concurrency patterns.

## Why

Python projects without a locked dependency manager (`poetry.lock`), type annotations, and
enforced formatting accumulate technical debt quickly. The services pattern (thin views + business
logic in `services.py`) makes Django/FastAPI code testable from Celery and management commands.
`asyncio.gather` reduces I/O-bound latency proportionally to the number of concurrent operations.

## When To Use

- Setting up a new Python project with Poetry and pyproject.toml
- Writing Django models, views, serializers, or admin configuration
- Creating FastAPI routes, Pydantic schemas, and dependency injection
- Writing pytest tests with fixtures, mocking, and parametrize
- Adding type hints and running `mypy --strict` on a file or module
- Configuring Black, isort, and flake8 for consistent formatting
- Implementing concurrent I/O with `asyncio.gather` or `TaskGroup`

## When NOT To Use

- Go / Rust / Node.js projects — language-specific skills cover those
- Data science / ML workflows — pandas, NumPy, and Jupyter patterns are out of scope here
- Legacy Python 2 codebases — methodology assumes Python 3.11+

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-setup.xml` | Poetry init, pyproject.toml layout, dependency groups, venv, pyenv integration |
| `content/02-django-patterns.xml` | `BaseModel`, services layer, thin views, serializers, admin with fieldsets |
| `content/03-fastapi-patterns.xml` | FastAPI app, `Depends()`, Pydantic schemas, background tasks |
| `content/04-pytest-patterns.xml` | conftest fixtures, factory fixtures, mocking, parametrize, Django DB tests |
| `content/05-asyncio-patterns.xml` | `asyncio.gather`, `TaskGroup`, semaphores, timeouts, async context managers |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Minimal Poetry pyproject.toml with dev group and tool config stubs |
| `templates/conftest.py` | Standard pytest conftest with `mock_db`, `api_client`, `authenticated_client` |
| `templates/pytest.ini.toml` | `[tool.pytest.ini_options]` block with Django settings and addopts |
