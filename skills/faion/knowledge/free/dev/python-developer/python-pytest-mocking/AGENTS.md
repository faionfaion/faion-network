---
slug: python-pytest-mocking
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use pytest-mock's mocker fixture instead of unittest.
content_id: "2b24d0d7cdeb405d"
tags: [pytest, mocking, testing, python, pytest-mock]
---
# pytest Mocking — mocker Fixture, Autospec, Spy, and Async Mocks

## Summary

**One-sentence:** Use pytest-mock's mocker fixture instead of unittest.

**One-paragraph:** Use pytest-mock's mocker fixture instead of unittest.mock directly. The mocker fixture auto-cleans up patches after each test, supports autospec for signature validation, provides AsyncMock for async callables, and exposes a spy() helper that calls through to the real implementation while recording calls.

## Applies If (ALL must hold)

- Isolating a unit from external dependencies: HTTP APIs, email services, databases, file systems.
- Testing error paths that are hard to trigger naturally: network timeouts, disk full, auth failures.
- Verifying that a dependency is called with the correct arguments.
- Controlling non-deterministic behavior: time, random values, UUID generation.
- Replacing async callables in async test code.

## Skip If (ANY kills it)

- Over-mocking: mocking every collaborator so the test only tests the mock configuration, not real behavior.
- Mocking internal private methods — tests become coupled to implementation details and break on refactoring.
- Replacing a database with mocks in integration tests — use a real test database with transactions and rollback instead.
- Tests where testcontainers or a real service is available — mocks diverge from real API contracts over time.

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
