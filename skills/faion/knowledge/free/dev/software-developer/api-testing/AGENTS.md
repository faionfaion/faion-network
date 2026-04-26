# API Testing

## Summary

API tests are organized in a pyramid: many unit tests, some integration tests against `TestClient`/`httpx`, targeted contract tests (Pact) only across team or service boundaries, and few E2E tests. Every integration test must validate the response body against the OpenAPI schema — status code alone is not enough. Snapshot `openapi.json` per PR and use `oasdiff` to classify breaking vs non-breaking changes.

## Why

Most regressions are schema drift — a field disappears, a type changes, a required field becomes optional. Asserting only on status codes misses these. Generating tests from the served `openapi.json` (not a hand-maintained spec) keeps tests and implementation in sync. Contract tests (Pact) are justified only when consumer and provider are in separate repos or teams; for single-repo monoliths, an integration test covers the same surface at lower cost.

## When To Use

- New REST/GraphQL service: generate happy-path + 4xx + 5xx tests from OpenAPI schema before implementation
- After every spec change to `openapi.yaml` — regenerate validation tests to catch drift
- Building integration tests with `TestClient` / `httpx.AsyncClient` for FastAPI or Django
- Adding negative tests (auth failures, validation, rate-limiting, idempotency)
- Frontend/backend contract is unstable across teams — drive Pact consumer tests from FE side

## When NOT To Use

- Pure unit-level logic with no transport or contract — plain pytest without schema validation
- Greenfield prototypes where contract changes hourly — Pact pacts create churn faster than value
- Single-team, single-repo monoliths where integration tests already cover the surface — contract tests are redundant
- Pure browser flows (form clicks, redirects) — use Playwright/Cypress instead
- Internal binary RPC with code-generated schemas — contract drift is impossible

## Content

| File | What's inside |
|------|---------------|
| `content/01-integration-testing.xml` | pytest + httpx patterns, auth fixtures, OpenAPI validation, parametrize |
| `content/02-contract-testing.xml` | Pact consumer/provider patterns, Pact Broker, can-i-deploy gate |
| `content/03-antipatterns.xml` | pactman misuse, weak assertions, credential leaks, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-contract-check.sh` | CI script: validate live responses against OpenAPI snapshot, fail on drift |
