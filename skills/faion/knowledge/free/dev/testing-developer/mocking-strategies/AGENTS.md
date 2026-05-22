---
slug: mocking-strategies
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers the five test-double types (Dummy/Stub/Spy/Mock/Fake), decision framework for what to mock (mock at boundaries, not internals), Python unittest.
content_id: "66da443901e8c430"
tags: [mocking, test-doubles, testing, unittest-mock, pytest-mock]
---
# Mocking Strategies

## Summary

**One-sentence:** Covers the five test-double types (Dummy/Stub/Spy/Mock/Fake), decision framework for what to mock (mock at boundaries, not internals), Python unittest.

**One-paragraph:** Covers the five test-double types (Dummy/Stub/Spy/Mock/Fake), decision framework for what to mock (mock at boundaries, not internals), Python unittest.mock / pytest-mock, JavaScript vi.mock / Jest, Go interface-based mocking, time mocking, and external API levels. Includes an over-mock linter script.

## Applies If (ALL must hold)

- Deciding whether to mock a dependency or use a real one
- Writing Python mocks with unittest.mock / pytest-mock
- Writing JavaScript mocks with Vitest vi.mock or Jest
- Writing Go mocks via interface substitution or mockery
- Diagnosing "mock swallows typo" bugs (MagicMock, wrong patch target)
- Auditing a test suite for over-mocking

## Skip If (ANY kills it)

- E2E tests where no mocking is desired — use e2e-testing
- Database isolation (use real DB with rollback) — use test-fixtures
- Fixture design decisions — use test-fixtures

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

- parent skill: `free/dev/testing-developer/`
