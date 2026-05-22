---
slug: tdd-workflow
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Red-Green-Refactor cycle for test-driven development: write one failing test, write minimal code to pass it, then improve structure without changing behavior.
content_id: "27ccc09764ef490f"
tags: [tdd, testing, red-green-refactor, verification, workflow]
---
# TDD Workflow

## Summary

**One-sentence:** Red-Green-Refactor cycle for test-driven development: write one failing test, write minimal code to pass it, then improve structure without changing behavior.

**One-paragraph:** Red-Green-Refactor cycle for test-driven development: write one failing test, write minimal code to pass it, then improve structure without changing behavior. Agents skip the RED step and write implementation first, then tests that validate what they wrote — this is rationalization, not verification. Without an enforced cycle, code is untestable by design and refactors break silently. TDD forces the interface to be designed from the consumer's perspective before any implementation exists.

## Applies If (ALL must hold)

- Bug-fix workflow: reproduce the bug as a failing test before touching production code.
- Pure-function or business-logic implementation where requirements are precise (validators, calculators, parsers).
- API contract design — tests document the public surface before any handler exists.
- Library / SDK work where consumers depend on a stable interface.
- Onboarding an agent to an unfamiliar codebase — writing tests first forces reading the existing API.

## Skip If (ANY kills it)

- Exploratory spikes or research code — feedback loop is faster without tests.
- UI prototypes where the design changes hourly.
- Glue scripts and one-off migrations.
- Code intrinsically hard to test (rendering, hardware drivers, framework internals).
- Hot-fix under outage pressure — write the fix, add the regression test in a follow-up PR.

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
