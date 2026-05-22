---
slug: test-fixtures
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a conftest.py + factory module skeleton that pins function-scope isolation, yield-based cleanup, and keyword-only factory overrides so order-dependent test failures never appear.
content_id: "306135a0e818ddb3"
complexity: medium
produces: code
est_tokens: 5400
tags: [testing, fixtures, factories, pytest, isolation]
---
# Test Fixtures

## Summary

**One-sentence:** Patterns for reusable, isolated test data — function-scope pytest fixtures with yield-cleanup, keyword-only factory overrides, savepoint-rollback DB sessions.

**One-paragraph:** Produces a working `conftest.py` and a factory module that pins the discipline behind reliable test data: default `scope="function"`, `yield`-based cleanup, keyword-only factory overrides with explicit defaults, sequenced determinism for snapshot stability, and savepoint rollback for DB tests. Eliminates "tests pass alone, fail in suite" — the dominant fixture failure mode caused by shared mutable state across wider scopes.

**Ефективно для:** Python розробника, який починає новий проєкт або витягує спільні setup-блоки з 200 інлайнових літералів — закладає шаблон, який не протікає станом між тестами.

## Applies If (ALL must hold)

- Test setup boilerplate exceeds 30% of test code or the same shape (User/Order/Product) recurs across dozens of files.
- Test suite uses pytest (Python) or a yield-based fixture runtime (vitest beforeEach/afterEach is comparable).
- Tests need a seeded DB, authenticated session, or third-party stub server with deterministic cleanup.
- Agent-written tests are involved — factories prevent LLMs from inventing inconsistent inline data.
- The team can commit to `scope="function"` as default and profile before widening.

## Skip If (ANY kills it)

- One-off test files where two inline literal objects are clearer than a factory.
- Fixtures that hide the actual scenario under test (magic constants obscure intent).
- Production-style mocks pretending to be fixtures — keep mocking and fixtures in separate modules.
- Snapshot tests where the "fixture" is the snapshot file — different concern, use `pytest-regressions` instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Model/entity definitions (User, Order, ...) | Python class / ORM model | `src/models/` or equivalent |
| Existing test files with repeated setup | `.py` files | `tests/` |
| DB session factory (for DB fixtures) | SQLAlchemy / Django ORM | `src/db/` |
| Coverage of `pytest --collect-only` baseline | text dump | CI artifact or local run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/testing` | Defines the broader test pyramid and AAA structure this fixture layer slots into. |
| `free/dev/testing-developer/tdd-workflow` | Red-green-refactor needs factories so the "Arrange" phase is cheap. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: function scope default, yield cleanup, keyword-only factories, sequenced determinism, conftest layering | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the fixture/factory module spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: scope leakage, faker non-determinism, factory drift, autouse cost, cleanup-order, parallel runner assumptions | ~1100 |
| `content/04-procedure.xml` | medium | 5-step recipe: identify repetition → write factory → wire fixture → assert isolation → ratchet scope | ~900 |
| `content/06-decision-tree.xml` | essential | Decide: inline literal vs factory vs full fixture | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-repeated-setup` | sonnet | AST-aware repetition detection across the test tree. |
| `write-factory-module` | sonnet | Mechanical scaffold from model + sample data. |
| `tune-scope` | opus | Cross-test reasoning about state mutability before widening scope. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest-db.py` | SQLAlchemy session fixture with savepoint rollback per test. |
| `templates/fixture-pollution-check.sh` | Runs pytest with random ordering seeds to detect order-dependent failures. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-fixtures.py` | Validate a fixture/factory module spec JSON against the canonical schema; checks defaults, scope, kwarg-only enforcement. | Pre-merge gate; weekly drift scan. |

## Related

- [[testing]] — parent multi-language testing playbook.
- [[unit-testing]] — sibling that consumes these factories.
- [[tdd-workflow]] — outer red-green-refactor flow.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides between three outcomes: inline literal (one-off, ≤2 fields), factory function (≥3 reuse sites, no resource cleanup needed), or full fixture (resource acquisition + cleanup). Use it the moment you spot a third copy of the same setup block — before reaching for `scope="session"`.
