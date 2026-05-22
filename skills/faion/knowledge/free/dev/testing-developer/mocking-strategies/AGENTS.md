---
slug: mocking-strategies
tier: free
group: dev
domain: dev
version: 2.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: c6881097df6b8595
summary: Produces a mocking-spec (per-dependency double type + boundary + tool) for a Python/JS/Go test suite, plus an over-mock lint report.
complexity: medium
produces: spec
est_tokens: 4400
tags: [mocking, test-doubles, unittest-mock, pytest-mock, vitest, jest]
---
# Mocking Strategies

## Summary

**One-sentence:** Produces a mocking-spec (per-dependency double type + boundary + tool) for a Python/JS/Go test suite, plus an over-mock lint report.

**One-paragraph:** Over-mocking is a silent suite killer: tests pass but production breaks because the mocked contract drifts. Under-mocking makes tests slow and non-deterministic. This methodology classifies every collaborator into a test-double type (Dummy/Stub/Spy/Mock/Fake), pins the mocking boundary (I/O, time, randomness, externals), prescribes autospec/spec discipline, and runs an over-mock lint pass against the existing suite.

**Ефективно для:** team whose Python/JS suite has accumulated MagicMock() noise and whose typo bugs slip past tests because mocks silently absorb attribute errors.

## Applies If (ALL must hold)

- Deciding whether to mock a dependency or use a real one.
- Writing Python mocks with unittest.mock / pytest-mock.
- Writing JavaScript mocks with Vitest vi.mock or Jest.
- Writing Go mocks via interface substitution or mockery.
- Auditing an existing suite for over-mocking.

## Skip If (ANY kills it)

- E2E tests where no mocking is desired → e2e-testing.
- Database isolation (use real DB with rollback) → integration-testing.
- Pure fixture design without mocking concerns → test-fixtures.
- Throwaway script with no test suite.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `dependency-graph.yaml` | list of {dep_name, boundary, mutability, third_party} | operator |
| `language` | python / typescript / go | repo |
| `runner` | pytest / vitest / jest / go-test | repo |
| `existing_test_dir` | path | repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-pytest]] or [[testing-javascript]] | Runner-specific scoping. |
| [[test-fixtures]] | Fake objects are a fixture-design problem. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: mock at boundaries, autospec mandatory, patch where used, no mocking what you don't own, vi.clearAllMocks each test, time mock via freezegun, prefer Fake to Mock for stateful deps. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the mocking-spec artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: MagicMock no spec, wrong-target patch, mocking value objects, missing clearAllMocks, mocking own code. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate deps → classify boundary → pick double → emit spec → lint suite. | ~700 |
| `content/05-examples.xml` | recommended | Python autospec example + Vitest module mock + Go interface mock end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Stub vs Mock vs Fake; full vs partial; mock vs leave-real. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_dependency_graph` | haiku | Mechanical YAML→typed list. |
| `classify_doubles` | sonnet | Tradeoff between stub simplicity and fake fidelity. |
| `audit_over_mocking` | opus | Cross-suite pattern detection — needs synthesis. |
| `emit_mocking_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/over-mock-lint.py` | Script detecting over-mocked Python test files. |
| `templates/mocking-spec.md` | Markdown wrapper for the JSON spec. |
| `templates/_smoke-test.yaml` | Minimum dependency graph (one HTTP client, one time call). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mocking-strategies.py` | Validates spec against the schema. | Pre-commit; in CI before lint. |

## Related

- [[testing-pytest]]
- [[integration-testing]]
- [[test-fixtures]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `is_own_code` (yes → leave real; no → continue), then on `is_io_or_time_or_random` (yes → mock at boundary; no → fake/stub by state), then on `verify_calls_needed` (yes → Mock with autospec; no → Stub/Fake). Each leaf cites a rule id.
