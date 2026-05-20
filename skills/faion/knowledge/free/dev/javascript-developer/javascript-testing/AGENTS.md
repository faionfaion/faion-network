---
slug: javascript-testing
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern testing patterns with Vitest and Jest.
content_id: "6c58d223e268ded4"
tags: [testing, vitest, jest, react-testing-library, msw]
---
# JavaScript Testing

## Summary

**One-sentence:** Modern testing patterns with Vitest and Jest.

**One-paragraph:** Modern testing patterns with Vitest and Jest. Configure Vitest (v2+) or Jest with jsdom environment. Write unit tests with `describe/it`, component tests with React Testing Library (query by role/label, use userEvent not fireEvent), mock API endpoints with MSW, and set coverage thresholds (80% lines/functions). Test behavior, not implementation; avoid snapshot tests on dynamically-generated HTML.

## Applies If (ALL must hold)

- Bootstrapping a test suite for a new TS/React/Node project (Vitest preferred, Jest acceptable).
- Adding tests around a refactor — write characterization tests first, then refactor under green.
- Building a component test harness with React Testing Library + userEvent + jsdom.
- Mocking modules, network (MSW), timers, or filesystem during tests.
- CI gate authoring: `vitest run --coverage` with thresholds and JUnit output.

## Skip If (ANY kills it)

- E2E flows that require a real browser and full backend — use Playwright/Cypress methodologies instead.
- Performance benchmarking — use `vitest bench`/`mitata`/`tinybench` patterns, not unit-test files.
- Visual regression — Storybook + Chromatic / Loki, not React Testing Library.
- Type-level tests for libraries — use `tsd`/`expect-type`, not Vitest assertions.

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

- parent skill: `free/dev/javascript-developer/`
