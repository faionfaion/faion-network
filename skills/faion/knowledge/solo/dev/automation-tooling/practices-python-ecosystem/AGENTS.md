---
slug: practices-python-ecosystem
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four foundational Python project conventions: FastAPI with Pydantic models and dependency injection, the standard `src/` project layout, explicit type hints on all public functions, and lockfile-based dependency management via uv (preferred 2026) or poetry.
content_id: "3626f96336ce68d0"
tags: [python, fastapi, project-structure, type-hints, dependency-management]
---
# Python Ecosystem Practices

## Summary

**One-sentence:** Four foundational Python project conventions: FastAPI with Pydantic models and dependency injection, the standard `src/` project layout, explicit type hints on all public functions, and lockfile-based dependency management via uv (preferred 2026) or poetry.

**One-paragraph:** Four foundational Python project conventions: FastAPI with Pydantic models and dependency injection, the standard `src/` project layout, explicit type hints on all public functions, and lockfile-based dependency management via uv (preferred 2026) or poetry.

## Applies If (ALL must hold)

- Greenfield FastAPI service setup — use as the layout and pattern template.
- Refactor passes adding type hints to an existing Python project.
- Onboarding a new developer or agent to a Python project — point to this as the house standard.
- Dependency conflict troubleshooting — check that a lockfile exists and is committed.

## Skip If (ANY kills it)

- Django-specific patterns — see practices-django-coding for DRF, models, services.
- Performance tuning or async architecture decisions — out of scope here.
- Projects with an existing house style that diverges (e.g., uses `hatch` instead of uv/poetry) — agent will overwrite it.

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

- parent skill: `solo/dev/automation-tooling/`
