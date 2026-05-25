# Django pytest Integration Tests

## Summary

**One-sentence:** Produces an integration-tests spec naming per-endpoint the security matrix (401/403/200/400/404), per-service the happy/error/edge cases, the transactional_db-scoped tests, the CI Postgres config, and the ≥ 80% coverage gate.

**Ефективно для:** Django/DRF projects where regressions slip through because tests assert only on status code, where SQLite-passing tests fail on Postgres in production, where permission combinations get missed for half the endpoints.

**One-paragraph:** Codifies the integration-test surface into one spec. Output names every endpoint with its 5 required test cases, every service-layer test class (one logical concept per test), every transactional_db case (on_commit, signals, atomic rollback), and the CI configuration (Postgres engine, coverage gate). Forbids: 200-only asserts, testing service logic via the view, missing permission combinations, running CI on SQLite when production is Postgres.

## Applies If (ALL must hold)

- Django ≥ 5.0 + DRF/Ninja + pytest-django installed.
- Service has ≥ 1 DRF endpoint and ≥ 1 service-layer function.
- CI runs against the production DB engine (PostgreSQL preferred).
- Team commits to coverage ≥ 80% gate.
- Output drives test codegen + CI config.

## Skip If (ANY kills it)

- Pure business logic with no HTTP — unit tests against services directly.
- E2E browser tests — Playwright/Cypress not pytest-django.
- Performance load tests — locust/k6 against a real env.
- Endpoint already integration-tested elsewhere — don't duplicate.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Endpoint list | YAML | [[django-api]] output |
| Service-layer function list | bullets | [[django-project-structure]] |
| CI runner config | YAML | .github/workflows/*.yml |
| Coverage current baseline | percentage | last pytest --cov run |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-fixtures]]` | api_client / authenticated_client / admin_client fixtures. |
| `[[django-pytest-factories]]` | factories used inside the integration tests. |
| `[[django-api]]` | endpoint matrix consumed here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: per-endpoint security matrix, service-layer direct tests, permission combinations, transactional_db cases, Postgres in CI, one concept per test | ~1300 |
| `content/02-output-contract.xml` | essential | JSON schema for the integration tests spec | ~1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: 200-only assert, view-tested service logic, missing permission combo, SQLite CI | ~800 |
| `content/04-procedure.xml` | deep | 6 steps: matrix → service tests → permission combos → transactional_db → CI → coverage | ~700 |
| `content/06-decision-tree.xml` | essential | Per endpoint: which fixture + which test cases? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_test_cases` | haiku | Mechanical fanout: endpoint × {401,403,200,400,404}. |
| `emit_integration_spec` | sonnet | Bounded transformation. |
| `audit_for_security` | opus | Permission combos + cross-user access checks. |

## Templates

| File | Purpose |
|---|---|
| `templates/integration-spec.json` | Reference output. |
| `templates/test_endpoint_skeleton.py` | Reference pytest module for one endpoint with all 5 cases. |
| `templates/ci-postgres.yml` | GitHub Actions snippet with Postgres service. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-integration.py` | Validate the integration spec JSON. | After spec emission. |

## Related

- [[django-pytest-fixtures]] — fixtures consumed by integration tests.
- [[django-pytest-mocking]] — boundary mocks (Celery, external API).
- [[django-api]] — endpoint contract under test.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per endpoint: write permission? → require force_authenticate per role; assert body. Per service: side effects (Celery, signals)? → transactional_db + mock at boundary. Per CI: production engine Postgres? → CI runs Postgres.
