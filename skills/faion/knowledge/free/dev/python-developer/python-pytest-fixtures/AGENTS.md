---
slug: python-pytest-fixtures
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: pytest fixtures: scopes, yield, factory pattern, composition, autouse — DI for tests.
content_id: "cceb22299bab846e"
complexity: medium
produces: code
est_tokens: 3700
tags: [pytest, fixtures, testing, python, dependency-injection]
---
# pytest Fixtures

## Summary

**One-sentence:** pytest fixtures: scopes, yield, factory pattern, composition, autouse — DI for tests.

**One-paragraph:** pytest fixtures are functions decorated with @pytest.fixture that provide reusable setup and teardown via dependency injection. They replace setUp/tearDown boilerplate and allow fine-grained lifecycle control via scopes (function/class/module/session) and yield. Factory fixtures parametrise creation; autouse fixtures inject automatically; composition makes complex setups linear.

**Ефективно для:** інженера, який пише або рефакторить тести — закриває петлю між разовою set-up прозою і повторним DI-фіксчуром із чітким scope і teardown.

## Applies If (ALL must hold)

- Any test that needs shared setup — DB connections, API clients, sample data.
- Tests where teardown matters — closing connections, cleaning temp files, flushing caches.
- Repeated setup across many tests — extract to fixture instead of helper function.
- Per-test parametrisation of setup data via factory fixtures.

## Skip If (ANY kills it)

- One-off test with no shared setup.
- Setup involves a global side effect (env vars) — use monkeypatch fixture instead.
- Class-based unittest.TestCase tests — fixtures are pytest-only.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pytest installed | package | uv add --dev pytest |
| tests/conftest.py | Python | repo root tests/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-pytest-setup` | Defines pytest config and discovery conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: pick narrowest scope, yield for teardown, factory fixture for parametrised setup, autouse rarely, composition by dependency, no I/O in module-scope without cleanup. | ~1000 |
| `content/02-output-contract.xml` | essential | Shape: tests/conftest.py with fixtures sorted by scope; per-test files use them via DI. Forbidden: setUp/tearDown style, autouse for everything, fixture with side effects no teardown. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: scope too wide, no teardown, autouse on heavy fixture, mutable shared state, fixture-of-fixture infinite loop. | ~800 |
| `content/04-procedure.xml` | medium | Steps: identify shared setup → pick scope → write fixture (yield if teardown) → compose dependencies → register in conftest. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: setup needed once per session? → session. Per module? → module. Per test? → function (default). Need parametrisation? → factory fixture. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-conftest` | haiku | Boilerplate from template. |
| `design-fixture-graph` | sonnet | Compose dependencies with scope reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Skeleton: function-scope client, session-scope DB, factory fixture, yield teardown. |
| `templates/test_with_fixtures.py` | Tests composing the fixtures. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-fixtures.py` | Check that fixtures with side effects use yield, no autouse on session-scope without justification. | Pre-commit. |

## Related

- [[python-pytest-setup]]
- [[python-pytest-async]]
- [[python-pytest-mocking]]
- [[python-pytest-parametrize]]

## Decision tree

The tree at content/06-decision-tree.xml decides the right scope, factory vs plain fixture, and autouse vs explicit injection. Walk it whenever you write a new conftest entry.
