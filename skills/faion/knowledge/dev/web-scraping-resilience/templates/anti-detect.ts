// purpose: Anti-detect headers + navigator.webdriver override for Playwright contexts.
// consumes: BrowserContext.
// produces: hardened context with minimal first-pass detection defeated.
// depends-on: playwright >= 1.40; optionally playwright-stealth.
// token-budget-impact: ~220 tokens when loaded as context.

import type { BrowserContext } from "playwright";

const USER_AGENTS = [
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
];

export async function applyAntiDetect(ctx: BrowserContext): Promise<void> {
  const ua = USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
  await ctx.setExtraHTTPHeaders({
    "User-Agent": ua,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  });

  await ctx.addInitScript(() => {
    // navigator.webdriver -> undefined
    Object.defineProperty(navigator, "webdriver", { get: () => undefined });
    // plugins must look populated
    Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, "languages", { get: () => ["en-US", "en"] });
  });
}
