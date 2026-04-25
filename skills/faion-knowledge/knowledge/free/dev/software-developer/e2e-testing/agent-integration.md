# Agent Integration — E2E Testing

## When to use
- Validating critical revenue paths (signup, checkout, payment, login) with real browser + real backend.
- Smoke suite gating production deploys — 5–15 fast Playwright tests, run after deploy, roll back on failure.
- Cross-browser parity (Chromium / WebKit / Firefox) where unit tests can't catch engine-specific bugs.
- Visual-regression baselines for marketing pages where pixel-level drift breaks brand.
- LLM-generated UI changes — agents shipping React/Vue PRs need an E2E gate that exercises the rendered DOM, not the JSX.
- Replacing a brittle Selenium suite — Playwright auto-waits eliminate ~80% of historical flakes.

## When NOT to use
- Validating business-rule branches that pure unit / integration tests already cover. E2E is the slowest, most expensive layer of the test pyramid; do not duplicate.
- Edge cases on input validation. Drive forms via API tests; the browser layer is wasted cycles.
- Performance benchmarking — Playwright's measurement overhead distorts numbers. Use Lighthouse CI / k6 / WebPageTest.
- Pre-MVP UIs that change shape weekly — fixture/selector churn outpaces value.
- Anything you can't seed and tear down deterministically (third-party SaaS popups, payment gateways without sandbox modes).

## Where it fails / limitations
- **Test-data drift.** Tests share staging DB; one flaky test leaves orphaned rows; next run fails on `unique_email` violation. Always seed via API in `beforeEach` with timestamped data, clean up in `afterEach`.
- **Auth state explosion.** Logging in via UI per test is slow. Use `storageState` (saved auth cookies) but agents forget to refresh when sessions expire.
- **Network-dependent flake.** Real third-party calls (Stripe, Auth0) on every run → 1–2% flake rate. Mock at the network layer with `page.route()` or run against sandbox tenants.
- **Selector rot.** CSS selectors break on minor DOM tweaks. Force `data-testid` discipline; agents otherwise default to fragile XPath.
- **Visual snapshot churn.** Anti-aliasing differences across CI runners blow up `toHaveScreenshot`. Pin OS/browser version, allow `maxDiffPixelRatio: 0.01`, run snapshot updates only on Linux runners.
- **Parallel test pollution.** `fullyParallel: true` with shared accounts → race conditions. Either isolate per-worker accounts (`process.env.TEST_WORKER_INDEX`) or serialize with `test.describe.configure({ mode: 'serial' })`.
- **CI runner cost.** Browser tests are 10–20x slower than unit. Limit to <50 tests in critical path; gate non-critical to nightly.
- **Mobile emulation lies.** `devices['Pixel 5']` simulates viewport + UA but not real touch jitter or low-power throttling. For real device coverage use BrowserStack / Sauce.

## Agentic workflow
Decompose E2E into three phases handled by separate subagents: (1) a **journey-mapper** subagent reads product specs (`spec.md`, Linear ticket, Jira) and emits a list of user journeys with success criteria; (2) a **page-object-author** subagent writes/updates page objects in `e2e/pages/` (one POM per route, methods named after user actions); (3) a **spec-writer** subagent generates `.spec.ts` files using fixtures + POM + API helpers. Run `npx playwright test --reporter=list` and feed failures back to a **flake-triage** subagent that classifies each failure as: real bug / selector drift / timing / data pollution / infra. Persist artifacts (`test-results/`, traces, videos) for human review on first failure; auto-retry only on infra class.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `npm run test:e2e` after impl tasks; blocks merge if smoke fails.
- A purpose-built **playwright-trace-agent** (worth creating): consumes `trace.zip`, reports the failing locator + last network call + DOM diff vs prior run.
- A **journey-mapper-agent** (worth creating): converts BA acceptance criteria into a list of `test('...', ...)` stubs and stable `data-testid` proposals.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `.env.test`, `playwright.config.ts`, fixture credentials before commit.

### Prompt pattern
Spec scaffold:
```
You are a Playwright 1.4x engineer. Generate e2e/checkout.spec.ts
covering the "guest checkout" journey:
- Arrange: createTestProduct() via API, page.goto('/products/$id')
- Act: addToCart, fill ShippingAddress (POM), fill PaymentDetails (POM)
- Assert: confirmation page shows order #, email sent
Use POMs from e2e/pages/, fixtures from e2e/fixtures.ts.
Do NOT use page.waitForTimeout. Do NOT use CSS selectors —
only getByRole / getByTestId.
Run: npx playwright test e2e/checkout.spec.ts --project=chromium.
```

Flake triage:
```
Read test-results/<failed>/error-context.md and trace.zip.
Classify failure as: real-bug | selector-drift | timing | data |
infra. For selector-drift, propose new data-testid + minimal POM
diff. For data, propose isolated seed in beforeEach.
Output JSON: {classification, evidence, fix}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx playwright test` | Run E2E suite | https://playwright.dev/docs/intro |
| `npx playwright codegen` | Record interactions → starter spec | https://playwright.dev/docs/codegen |
| `npx playwright show-trace` | Inspect failed test traces | https://playwright.dev/docs/trace-viewer |
| `npx playwright install` | Install browser binaries | bundled |
| Cypress | Alt runner; better dev DX, single-tab | https://docs.cypress.io |
| WebdriverIO | Cross-browser, mobile-friendly | https://webdriver.io |
| `lighthouse-ci` | Perf E2E gate | https://github.com/GoogleChrome/lighthouse-ci |
| `axe-playwright` | A11y inside E2E | https://github.com/abhinaba-ghosh/axe-playwright |
| `percy` / `chromatic` | Visual regression as a service | https://percy.io / https://chromatic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrowserStack / Sauce Labs | SaaS | yes (REST API) | Real-device cloud; agent can post test session and parse JSON results. |
| Microsoft Playwright Service | SaaS (preview) | yes | Hosted Playwright workers; faster CI; no infra ops. |
| Chromatic | SaaS | yes | Visual diffs per PR; webhooks + API for agent triage. |
| Percy | SaaS | yes | Visual regression with REST API; integrates with Playwright/Cypress. |
| Cypress Cloud | SaaS | yes | Test recording + parallel orchestration; API for results. |
| Playwright + GitHub Actions | OSS | yes | `actions/setup-node` + `playwright install --with-deps`; HTML report artifact. |
| Allure / ReportPortal | OSS | yes | Rich reporting + ML-based flaky test detection. |
| Datadog Synthetics | SaaS | yes | Production smoke tests on schedule; agent reads incident webhook. |
| Checkly | SaaS | yes | Playwright-as-a-monitor; cron-driven prod E2E. |

## Templates & scripts
See `templates.md` and `examples.md` for `playwright.config.ts`, POMs, fixtures. Add a smoke runner that gates deploy (≤50 lines):

```bash
#!/usr/bin/env bash
# smoke-gate.sh — block deploy if smoke E2E fails on staging URL.
# Usage: BASE_URL=https://staging.example.com smoke-gate.sh
set -euo pipefail
BASE_URL="${BASE_URL:?BASE_URL required}"
TIMEOUT="${TIMEOUT:-300}"
TAG="${SMOKE_TAG:-@smoke}"
echo "smoke against $BASE_URL"
npx playwright install --with-deps chromium >/dev/null
timeout "${TIMEOUT}" npx playwright test \
  --project=chromium \
  --grep "${TAG}" \
  --reporter=list,html \
  --workers=2 \
  || { echo "smoke FAILED — see playwright-report/"; exit 1; }
echo "smoke OK"
```

Wire into deploy pipeline after staging promotion, before prod cutover.

## Best practices
- **One POM per route.** `LoginPage` → `/login`, `DashboardPage` → `/dashboard`. Methods named after user intent (`login()`, `logout()`), not DOM events (`clickButton()`).
- **`data-testid` is the only stable selector.** Discipline at code-review time; agents otherwise default to text matchers that break on i18n.
- **Seed/tear-down via API, never via UI.** UI seeding is slow + flaky and tests something other than the SUT.
- **Reuse `storageState` for authenticated tests.** Log in once in global setup; saved cookies for the rest. Refresh if 401 leaks.
- **Tag tests** (`@smoke`, `@critical`, `@nightly`). Drives deploy gates.
- **Mock third-party calls at the network boundary** (`page.route('https://api.stripe.com/**', ...)`); never depend on live SaaS in CI.
- **Trace + video on first retry only.** Cheaper CI, still recoverable on failure.
- **Pin browser version in CI** (`npx playwright install --with-deps chromium@1.40.0`) to match local snapshot baselines.
- **Fail fast on console errors.** Hook `page.on('pageerror', ...)` and `page.on('console', ...)` to surface JS errors as test failures.
- **Limit suite to <50 critical-path tests** + a separate nightly suite. E2E is for journeys, not coverage.

## AI-agent gotchas
- **Selector drift after refactor.** Agent renames `<button id="submit">` → `<button data-cy="submit">`; tests using `#submit` silently fail. Prompt agents to update tests in the same PR; gate via `npm run test:e2e:smoke`.
- **`page.waitForTimeout(5000)` reflex.** LLMs trained on old Selenium code reach for arbitrary sleeps. Ban it via lint rule `no-restricted-syntax`.
- **Test independence violations.** Agent reuses a single `testUser` for two tests; second run hits `unique_email`. Force per-test factory + cleanup.
- **Hard-coded URLs / ports.** `goto('http://localhost:3000/...')` instead of `baseURL`. Breaks in CI / staging.
- **Race on async UI.** Agent fills form then asserts URL change without `await expect(page).toHaveURL(...)` — assertion runs pre-navigation. Always assert state, not commands.
- **Visual snapshots committed from a Mac runner.** Pixel diffs vs Linux CI; entire snapshot suite red. Force snapshot updates from one OS.
- **Parallel auth conflicts.** Agents share one test account across workers; concurrent password change → cascading failures. Use `worker-scoped` accounts.
- **`page.locator(...).click({ force: true })`.** Bypasses actionability checks; hides real UI bugs (overlapping elements). Force = code smell.
- **Excessive E2E suite size.** LLMs love writing tests; suite balloons to 200+ at 30 min CI. Enforce a budget; promote unit/integration when possible.
- **Mocking too much.** If `page.route()` mocks the entire backend, you're now running an integration test in browser drag — far slower with no extra signal. Pull back to MSW + component tests.
- **Stripe / OAuth iframes.** Agents try to fill iframe content with `page.fill`; need `frameLocator()`. Symptom: timeout on `input[name=cardNumber]`.
- **CI-only failures from missing `--with-deps`.** Headless Linux missing `libnss3` etc. Always install with deps in CI image.
- **Trace ZIPs leak secrets.** Auth tokens in network logs end up in artifacts. Scrub via `playwright.config.ts` `recordHar` filters or `.gitignore` artifacts in public repos.

## References
- Playwright Documentation — https://playwright.dev/docs/intro
- Playwright Best Practices — https://playwright.dev/docs/best-practices
- Test pyramid critique — https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
- Cypress Best Practices — https://docs.cypress.io/guides/references/best-practices
- Visual regression with Percy — https://docs.percy.io/docs/playwright
- Sibling methodologies: `free/dev/software-developer/integration-testing/`, `free/dev/software-developer/test-fixtures/`, `pro/dev/devops-engineer/` for CI gates.
