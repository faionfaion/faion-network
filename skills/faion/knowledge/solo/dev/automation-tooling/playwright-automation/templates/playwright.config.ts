// purpose: Playwright config with trace='on-first-retry' + cross-browser projects
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for playwright-automation
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

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
