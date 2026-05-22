---
slug: e2e-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a critical-path Playwright E2E suite (<50 specs) with Page Object Model, data-testid + ARIA locators, API-based seeding, and a smoke-gate script wired into deploy.
content_id: "c0f5c08662c55afe"
complexity: medium
produces: code
est_tokens: 4200
tags: [playwright, e2e, testing, browser-automation, pom]
---
# End-to-End Testing with Playwright

## Summary

**One-sentence:** Produces a critical-path Playwright E2E suite (<50 specs) with Page Object Model, data-testid + ARIA locators, API-based seeding, and a smoke-gate script wired into deploy.

**One-paragraph:** Playwright E2E validates complete user journeys through the full application stack — rendered DOM, browser engine, real backend. Core rules: one Page Object per route with intent-named methods (`login()`, not `clickSubmitButton()`); locate only via `getByRole`, `getByLabel`, or `getByTestId`; seed and clean up test data via API in `beforeEach`/`afterEach`; cap the critical-path suite at less than 50 tests so it stays under 30 minutes in CI; reuse `storageState` for authenticated flows; mock third-party APIs at the network boundary with `page.route()`. E2E covers journeys; unit and integration tests cover logic.

**Ефективно для:** signup/login/checkout/payment journeys, post-deploy smoke gates, cross-browser parity checks, visual-regression baselines on marketing pages, LLM-generated UI changes that need a rendered-DOM gate.

## Applies If (ALL must hold)

- Critical revenue/auth paths (login, signup, checkout, payment) need a real browser + real backend.
- Smoke suite gates production deploys — 5-15 fast tests, run post-deploy, roll back on failure.
- Cross-browser parity matters where engine-specific bugs can't be caught by unit tests.
- LLM-generated UI changes need a rendered DOM gate before merge.

## Skip If (ANY kills it)

- Business-rule branches already covered by unit or integration tests — duplicating them adds cost with no signal.
- Input validation edge cases — drive via API tests; the browser layer is wasted cycles.
- Performance benchmarking — Playwright measurement overhead distorts numbers; use Lighthouse CI / k6.
- Pre-MVP UIs changing shape weekly — fixture/selector churn outpaces value.
- Third-party flows without a sandbox mode — non-deterministic, cannot be cleaned up.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of critical user journeys | Markdown bullet list | PM/BA spec or `journeys.md` |
| Staging URL + test API base URL | env vars `BASE_URL`, `API_URL` | CI secrets / `.env.test` |
| Test-data API (create/delete user, seed product) | REST endpoints | backend test fixtures |
| `data-testid` attributes on critical elements | HTML attributes | frontend code |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `integration-testing` | Knows the API endpoints used for seeding test data. |
| `javascript` | TS strict-mode + ESLint conventions apply to spec files. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules: locator policy, no sleeps, API seeding, POM, suite cap, mocking | ~800 |
| `content/02-output-contract.xml` | essential | Required project shape: `e2e/pages/*.ts`, `e2e/fixtures.ts`, `e2e/*.spec.ts`, `playwright.config.ts` | ~700 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: hard sleeps, CSS selectors, shared accounts, cross-OS snapshots, `force:true`, unbounded suite, leaked traces | ~700 |
| `content/04-procedure.xml` | medium | 6-step procedure: enumerate journeys → write POMs → write specs → wire smoke gate → run → triage flakes | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "Is this a critical user journey not covered by unit/integration tests?" | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Enumerate journeys from spec | sonnet | Pattern-match against templates; no novel reasoning. |
| Write Page Object skeleton | sonnet | Mechanical from data-testid list + route. |
| Write spec.ts using POM | sonnet | Compose POM calls + fixtures. |
| Triage failed test (trace.zip) | opus | Multi-modal reasoning across screenshot + network + DOM. |

## Templates

| File | Purpose |
|------|---------|
| `templates/page-object.ts` | POM skeleton with constructor, goto, action, expect methods. |
| `templates/playwright.config.ts` | Multi-browser config with retries, reporters, baseURL, webServer. |
| `templates/smoke-gate.sh` | Deploy gate script running `@smoke`-tagged tests against staging URL. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-e2e-testing.py` | Validates that an E2E project directory matches the output contract (POMs exist, no `waitForTimeout`, no CSS selectors). | Pre-commit gate; CI before `npx playwright test`. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[integration-testing]]` — API-level seeding endpoints
- `[[mocking-strategies]]` — choosing the right test double at the network boundary

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether an incoming testing need belongs in E2E at all: critical journey not covered cheaper → write E2E; logic branch covered by unit/integration → skip; pre-MVP UI churning weekly → skip.
