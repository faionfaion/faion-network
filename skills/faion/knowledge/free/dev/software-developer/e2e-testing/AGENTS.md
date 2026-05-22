---
slug: e2e-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: End-to-end testing with Playwright validates complete user journeys through the full application stack.
content_id: "c0f5c08662c55afe"
tags: [playwright, e2e, testing, browser-automation, pom]
---
# End-to-End Testing with Playwright

## Summary

**One-sentence:** End-to-end testing with Playwright validates complete user journeys through the full application stack.

**One-paragraph:** End-to-end testing with Playwright validates complete user journeys through the full application stack. Core rules: use Page Object Model (one POM per route), select only via `data-testid` or ARIA roles, seed/tear-down test data via API never via UI, and limit the critical-path suite to less than 50 tests. E2E covers journeys; unit and integration tests cover logic.

## Applies If (ALL must hold)

- Critical revenue/auth paths (login, signup, checkout, payment) with a real browser + real backend.
- Smoke suite gating production deploys — 5-15 fast tests, run post-deploy, roll back on failure.
- Cross-browser parity where engine-specific bugs can't be caught by unit tests.
- Visual-regression baselines for marketing pages.
- LLM-generated UI changes that need a rendered DOM gate.

## Skip If (ANY kills it)

- Business-rule branches already covered by unit or integration tests — duplicating them adds cost with no signal.
- Input validation edge cases — drive via API tests; the browser layer is wasted cycles.
- Performance benchmarking — Playwright measurement overhead distorts numbers; use Lighthouse CI / k6.
- Pre-MVP UIs changing shape weekly — fixture/selector churn outpaces value.
- Third-party flows without a sandbox mode — non-deterministic, cannot be cleaned up.

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
