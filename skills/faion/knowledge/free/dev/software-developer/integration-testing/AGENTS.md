---
slug: integration-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces integration tests that run against real DB/queue/cache via Testcontainers (pinned images), use transaction-rollback per test, run in seconds, and split unit/integration into separate suites.
content_id: "5dcd59ab61d8b173"
complexity: medium
produces: code
est_tokens: 4000
tags: [testing, integration, testcontainers, pytest, postgres]
---
# Integration Testing (Testcontainers + transaction rollback)

## Summary

**One-sentence:** Produces integration tests that run against real DB/queue/cache via Testcontainers (pinned images), use transaction-rollback per test, run in seconds, and split unit/integration into separate suites.

**One-paragraph:** Integration tests verify that components work together using REAL dependencies (Postgres, Redis, RabbitMQ) — never mock the ORM or the connection. Use Testcontainers with pinned image tags; one session-scoped container, function-scoped transaction-rollback session per test. Override DI to inject the test session; clear overrides after the test. Generate auth tokens via fixtures, not hardcoded strings. Assert both HTTP status and body shape. Keep unit and integration tests in separate dirs (`tests/unit/`, `tests/integration/`); integration suite must stay under 5 minutes.

**Ефективно для:** services with real database/queue dependencies, refactors moving from mocked-DB unit tests to real-DB integration, CI pipelines suffering from flaky teardown-based cleanup, suites where image-tag drift causes intermittent failures.

## Applies If (ALL must hold)

- Service uses a real database, queue, or cache that has Testcontainers support.
- CI can run Docker (Testcontainers) or has access to a CI-native service.
- Team can split unit and integration test execution.
- Test suite can adopt transaction-rollback fixtures.

## Skip If (ANY kills it)

- Pure compute library — no external dependencies.
- CI has no Docker access and no service-block support.
- Codebase relies on global ORM state that cannot be transaction-isolated.
- Time pressure where unit tests cover the contract sufficiently.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Stack (Postgres/MySQL/Redis/RabbitMQ) | string | infra ADR |
| ORM/driver (SQLAlchemy/pgx/Prisma) | string | tech stack |
| Web framework (FastAPI/Flask/Gin/Express) | string | tech stack |
| Existing test runner (pytest/jest/go test) | string | project config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[mocking-strategies]]` | Decide what to mock (third-party APIs) and what to keep real (DB, queue). |
| `[[python-fastapi]]` or `[[go-http-handlers]]` | Provides the DI override pattern the tests use. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: real DBs, transaction rollback, pinned images, separate dirs, time cap, pyramid 70/20/10, session fixture, DI override, status+body asserts | ~800 |
| `content/02-output-contract.xml` | essential | Required test directory shape + fixture invariants | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: mocked ORM, unpinned image, fresh container per test, teardown deletion | ~600 |
| `content/04-procedure.xml` | medium | 5-step procedure: pin image -> session fixture -> tx fixture -> DI override -> CI wiring | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Does the service use a real external dependency that Testcontainers supports?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate conftest.py | sonnet | Pattern from templates. |
| Migrate test from mocked-DB | opus | AST + dependency reasoning. |
| CI services block | haiku | YAML boilerplate. |
| Triage flaky integration test | opus | Multi-source diagnosis (ORM, transaction, container). |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest-postgres.py` | Session-scoped Testcontainers Postgres + per-test transaction-rollback fixture. |
| `templates/github-actions-services.yml` | GitHub Actions services block for CI-native Postgres (faster than Testcontainers in CI). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-integration-testing.py` | Verifies pinned image tags, separate tests/unit and tests/integration dirs, transaction rollback fixture present. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[mocking-strategies]]` — what to mock at integration scope
- `[[e2e-testing]]` — outer layer of the test pyramid

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: real dependency present yes/no, Testcontainers-supported yes/no, CI can run Docker yes/no.
