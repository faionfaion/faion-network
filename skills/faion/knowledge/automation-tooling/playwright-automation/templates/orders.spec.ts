// purpose: Example spec using role locators, auto-wait, and storageState
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for playwright-automation
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

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
