# Integration Testing

## Summary

**One-sentence:** Produces an integration-test config (pytest + Testcontainers + respx/WireMock) with rollback isolation, FastAPI/Django dependency overrides, and factory fixtures.

**One-paragraph:** Integration tests catch the class of bugs unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and middleware failures. Without containerised dependencies + rollback isolation they become slow, order-dependent, and flaky in CI. This methodology emits a runnable conftest set, dependency-override fixtures, and a WireMock/respx contract for external HTTP — pinned to the rollback-by-default discipline.

**Ефективно для:** backend team facing growing test suites where order-dependence and flakes from shared DB state are eating PR velocity.

## Applies If (ALL must hold)

- Code under test touches a database, message queue, or external HTTP service.
- pytest is the runner (or Django's pytest-django plugin).
- Docker is available locally and in CI for Testcontainers.
- Test data can be regenerated from factories — no production-data dependencies.
- Suite duration target is ≤5 minutes.

## Skip If (ANY kills it)

- Testing a single pure function with no external calls → unit-testing.
- Full user journey through a browser → e2e-testing.
- Environment cannot run Docker (some sandboxes) — must fall back to in-memory SQLite.
- Test depends on third-party SaaS behaviour that no fixture can model (run a smoke test in staging instead).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `service-graph.yaml` | list of {service, db_engine, external_apis} | operator |
| `framework` | fastapi / django / flask | repo |
| `parallel_target` | integer (worker count) | CI config |
| `secrets-redirect` | env-var names that must never hit real services | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-pytest]] | pytest-fixture scoping and parametrisation. |
| [[test-fixtures]] | factory pattern + scope decisions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: rollback default, Testcontainers scoping, dependency_overrides clear, respx vs WireMock pick, factory uniqueness, no prod data, ban mocking the layer under test. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the integration-test-config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: prod DB in CI, mocking the integration layer, shared state, missing dependency_overrides.clear(), hard-coded emails. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: inventory services → pick isolation → wire conftest → emit factories → wire external mocks. | ~700 |
| `content/05-examples.xml` | recommended | Postgres rollback + FastAPI client + respx mock end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks rollback vs truncate vs unique-ID; respx vs WireMock. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_service_graph` | haiku | Mechanical YAML→typed list. |
| `pick_isolation_strategy` | sonnet | Tradeoff between speed and constraint-violation accuracy. |
| `audit_dependency_overrides` | opus | Subtle leakage across tests when overrides aren't cleared. |
| `emit_conftest` | sonnet | Mechanical but must be importable. |

## Templates

| File | Purpose |
|---|---|
| `templates/conftest_postgres.py` | Session-scoped Postgres container + function-scoped transaction rollback session. |
| `templates/conftest_django.py` | Django conftest with Factory Boy UserFactory and admin_user fixture. |
| `templates/fastapi_client.py` | FastAPI TestClient and AsyncClient fixtures with dependency override. |
| `templates/_smoke-test.yaml` | Minimum service graph (one Postgres, one FastAPI app). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-integration-testing.py` | Validates emitted config JSON against the schema. | Pre-commit; in CI before publishing config. |

## Related

- [[testing-pytest]]
- [[unit-testing]]
- [[e2e-testing]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `db_engine_required` (yes → Testcontainers + rollback; no → in-memory), then on `parallel_target` (≥2 → unique-ID factories; 1 → sequence-based), then on `external_http_calls` (none → no mock; few/simple → respx; many/complex → WireMock container). Each leaf cites a rule id.
