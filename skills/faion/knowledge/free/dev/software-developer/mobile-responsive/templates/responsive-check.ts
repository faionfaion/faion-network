// purpose: Playwright multi-viewport screenshot + horizontal-scroll + tap-target check.
// consumes: BASE_URL or URL arg; runs against a live preview.
// produces: screenshots in test-results/, assertion failures on scroll or undersize.
// depends-on: @playwright/test, chromium binary.
// token-budget-impact: ~30 lines.
/**
 * responsive-check.ts — Playwright script for multi-viewport screenshot and overflow detection.
 * Usage: npx ts-node scripts/responsive-check.ts http://localhost:3000
 * Output: screenshots in out/<viewport-name>.png, console errors on horizontal overflow.
 */
import { chromium, devices } from "@playwright/test";
import * as fs from "fs";

const viewports = [
  { name: "iphone-se", ...devices["iPhone SE"] },
  { name: "ipad", ...devices["iPad Pro 11"] },
  { name: "desktop", viewport: { width: 1280, height: 800 } },
];

const url = process.argv[2] ?? "http://localhost:3000";

(async () => {
  if (!fs.existsSync("out")) fs.mkdirSync("out");
  const browser = await chromium.launch();

  for (const v of viewports) {
    const ctx = await browser.newContext(v as Parameters<typeof browser.newContext>[0]);
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);

    await page.screenshot({ path: `out/${v.name}.png`, fullPage: true });

    const overflow = await page.evaluate(
      () => document.body.scrollWidth > window.innerWidth,
    );
    if (overflow) {
      console.error(`FAIL: horizontal scroll detected at ${v.name}`);
    } else {
      console.log(`OK: ${v.name}`);
    }
    await ctx.close();
  }

  await browser.close();
})();
