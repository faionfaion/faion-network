// purpose: Playwright spec verifying loading / success / error states + latency
// consumes: live build URL with action inventory
// produces: pass/fail signals + observed latency feeding the visibility-of-system-status artefact
// depends-on: content/01-core-rules.xml (r1-feedback-thresholds, r3-three-states)
// token-budget-impact: external tool; no LLM token cost
//
// loading-state.spec.ts — Playwright tests for system status visibility
// Tests: submit button loading state, file upload progress indicator
// Usage: npx playwright test loading-state.spec.ts

import { test, expect } from '@playwright/test';

test('submit button shows loading state during async operation', async ({ page }) => {
  await page.goto('/checkout');
  await page.fill('[name="email"]', 'test@example.com');

  const submitButton = page.locator('button[type="submit"]');

  // Click and immediately verify loading state appears within 100ms
  const [_] = await Promise.all([
    submitButton.click(),
    expect(submitButton).toHaveAttribute('aria-busy', 'true', { timeout: 100 }),
  ]);

  // Button must be disabled during async operation (prevents double-submit)
  await expect(submitButton).toBeDisabled();

  // Wait for completion and verify status region appears
  await expect(page.locator('[role="status"]')).toBeVisible({ timeout: 10_000 });
});

test('submit button re-enables after success', async ({ page }) => {
  await page.goto('/checkout');
  const submitButton = page.locator('button[type="submit"]');
  await submitButton.click();

  // After operation completes, button should not remain disabled indefinitely
  await expect(submitButton).not.toHaveAttribute('aria-busy', 'true', { timeout: 15_000 });
});

test('file upload shows progress indicator within 500ms', async ({ page }) => {
  await page.goto('/upload');

  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser'),
    page.click('[data-testid="upload-trigger"]'),
  ]);

  await fileChooser.setFiles('tests/fixtures/sample.pdf');

  // Progress bar must appear quickly — skeleton screen or progress indicator
  await expect(page.locator('[role="progressbar"]')).toBeVisible({ timeout: 500 });
});

test('error state appears and does not auto-dismiss', async ({ page }) => {
  // Simulate network failure
  await page.route('**/api/submit', (route) => route.abort('failed'));
  await page.goto('/checkout');

  const submitButton = page.locator('button[type="submit"]');
  await submitButton.click();

  const errorMessage = page.locator('[role="alert"]');
  await expect(errorMessage).toBeVisible({ timeout: 5_000 });

  // Error must not auto-dismiss — wait 6 seconds and verify still visible
  await page.waitForTimeout(6_000);
  await expect(errorMessage).toBeVisible();
});
