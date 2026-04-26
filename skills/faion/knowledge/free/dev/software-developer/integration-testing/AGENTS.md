# Integration Testing

## Summary

Integration testing verifies that multiple components work correctly together using real dependencies (databases, APIs, message queues) or realistic test doubles. Every test must control its own data, roll back after the test, and run in seconds — not milliseconds.

## Why

Unit tests prove logic; integration tests prove that the seams between components behave correctly under real I/O. Mocking the database in an "integration test" defeats the purpose — the test proves nothing about the actual ORM query, transaction boundary, or migration schema.

## When To Use

- Database interactions: ORM queries, transactions, migrations.
- API endpoints tested with a real request/response cycle (TestClient / supertest).
- Message queue producers and consumers (RabbitMQ, Kafka, SQS).
- Auth flows: token issuance, role checks, expired/forged tokens.
- Outbound HTTP integrations against WireMock / mockoon / Pact.

## When NOT To Use

- Pure functions / stateless logic — unit tests are faster and more focused.
- Cross-service flows that require a browser or multiple processes — use E2E (Playwright/Cypress).
- Performance benchmarking — use dedicated load tools (k6, Locust).
- Fast inner-loop development feedback — run integration suite on CI and on-demand only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core rules: real deps, transaction isolation, cleanup, test pyramid ratios. |
| `content/02-python-patterns.xml` | pytest fixtures for PostgreSQL (Testcontainers), FastAPI TestClient, auth headers, async client. |
| `content/03-typescript-patterns.xml` | Supertest patterns for Node.js APIs with database setup/teardown. |
| `content/04-antipatterns.xml` | Common failures: mocking the DB, shared state, container leakage, async/sync confusion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest-postgres.py` | Session-scoped Testcontainers Postgres + per-test transaction-rollback fixture. |
| `templates/github-actions-services.yml` | GitHub Actions services block for CI-native Postgres (faster than Testcontainers). |
