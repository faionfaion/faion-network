---
slug: testing-js-ts-frontend
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Frontend component tests MUST use @testing-library/react (or -vue, -svelte) for DOM-centric assertions.
content_id: "a7a5263e18c5baac"
tags: [testing, vitest, jest, testing-library, typescript]
---
# Frontend JS/TS Testing with Vitest and Testing Library

## Summary

**One-sentence:** Frontend component tests MUST use @testing-library/react (or -vue, -svelte) for DOM-centric assertions.

**One-paragraph:** Frontend component tests MUST use @testing-library/react (or -vue, -svelte) for DOM-centric assertions. New projects default to vitest; legacy projects may remain on jest. Agents must be told the runner explicitly or they default to jest globals in vitest projects.

## Applies If (ALL must hold)

- Adding tests to a React/Vue/Svelte component that has no test coverage.
- Standardising test style across a frontend codebase where engineers reinvent patterns per component.
- Producing first-cut component tests during SDD in-progress/ so review focuses on behaviour, not boilerplate.
- Any Vite-based frontend project — vitest is the canonical choice.

## Skip If (ANY kills it)

- Browser E2E (multi-page flows, auth, navigation) — see playwright-automation.
- Performance testing — see perf-test-basics.
- Node.js backend JS/TS — Testing Library is DOM-only; use plain vitest/jest without render helpers.
- When the project already has a strong jest configuration with custom matchers — migrating to vitest mid-project creates churn without value.

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

- parent skill: `solo/dev/automation-tooling/`
