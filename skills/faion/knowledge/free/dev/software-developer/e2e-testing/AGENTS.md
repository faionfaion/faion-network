# E2E Testing

## Summary

End-to-end testing with Playwright validates complete user journeys through the full application stack. Core rules: use Page Object Model (one POM per route), select only via `data-testid` or ARIA roles, seed/tear-down test data via API never via UI, and limit the critical-path suite to <50 tests. E2E covers journeys; unit and integration tests cover logic.

## Why

E2E tests are the only layer that validates the rendered DOM, browser engine behavior, and real backend integration together. They are 10-20x slower than unit tests and are the most expensive to maintain, so they must be reserved for critical user journeys (signup, checkout, payment) and smoke gates on deploys, not for logic branches already covered by cheaper tests.

## When To Use

- Critical revenue/auth paths (login, signup, checkout, payment) with a real browser + real backend.
- Smoke suite gating production deploys — 5-15 fast tests, run post-deploy, roll back on failure.
- Cross-browser parity where engine-specific bugs can't be caught by unit tests.
- Visual-regression baselines for marketing pages.
- LLM-generated UI changes that need a rendered DOM gate.

## When NOT To Use

- Business-rule branches already covered by unit or integration tests — duplicating them adds cost with no signal.
- Input validation edge cases — drive via API tests; the browser layer is wasted cycles.
- Performance benchmarking — Playwright measurement overhead distorts numbers; use Lighthouse CI / k6.
- Pre-MVP UIs changing shape weekly — fixture/selector churn outpaces value.
- Third-party flows without a sandbox mode — non-deterministic, cannot be cleaned up.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Test pyramid position, suite size budget, selector discipline rules. |
| `content/02-page-object-model.xml` | POM structure, method naming conventions, locator rules. |
| `content/03-test-data.xml` | API-based seed/teardown pattern, fixtures, storageState for auth. |
| `content/04-antipatterns.xml` | Hard-coded waits, flaky selectors, test interdependence, over-mocking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playwright.config.ts` | Multi-browser config with retries, reporters, baseURL, webServer. |
| `templates/page-object.ts` | POM skeleton with constructor, goto, action, and assertion methods. |
| `templates/smoke-gate.sh` | Deploy gate script running `@smoke`-tagged tests against a staging URL. |
