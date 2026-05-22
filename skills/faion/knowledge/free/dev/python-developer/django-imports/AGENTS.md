---
slug: django-imports
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Import organization rules for Django multi-app projects: PEP 8 section order, mandatory aliases for cross-app imports, TYPE_CHECKING guards for type-only imports, string FK references and apps.
content_id: "9b3df72f9d943b7e"
tags: [django, imports, circular-dependencies, pep8]
---
# Django Import Patterns

## Summary

**One-sentence:** Import organization rules for Django multi-app projects: PEP 8 section order, mandatory aliases for cross-app imports, TYPE_CHECKING guards for type-only imports, string FK references and apps.

**One-paragraph:** Import organization rules for Django multi-app projects: PEP 8 section order, mandatory aliases for cross-app imports, TYPE_CHECKING guards for type-only imports, string FK references and apps.get_model() to break circular dependencies. Core rule: cross-app imports MUST use aliases (from apps.users import models as user_models) — even when no current naming collision exists, future apps will collide.

## Applies If (ALL must hold)

- Setting up a new Django project: pyproject.toml ruff/isort config with known-first-party.
- Adding a new app to a multi-app project: establish the cross-app alias convention before duplicate User collisions appear.
- Resolving ImportError: cannot import name '...' from circular cross-app dependencies.
- Adding type hints to legacy Django code: use if TYPE_CHECKING: blocks for type-only imports.
- Setting up CI gates: ruff I (isort) auto-sort on staged files in pre-commit.
- Code review of Django PRs: verify import order and aliasing follow the rules.

## Skip If (ANY kills it)

- Single-app projects — alias rules add noise without benefit.
- Codebases with a core.imports shim or central re-export — duplicating direct imports defeats the shim.
- One-off management commands or scripts where readability beats convention.
- Pure data pipelines (Airflow DAGs, Prefect flows) — Django ORM rarely involved.

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

- parent skill: `free/dev/python-developer/`
