/**
 * touch-target-audit.js — Flag tap targets smaller than 44x44 at mobile viewport.
 * Input: URL passed as first argument.
 * Output: JSON array of elements below threshold to stdout.
 *
 * Install: npm i -D @playwright/test playwright
 * Run: node touch-target-audit.js https://example.com
 */
const { chromium, devices } = require("playwright");

(async () => {
  const url = process.argv[2];
  if (!url) {
    console.error("Usage: node touch-target-audit.js <url>");
    process.exit(1);
  }

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices["iPhone 13"] });
  const page = await ctx.newPage();

  await page.goto(url, { waitUntil: "networkidle" });

  const small = await page.$$eval(
    'a, button, [role="button"], input[type="submit"], input[type="reset"], [onclick]',
    (els) =>
      els
        .map((el) => {
          const r = el.getBoundingClientRect();
          return {
            tag: el.tagName,
            text: (el.innerText || el.value || "").slice(0, 60).trim(),
            w: Math.round(r.width),
            h: Math.round(r.height),
            tooSmall: r.width < 44 || r.height < 44,
          };
        })
        .filter((e) => e.tooSmall)
  );

  console.log(JSON.stringify(small, null, 2));
  console.error(`Found ${small.length} element(s) below 44x44 threshold.`);

  await browser.close();
  process.exit(small.length > 0 ? 1 : 0);
})();
