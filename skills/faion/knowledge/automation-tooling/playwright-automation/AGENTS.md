# Playwright Automation

## Summary

**One-sentence:** Generates a Playwright test or scraping script using role-based locators, auto-wait, storageState auth reuse, and on-first-retry trace capture.

**One-paragraph:** Playwright is a cross-browser automation library (Chromium/Firefox/WebKit) with first-class auto-wait, trace viewer, and storageState auth reuse. This methodology produces a Playwright TypeScript test or one-off mjs scraping script that uses role/label/text locators (never CSS unless no semantic role exists), never page.waitForTimeout, authenticates once via storageState, and configures trace='on-first-retry' + screenshot='only-on-failure' to keep CI artefact size manageable.

**Ефективно для:**

- Cross-browser E2E tests (Chromium/Firefox/WebKit) with auto-waiting and trace viewer.
- Agentic web tasks: login flows, form filling, scraping requiring JS execution.
- Visual regression via toHaveScreenshot() snapshots + diff threshold.
- Authenticate once via storageState and reuse across hundreds of headless agent runs.

## Applies If (ALL must hold)

- Cross-browser E2E tests (Chromium/Firefox/WebKit) with auto-waiting and trace viewer.
- Agentic web tasks: login flows, form filling, scraping requiring JS execution.
- Visual regression testing via toHaveScreenshot() snapshots.
- API testing alongside UI in one session (page.request).
- Replacing legacy Selenium/Cypress suites for speed and reliability.
- Authenticating once, reusing storageState across many headless agent runs.

## Skip If (ANY kills it)

- Pure HTTP scraping where the target renders server-side (use httpx/fetch, 100x cheaper).
- Mobile-app E2E testing (use Appium, Detox, Maestro).
- Sub-millisecond unit tests of UI components (use Vitest + Testing Library).
- Targets with hard bot-detection (Cloudflare Turnstile aggressive mode).
- Long-lived stateful sessions (hours) — use a real browser profile.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target URL + flow description | plain text | user / task brief |
| Credentials (PW_USER / PW_PASS) | env vars or secret store | 1Password / .env |
| Selector strategy decision | preferred locator order documented | frontend team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[testing-js-ts-frontend]] | shares Playwright Test runner conventions and reporter setup |
| [[puppeteer-agent-workflow]] | alternative — read to confirm Playwright is the right tool |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-playwright-vs-fetch` | sonnet | decision tree application — light judgment |
| `write-spec-file` | sonnet | synthesise locator strategy + assertion plan |
| `convert-codegen-css-to-roles` | haiku | mechanical rewrite of selectors |

## Templates

| File | Purpose |
|------|---------|
| `templates/playwright.config.ts` | Playwright config with trace='on-first-retry' + cross-browser projects |
| `templates/global-setup.ts` | Authenticate once and persist storageState to auth.json |
| `templates/orders.spec.ts` | Example spec using role locators, auto-wait, and storageState |
| `templates/artefact.json` | Sample artefact metadata consumed by validate-playwright-automation.py |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-playwright-automation.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-agent-workflow]]
- [[testing-js-ts-frontend]]
- [[trunk-based-ci-gates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  globalSetup: require.resolve('./tests/global-setup.ts'),
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: 'line',
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    storageState: 'auth.json',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
  ],
});
```

### `templates/global-setup.ts`

```typescript
import { chromium, FullConfig } from '@playwright/test';

export default async function globalSetup(_config: FullConfig) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(`${process.env.BASE_URL}/login`);
  await page.getByLabel('Email').fill(process.env.PW_USER!);
  await page.getByLabel('Password').fill(process.env.PW_PASS!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL('**/dashboard');
  await ctx.storageState({ path: 'auth.json' });
  await browser.close();
}
```

### `templates/orders.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Orders', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/orders');
  });

  test('loads order table for authenticated user', async ({ page }) => {
    const table = page.getByRole('table', { name: /orders/i });
    await expect(table).toBeVisible();
    const rows = await table.getByRole('row').count();
    expect(rows).toBeGreaterThan(1);
  });

  test('filter by status narrows results', async ({ page }) => {
    await page.getByLabel('Status').selectOption('shipped');
    await expect(page.getByRole('cell', { name: /pending/i })).toHaveCount(0);
  });
});
```

### `templates/artefact.json`

```json
{
  "filename": "tests/orders.spec.ts",
  "language": "typescript",
  "uses_role_locators": true,
  "has_wait_for_timeout": false,
  "trace_mode": "on-first-retry",
  "screenshot_mode": "only-on-failure",
  "auth_via_storage_state": true,
  "cross_browser": true
}
```
