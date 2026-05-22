---
slug: mocking-strategies
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Test doubles (stubs, mocks, spies, fakes) isolate code under test from external dependencies.
content_id: "66da443901e8c430"
tags: [testing, mocking, test-doubles, unit-tests]
---
# Mocking Strategies

## Summary

**One-sentence:** Test doubles (stubs, mocks, spies, fakes) isolate code under test from external dependencies.

**One-paragraph:** Test doubles (stubs, mocks, spies, fakes) isolate code under test from external dependencies. Use the smallest double that validates the required behavior: fake for repository abstractions, stub for state return values, mock only when the call itself is part of the contract, spy to wrap real objects.

## Applies If (ALL must hold)

- Isolating unit tests from databases, HTTP services, filesystems, clocks, or randomness
- Testing error handling and edge cases by controlling what a dependency returns
- Verifying that a specific interaction (e.g., email sent on order placement) occurred
- Replacing slow I/O with instant in-memory fakes for the service layer
- Writing characterization tests around legacy code by stubbing its dependencies

## Skip If (ANY kills it)

- Integration tests that should hit a real DB/queue/cache — use Testcontainers instead
- Pure functions — they need no mocks; mocking their inputs reveals a design smell
- Tests of the boundary itself (the HTTP client, the SQL layer) — test against real or VCR-recorded backend
- End-to-end tests — should exercise real services in a controlled environment
- When a 30-line FakeRepository is cheaper to maintain than setting up mocks per test

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
