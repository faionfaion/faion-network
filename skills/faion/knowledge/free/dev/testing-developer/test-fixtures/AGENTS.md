---
slug: test-fixtures
tier: free
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers fixture creation patterns (Factory Boy, Builder, Object Mother), pytest fixture scopes and composition, database isolation strategies (transactional rollback, Django test DB, SQLAlchemy), cleanup with yield, and conftest organization.
content_id: "e78df984790eaa80"
tags: [fixtures, testing, factory-boy, pytest, database-testing]
---
# Test Fixtures

## Summary

**One-sentence:** Covers fixture creation patterns (Factory Boy, Builder, Object Mother), pytest fixture scopes and composition, database isolation strategies (transactional rollback, Django test DB, SQLAlchemy), cleanup with yield, and conftest organization.

**One-paragraph:** Covers fixture creation patterns (Factory Boy, Builder, Object Mother), pytest fixture scopes and composition, database isolation strategies (transactional rollback, Django test DB, SQLAlchemy), cleanup with yield, and conftest organization. Applies to Python-centric projects but principles transfer to other languages.

## Applies If (ALL must hold)

- Designing pytest fixtures for a new project or refactoring existing ones
- Setting up Factory Boy for Django/SQLAlchemy model factories
- Implementing transactional rollback isolation for database tests
- Debugging scope mismatch or fixture teardown ordering issues
- Identifying Mystery Guest / God Fixture anti-patterns in a test suite

## Skip If (ANY kills it)

- pytest-specific test patterns (parametrize, markers) — use testing-pytest
- E2E test data setup — use e2e-testing
- JavaScript test fixtures — use testing-javascript

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
