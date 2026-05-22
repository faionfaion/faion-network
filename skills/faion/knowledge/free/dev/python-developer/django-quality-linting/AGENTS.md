---
slug: django-quality-linting
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every Django project MUST have Ruff (linting + formatting), mypy + django-stubs (static type checking), and pre-commit hooks committed to the repo.
content_id: "1b07c63ab6fa1d6d"
tags: [django, ruff, mypy, pre-commit, type-checking]
---
# Django Linting and Static Analysis Stack

## Summary

**One-sentence:** Every Django project MUST have Ruff (linting + formatting), mypy + django-stubs (static type checking), and pre-commit hooks committed to the repo.

**One-paragraph:** Every Django project MUST have Ruff (linting + formatting), mypy + django-stubs (static type checking), and pre-commit hooks committed to the repo. This replaces the legacy Flake8/Black/isort trinity and gates every commit automatically.

## Applies If (ALL must hold)

- New Django project — wire pre-commit + ruff + mypy + django-stubs + Sentry on day one.
- CI gate setup — block PRs on ruff, mypy, security scan, coverage threshold.
- Adding type hints incrementally to an existing Django project.
- Onboarding new developers who need mechanical enforcement of conventions.
- Any project that cannot afford the cost of production attribute errors.

## Skip If (ANY kills it)

- Throwaway prototypes — full quality stack costs more than the prototype is worth; use ruff alone.
- Codebases on Django older than 4.2 — django-stubs examples assume recent versions.
- Legacy projects under feature freeze — ROI on adding quality tooling is low; reserve for rewrites.

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
