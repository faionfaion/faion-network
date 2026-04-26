// tests/a11y/wcag22.spec.js
// Purpose: WCAG 2.2 AA automated checks — target size (2.5.8) and drag alternatives (2.5.7).
// Requires: @playwright/test, @axe-core/playwright (axe-core >= 4.8)
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('WCAG 2.2 target-size minimum 24x24 CSS px (SC 2.5.8)', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag22aa'])
    .withRules(['target-size'])
    .analyze();
  expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
});

test('No drag-only interactions — button alternative required (SC 2.5.7)', async ({ page }) => {
  // Heuristic: every [draggable="true"] element must have a sibling or parent button
  // with data-move or aria-label containing "move" / "up" / "down".
  await page.goto('/board');
  const draggables = await page.$$eval('[draggable="true"]', els =>
    els.map(el => ({
      tag: el.tagName,
      text: el.textContent?.trim().slice(0, 40),
      hasButtonAlt: !!el.closest('[data-draggable-container]')
        ?.querySelector('button[data-move], button[aria-label*="move" i], button[aria-label*="up" i]'),
    }))
  );
  const failing = draggables.filter(d => !d.hasButtonAlt);
  expect(failing, `Drag items without button alternatives: ${JSON.stringify(failing)}`).toEqual([]);
});

test('Paste not blocked on auth inputs (SC 3.3.8)', async ({ page }) => {
  await page.goto('/login');
  const blocked = await page.$$eval('input[type="password"], input[type="email"]', inputs =>
    inputs
      .filter(el => el.getAttribute('autocomplete') === 'off' || el.onpaste)
      .map(el => ({ type: el.type, name: el.name }))
  );
  expect(blocked, `Paste blocked on: ${JSON.stringify(blocked)}`).toEqual([]);
});
