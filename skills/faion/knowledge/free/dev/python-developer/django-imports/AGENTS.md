# Django Import Patterns

## Summary

Import organization rules for Django multi-app projects: PEP 8 section order, mandatory aliases for cross-app imports, `TYPE_CHECKING` guards for type-only imports, string FK references and `apps.get_model()` to break circular dependencies. Core rule: cross-app imports MUST use aliases (`from apps.users import models as user_models`) — even when no current naming collision exists, future apps will collide.

## Why

Unaliased cross-app imports are the primary cause of `ImportError: cannot import name 'User'` circular-dependency crashes in Django multi-app projects. String FK references (`'users.User'`) and `apps.get_model()` move resolution to after all apps are loaded, making circular imports structurally impossible for the model layer.

## When To Use

- Setting up a new Django project: `pyproject.toml` ruff/isort config with `known-first-party`.
- Adding a new app: establish the cross-app alias convention before duplicate `User` collisions appear.
- Resolving `ImportError: cannot import name '...'` from circular cross-app deps.
- Adding type hints to legacy Django code: `if TYPE_CHECKING:` blocks for type-only imports.
- CI gate: ruff `I` (isort) auto-sort on staged files.

## When NOT To Use

- Single-app projects — alias rules add noise without benefit.
- Codebases with a `core.imports` shim or central re-export — duplicating direct imports defeats it.
- One-off management commands or scripts where readability beats convention.
- Pure data pipelines (Airflow DAGs, Prefect flows) — Django ORM rarely involved.

## Content

| File | What's inside |
|------|---------------|
| `content/01-import-order.xml` | PEP 8 + Django section order; absolute vs relative rules; multi-dot relative ban. |
| `content/02-circular-deps.xml` | Strategy ladder: string FK refs → `apps.get_model()` → `TYPE_CHECKING` → function-scoped → core/ extraction. |
| `content/03-antipatterns.xml` | Unaliased cross-app imports; wildcard imports; `from __future__ import annotations` + DRF introspection; PEP 810 in 3.12 code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruff-isort-config.toml` | `[tool.ruff.lint.isort]` block with `known-first-party`, `section-order`, Django sections. |
| `templates/find-circular-imports.sh` | Script: grep for unaliased cross-app model imports likely to cause circular deps. |
