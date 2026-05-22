---
slug: python
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a Python 3.11+ project applying the full stack — Poetry deps, Django services pattern, FastAPI Depends/Pydantic v2, pytest fixtures, mypy --strict, ruff, asyncio.gather/TaskGroup — with one canonical scaffold per framework.
content_id: "340b5011d8539b9a"
complexity: deep
produces: code
est_tokens: 5500
tags: [python, django, fastapi, pytest, mypy, ruff, asyncio]
---
# Python Ecosystem

## Summary

**One-sentence:** Produces a Python 3.11+ project applying the full stack — Poetry deps, Django services pattern, FastAPI Depends/Pydantic v2, pytest fixtures, mypy --strict, ruff, asyncio.gather/TaskGroup — with one canonical scaffold per framework.

**One-paragraph:** Patterns for the full Python stack. Poetry for dep management (`poetry.lock` committed). Django: business logic in `services.py`, not views; services receive domain types (not request objects); multi-step DB ops wrapped in `@transaction.atomic`. FastAPI: `Depends()` for DB sessions + auth; Pydantic v2 request/response schemas; async routes calling service functions. pytest: fixtures + mocking + parametrize. mypy `--strict` on the public boundary first (`services/*.py` + route handlers); `X | None`, not `Optional[X]`. ruff for both lint + format (replaces black/isort/flake8). asyncio: `asyncio.gather()` or `TaskGroup` for independent concurrent I/O.

**Ефективно для:** new Python services, migrations from black/flake8 to ruff, refactors moving business logic out of Django views, services adopting mypy --strict for the first time, asyncio code mistakenly running sequential awaits.

## Applies If (ALL must hold)

- Python >= 3.11.
- One of: Django (>=5), FastAPI (>=0.110), or general-purpose Python with type hints.
- Team accepts Poetry as the dep manager (or willing to migrate).
- mypy --strict run is acceptable on at least the public boundary.

## Skip If (ANY kills it)

- Python 2 or pre-3.11 legacy code (upgrade first).
- Data-science notebooks where mypy --strict is impractical.
- Single-file scripts where the methodology overhead is more than the script.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Project type | django / fastapi / general | tech stack ADR |
| Python version | semver string | engines |
| Poetry version | semver string | infra ADR |
| Pre-commit config | YAML | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python-poetry-setup]]` | Poetry pin + lockfile rules. |
| `[[python-fastapi]]` | FastAPI-specific patterns if framework=FastAPI. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: services-not-views, asyncio.gather, type public boundary, ruff replaces black/isort/flake8, Python 3.11+, `X \| None` syntax | ~700 |
| `content/01-project-setup.xml` | essential | Pyenv + Poetry + venv layout (kept) | ~700 |
| `content/02-django-patterns.xml` | essential | services.py, transaction.atomic, ORM patterns (kept) | ~800 |
| `content/02-output-contract.xml` | essential | Required project shape + invariants | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: logic in views, sequential awaits, Optional[X] over X\|None, black+ruff conflict, missing services/ layer | ~700 |
| `content/03-fastapi-patterns.xml` | essential | FastAPI routes/deps/schemas (kept) | ~700 |
| `content/04-procedure.xml` | medium | 6-step procedure for a new Python service | ~900 |
| `content/04-pytest-patterns.xml` | essential | pytest fixtures/parametrize (kept) | ~700 |
| `content/05-asyncio-patterns.xml` | essential | gather, TaskGroup, semaphore (kept) | ~600 |
| `content/06-decision-tree.xml` | essential | Root question on Python >= 3.11 and mypy --strict | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold Django service | sonnet | Templated. |
| Scaffold FastAPI route | sonnet | Templated. |
| asyncio refactor (sequential -> gather) | opus | Concurrency reasoning. |
| mypy --strict migration | opus | AST-level type inference. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Poetry pyproject with ruff + mypy + pytest config. |
| `templates/pytest.ini.toml` | pytest configuration (asyncio, coverage). |
| `templates/conftest.py` | Shared fixtures (event loop, DB session). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python.py` | Checks Python version, ruff config, mypy strict, services/ layer presence. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[python-poetry-setup]]` — Poetry lockfile rules
- `[[python-fastapi]]` — FastAPI specifics
- `[[language-framework-guide]]` — stack selection feeding into this

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Python 3.11+, mypy strict acceptable, Poetry acceptable; routes Django/FastAPI/general work into the right sibling content.
