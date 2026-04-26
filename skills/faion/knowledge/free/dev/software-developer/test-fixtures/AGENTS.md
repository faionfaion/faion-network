# Test Fixtures

## Summary

Patterns for creating reusable, isolated test data: pytest fixtures with yield-based cleanup, factory functions with keyword-only overrides, database session rollback fixtures, and TypeScript factory helpers. Core rule: `scope="function"` is the safe default — only widen after profiling proof and immutability check; factories must use sequenced determinism, not random Faker, to keep snapshots stable.

## Why

When test setup boilerplate exceeds 30% of test code, fixture consolidation eliminates duplication and prevents cross-test state pollution. Without isolation, one test's mutation causes a neighbor's failure in a random order — a bug that takes hours to isolate. Factory functions with keyword-only overrides create a single source of truth for test object defaults so that changing a model field breaks only the factory, not 200 tests.

## When To Use

- Test suites where setup boilerplate has grown past 30% of test code.
- Multi-language repos where shared test data shapes (User, Order, Product) recur across dozens of files.
- Integration/E2E tests needing a seeded DB, authenticated session, or third-party stub server.
- Property-based testing where factories wrap arbitrary instances with sensible defaults.
- Agent-written tests — factories prevent LLMs from inventing inconsistent inline data.

## When NOT To Use

- One-off test files where two inline literal objects are clearer than a factory.
- When a fixture hides the actual scenario under test (magic constants obscure intent).
- Production-style mocks pretending to be fixtures — keep mocking and fixtures separate.
- Snapshot tests where the "fixture" is the snapshot file — different concern.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pytest-fixtures.xml` | Scopes, yield cleanup, fixture composition, `conftest.py` layout. |
| `content/02-factories.xml` | Factory functions, factory_boy, Faker seeding, builder pattern for complex objects. |
| `content/03-ts-fixtures.xml` | TypeScript factory helpers, fishery, Jest fixture patterns. |
| `content/04-antipatterns.xml` | Scope leakage, yield+cleanup race, factory drift, Faker non-determinism. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest-db.py` | SQLAlchemy session fixture with savepoint rollback for isolation. |
| `templates/fixture-pollution-check.sh` | Runs pytest with random order seeds to detect order-dependent failures. |
