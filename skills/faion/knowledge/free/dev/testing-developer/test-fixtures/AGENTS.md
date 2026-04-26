# Test Fixtures

Fixture design patterns for maintainable test data: Factory, Builder, Object Mother, pytest fixtures, and database isolation.

## Summary

Covers fixture creation patterns (Factory Boy, Builder, Object Mother), pytest fixture scopes and composition, database isolation strategies (transactional rollback, Django test DB, SQLAlchemy), cleanup with yield, and conftest organization. Applies to Python-centric projects but principles transfer to other languages.

## Why

Poor fixture design causes the most persistent test suite problems: Mystery Guest (unclear data origins), God Fixture (too much shared state), scope mismatches (session fixture with function-scoped side effects), and sequence collisions in parallel runs. Structured factory patterns eliminate these.

## When To Use

- Designing pytest fixtures for a new project or refactoring existing ones
- Setting up Factory Boy for Django/SQLAlchemy model factories
- Implementing transactional rollback isolation for database tests
- Debugging scope mismatch or fixture teardown ordering issues
- Identifying Mystery Guest / God Fixture anti-patterns in a test suite

## When NOT To Use

- pytest-specific test patterns (parametrize, markers) → use `testing-pytest`
- E2E test data setup → use `e2e-testing`
- JavaScript test fixtures → use `testing-javascript`

## Content

| File | What it covers |
|------|---------------|
| `content/01-patterns.xml` | Factory/Builder/Object Mother patterns, when to use each, anti-patterns (Mystery Guest, God Fixture) |
| `content/02-pytest-fixtures.xml` | Fixture scopes, yield cleanup, composition (vertical/horizontal), conftest layering, autouse |
| `content/03-database-fixtures.xml` | Django TestCase vs pytest-django, transactional rollback, SQLAlchemy fixtures, sequence collision in xdist |

## Templates

| File | Purpose |
|------|---------|
| `templates/factory-boy-factory.py` | Factory Boy base factory with traits and sub-factories |
| `templates/conftest-transactional.py` | Transactional rollback fixture for pytest-django |
