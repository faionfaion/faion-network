---
slug: testing-patterns
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Proven structural and data patterns for writing maintainable, reliable tests — applicable across Python, TypeScript, and Go.
content_id: "eecdde02f42a7f18"
tags: [testing, test-patterns, aaa, page-object-model, test-doubles]
---
# Testing Patterns

## Summary

**One-sentence:** Proven structural and data patterns for writing maintainable, reliable tests — applicable across Python, TypeScript, and Go.

**One-paragraph:** Proven structural and data patterns for writing maintainable, reliable tests — applicable across Python, TypeScript, and Go. Covers test structure (AAA/GWT), data creation (Builder/Object Mother), test doubles, architecture strategy (pyramid), UI patterns (POM), isolation, and property-based testing.

## Applies If (ALL must hold)

- Establishing or reviewing a test strategy for a new project
- Refactoring tangled tests that are hard to maintain
- Adding test coverage to a module with complex data setup
- Building E2E test suites that need to survive UI churn
- Choosing between test double types (mock vs stub vs fake)

## Skip If (ANY kills it)

- Trivial one-off scripts with no business logic
- Pure data-transformation functions with no branches — just use direct assertions

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
