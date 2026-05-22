// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

import { test as base, Page } from '@playwright/test';
import { LoginPage } from './login-page';
import { DashboardPage } from './login-page';

type CustomFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<CustomFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  // Pre-authenticated via API — skips login UI for faster test setup
  authenticatedPage: async ({ page }, use) => {
    await page.request.post('/api/auth/login', {
      data: { email: 'test@example.com', password: 'testpassword' },
    });
    await use(page);
  },
});

export { expect } from '@playwright/test';

// Usage:
// import { test, expect } from '../fixtures/playwright-fixtures';
//
// test('dashboard shows welcome', async ({ authenticatedPage, dashboardPage }) => {
//   await dashboardPage.goto();
//   await expect(dashboardPage.welcomeMessage).toBeVisible();
// });
