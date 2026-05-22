---
slug: refactoring-patterns
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Catalog of structural code transformations that improve readability and maintainability without changing external behavior: Extract Method/Function, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Numbers, Decompose Conditional, Rename for Clarity, Move Method.
content_id: "2b95c58304d49a1b"
tags: [refactoring, code-quality, patterns, maintainability]
---
# Refactoring Patterns

## Summary

**One-sentence:** Catalog of structural code transformations that improve readability and maintainability without changing external behavior: Extract Method/Function, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Numbers, Decompose Conditional, Rename for Clarity, Move Method.

**One-paragraph:** Catalog of structural code transformations that improve readability and maintainability without changing external behavior: Extract Method/Function, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Numbers, Decompose Conditional, Rename for Clarity, Move Method. Each is applied one at a time, with tests green before and after.

## Applies If (ALL must hold)

- Preparatory refactoring before a feature lands ("make the change easy, then make the easy change").
- Reducing cyclomatic complexity / function length flagged by linters or code review.
- Eliminating duplication detected by jscpd, pylint duplicate-code, or similar.
- Modernizing legacy modules: replacing magic constants, decomposing god classes, extracting strategies.
- Pre-test refactoring to make seams for mocks before adding tests.
- Post-merge cleanup pass over a freshly delivered feature.

## Skip If (ANY kills it)

- During the same change as a behavior modification — refactoring requires "tests stay green and behavior unchanged".
- When tests do not exist or do not cover the affected code paths. Add characterization tests first.
- Hot paths where the "messy" form is intentional (manual loop unrolling, allocation reuse).
- Right before a release window — defer to next cycle.
- Generated code, vendored libraries, or migration scripts.

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
