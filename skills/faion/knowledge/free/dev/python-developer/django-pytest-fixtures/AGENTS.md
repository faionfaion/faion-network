---
slug: django-pytest-fixtures
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest-django provides database fixtures with distinct transaction semantics (db, transactional_db, django_db_reset_sequences).
content_id: "878ad525a1804ebe"
tags: [django, pytest, fixtures, conftest, testing]
---
# Django pytest Fixtures

## Summary

**One-sentence:** pytest-django provides database fixtures with distinct transaction semantics (db, transactional_db, django_db_reset_sequences).

**One-paragraph:** pytest-django provides database fixtures with distinct transaction semantics (db, transactional_db, django_db_reset_sequences). Choosing the correct one and composing fixtures explicitly in conftest.py is the foundation of a reliable, fast, and maintainable Django test suite.

## Applies If (ALL must hold)

- Writing unit or integration tests for Django models, services, and utilities.
- Setting up DRF API clients for endpoint tests.
- Sharing test data across a test module or session without re-creating it for each test.
- Replacing Django TestCase setUp/tearDown with composable, reusable fixtures.
- Debugging flaky tests caused by transaction semantics or fixture scope mismatches.

## Skip If (ANY kills it)

- Pure unit tests of helpers or pure functions with no Django dependency — plain pytest (no pytest-django) is faster and clearer.
- One-off scripts or ad-hoc manage.py shell exploration — fixture infrastructure overhead is not justified.
- Tests that must run inside manage.py test (legacy CI gates with Django runner) until that constraint is removed.

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
