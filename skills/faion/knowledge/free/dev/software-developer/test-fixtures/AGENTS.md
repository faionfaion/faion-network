---
slug: test-fixtures
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for creating reusable, isolated test data: pytest fixtures with yield-based cleanup, factory functions with keyword-only overrides, database session rollback fixtures, and TypeScript factory helpers.
content_id: "e78df984790eaa80"
tags: [testing, fixtures, factories, test-data, isolation]
---
# Test Fixtures

## Summary

**One-sentence:** Patterns for creating reusable, isolated test data: pytest fixtures with yield-based cleanup, factory functions with keyword-only overrides, database session rollback fixtures, and TypeScript factory helpers.

**One-paragraph:** Patterns for creating reusable, isolated test data: pytest fixtures with yield-based cleanup, factory functions with keyword-only overrides, database session rollback fixtures, and TypeScript factory helpers. When test setup boilerplate exceeds 30% of test code, fixture consolidation eliminates duplication and prevents cross-test state pollution. Without isolation, one test's mutation causes a neighbor's failure in a random order — a bug that takes hours to isolate.

## Applies If (ALL must hold)

- Test suites where setup boilerplate has grown past 30% of test code.
- Multi-language repos where shared test data shapes (User, Order, Product) recur across dozens of files.
- Integration/E2E tests needing a seeded DB, authenticated session, or third-party stub server.
- Property-based testing where factories wrap arbitrary instances with sensible defaults.
- Agent-written tests — factories prevent LLMs from inventing inconsistent inline data.

## Skip If (ANY kills it)

- One-off test files where two inline literal objects are clearer than a factory.
- When a fixture hides the actual scenario under test (magic constants obscure intent).
- Production-style mocks pretending to be fixtures — keep mocking and fixtures separate.
- Snapshot tests where the "fixture" is the snapshot file — different concern.

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

- parent skill: `free/dev/software-developer/`
