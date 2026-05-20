---
slug: django-pytest-integration
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integration tests for Django projects cover API endpoints, service layer logic, and database transaction behavior.
content_id: "7b4cf0dd7195bc90"
tags: [django, pytest, integration-testing, drf, api-testing]
---
# Django pytest Integration Tests

## Summary

**One-sentence:** Integration tests for Django projects cover API endpoints, service layer logic, and database transaction behavior.

**One-paragraph:** Integration tests for Django projects cover API endpoints, service layer logic, and database transaction behavior. Every DRF endpoint needs tests for authentication (401), authorization (403), happy path (200/201), validation errors (400), and not-found (404). Use APIClient.force_authenticate, pytest factories for data, and format='json' on all requests.

## Applies If (ALL must hold)

- Testing DRF viewsets, APIView, or Django views end-to-end.
- Verifying authentication and permission enforcement on each endpoint.
- Testing transaction rollback and atomic operations in services.
- Verifying response shape (status code AND payload fields) after a successful call.
- Testing filtering, pagination, and query parameters.

## Skip If (ANY kills it)

- Pure business logic with no HTTP layer — use unit tests against the service class directly.
- End-to-end browser tests — use Playwright or Cypress for UI flows.
- Performance load tests — use locust or k6 against a real environment.

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
