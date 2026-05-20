---
slug: python
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for the full Python development stack: Poetry for dependency management, Django models/views/services/admin, FastAPI routes/dependencies/schemas, pytest fixtures/mocking/parametrize, type hints with `mypy --strict`, ruff formatting, venv/pyenv, and asyncio concurrency patterns.
content_id: "340b5011d8539b9a"
tags: [python, django, fastapi, pytest, asyncio]
---
# Python Ecosystem

## Summary

**One-sentence:** Patterns for the full Python development stack: Poetry for dependency management, Django models/views/services/admin, FastAPI routes/dependencies/schemas, pytest fixtures/mocking/parametrize, type hints with `mypy --strict`, ruff formatting, venv/pyenv, and asyncio concurrency patterns.

**One-paragraph:** Patterns for the full Python development stack: Poetry for dependency management, Django models/views/services/admin, FastAPI routes/dependencies/schemas, pytest fixtures/mocking/parametrize, type hints with `mypy --strict`, ruff formatting, venv/pyenv, and asyncio concurrency patterns.

## Applies If (ALL must hold)

- Setting up a new Python project with Poetry and pyproject.toml
- Writing Django models, views, serializers, or admin configuration
- Creating FastAPI routes, Pydantic schemas, and dependency injection
- Writing pytest tests with fixtures, mocking, and parametrize
- Adding type hints and running `mypy --strict` on a file or module
- Configuring ruff for consistent formatting
- Implementing concurrent I/O with `asyncio.gather` or `TaskGroup`

## Skip If (ANY kills it)

- Go / Rust / Node.js projects — language-specific skills cover those
- Data science / ML workflows — pandas, NumPy, and Jupyter patterns are out of scope here
- Legacy Python 2 codebases — methodology assumes Python 3.11+

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/software-developer/`
