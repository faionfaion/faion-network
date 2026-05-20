---
slug: django-pytest
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest with pytest-django is the modern Django test stack.
content_id: "b55270b7ec7377f0"
tags: [django, pytest, testing, fixtures, tdd]
---
# Django Testing with pytest

## Summary

**One-sentence:** pytest with pytest-django is the modern Django test stack.

**One-paragraph:** pytest with pytest-django is the modern Django test stack. Tests use fixtures (not TestCase), factory_boy for test data, APIClient.force_authenticate for auth, and the db fixture for database access. Every test is a function or class method — no TestCase inheritance. Block all real network calls with an autouse socket monkeypatch.

## Applies If (ALL must hold)

- New Django projects — pytest-django is the default over TestCase
- Adding cross-cutting fixtures (API client, authenticated user, factory) reused across many tests
- Integration tests against DRF endpoints with APIClient and JWT/session auth
- Testing services, models, and database operations
- Adding negative tests (auth failures, validation errors)

## Skip If (ANY kills it)

- Projects already heavily invested in TestCase where mixed styles cause confusion — pick one
- Test environments without DB access (pure logic) — plain pytest without pytest-django is lighter
- Async test suites using httpx.AsyncClient against ASGI directly — db fixture and sync ORM complicate things; use pytest-asyncio with manual setup
- Code paths relying on call_command-style isolation where TestCase transaction handling is simpler

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
