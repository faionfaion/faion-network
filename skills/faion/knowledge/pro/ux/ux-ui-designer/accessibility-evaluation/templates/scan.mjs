// scan.mjs — Playwright + axe-core WCAG scanner
// Input: urls.txt (one URL per line), optional output directory
// Output: per-page JSON files consumed by triage agent
// Install: npm i playwright @axe-core/playwright
// Usage: node scan.mjs urls.txt [out/]
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [, , urlsPath, outDir = 'axe-out'] = process.argv;
if (!urlsPath) { console.error('Usage: node scan.mjs <urls.txt> [outDir]'); process.exit(1); }

mkdirSync(outDir, { recursive: true });
const urls = readFileSync(urlsPath, 'utf8').split('\n').map(u => u.trim()).filter(Boolean);
const browser = await chromium.launch();

for (const url of urls) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();
  const slug = url.replace(/[^a-z0-9]+/gi, '_').slice(0, 80);
  writeFileSync(join(outDir, `${slug}.json`), JSON.stringify(results, null, 2));
  console.log(`[${results.violations.length} violations] ${url}`);
  await ctx.close();
}
await browser.close();
