---
name: faion-testing-e2e
user-invocable: false
description: "E2E testing: Playwright, Cypress, page objects, fixtures"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npx playwright:*, npx cypress:*)
---

# E2E Testing (Playwright & Cypress)

## Playwright (Recommended)

### Installation

```bash
npm install --save-dev @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
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
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Page Object Pattern

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByTestId('email-input');
    this.passwordInput = page.getByTestId('password-input');
    this.submitButton = page.getByTestId('submit-button');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Usage
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

### Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

type Fixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('test@example.com', 'password');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### API Testing

```typescript
import { test, expect } from '@playwright/test';

test('should create user via API', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'John', email: 'john@example.com' },
  });

  expect(response.status()).toBe(201);
  const user = await response.json();
  expect(user.id).toBeDefined();
});
```

### Running Playwright

```bash
npx playwright test              # Run all tests
npx playwright test --headed     # With browser UI
npx playwright test --debug      # Debug mode
npx playwright test --ui         # UI mode
npx playwright codegen URL       # Generate tests
```

## Cypress (Alternative)

### Installation

```bash
npm install --save-dev cypress
```

### Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.ts',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
  },
});
```

### Basic Test

```typescript
// cypress/e2e/auth.cy.ts
describe('Authentication', () => {
  it('should login successfully', () => {
    cy.visit('/');
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="email-input"]').type('user@example.com');
    cy.get('[data-testid="password-input"]').type('password');
    cy.get('[data-testid="submit-button"]').click();

    cy.url().should('include', '/dashboard');
  });
});
```

### Custom Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="email-input"]').type(email);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="submit-button"]').click();
  cy.url().should('include', '/dashboard');
});

// Usage
cy.login('user@example.com', 'password');
```

## Sources

- [Playwright Documentation](https://playwright.dev/docs/intro) - official Playwright docs
- [Cypress Documentation](https://docs.cypress.io/) - official Cypress docs
- [Playwright Best Practices](https://playwright.dev/docs/best-practices) - official best practices
- [Page Object Model](https://playwright.dev/docs/pom) - POM pattern in Playwright
- [Testing Library Principles](https://testing-library.com/docs/guiding-principles) - user-centric testing
