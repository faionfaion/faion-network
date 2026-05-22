---
slug: api-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: API tests are organized in a pyramid: many unit tests, some integration tests against TestClient/httpx, targeted contract tests (Pact) only across team or service boundaries, and few E2E tests.
content_id: "c80e7177e2b3dc32"
tags: [api, testing, integration-testing, openapi, pact]
---
# API Testing

## Summary

**One-sentence:** API tests are organized in a pyramid: many unit tests, some integration tests against TestClient/httpx, targeted contract tests (Pact) only across team or service boundaries, and few E2E tests.

**One-paragraph:** API tests are organized in a pyramid: many unit tests, some integration tests against TestClient/httpx, targeted contract tests (Pact) only across team or service boundaries, and few E2E tests. Every integration test must validate the response body against the OpenAPI schema — status code alone is not enough. Snapshot openapi.json per PR and use oasdiff to classify breaking vs non-breaking changes.

## Applies If (ALL must hold)

- New REST/GraphQL service: generate happy-path + 4xx + 5xx tests from OpenAPI schema before implementation
- After every spec change to openapi.yaml — regenerate validation tests to catch drift
- Building integration tests with TestClient / httpx.AsyncClient for FastAPI or Django
- Adding negative tests (auth failures, validation, rate-limiting, idempotency)
- Frontend/backend contract is unstable across teams — drive Pact consumer tests from FE side

## Skip If (ANY kills it)

- Pure unit-level logic with no transport or contract — plain pytest without schema validation
- Greenfield prototypes where contract changes hourly — Pact pacts create churn faster than value
- Single-team, single-repo monoliths where integration tests already cover the surface — contract tests are redundant
- Pure browser flows (form clicks, redirects) — use Playwright/Cypress instead
- Internal binary RPC with code-generated schemas — contract drift is impossible

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
