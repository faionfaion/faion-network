// purpose: storageState auth setup project (runs once before all test projects)
// consumes: TEST_USER_EMAIL + TEST_USER_PASSWORD env vars
// produces: persisted .auth/user.json that other projects load via storageState
// depends-on: setup project wired in playwright.config.ts via dependencies: ['setup']
// token-budget-impact: ~150 tokens
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
