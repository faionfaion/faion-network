---
slug: python-pytest-fixtures
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest fixtures are functions decorated with @pytest.
content_id: "cceb22299bab846e"
tags: [pytest, fixtures, testing, python, dependency-injection]
---
# pytest Fixtures — Scopes, Yield, Factory, and Composition

## Summary

**One-sentence:** pytest fixtures are functions decorated with @pytest.

**One-paragraph:** pytest fixtures are functions decorated with @pytest.fixture that provide reusable setup and teardown logic through dependency injection. They eliminate setUp/tearDown boilerplate and allow fine-grained resource lifecycle control via scopes and yield.

## Applies If (ALL must hold)

- Any test that needs shared setup — database connections, API clients, sample data.
- Tests where teardown matters — closing connections, cleaning temp files, flushing caches.
- Tests needing flexible data — factory fixtures allow per-test customization without repetition.
- Expensive setup that can be shared — session-scoped fixtures run once for the whole test suite.
- Composing complex test scenarios from smaller reusable pieces.

## Skip If (ANY kills it)

- One-off setup that is only used in a single test — inline setup is clearer.
- autouse=True for fixtures with DB or HTTP side effects — applies to ALL tests in scope, causing surprises.
- Sharing mutable state between tests via a wide-scoped fixture — use function scope or reset the state explicitly.
- Fixtures that depend on test execution order — pytest-randomly will expose the dependency as a flake.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/python-developer/`
