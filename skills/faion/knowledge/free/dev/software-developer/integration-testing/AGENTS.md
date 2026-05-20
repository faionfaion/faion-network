---
slug: integration-testing
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integration testing verifies that multiple components work correctly together using real dependencies (databases, APIs, message queues) or realistic test doubles.
content_id: "5dcd59ab61d8b173"
tags: [testing, integration, pytest, testcontainers, database]
---
# Integration Testing

## Summary

**One-sentence:** Integration testing verifies that multiple components work correctly together using real dependencies (databases, APIs, message queues) or realistic test doubles.

**One-paragraph:** Integration testing verifies that multiple components work correctly together using real dependencies (databases, APIs, message queues) or realistic test doubles. Every test must control its own data, roll back after the test, and run in seconds — not milliseconds. Real integration tests prove actual ORM queries, transaction boundaries, and schema migrations; mocking the database defeats the purpose.

## Applies If (ALL must hold)

- Database interactions: ORM queries, transactions, migrations.
- API endpoints tested with a real request/response cycle (TestClient / supertest).
- Message queue producers and consumers (RabbitMQ, Kafka, SQS).
- Auth flows: token issuance, role checks, expired/forged tokens.
- Outbound HTTP integrations against WireMock / mockoon / Pact.
- Migration safety: every migration runs in CI on a fresh database before merge.

## Skip If (ANY kills it)

- Pure functions / stateless logic — unit tests are faster and more focused.
- Cross-service end-to-end flows that need browsers / multiple processes — use E2E (Playwright/Cypress) instead.
- Performance benchmarking — use dedicated load tools (k6, Locust).
- Fast inner-loop development feedback — keep these in a separate `tests/integration/` and run on CI + on-demand.

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
