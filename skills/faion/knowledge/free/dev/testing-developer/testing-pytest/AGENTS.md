---
slug: testing-pytest
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers pytest configuration, fixture scopes and composition, parametrize patterns, mocking with unittest.
content_id: "a24ec990a7c53f98"
tags: [pytest, testing, python, fixtures, parametrize]
---
# Testing with pytest

## Summary

**One-sentence:** Covers pytest configuration, fixture scopes and composition, parametrize patterns, mocking with unittest.

**One-paragraph:** Covers pytest configuration, fixture scopes and composition, parametrize patterns, mocking with unittest.mock/pytest-mock, parallel execution with xdist, async testing, and coverage reporting. Primary testing framework for Python projects.

## Applies If (ALL must hold)

- Writing Python tests with pytest (unit, integration, or functional)
- Designing fixture hierarchies (scope, composition, yield cleanup)
- Setting up pytest configuration (pyproject.toml, markers, coverage)
- Parametrizing tests to cover edge cases without duplication
- Mocking external dependencies via unittest.mock or pytest-mock
- Running tests in parallel with pytest-xdist
- Testing async code with pytest-asyncio

## Skip If (ANY kills it)

- E2E browser tests — use e2e-testing
- Go tests — use testing-go
- JavaScript tests — use testing-javascript
- General fixture design patterns (framework-agnostic) — use test-fixtures

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
