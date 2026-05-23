// purpose: Bounded Playwright context pool with p-limit-style concurrency.
// consumes: Browser handle, concurrency cap (default 3).
// produces: acquire/release API + high-water-mark observable.
// depends-on: playwright >= 1.40.
// token-budget-impact: ~200 tokens when loaded as context.

import type { Browser, BrowserContext, Page } from "playwright";

export interface Pool {
  withPage<T>(fn: (page: Page) => Promise<T>): Promise<T>;
  highWaterMark(): number;
  drain(): Promise<void>;
}

export function createPool(browser: Browser, cap: number = 3): Pool {
  if (cap < 1 || cap > 50) throw new Error(`cap out of range: ${cap}`);
  let inUse = 0;
  let hwm = 0;
  const waiters: Array<() => void> = [];

  async function acquire(): Promise<BrowserContext> {
    while (inUse >= cap) {
      await new Promise<void>(resolve => waiters.push(resolve));
    }
    inUse++;
    if (inUse > hwm) hwm = inUse;
    return browser.newContext();
  }

  function release(ctx: BrowserContext): Promise<void> {
    inUse--;
    const w = waiters.shift();
    if (w) w();
    return ctx.close();
  }

  async function withPage<T>(fn: (page: Page) => Promise<T>): Promise<T> {
    const ctx = await acquire();
    const page = await ctx.newPage();
    try {
      return await fn(page);
    } finally {
      await page.close().catch(() => {});
      await release(ctx);
    }
  }

  function highWaterMark() { return hwm; }
  async function drain() { /* contexts close in their own finally */ }

  return { withPage, highWaterMark, drain };
}
