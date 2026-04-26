# Testing with pytest

pytest 8.x test suite authoring: fixtures, parametrization, markers, async testing, coverage, and CI integration.

## Summary

Covers pytest configuration, fixture scopes and composition, parametrize patterns, mocking with unittest.mock/pytest-mock, parallel execution with xdist, async testing, and coverage reporting. Primary testing framework for Python projects.

## Why

pytest is the de-facto Python test runner. Its fixture injection model, plugin ecosystem, and parametrize decorator eliminate boilerplate and enforce isolation. Knowing scope rules and conftest layering prevents the most common pytest anti-patterns that cause hard-to-debug test pollution.

## When To Use

- Writing Python tests with pytest (unit, integration, or functional)
- Designing fixture hierarchies (scope, composition, yield cleanup)
- Setting up pytest configuration (pyproject.toml, markers, coverage)
- Parametrizing tests to cover edge cases without duplication
- Mocking external dependencies via unittest.mock or pytest-mock
- Running tests in parallel with pytest-xdist
- Testing async code with pytest-asyncio

## When NOT To Use

- E2E browser tests → use `e2e-testing`
- Go tests → use `testing-go`
- JavaScript tests → use `testing-javascript`
- General fixture design patterns (framework-agnostic) → use `test-fixtures`

## Content

| File | What it covers |
|------|---------------|
| `content/01-configuration.xml` | pyproject.toml setup, plugin selection, markers, coverage, xdist config |
| `content/02-fixtures.xml` | Fixture scopes (function/class/module/session), yield cleanup, conftest layering, factory fixtures |
| `content/03-patterns.xml` | AAA structure, parametrize (basic/IDs/cartesian/indirect), mocking patterns, async tests, debugging |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject-pytest.toml` | pytest + coverage + xdist + asyncio config block |
| `templates/conftest-base.py` | Base conftest.py with common fixtures (db, client, factory) |
