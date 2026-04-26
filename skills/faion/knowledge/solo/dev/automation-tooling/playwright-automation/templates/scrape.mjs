#!/usr/bin/env node
// scrape.mjs — headless scrape with auth reuse via storageState
// Usage: PW_USER=user@example.com PW_PASS=pass node scrape.mjs https://target.example/orders
// Auth is saved to ./auth.json on first login and reused on subsequent runs.

import { chromium } from 'playwright';
import fs from 'node:fs';

const URL = process.argv[2] ?? process.exit(1, 'URL argument required');
const AUTH = './auth.json';

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  storageState: fs.existsSync(AUTH) ? AUTH : undefined,
  viewport: { width: 1280, height: 720 },
  // Set realistic userAgent — default Playwright UA gets blocked by bot detection
  userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
});
const page = await ctx.newPage();

await page.goto(URL, { waitUntil: 'domcontentloaded' });

// Login if needed
if (await page.getByRole('button', { name: /sign in/i }).isVisible()) {
  await page.getByLabel('Email').fill(process.env.PW_USER);
  await page.getByLabel('Password').fill(process.env.PW_PASS);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL('**/orders');
  await ctx.storageState({ path: AUTH });
}

// Extract table rows
const rows = await page.getByRole('row').all();
const data = [];
for (const r of rows.slice(1)) {
  data.push(await r.allInnerTexts());
}

console.log(JSON.stringify(data, null, 2));
await browser.close();
