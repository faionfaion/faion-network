---
slug: testing-javascript
tier: free
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers the Vitest vs Jest decision tree (2025), unit and component testing patterns, React Testing Library integration, MSW v2 for API mocking, fake timers, coverage configuration, and common pitfalls (ESM/CJS confusion, jsdom layout limitations, MSW v1→v2 migration, fake timer leaks).
content_id: "a4f472ae25eb8750"
tags: [vitest, jest, testing, react-testing-library, msw]
---
# Testing in JavaScript

## Summary

**One-sentence:** Covers the Vitest vs Jest decision tree (2025), unit and component testing patterns, React Testing Library integration, MSW v2 for API mocking, fake timers, coverage configuration, and common pitfalls (ESM/CJS confusion, jsdom layout limitations, MSW v1→v2 migration, fake timer leaks).

**One-paragraph:** Covers the Vitest vs Jest decision tree (2025), unit and component testing patterns, React Testing Library integration, MSW v2 for API mocking, fake timers, coverage configuration, and common pitfalls (ESM/CJS confusion, jsdom layout limitations, MSW v1→v2 migration, fake timer leaks).

## Applies If (ALL must hold)

- Setting up a new JavaScript/TypeScript test suite (Vitest or Jest)
- Writing unit tests for React components with React Testing Library
- Mocking HTTP calls with MSW (v2 API)
- Debugging ESM/CJS import resolution errors in tests
- Configuring fake timers without leaking state
- Migrating from Jest to Vitest

## Skip If (ANY kills it)

- E2E browser tests — use e2e-testing
- Go tests — use testing-go
- Python tests — use testing-pytest
- General mocking strategy decisions — use mocking-strategies

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
