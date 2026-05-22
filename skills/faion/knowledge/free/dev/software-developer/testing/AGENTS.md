---
slug: testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Cross-language testing: pytest, Jest/Vitest, Go testing, Playwright, Cypress. AAA, isolated, idempotent, 80% branches.
content_id: "dd29eb8ce0bb0e79"
complexity: medium
produces: code
est_tokens: 4000
tags: [testing, pytest, vitest, playwright, tdd]
---
# Testing (Multi-Language)

## Summary

**One-sentence:** Cross-language testing: pytest, Jest/Vitest, Go testing, Playwright, Cypress. AAA, isolated, idempotent, 80% branches.

**One-paragraph:** Comprehensive testing patterns for pytest (Python), Jest/Vitest (JavaScript/TypeScript), Go's testing package, Playwright (E2E), and Cypress. Every test follows Arrange-Act-Assert. Tests are isolated, idempotent, run in any order. Coverage threshold: 80% branches minimum.

**Ефективно для:** інженера в полі-glot репо, який потребує спільних правил тестування поверх різних рантаймів — закриває петлю між мовою і фундаментом 'isolated/idempotent/AAA'.

## Applies If (ALL must hold)

- Unit testing pure functions and services with mocks for external dependencies.
- Configuring pytest, Jest, or Vitest for a new project.
- Integration testing components with database or HTTP server.
- End-to-end testing user flows with Playwright/Cypress.

## Skip If (ANY kills it)

- Single-runtime project — load the language-specific methodology directly (python-pytest-setup, etc.).
- Pure UI work with no JS logic — visual regression instead.
- Hardware/embedded — different test strategy entirely.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Test runners installed per language | package | language-specific |
| Source code with logic to test | src/ | repo |
| CI runner | config | .github/workflows/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/unit-testing` | AAA pattern this generalises. |
| `free/dev/software-developer/tdd-workflow` | Red-Green-Refactor cycle that wires into the test suites. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: AAA pattern, isolation, idempotence, mock at process boundary, coverage ≥80% branches, fast unit tests + slow lane separation. | ~1100 |
| `content/02-output-contract.xml` | essential | Shape: per-language config + tests/ tree mirroring src/ + coverage gate + CI matrix per language. Forbidden: tests with order dependency, shared mutable state, network in unit lane. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: order-dependent tests, shared state, slow tests in unit lane, hidden cleanup failures, snapshot abuse. | ~800 |
| `content/04-procedure.xml` | medium | Steps: pick runner per language → wire config → structure tests by AAA → add coverage gate → split unit/integration/e2e lanes → wire CI matrix. | ~800 |
| `content/06-decision-tree.xml` | essential | Tree: pure logic? → unit. DB/HTTP server? → integration. Browser? → E2E. Visual? → Chromatic. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-test-lane` | sonnet | Decide unit vs integration vs e2e. |
| `scaffold-config` | haiku | Template fill per runner. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vitest.config.ts` | Vitest config with coverage and exclude patterns. |
| `templates/playwright.config.ts` | Playwright config with projects and base URL. |
| `templates/test_aaa.py` | Python AAA test skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing.py` | Detect order dependency (running subset reorders changes outcome) and shared state. | CI. |

## Related

- [[unit-testing]]
- [[tdd-workflow]]
- [[python-pytest-setup]]
- [[e2e-testing]]

## Decision tree

The tree at content/06-decision-tree.xml routes between unit / integration / E2E / visual lanes per language and per test character. Walk it before adding any new test.
