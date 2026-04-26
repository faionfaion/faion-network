// verify-escape-exits.spec.js — verify Escape key closes all modals
// Requires: Playwright (npm install -D playwright)
// Usage: npx playwright test verify-escape-exits.spec.js
// Set BASE_URL env var or update the goto() call below.

const { test, expect } = require('@playwright/test');

// Add all trigger/modal pairs for your product here.
const MODAL_TRIGGERS = [
  { trigger: '[data-testid="delete-btn"]', modal: '[role="dialog"]' },
  { trigger: '[data-testid="settings-btn"]', modal: '[aria-label="Settings"]' },
  // Example: { trigger: '[data-testid="share-btn"]', modal: '[aria-label="Share dialog"]' },
];

for (const { trigger, modal } of MODAL_TRIGGERS) {
  test(`Escape closes modal triggered by ${trigger}`, async ({ page }) => {
    await page.goto(process.env.BASE_URL || 'http://localhost:3000');
    await page.click(trigger);
    await expect(page.locator(modal)).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator(modal)).not.toBeVisible();
  });
}
