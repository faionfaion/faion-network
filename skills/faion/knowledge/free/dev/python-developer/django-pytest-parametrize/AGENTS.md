---
slug: django-pytest-parametrize
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest.
content_id: "cb26098fd6055e04"
tags: [django, pytest, parametrize, testing, validation]
---
# Django pytest Parametrize

## Summary

**One-sentence:** pytest.

**One-paragraph:** pytest.mark.parametrize eliminates repetitive tests by running the same test body with different input-output pairs. Use it for validator tests (input/valid), API validation matrices (field/value/error), permission role grids, and any set of tests that differ only in data. Each parameter set is one independently runnable test.

## Applies If (ALL must hold)

- Validator tests: one function testing many input/expected-output pairs.
- API validation matrices: same endpoint, different invalid fields and expected error messages.
- Permission role grids: same endpoint, different user roles, expected status codes.
- Error-code tests: same function, different inputs, different sets of error codes expected.
- Any group of tests that differ only in the data they operate on.

## Skip If (ANY kills it)

- Test cases that need substantially different setup or teardown — use separate fixtures or separate test functions.
- Parameter lists longer than ~20 rows — consider splitting into focused test functions with descriptive names instead.
- Cases where the test body logic changes significantly per parameter — parametrize is for data variation, not control-flow variation.

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
