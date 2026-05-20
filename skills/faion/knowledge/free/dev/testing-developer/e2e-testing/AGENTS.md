---
slug: e2e-testing
tier: free
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Guides writing maintainable E2E tests using the Page Object Model, handling authentication, API mocking, visual regression, and sharded CI pipelines.
content_id: "c0f5c08662c55afe"
tags: [e2e, playwright, cypress, testing, browser-automation]
---
# E2E Testing

## Summary

**One-sentence:** Guides writing maintainable E2E tests using the Page Object Model, handling authentication, API mocking, visual regression, and sharded CI pipelines.

**One-paragraph:** Guides writing maintainable E2E tests using the Page Object Model, handling authentication, API mocking, visual regression, and sharded CI pipelines. Covers Playwright (primary) and Cypress (secondary).

## Applies If (ALL must hold)

- Writing or reviewing Playwright / Cypress test suites
- Setting up E2E infrastructure from scratch (config, auth, CI sharding)
- Debugging flaky tests or selector failures
- Adding visual regression checks
- Migrating from Cypress to Playwright

## Skip If (ANY kills it)

- Unit or integration tests (no browser needed) → use unit-testing or testing-pytest
- API-only testing → use HTTP client directly
- OAuth flows with real external providers (use storageState workaround instead)

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
