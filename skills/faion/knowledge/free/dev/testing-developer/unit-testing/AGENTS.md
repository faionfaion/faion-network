---
slug: unit-testing
tier: free
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers the FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), Arrange-Act-Assert structure, test naming conventions (method-scenario-expected, should-when, given-when-then), coverage strategies (line vs branch vs mutation), test categories, and the most damaging anti-patterns (testing implementation, not behavior).
content_id: "0f0eecaea7164387"
tags: [unit-testing, test-quality, first-properties, code-coverage, anti-patterns]
---
# Unit Testing

## Summary

**One-sentence:** Covers the FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), Arrange-Act-Assert structure, test naming conventions (method-scenario-expected, should-when, given-when-then), coverage strategies (line vs branch vs mutation), test categories, and the most damaging anti-patterns (testing implementation, not behavior).

**One-paragraph:** Covers the FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), Arrange-Act-Assert structure, test naming conventions (method-scenario-expected, should-when, given-when-then), coverage strategies (line vs branch vs mutation), test categories, and the most damaging anti-patterns (testing implementation, not behavior).

## Applies If (ALL must hold)

- Writing the first unit tests for a function, method, or class
- Reviewing unit test quality (FIRST compliance, AAA structure, naming)
- Choosing a coverage strategy for a new module
- Identifying test anti-patterns: testing internals, slow unit tests, non-isolated fixtures
- Onboarding new developers to the project test style

## Skip If (ANY kills it)

- pytest-specific features (fixtures, parametrize) — use testing-pytest
- Mocking strategy decisions — use mocking-strategies
- E2E tests — use e2e-testing
- Test fixture design — use test-fixtures

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
