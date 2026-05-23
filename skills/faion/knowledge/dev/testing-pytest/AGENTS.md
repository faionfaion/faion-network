# Testing with pytest

## Summary

**One-sentence:** Produces a pytest 8.x suite: fixture scopes wired correctly, `parametrize` for case explosion, `pytest-mock` for collaborators, `pytest-xdist` for parallel CI, coverage gated in `pyproject.toml`.

**One-paragraph:** Covers pytest configuration, fixture scopes and composition, `parametrize` patterns, mocking with `unittest.mock` / `pytest-mock`, parallel execution with xdist, async testing, and coverage reporting. pytest is the de-facto Python test runner. Its fixture injection model, plugin ecosystem, and parametrize decorator eliminate boilerplate and enforce isolation. Knowing scope rules and conftest layering prevents the most common pytest anti-patterns that cause hard-to-debug test pollution.

**Ефективно для:** any Python project on pytest 8.x — Django, FastAPI, plain library code; CI suites that need `-n auto` parallelism; async pytest via `pytest-asyncio`; fixture trees deeper than 2 levels.

## Applies If (ALL must hold)

- Writing Python tests with pytest (unit, integration, or functional)
- Migrating `unittest.TestCase` classes to pytest function style
- Building a fixture tree with `conftest.py` at multiple levels
- Parametrizing a case explosion (≥4 input rows)
- Speeding up CI with `pytest-xdist` parallel workers

## Skip If (ANY kills it)

- Non-Python tests — use `[[testing-go]]` or `[[testing-javascript]]`
- End-to-end browser tests — use `[[e2e-testing]]`
- Project still on `unittest` with no migration appetite — defer

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pytest dep | `pytest>=8.0` in pyproject.toml / requirements | `pip install pytest` |
| pyproject.toml or pytest.ini | TOML/INI | project root |
| Function under test | Python module | source tree |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[unit-testing]]` | FIRST principles |
| `[[mocking-strategies]]` | When to mock vs use real collaborator |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author parametrized test | sonnet | Pattern from template. |
| Pick fixture scope | sonnet | Rubric from r2. |
| Diagnose order-dependent failure | opus | Cross-fixture state reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py.tmpl` | Project-wide fixture skeleton with scopes and teardown. |
| `templates/test_module.py.tmpl` | Function-style test with parametrize + mocker. |
| `templates/pyproject-pytest.toml.tmpl` | Pyproject section for pytest + coverage config. |
| `templates/test_async.py.tmpl` | Async test using `@pytest.mark.asyncio`. |
| `templates/_smoke-test.py` | Minimal pytest sanity test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-pytest.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/dev/testing-developer/`
- `[[testing-go]]`
- `[[testing-javascript]]`
- `[[testing-patterns]]`
- `[[unit-testing]]`
- `[[mocking-strategies]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether testing-pytest applies: root question — "Is the test target Python code intended for pytest 8.x?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
