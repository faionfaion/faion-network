# E2E Testing

## Summary

**One-sentence:** Produces an E2E test-suite config (Playwright primary, Cypress secondary) with POM, storageState auth, route-mocked APIs, sharded CI, and trace artefacts.

**One-paragraph:** E2E suites validate full user journeys across real browsers. Without structure (Page Object Model, fixtures, data factories, sharding) they become slow, flaky, and silently disabled. This methodology turns a project's user-journey list into a runnable Playwright project: config file, POM base class, storageState auth, route-mocked third-party APIs, factory functions, and a sharded GitHub Actions workflow with merged blob reports.

**Ефективно для:** team migrating off slow Cypress suites or starting a fresh Playwright project who needs a defensible structure on day one.

## Applies If (ALL must hold)

- Writing or reviewing Playwright / Cypress test suites for a real web app.
- Setting up E2E infrastructure from scratch (config, auth, CI sharding).
- Debugging flaky tests or selector failures.
- Adding visual regression checks (component-scoped, masked).
- Migrating from Cypress to Playwright.

## Skip If (ANY kills it)

- Unit or integration scope (no browser needed) → use unit-testing or testing-pytest.
- API-only testing — use an HTTP client instead.
- OAuth flows with real external providers (use API-token injection workaround, not UI login).
- Single-developer prototype with no production users.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `user-journeys.yaml` | list of {journey_name, steps, expected_outcome} | operator |
| `app-base-url` | URL | infra |
| `test-user-credentials` | 1Password entry | secrets store |
| `ci-machine-count` | integer (shard target) | CI config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[testing-patterns]] | AAA / Given-When-Then framing used inside each test. |
| [[github-repo-bootstrap]] | CI workflow lives in a repo with branch protection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: pyramid, POM, role selectors, storageState, route mocking, factories, no fixed sleeps, sharded CI. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the emitted suite-config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: fixed sleep, CSS selectors, full-page screenshots, UI OAuth, shared test state. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate journeys → scaffold POM → wire auth → shard CI → publish report. | ~700 |
| `content/05-examples.xml` | recommended | Checkout-flow journey worked end to end with POM + factory. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Playwright vs Cypress; full vs component screenshot; sharded vs single-runner. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_journeys` | haiku | Mechanical YAML→typed list. |
| `scaffold_pom` | sonnet | Tradeoffs (which selectors, which fixtures) require sound reasoning. |
| `audit_flakiness_risks` | opus | Subtle cross-test contamination + selector brittleness. |
| `emit_ci_workflow` | sonnet | Mechanical YAML emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/playwright.config.ts` | Full Playwright config: projects, sharding, reporter, retries. |
| `templates/pom-base.ts` | Abstract base Page class with navigation helpers. |
| `templates/auth-setup.ts` | storageState auth setup fixture. |
| `templates/factory.ts` | Data factory with faker, builder pattern. |
| `templates/ci-workflow.yml` | GitHub Actions sharded Playwright workflow. |
| `templates/_smoke-test.yaml` | Minimum journey list (login → dashboard). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-patterns]]
- [[unit-testing]]
- [[mocking-strategies]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches first on `framework` (greenfield → Playwright; legacy Cypress maintained → Cypress with migration plan), then on `visual_regression_needed` (component-scoped vs none), then on `ci_machine_budget` (≥4 → shard; <4 → single runner). Each leaf cites a rule id in 01-core-rules.xml.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: process.env.CI
    ? [['blob'], ['github']]
    : [['html', { open: 'on-failure' }]],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Auth setup — runs before all other projects
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 14'] },
      dependencies: ['setup'],
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### `templates/pom-base.ts`

```typescript
import { type Page, type Locator } from '@playwright/test';

/**
 * Abstract base class for Page Objects.
 * Extend this for every page or major feature section.
 */
export abstract class BasePage {
  protected readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  abstract readonly url: string;

  async navigate(params?: Record<string, string>): Promise<void> {
    const searchParams = params ? '?' + new URLSearchParams(params).toString() : '';
    await this.page.goto(this.url + searchParams);
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  /** Convenience: wait for a locator to be visible */
  async waitForVisible(locator: Locator, timeout = 5000): Promise<void> {
    await locator.waitFor({ state: 'visible', timeout });
  }

  /** Returns current page title */
  async title(): Promise<string> {
    return this.page.title();
  }
}

// Example concrete Page Object:
//
// export class LoginPage extends BasePage {
//   readonly url = '/login';
//   readonly emailInput = this.page.getByLabel('Email');
//   readonly passwordInput = this.page.getByLabel('Password');
//   readonly submitButton = this.page.getByRole('button', { name: 'Sign in' });
//
//   async login(email: string, password: string): Promise<void> {
//     await this.emailInput.fill(email);
//     await this.passwordInput.fill(password);
//     await this.submitButton.click();
//   }
// }
```

### `templates/auth-setup.ts`

```typescript
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../.auth/user.json');

/**
 * Global auth setup — runs once before all tests.
 * Saves storageState so tests can skip the login UI.
 *
 * Usage in playwright.config.ts:
 *   projects: [
 *     { name: 'setup', testMatch: /.*\.setup\.ts/ },
 *     { name: 'chromium', dependencies: ['setup'], use: { storageState: authFile } },
 *   ]
 */
setup('authenticate as default user', async ({ page }) => {
  await page.goto('/login');

  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for successful redirect
  await page.waitForURL('/dashboard');
  await expect(page.getByRole('navigation')).toBeVisible();

  // Save session state for reuse across tests
  await page.context().storageState({ path: authFile });
});

// For admin role, add a second setup:
// setup('authenticate as admin', async ({ page }) => { ... })
// and reference a separate authFile path in config.
```

### `templates/factory.ts`

```typescript
import { faker } from '@faker-js/faker';

// ---- Type definitions (adapt to your domain models) ----

export interface UserData {
  email: string;
  name: string;
  password: string;
  role: 'user' | 'admin';
}

export interface ProductData {
  name: string;
  price: number;
  sku: string;
  inStock: boolean;
}

// ---- Factories ----

export function createUser(overrides: Partial<UserData> = {}): UserData {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    password: faker.internet.password({ length: 12 }),
    role: 'user',
    ...overrides,
  };
}

export function createAdmin(overrides: Partial<UserData> = {}): UserData {
  return createUser({ role: 'admin', ...overrides });
}

export function createProduct(overrides: Partial<ProductData> = {}): ProductData {
  return {
    name: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 1, max: 500 })),
    sku: faker.string.alphanumeric(8).toUpperCase(),
    inStock: faker.datatype.boolean(),
    ...overrides,
  };
}

// ---- Builder pattern for complex objects ----

export class OrderBuilder {
  private data: Record<string, unknown> = {
    userId: faker.string.uuid(),
    items: [],
    status: 'pending',
  };

  withUser(userId: string): this {
    this.data.userId = userId;
    return this;
  }

  withItem(productId: string, quantity = 1): this {
    (this.data.items as unknown[]).push({ productId, quantity });
    return this;
  }

  withStatus(status: string): this {
    this.data.status = status;
    return this;
  }

  build() {
    return { ...this.data };
  }
}
```

### `templates/ci-workflow.yml`

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-test:
    name: E2E (shard ${{ matrix.shard }}/${{ strategy.job-total }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium firefox

      - name: Run Playwright tests (shard ${{ matrix.shard }}/4)
        run: npx playwright test --shard=${{ matrix.shard }}/4
        env:
          BASE_URL: ${{ secrets.TEST_BASE_URL || 'http://localhost:3000' }}
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
          CI: true

      - name: Upload blob report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: blob-report-${{ matrix.shard }}
          path: blob-report/
          retention-days: 1

  merge-reports:
    name: Merge E2E Reports
    if: always()
    needs: e2e-test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci

      - name: Download blob reports
        uses: actions/download-artifact@v4
        with:
          path: all-blob-reports
          pattern: blob-report-*
          merge-multiple: true

      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-blob-reports

      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### `templates/_smoke-test.yaml`

```yaml
journeys:
  - journey_name: login-then-dashboard
    steps:
      - {action: visit, url: /login}
      - {action: fill, label: Email, value: $env.TEST_USER_EMAIL}
      - {action: fill, label: Password, value: $env.TEST_USER_PASSWORD}
      - {action: click, role: button, name: Sign in}
    expected_outcome:
      route: /dashboard
      visible: navigation

drivers:
  framework_preference: greenfield
  visual_regression_needed: false
  ci_machine_budget: 4
  journey_count: 1
```
