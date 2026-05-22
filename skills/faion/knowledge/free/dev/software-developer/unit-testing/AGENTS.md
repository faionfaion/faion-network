---
slug: unit-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for writing isolated, deterministic tests that verify a single behavior per test using the Arrange-Act-Assert pattern.
content_id: "0f0eecaea7164387"
tags: [unit-testing, pytest, aaa-pattern, test-doubles, tdd]
---
# Unit Testing

## Summary

**One-sentence:** A methodology for writing isolated, deterministic tests that verify a single behavior per test using the Arrange-Act-Assert pattern.

**One-paragraph:** A methodology for writing isolated, deterministic tests that verify a single behavior per test using the Arrange-Act-Assert pattern. Each test names its scenario explicitly (`test_<behavior>_when_<context>`), uses fixtures or fakes for setup, and mocks only at process boundaries (network, disk, clock).

## Applies If (ALL must hold)

- New code with branching logic, math, parsing, validation, or state transitions.
- Refactoring legacy code — safety net before changing internals.
- Bug fixes — write the failing test first, then fix.
- Boundary cases: empty inputs, min/max, off-by-one, unicode, time zones.
- TDD workflow: spec → failing test → impl → green → refactor.
- New code with branching logic, math, parsing, validation, or state transitions — pure functions and small classes.
- Refactor of legacy code where you need a safety net before changing internals.
- Bug fixes — write a failing test reproducing the bug FIRST, then fix.
- Boundary cases (empty inputs, max/min, off-by-one, time-zones, locale, unicode edge cases).
- Self-documenting executable specs alongside docs.

## Skip If (ANY kills it)

- Pure plumbing (controller → service → repo) — integration test is more honest.
- UI rendering — visual regression or snapshot tests catch more; unit tests on JSX are brittle.
- Network protocols, DB-specific queries, cache eviction — needs real dependency.
- Code ≤5 lines that is trivially correct (`return a + b`).
- High-churn experimental / spike code — tests rot faster than the code; defer.
- Pure plumbing (controller calls service calls repo) — integration test is more honest, fewer mocks.
- UI rendering — visual regression / snapshot tests catch more, unit tests on JSX/HTML brittle.
- Network protocols, DB-specific queries, cache eviction — needs a real dependency, integration territory.
- Code that's ≤5 lines and trivially correct (`def add(a, b): return a + b`) — coverage noise.
- High-churn experimental code (spike, prototype) — tests rot faster than the code; defer.

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
