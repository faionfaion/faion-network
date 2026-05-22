---
slug: django-quality
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Quality toolchain for Django projects: ruff (format + lint), mypy + django-stubs (typing), bandit (security), and pre-commit hooks orchestrating all of them.
content_id: "9490b9388aed7bce"
tags: [django, ruff, mypy, quality, pre-commit]
---
# Django Code Quality Tools

## Summary

**One-sentence:** Quality toolchain for Django projects: ruff (format + lint), mypy + django-stubs (typing), bandit (security), and pre-commit hooks orchestrating all of them.

**One-paragraph:** Quality toolchain for Django projects: ruff (format + lint), mypy + django-stubs (typing), bandit (security), and pre-commit hooks orchestrating all of them. The canonical setup is pyproject.toml-only — no separate .flake8, no setup.cfg, no black/isort alongside ruff.

## Applies If (ALL must hold)

- Bootstrapping a new Django project before first feature commit.
- Migrating a legacy Django repo from black+isort+flake8 to ruff.
- Onboarding agents to a Django codebase that needs a deterministic baseline.
- Adding type-checking incrementally module by module via mypy overrides.

## Skip If (ANY kills it)

- Non-Django Python projects — drop mypy_django_plugin and DJ rules; rest still applies.
- Single-script utilities where pre-commit setup exceeds the code itself.
- Legacy migration files — gate with --diff first or you'll create a 5k-line format PR.

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
