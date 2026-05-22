---
slug: django-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest-based testing patterns for Django projects using model_bakery (or factory_boy) for fixtures, @pytest.
content_id: "f5886eaa8721df0f"
tags: [django, pytest, testing, fixtures, model-bakery]
---
# Django Testing Reference

## Summary

**One-sentence:** pytest-based testing patterns for Django projects using model_bakery (or factory_boy) for fixtures, @pytest.

**One-paragraph:** pytest-based testing patterns for Django projects using model_bakery (or factory_boy) for fixtures, @pytest.mark.django_db for DB access, and APIClient for DRF endpoint tests. The core rule: service-layer tests must call real code, not mocks; mock only at process boundaries (outbound HTTP, S3, third-party SDKs).

## Applies If (ALL must hold)

- Adding test coverage to a new Django app: pytest-django + model_bakery is the canonical default.
- Generating or reviewing service-layer tests where the "no mocks for in-app code" rule must be enforced.
- Migrating from unittest.TestCase to pytest style.
- Setting up parametrized tests for validation/calculation services.
- Adding DRF API tests without writing the full request stack manually.

## Skip If (ANY kills it)

- Non-Django Python projects — patterns assume @pytest.mark.django_db, app fixtures, Django settings.
- Pure unit tests of pure functions with no DB access — skip model_bakery overhead.
- Browser / E2E tests — use playwright (pytest-playwright).
- Performance / load testing — use locust or k6.
- Codebases standardized on unittest.TestCase where migration is out of scope.

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
