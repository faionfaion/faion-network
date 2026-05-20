---
slug: django-pytest-mocking
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Mock external service calls at the integration boundary: patch at the import site (not definition site), use the responses library for HTTP calls, and freezegun for datetime-dependent logic.
content_id: "573f8c113f65de09"
tags: [django, pytest, mocking, testing, freezegun]
---
# Django pytest Mocking

## Summary

**One-sentence:** Mock external service calls at the integration boundary: patch at the import site (not definition site), use the responses library for HTTP calls, and freezegun for datetime-dependent logic.

**One-paragraph:** Mock external service calls at the integration boundary: patch at the import site (not definition site), use the responses library for HTTP calls, and freezegun for datetime-dependent logic. Always verify mock calls with expected arguments. Never mock Django ORM internals.

## Applies If (ALL must hold)

- Tests that call external APIs (Stripe, Twilio, SendGrid, AWS, partner webhooks).
- Tests that depend on the current time (expiry checks, scheduling, time-limited coupons).
- Tests where a Celery task would be enqueued but you only want to verify it was triggered.
- Tests that make HTTP requests to third-party services.

## Skip If (ANY kills it)

- Tests of the real integration path — use a staging environment or integration test suite for end-to-end verification with real credentials.
- Mocking Django ORM methods (objects.filter, objects.create) — use real test data with the db fixture instead.
- Mocking time.sleep to "speed up" rate-limit tests — patch the rate-limiter directly, not sleep.

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
