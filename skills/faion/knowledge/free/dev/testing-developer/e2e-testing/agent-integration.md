# Agent Integration — E2E Testing (Playwright & Cypress)

## When to use

- Greenfield E2E setup for a new web app: pick Playwright by default unless team is JS-only and project small.
- Validating critical user journeys (signup, login, checkout, password reset) before each release tag.
- Cross-browser smoke (Chromium, Firefox, WebKit) on a release candidate; agent runs the suite, captures traces on failure.
- Visual regression on a marketing site or design-system Storybook by snapshot diffs.
- Migrating a Cypress suite to Playwright when scale, parallelism, or cross-browser are the bottleneck.
- Writing Page Objects from a freshly built UI (HTML + selectors known) — mechanical, perfect agent task.
- Authentication state management: factor out a `globalSetup` that produces a `storageState.json` reused across tests.

## When NOT to use

- Replacing unit/integration tests — keep the pyramid: ~70% unit, ~20% integration, ~10% E2E.
- Asserting on internal implementation (component state, redux store) — wrong layer; use component tests (Vitest, Cypress component testing) instead.
- Heavy backend logic that's faster to assert via API tests; only use E2E when UI behaviour is the unit under test.
- Native mobile apps — use Appium/WebdriverIO/Maestro; Playwright/Cypress are web-only.
- Pre-deploy smoke against a staging environment that's not yet stable — flaky infra masks real failures.
- Quick bug reproduction in dev — Playwright `codegen` is fine, but a unit test usually pins the bug faster.

## When to choose Playwright vs Cypress

- **Playwright**: cross-browser (incl. WebKit/Safari), polyglot teams, big suites (1000+ tests), multi-tab/multi-context, API + UI in one runner, native sharding, mobile emulation.
- **Cypress**: small JS-only team, time-travel debugger preferred, suite stays under ~500 tests, no Safari coverage required, Cypress Cloud already paid for.

## Where it fails / limitations

- **Flakiness drives the cost**, not test count. Every flaky test that "retries to green" silently erodes trust. Aim for zero retries needed in CI.
- **Selectors are the failure surface.** `nth-child`, deep CSS, XPath all break on small UI changes. `data-testid` + role/label are the only durable picks.
- **Auth flows with OAuth/SSO** can't run real OAuth in CI without a test tenant; mocking via `page.route` is necessary but easy to get wrong (CSRF, cookies, redirect URLs).
- **Storage state expiry.** A `globalSetup` token expires mid-CI run; tests turn red Friday afternoon for no apparent reason. Refresh on a TTL.
- **Visual regression** on dynamic content (timestamps, A/B variants, ads) produces noise. Mask, freeze time, or skip those areas.
- **Trace files are large** (~10-50 MB each). CI artifact storage explodes if always-on. Capture only on failure.
- **Container CPU starvation** in shared CI runners makes Playwright timeouts misfire. Match `workers` to actual cores; do not autodetect on shared infra.
- **Cross-context state pollution.** A test that authenticates a user without isolating cookies/storage can affect the next test. Use `test.use({ storageState: ... })` per project, not globally.
- **Network mocks vs real backend** — mixing them creates non-deterministic results. Pick one strategy per test file.
- **Database state** for E2E is the silent killer. Without a reset between tests (API call, Postgres truncate, container reset), order matters.

## Agentic workflow

Drive E2E as a layered codebase: `tests/e2e/{auth,checkout,catalog}/*.spec.ts`, `tests/e2e/pages/*.ts` (Page Objects), `tests/e2e/fixtures/*.ts` (auth, data builders), `tests/e2e/playwright.config.ts`. The agent generates Page Objects from URLs/HTML via `playwright codegen`, refines them to use `getByRole`/`getByTestId`, then writes test cases per acceptance criterion. CI runs sharded (`--shard=N/M`), traces and screenshots only on failure, HTML report uploaded as artifact. The agent never edits Page Objects from inside a test file; encapsulation is enforced.

### Recommended subagents

- `faion-testing-developer` (`e2e-testing`, `test-fixtures`, `mocking-strategies`) — Owns the methodology; produces specs, fixtures, and POs.
- `faion-frontend-developer` — Pairs to add `data-testid` attributes where missing; agents must not invent `data-testid` values without a code change.
- `faion-cicd-engineer` — Wires sharded GitHub Actions matrix, browser cache, trace upload, retry policy.
- `faion-sdd-executor-agent` — Treats user-journey AC as E2E test gates; PR can't merge without the spec passing.
- `faion-improver` — Periodic flake hunt: order tests by failure rate, propose fixes (selector hardening, mocking, data isolation).
- General-purpose `Task` subagent for Cypress→Playwright migration: mechanical conversion of `cy.*` chains to `await page.*` + Page Objects.

### Prompt pattern

Generate POs + spec from an AC:

```
AC: "User can complete checkout with credit card and see confirmation page".
Inputs: CheckoutPage HTML excerpt, ConfirmPage URL pattern, test card 4242 4242 4242 4242.
Tasks:
1. Page Objects in tests/e2e/pages/checkout.ts and confirm.ts.
   - Use page.getByRole / getByTestId only. No nth-child, no XPath.
2. Auth state via storageState (do NOT log in via UI in this spec).
3. Spec tests/e2e/checkout/checkout.spec.ts: happy path + invalid card + declined card (parametrized via test.describe.each-style).
4. Mock /api/payment/* with page.route to return canned responses.
5. Capture trace: `--trace=on-first-retry`.
Run npx playwright test --project=chromium checkout.spec.ts. Stop on first failure with full trace.
```

Cypress→Playwright conversion:

```
For tests/e2e/cypress/<file>.cy.ts:
- Convert cy.visit/cy.get/cy.click to await page.goto/getByX/click.
- Convert cy.intercept to page.route + route.fulfill.
- Move login flows into storageState produced by globalSetup.
- Replace cy.contains() with getByText() (case-sensitive default).
Output Playwright spec + diff. Do not change selectors that already use data-testid.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx playwright` | Test runner, codegen, trace viewer | https://playwright.dev/docs/intro |
| `playwright install --with-deps` | Install browser binaries + OS deps | https://playwright.dev/docs/cli |
| `npx playwright codegen <url>` | Auto-generate test code by clicking | https://playwright.dev/docs/codegen |
| `npx playwright show-trace` | Open `.zip` trace from failed run | https://playwright.dev/docs/trace-viewer |
| `npx playwright show-report` | Open HTML report | https://playwright.dev/docs/test-reporters |
| `cypress` (CLI) | Runner, GUI, dashboard | https://docs.cypress.io |
| `cypress open` / `cypress run` | Interactive vs headless | https://docs.cypress.io/guides/guides/command-line |
| `mockoon-cli` / `wiremock` | Run a stub server in CI for stable backends | https://mockoon.com |
| `msw` (mock service worker) | Network mocks shared across unit + E2E | https://mswjs.io |
| `lighthouse-ci` | Perf budgets along E2E runs | https://github.com/GoogleChrome/lighthouse-ci |
| `pa11y-ci` / `axe-core` | A11y assertions inside E2E | https://github.com/pa11y/pa11y-ci / https://github.com/dequelabs/axe-core |
| `lhci collect --upload.target=temporary-public-storage` | Per-PR Lighthouse reports | https://github.com/GoogleChrome/lighthouse-ci |
| `screenshot-tester` / `pixelmatch` | DIY visual diff if avoiding SaaS | https://github.com/mapbox/pixelmatch |
| `argosci` | OSS visual regression CI integration | https://argos-ci.com |
| `xvfb-run` | Headless display for non-headless mode in CI | https://wiki.archlinux.org/title/Xvfb |
| `docker-compose` | Stand up app + DB + mock server for E2E | https://docs.docker.com/compose/ |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — `microsoft/playwright-github-action`, matrix sharding | Standard CI |
| GitLab CI | SaaS/self-host | Yes — `parallel: matrix:` for sharding | Mirror of GH workflow |
| Playwright Browsers Docker image (`mcr.microsoft.com/playwright`) | OSS | Yes — pinned tag per Playwright version | Avoid OS-dependency drift |
| Cypress Cloud | SaaS | Yes — `cypress run --record` | Required for parallel + Dashboard |
| Currents.dev | SaaS | Yes — Cypress Cloud-compatible | Cheaper alternative |
| Sauce Labs / BrowserStack | SaaS | Yes — REST + provider config | Real-device + Safari |
| LambdaTest | SaaS | Yes — REST + provider config | Cross-browser cloud |
| QA Wolf | SaaS | Partially — managed E2E service | Outsource flake fighting |
| Percy | SaaS | Yes — `@percy/playwright`, `@percy/cypress` | Visual regression |
| Chromatic | SaaS | Yes — `chromatic` CLI | Storybook-driven visual diff |
| Argos | SaaS+OSS | Yes — `argos-ci` CLI | OSS-friendly visual diff |
| Applitools | SaaS | Yes — SDK | AI-assisted visual diff |
| Datadog Synthetics | SaaS | Yes — REST | Synthetic monitoring + browser tests |
| Checkly | SaaS | Yes — REST + Playwright runtime | Synthetic + post-deploy E2E |
| MSW (Mock Service Worker) | OSS | Yes — JS API | Reuse same mocks in unit and E2E |
| Mockoon Cloud | SaaS | Yes — REST | Hosted mock APIs |

## Templates & scripts

See methodology `templates.md` for full POM, fixtures, GH Actions config. Inline minimal `playwright.config.ts` (≤30 lines):

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
  ],
  globalSetup: './tests/e2e/globalSetup.ts',
});
```

Inline GH Actions sharded run (≤25 lines):

```yaml
jobs:
  e2e:
    runs-on: ubuntu-latest
    container: mcr.microsoft.com/playwright:v1.50.0-jammy
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --shard=${{ matrix.shard }}/4
        env: { CI: 'true' }
      - if: failure()
        uses: actions/upload-artifact@v4
        with: { name: trace-${{ matrix.shard }}, path: test-results/, retention-days: 7 }
```

## Best practices

- **One test file = one user journey.** Test isolation > test reuse.
- **`data-testid` on every interactive element**; ban `nth-child`, deep CSS, XPath in PRs.
- **Page Objects encapsulate locators only.** Business assertions live in spec files. Don't put `expect(...)` inside POs.
- **`storageState` per role** (admin, user, guest) generated once in `globalSetup`; refresh TTL ≤ test-run length.
- **Mock external network** (`page.route` or MSW) to remove third-party flake; always have one suite that exercises the real network for confidence.
- **Reset DB state per test** via API call (preferred), `truncate` script, or seeded fixture; never rely on test-order to set state.
- **Trace `on-first-retry`**, screenshots `only-on-failure`, video `retain-on-failure` — keeps artifacts manageable.
- **`fullyParallel: true`** + match workers to CI cores. Don't over-parallelise on shared runners.
- **Forbid `.only`** in CI (`forbidOnly: !!process.env.CI`); accidental `.only` is a common cause of "10 tests passed" lying.
- **Frozen time + locale** for visual snapshots; mask dynamic regions (clocks, ads, A/B copy).
- **No `await page.waitForTimeout(...)`**. Replace with auto-wait via locator assertions (`await expect(locator).toBeVisible()`).
- **Single source of selectors.** If a test needs a new selector, it goes through a PO change in the same PR; ad-hoc selectors in spec are reviewed as smell.

## AI-agent gotchas

- **Inventing `data-testid` values**. Agents will write tests against `data-testid="cart-button"` without checking it exists in the app. Always verify via `WebFetch`/`page.content()` or fail the task.
- **Auto-generated codegen output** uses brittle CSS selectors. Treat codegen as a starting draft — agent must rewrite to `getByRole`/`getByTestId` before commit.
- **`page.waitForTimeout(...)`** sneaks into agent code from blogs. Reject in review; replace with locator-based waits.
- **`expect(locator).toBeVisible({ timeout: 30000 })`** padded "to make it pass". Agents tune timeouts upward instead of fixing flake; reviewer rule: timeouts > default need a comment.
- **Login in every test** because the agent doesn't know about `storageState`. Force `globalSetup` + `test.use({ storageState })`.
- **Trace files committed by mistake** when agent stages `test-results/` recursively. Add `test-results/` to `.gitignore` and verify pre-commit.
- **Mock + real backend mixed** in same spec because the agent didn't track which routes are mocked. Force a comment block at top: "MOCKS: /api/payment/*; REAL: /api/catalog/*".
- **Cypress→Playwright partial conversion**. Agents leave `cy.*` in commented-out form. Reviewer: assert no `cy.` token remains in `tests/e2e/`.
- **Visual diffs against generated content** (avatars, charts, timestamps). Agents that don't mask produce 100% diff churn; force `--mask` regions or skip.
- **Storage state baked with prod creds**. Agents that grab a real cookie from local browsing put it in `globalSetup`. Always create a test user via API setup.
- **Parallelism races on DB**. Agents enable `fullyParallel: true` on a suite that shares a single seeded DB row. Either isolate per worker (DB per worker) or serialise the file with `test.describe.serial`.
- **Headless vs headed env divergence.** Tests pass headed locally, fail headless in CI (font rendering, animations). Always run headless locally before pushing.

## References

- Methodology README: `./README.md`
- Playwright docs: https://playwright.dev/docs/intro
- Playwright best practices: https://playwright.dev/docs/best-practices
- Playwright Page Object Model: https://playwright.dev/docs/pom
- Playwright sharding: https://playwright.dev/docs/test-sharding
- Cypress docs: https://docs.cypress.io
- Cypress real-world app: https://github.com/cypress-io/cypress-realworld-app
- MSW (mock service worker): https://mswjs.io
- @msw/playwright: https://github.com/mswjs/playwright
- Percy: https://percy.io
- Chromatic: https://www.chromatic.com
- Argos CI: https://argos-ci.com
- Applitools: https://applitools.com
- Microsoft Playwright Docker image: https://mcr.microsoft.com/en-us/product/playwright/about
- BrowserStack — Playwright vs Cypress 2025: https://www.browserstack.com/guide/playwright-vs-cypress
- Lighthouse CI: https://github.com/GoogleChrome/lighthouse-ci
- axe-core: https://github.com/dequelabs/axe-core
