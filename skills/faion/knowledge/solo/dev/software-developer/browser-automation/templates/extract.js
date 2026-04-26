// extract.js — Playwright extractor with Zod schema validation.
// Usage: URL=https://example.com/products npx playwright install chromium && node extract.js
const { chromium } = require('playwright');
const { z } = require('zod');

const Item = z.object({
  title: z.string().min(1),
  price: z.number().positive(),
  url: z.string().url(),
});

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (compatible; bot/1.0)',
  });
  const page = await context.newPage();

  // Block non-essential resources for speed
  await page.route('**/*.{png,jpg,svg,woff2,gif,css}', (r) => r.abort());

  await page.goto(process.env.URL, { waitUntil: 'networkidle' });

  const raw = await page.locator('article.product').evaluateAll((els) =>
    els.map((e) => ({
      title: e.querySelector('h2')?.textContent?.trim(),
      price: parseFloat(e.querySelector('.price')?.textContent?.replace(/[^0-9.]/g, '')),
      url: e.querySelector('a')?.href,
    })),
  );

  const items = raw
    .map((r, i) => {
      const result = Item.safeParse(r);
      if (!result.success) console.error(`row ${i} skipped:`, result.error.flatten());
      return result.success ? result.data : null;
    })
    .filter(Boolean);

  console.log(JSON.stringify(items, null, 2));
  await browser.close();
})();
