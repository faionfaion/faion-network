---
slug: python-pytest-parametrize
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: @pytest.
content_id: "8446275e77fd8ff0"
tags: [pytest, parametrize, testing, python]
---
# pytest Parametrize — Input Matrices, IDs, Stacking, and Indirect

## Summary

**One-sentence:** @pytest.

**One-paragraph:** @pytest.mark.parametrize eliminates repeated test functions by running a single test body against multiple (input, expected) pairs. Use pytest.param() for per-case marks and ids; stack decorators for cartesian products; use indirect=True to feed params through fixtures.

## Applies If (ALL must hold)

- Validation functions with many valid/invalid input cases.
- Business logic with multiple branches that need individual coverage.
- Boundary conditions: empty string, None, zero, max value, off-by-one.
- Cross-product testing: multiple statuses × multiple roles, or multiple backends.
- Converting repetitive similar tests into a single parametrized test.

## Skip If (ANY kills it)

- Tests that require entirely different setup per case — use separate test functions or fixtures instead.
- More than ~20 params in one decorator — split into multiple focused test functions for readability.
- Cases where the "expected" differs so much that the test body becomes a conditional — that is multiple tests.

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
