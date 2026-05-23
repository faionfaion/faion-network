# Test Fixtures

## Summary

**One-sentence:** Produces a fixture-design config (Factory Boy + scope choices + rollback strategy + xdist isolation) for pytest/pytest-django suites.

**One-paragraph:** Poor fixture design causes the most persistent test-suite problems: Mystery Guest (data appearing from nowhere), God Fixture (one fixture creates everything), scope mismatches, and Sequence collisions under xdist. This methodology emits a fixture-design config that pins the Factory/Builder/Object-Mother choice per model, scope per fixture, transactional rollback wiring, and a worker-id-aware DB setup for parallel runs.

**Ефективно для:** Python backend whose pytest suite has 3+ "magic" autouse fixtures, where new contributors can't tell which fixture creates which row.

## Applies If (ALL must hold)

- Designing pytest fixtures for a new project or refactoring existing ones.
- Setting up Factory Boy for Django/SQLAlchemy model factories.
- Implementing transactional rollback isolation for database tests.
- Debugging scope-mismatch or fixture-teardown ordering issues.
- Identifying Mystery Guest / God Fixture anti-patterns in a suite.

## Skip If (ANY kills it)

- pytest-specific test patterns (parametrize, markers) → testing-pytest.
- E2E test data setup → e2e-testing.
- JavaScript test fixtures → testing-javascript.
- Decision is about mocking, not fixtures → mocking-strategies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `model-inventory.yaml` | list of {model, reuse_count, has_unique_fields, has_subobjects} | operator |
| `framework` | django / sqlalchemy / sqlmodel | repo |
| `xdist_workers` | integer | CI config |
| `conftest_path` | path | repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-pytest]] | scope semantics and yield-fixture mechanics. |
| [[integration-testing]] | DB rollback discipline aligns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: scope must match state, yield not addfinalizer, no Mystery Guest, no God Fixture, factory uniqueness, xdist worker DB, autouse documented. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the fixture-design config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: Mystery Guest, God Fixture, wide-scope+stateful, Sequence collisions, undocumented autouse. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: inventory models → pick pattern (Factory/Builder/Mother) → assign scope → wire rollback → emit conftest. | ~700 |
| `content/05-examples.xml` | recommended | Django Factory Boy + sqlalchemy rollback + xdist worker_id end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Factory vs Builder vs Object Mother; function vs module vs session scope; UUID vs Sequence. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_model_inventory` | haiku | Mechanical YAML→typed list. |
| `pick_pattern_per_model` | sonnet | Tradeoff between Factory simplicity and Builder/Mother semantic clarity. |
| `audit_existing_fixtures` | opus | Detecting Mystery Guest / God Fixture in existing conftest. |
| `emit_conftest` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/factory-boy-factory.py` | Factory Boy base factory with traits and sub-factories. |
| `templates/conftest-transactional.py` | Transactional rollback fixture for pytest-django. |
| `templates/_smoke-test.yaml` | Minimum model inventory. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-test-fixtures.py` | Validates emitted config against the schema. | Pre-commit. |

## Related

- [[testing-pytest]]
- [[integration-testing]]
- [[mocking-strategies]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `has_subobjects` (yes → SubFactory; no → continue), then on `has_many_optional_fields` (yes → Builder; no → continue), then on `domain_scenarios_named` (yes → Object Mother; no → plain Factory). Scope branches on `is_stateful` and `xdist_workers`. Each leaf cites a rule id.
