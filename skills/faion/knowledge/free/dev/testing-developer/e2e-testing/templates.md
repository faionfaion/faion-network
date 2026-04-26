# E2E Testing Templates

Copy-paste configurations and templates for Playwright and Cypress E2E testing.

---

## Table of Contents

1. [Playwright Configuration](#1-playwright-configuration)
2. [Cypress Configuration](#2-cypress-configuration)
3. [Page Object Templates](#3-page-object-templates)
4. [Fixture Templates](#4-fixture-templates)
5. [Data Factory Templates](#5-data-factory-templates)
6. [GitHub Actions Workflows](#6-github-actions-workflows)
7. [Authentication Templates](#7-authentication-templates)
8. [API Mocking Templates](#8-api-mocking-templates)
9. [Visual Testing Templates](#9-visual-testing-templates)

---

## 1. Playwright Configuration

### Full Configuration (playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './e2e',

  // Test file pattern
  testMatch: '**/*.spec.ts',

  // Timeout for each test
  timeout: 30_000,

  // Timeout for expect assertions
  expect: {
    timeout: 5_000,
  },

  // Run tests in parallel
  fullyParallel: true,

  // Fail the build on CI if test.only is left in code
  forbidOnly: !!process.env.CI,

  // Retry failed tests
  retries: process.env.CI ? 2 : 0,

  // Number of workers
  workers: process.env.CI ? 1 : undefined,

  // Reporter
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],

  // Shared settings for all projects
  use: {
    // Base URL
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Collect trace on first retry
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'on-first-retry',

    // Viewport
    viewport: { width: 1280, height: 720 },

    // Ignore HTTPS errors
    ignoreHTTPSErrors: true,

    // Action timeout
    actionTimeout: 10_000,

    // Navigation timeout
    navigationTimeout: 30_000,
  },

  // Projects for different browsers
  projects: [
    // Setup project for authentication
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },

    // Desktop browsers
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Mobile browsers
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 7'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 14'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],

  // Local dev server
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

### Minimal Configuration

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## 2. Cypress Configuration

### Full Configuration (cypress.config.ts)

```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    supportFile: 'cypress/support/e2e.ts',
    fixturesFolder: 'cypress/fixtures',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',

    // Viewport
    viewportWidth: 1280,
    viewportHeight: 720,

    // Timeouts
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 30000,
    requestTimeout: 10000,
    responseTimeout: 30000,

    // Video recording
    video: true,
    videoCompression: 32,

    // Screenshots
    screenshotOnRunFailure: true,

    // Retries
    retries: {
      runMode: 2,
      openMode: 0,
    },

    // Experimental features
    experimentalStudio: true,

    setupNodeEvents(on, config) {
      // Tasks
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
        async seedDatabase(data) {
          // Database seeding logic
          return null;
        },
      });

      return config;
    },
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
});
```

### Support File (cypress/support/e2e.ts)

```typescript
import './commands';

// Hide fetch/XHR requests in command log
const app = window.top;
if (app && !app.document.head.querySelector('[data-hide-command-log-request]')) {
  const style = app.document.createElement('style');
  style.innerHTML = '.command-name-request, .command-name-xhr { display: none }';
  style.setAttribute('data-hide-command-log-request', '');
  app.document.head.appendChild(style);
}

// Global beforeEach
beforeEach(() => {
  // Preserve cookies/localStorage between tests if needed
});

// Global afterEach
afterEach(() => {
  // Cleanup
});

// Catch uncaught exceptions
Cypress.on('uncaught:exception', (err) => {
  // Return false to prevent Cypress from failing the test
  if (err.message.includes('ResizeObserver')) {
    return false;
  }
  return true;
});
```

### Custom Commands (cypress/support/commands.ts)

```typescript
/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      getByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
      login(email: string, password: string): Chainable<void>;
      logout(): Chainable<void>;
    }
  }
}

Cypress.Commands.add('getByTestId', (testId: string) => {
  return cy.get(`[data-testid="${testId}"]`);
});

Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session(
    [email],
    () => {
      cy.visit('/login');
      cy.getByTestId('email-input').type(email);
      cy.getByTestId('password-input').type(password);
      cy.getByTestId('submit-button').click();
      cy.url().should('include', '/dashboard');
    },
    {
      validate: () => {
        cy.getCookie('session').should('exist');
      },
    }
  );
});

Cypress.Commands.add('logout', () => {
  cy.clearCookies();
  cy.clearLocalStorage();
});

export {};
```

---

## 3. Page Object Templates

### Base Page (Playwright)

```typescript
// pages/BasePage.ts
import { Page, Locator, expect } from '@playwright/test';

export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Common elements
  readonly header = () => this.page.getByRole('banner');
  readonly footer = () => this.page.getByRole('contentinfo');
  readonly loader = () => this.page.getByTestId('loader');
  readonly toast = () => this.page.getByRole('alert');

  // Navigation
  async navigateTo(path: string) {
    await this.page.goto(path);
    await this.waitForPageLoad();
  }

  // Wait helpers
  async waitForPageLoad() {
    await this.loader().waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
  }

  async waitForToast(message?: string) {
    if (message) {
      await expect(this.toast()).toContainText(message);
    } else {
      await this.toast().waitFor({ state: 'visible' });
    }
  }

  // Utility methods
  async getPageTitle(): Promise<string> {
    return this.page.title();
  }

  async getCurrentUrl(): Promise<string> {
    return this.page.url();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }
}
```

### Feature Page Object (Playwright)

```typescript
// pages/ProductsPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';
import { ProductDetailPage } from './ProductDetailPage';

export class ProductsPage extends BasePage {
  readonly url = '/products';

  // Locators
  readonly searchInput = () => this.page.getByPlaceholder('Search products...');
  readonly categoryFilter = () => this.page.getByRole('combobox', { name: 'Category' });
  readonly sortSelect = () => this.page.getByRole('combobox', { name: 'Sort by' });
  readonly productGrid = () => this.page.getByTestId('product-grid');
  readonly productCards = () => this.page.getByTestId('product-card');
  readonly emptyState = () => this.page.getByTestId('empty-state');
  readonly pagination = () => this.page.getByRole('navigation', { name: 'Pagination' });
  readonly loadMoreButton = () => this.page.getByRole('button', { name: 'Load more' });

  // Single product locators
  productCard(productName: string): Locator {
    return this.productCards().filter({ hasText: productName });
  }

  productPrice(productName: string): Locator {
    return this.productCard(productName).getByTestId('price');
  }

  addToCartButton(productName: string): Locator {
    return this.productCard(productName).getByRole('button', { name: 'Add to Cart' });
  }

  // Actions
  async goto() {
    await this.navigateTo(this.url);
  }

  async search(query: string) {
    await this.searchInput().fill(query);
    await this.searchInput().press('Enter');
    await this.waitForPageLoad();
  }

  async filterByCategory(category: string) {
    await this.categoryFilter().selectOption(category);
    await this.waitForPageLoad();
  }

  async sortBy(option: string) {
    await this.sortSelect().selectOption(option);
    await this.waitForPageLoad();
  }

  async addToCart(productName: string) {
    await this.addToCartButton(productName).click();
    await this.waitForToast('Added to cart');
  }

  async openProduct(productName: string): Promise<ProductDetailPage> {
    await this.productCard(productName).click();
    await this.page.waitForURL(/\/products\/[\w-]+/);
    return new ProductDetailPage(this.page);
  }

  async getProductCount(): Promise<number> {
    return this.productCards().count();
  }

  async loadMore() {
    await this.loadMoreButton().click();
    await this.waitForPageLoad();
  }

  // Assertions
  async expectProductVisible(productName: string) {
    await expect(this.productCard(productName)).toBeVisible();
  }

  async expectNoResults() {
    await expect(this.emptyState()).toBeVisible();
    await expect(this.productCards()).toHaveCount(0);
  }
}
```

### Cypress Page Object

```typescript
// cypress/pages/LoginPage.ts
export class LoginPage {
  // Selectors
  private selectors = {
    emailInput: '[data-testid="email-input"]',
    passwordInput: '[data-testid="password-input"]',
    submitButton: '[data-testid="submit-button"]',
    rememberMe: '[data-testid="remember-me"]',
    errorMessage: '[role="alert"]',
    forgotPassword: '[data-testid="forgot-password"]',
  };

  visit() {
    cy.visit('/login');
    return this;
  }

  typeEmail(email: string) {
    cy.get(this.selectors.emailInput).clear().type(email);
    return this;
  }

  typePassword(password: string) {
    cy.get(this.selectors.passwordInput).clear().type(password);
    return this;
  }

  checkRememberMe() {
    cy.get(this.selectors.rememberMe).check();
    return this;
  }

  submit() {
    cy.get(this.selectors.submitButton).click();
    return this;
  }

  login(email: string, password: string) {
    this.typeEmail(email);
    this.typePassword(password);
    this.submit();
    return this;
  }

  // Assertions
  assertErrorVisible(message?: string) {
    if (message) {
      cy.get(this.selectors.errorMessage).should('contain', message);
    } else {
      cy.get(this.selectors.errorMessage).should('be.visible');
    }
    return this;
  }

  assertRedirectToDashboard() {
    cy.url().should('include', '/dashboard');
    return this;
  }
}

// Usage
const loginPage = new LoginPage();
loginPage.visit().login('user@example.com', 'password').assertRedirectToDashboard();
```

---

## 4. Fixture Templates

### Playwright Custom Fixtures

```typescript
// fixtures/index.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { ProductsPage } from '../pages/ProductsPage';
import { CartPage } from '../pages/CartPage';

// Define fixture types
type Pages = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  productsPage: ProductsPage;
  cartPage: CartPage;
};

type AuthFixtures = {
  authenticatedPage: Page;
  adminPage: Page;
};

type DataFixtures = {
  testUser: TestUser;
  testProducts: Product[];
};

// Extend base test
export const test = base.extend<Pages & AuthFixtures & DataFixtures>({
  // Page fixtures
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  productsPage: async ({ page }, use) => {
    await use(new ProductsPage(page));
  },

  cartPage: async ({ page }, use) => {
    await use(new CartPage(page));
  },

  // Authenticated page fixture
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: '.auth/user.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  // Admin page fixture
  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: '.auth/admin.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  // Test data fixtures
  testUser: async ({}, use) => {
    const user = {
      id: 'test-user-id',
      email: 'test@example.com',
      name: 'Test User',
    };
    await use(user);
  },

  testProducts: async ({}, use) => {
    const products = [
      { id: '1', name: 'Product 1', price: 99.99 },
      { id: '2', name: 'Product 2', price: 149.99 },
    ];
    await use(products);
  },
});

export { expect };
```

### Using Custom Fixtures

```typescript
// tests/products.spec.ts
import { test, expect } from '../fixtures';

test.describe('Products', () => {
  test('should display products', async ({ productsPage, testProducts }) => {
    // Mock API with test data
    await productsPage.page.route('**/api/products', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ products: testProducts }),
      });
    });

    await productsPage.goto();

    for (const product of testProducts) {
      await productsPage.expectProductVisible(product.name);
    }
  });

  test('should add to cart (authenticated)', async ({ authenticatedPage }) => {
    const productsPage = new ProductsPage(authenticatedPage);
    await productsPage.goto();
    await productsPage.addToCart('Product 1');
  });
});
```

---

## 5. Data Factory Templates

### Complete Factory Setup

```typescript
// fixtures/factories/index.ts
import { faker } from '@faker-js/faker';

// Types
interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  avatar?: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: string;
}

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  inStock: boolean;
  quantity: number;
  images: string[];
  rating: number;
}

interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  shippingAddress: Address;
  createdAt: string;
}

interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

// Base factory helper
function createFactory<T>(generator: (overrides?: Partial<T>) => T) {
  return {
    create: (overrides?: Partial<T>): T => generator(overrides),
    createMany: (count: number, overrides?: Partial<T>): T[] =>
      Array.from({ length: count }, () => generator(overrides)),
  };
}

// User Factory
export const userFactory = createFactory<User>((overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email().toLowerCase(),
  firstName: faker.person.firstName(),
  lastName: faker.person.lastName(),
  phone: faker.phone.number(),
  avatar: faker.image.avatar(),
  role: 'user',
  createdAt: faker.date.past().toISOString(),
  ...overrides,
}));

// Product Factory
export const productFactory = createFactory<Product>((overrides = {}) => ({
  id: faker.string.uuid(),
  name: faker.commerce.productName(),
  description: faker.commerce.productDescription(),
  price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
  category: faker.commerce.department(),
  inStock: faker.datatype.boolean({ probability: 0.8 }),
  quantity: faker.number.int({ min: 0, max: 100 }),
  images: Array.from({ length: 3 }, () => faker.image.url()),
  rating: faker.number.float({ min: 1, max: 5, fractionDigits: 1 }),
  ...overrides,
}));

// Address Factory
export const addressFactory = createFactory<Address>((overrides = {}) => ({
  street: faker.location.streetAddress(),
  city: faker.location.city(),
  state: faker.location.state(),
  zipCode: faker.location.zipCode(),
  country: faker.location.country(),
  ...overrides,
}));

// Order Factory
export const orderFactory = createFactory<Order>((overrides = {}) => {
  const items = productFactory.createMany(faker.number.int({ min: 1, max: 5 }));
  return {
    id: `ORD-${faker.string.alphanumeric(8).toUpperCase()}`,
    userId: faker.string.uuid(),
    items: items.map((p) => ({
      productId: p.id,
      name: p.name,
      price: p.price,
      quantity: faker.number.int({ min: 1, max: 3 }),
    })),
    total: items.reduce((sum, item) => sum + item.price, 0),
    status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
    shippingAddress: addressFactory.create(),
    createdAt: faker.date.recent().toISOString(),
    ...overrides,
  };
});

// Specific scenarios
export const createTestUser = () =>
  userFactory.create({
    email: 'test@example.com',
    firstName: 'Test',
    lastName: 'User',
    role: 'user',
  });

export const createAdminUser = () =>
  userFactory.create({
    email: 'admin@example.com',
    firstName: 'Admin',
    lastName: 'User',
    role: 'admin',
  });

export const createOutOfStockProduct = () =>
  productFactory.create({
    inStock: false,
    quantity: 0,
  });

export const createExpensiveProduct = () =>
  productFactory.create({
    price: 999.99,
    name: 'Premium Product',
  });
```

---

## 6. GitHub Actions Workflows

### Full Playwright CI Workflow

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  CI: true
  BASE_URL: http://localhost:3000

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    strategy:
      fail-fast: false
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build application
        run: npm run build

      - name: Run E2E tests
        run: npx playwright test --shard=${{ matrix.shard }}
        env:
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}

      - name: Upload blob report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: blob-report-${{ strategy.job-index }}
          path: blob-report/
          retention-days: 7

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ strategy.job-index }}
          path: test-results/
          retention-days: 7

  merge-reports:
    if: always()
    needs: [e2e]
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Download blob reports
        uses: actions/download-artifact@v4
        with:
          pattern: blob-report-*
          path: all-blob-reports
          merge-multiple: true

      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-blob-reports

      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14
```

### Simple Playwright CI Workflow

```yaml
# .github/workflows/e2e-simple.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npx playwright install --with-deps

      - name: Run tests
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### Cypress CI Workflow

```yaml
# .github/workflows/cypress.yml
name: Cypress E2E

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  cypress:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm run start
          wait-on: 'http://localhost:3000'
          wait-on-timeout: 120

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots
          retention-days: 7

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: cypress-videos
          path: cypress/videos
          retention-days: 7
```

---

## 7. Authentication Templates

### Auth Setup File (Playwright)

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../.auth/user.json');
const adminAuthFile = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as user', async ({ page }) => {
  await page.goto('/login');

  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign In' }).click();

  await page.waitForURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  await page.context().storageState({ path: authFile });
});

setup('authenticate as admin', async ({ page }) => {
  await page.goto('/login');

  await page.getByLabel('Email').fill(process.env.TEST_ADMIN_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_ADMIN_PASSWORD!);
  await page.getByRole('button', { name: 'Sign In' }).click();

  await page.waitForURL('/admin');
  await expect(page.getByRole('heading', { name: 'Admin Panel' })).toBeVisible();

  await page.context().storageState({ path: adminAuthFile });
});
```

### API Authentication Helper

```typescript
// helpers/auth.ts
import { APIRequestContext, expect } from '@playwright/test';

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export async function loginViaAPI(
  request: APIRequestContext,
  email: string,
  password: string
): Promise<AuthTokens> {
  const response = await request.post('/api/auth/login', {
    data: { email, password },
  });

  expect(response.ok()).toBeTruthy();
  const data = await response.json();

  return {
    accessToken: data.accessToken,
    refreshToken: data.refreshToken,
  };
}

export async function refreshAccessToken(
  request: APIRequestContext,
  refreshToken: string
): Promise<string> {
  const response = await request.post('/api/auth/refresh', {
    data: { refreshToken },
  });

  expect(response.ok()).toBeTruthy();
  const data = await response.json();

  return data.accessToken;
}

export async function injectAuthToken(page: Page, token: string) {
  await page.addInitScript((token) => {
    localStorage.setItem('auth_token', token);
  }, token);
}
```

---

## 8. API Mocking Templates

### MSW Handler Setup

```typescript
// mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw';

// User handlers
const userHandlers = [
  http.get('/api/user/profile', async () => {
    return HttpResponse.json({
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      avatar: 'https://example.com/avatar.png',
    });
  }),

  http.put('/api/user/profile', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      ...body,
      updatedAt: new Date().toISOString(),
    });
  }),
];

// Product handlers
const productHandlers = [
  http.get('/api/products', async ({ request }) => {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '10');

    // Simulate delay
    await delay(100);

    return HttpResponse.json({
      products: Array.from({ length: limit }, (_, i) => ({
        id: `${(page - 1) * limit + i + 1}`,
        name: `Product ${(page - 1) * limit + i + 1}`,
        price: 99.99,
        category: category || 'electronics',
      })),
      total: 100,
      page,
      limit,
    });
  }),

  http.get('/api/products/:id', async ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      name: `Product ${id}`,
      description: 'Product description',
      price: 99.99,
      inStock: true,
    });
  }),
];

// Error handlers for testing
const errorHandlers = [
  http.get('/api/error/500', () => {
    return HttpResponse.json({ error: 'Internal server error' }, { status: 500 });
  }),

  http.get('/api/error/timeout', async () => {
    await delay(30000);
    return HttpResponse.json({});
  }),
];

export const handlers = [...userHandlers, ...productHandlers, ...errorHandlers];
```

### Playwright Route Mocking Utility

```typescript
// helpers/mockApi.ts
import { Page, Route } from '@playwright/test';

type MockResponse = {
  status?: number;
  body?: unknown;
  delay?: number;
  headers?: Record<string, string>;
};

export class ApiMocker {
  private page: Page;
  private mocks: Map<string, MockResponse> = new Map();

  constructor(page: Page) {
    this.page = page;
  }

  async mock(urlPattern: string, response: MockResponse) {
    this.mocks.set(urlPattern, response);

    await this.page.route(urlPattern, async (route: Route) => {
      const mock = this.mocks.get(urlPattern);
      if (!mock) {
        await route.continue();
        return;
      }

      if (mock.delay) {
        await new Promise((resolve) => setTimeout(resolve, mock.delay));
      }

      await route.fulfill({
        status: mock.status || 200,
        contentType: 'application/json',
        headers: mock.headers,
        body: JSON.stringify(mock.body),
      });
    });

    return this;
  }

  async mockError(urlPattern: string, statusCode: number, message: string) {
    return this.mock(urlPattern, {
      status: statusCode,
      body: { error: message },
    });
  }

  async mockTimeout(urlPattern: string, timeoutMs: number = 30000) {
    return this.mock(urlPattern, {
      delay: timeoutMs,
      body: {},
    });
  }

  async clear(urlPattern?: string) {
    if (urlPattern) {
      this.mocks.delete(urlPattern);
      await this.page.unroute(urlPattern);
    } else {
      for (const pattern of this.mocks.keys()) {
        await this.page.unroute(pattern);
      }
      this.mocks.clear();
    }
  }
}

// Usage
const mocker = new ApiMocker(page);
await mocker.mock('**/api/users', { body: { users: [] } });
await mocker.mockError('**/api/products', 500, 'Server error');
```

---

## 9. Visual Testing Templates

### Playwright Visual Testing Config

```typescript
// playwright.config.ts - Visual testing section
export default defineConfig({
  // ... other config

  expect: {
    toHaveScreenshot: {
      // Maximum allowed difference in pixels
      maxDiffPixels: 100,

      // Maximum allowed ratio of different pixels
      maxDiffPixelRatio: 0.01,

      // Anti-aliasing tolerance
      threshold: 0.2,

      // Animation handling
      animations: 'disabled',
    },
  },

  // Project for visual tests only
  projects: [
    {
      name: 'visual-chromium',
      testMatch: /.*\.visual\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
        // Consistent viewport for visual tests
        viewport: { width: 1280, height: 720 },
      },
    },
  ],
});
```

### Visual Test Template

```typescript
// tests/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Disable animations for consistent screenshots
    await page.addStyleTag({
      content: `
        *, *::before, *::after {
          animation-duration: 0s !important;
          animation-delay: 0s !important;
          transition-duration: 0s !important;
          transition-delay: 0s !important;
        }
      `,
    });
  });

  test('homepage', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      mask: [
        page.locator('[data-testid="dynamic-date"]'),
        page.locator('[data-testid="user-avatar"]'),
      ],
    });
  });

  test('login form states', async ({ page }) => {
    await page.goto('/login');

    // Default state
    await expect(page.getByTestId('login-form')).toHaveScreenshot('login-default.png');

    // Filled state
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password');
    await expect(page.getByTestId('login-form')).toHaveScreenshot('login-filled.png');

    // Error state
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.getByTestId('error-message').waitFor();
    await expect(page.getByTestId('login-form')).toHaveScreenshot('login-error.png');
  });

  test('responsive breakpoints', async ({ page }) => {
    await page.goto('/products');

    const breakpoints = [
      { name: 'desktop', width: 1920, height: 1080 },
      { name: 'laptop', width: 1366, height: 768 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'mobile', width: 375, height: 667 },
    ];

    for (const bp of breakpoints) {
      await page.setViewportSize({ width: bp.width, height: bp.height });
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`products-${bp.name}.png`);
    }
  });
});
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:chromium": "playwright test --project=chromium",
    "test:e2e:firefox": "playwright test --project=firefox",
    "test:e2e:webkit": "playwright test --project=webkit",
    "test:e2e:mobile": "playwright test --project=mobile-chrome --project=mobile-safari",
    "test:e2e:update-snapshots": "playwright test --update-snapshots",
    "test:e2e:report": "playwright show-report",
    "test:e2e:codegen": "playwright codegen http://localhost:3000",
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
  }
}
```
