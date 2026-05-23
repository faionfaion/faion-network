// purpose: Three pagination walker implementations for Playwright.
// consumes: Playwright Page, item-extractor function, dedupe key fn.
// produces: deduped item list + walk telemetry.
// depends-on: playwright >= 1.40.
// token-budget-impact: ~350 tokens when loaded as context.

import type { Page, Locator } from "playwright";

const HARD_CEILING = 500;

export interface WalkTelemetry {
  pattern: "next-button" | "infinite-scroll" | "load-more";
  pages_walked: number;
  items_collected: number;
  duplicate_count: number;
  stop_condition_observed: string;
}

export async function walkNextButton<T>(
  page: Page,
  extract: () => Promise<T[]>,
  keyOf: (t: T) => string,
  nextSelector: string
): Promise<{ items: T[]; telemetry: WalkTelemetry }> {
  const seen = new Set<string>();
  const items: T[] = [];
  let duplicate = 0;
  let pages = 0;
  let stop = "";
  while (pages < HARD_CEILING) {
    pages++;
    for (const it of await extract()) {
      const k = keyOf(it);
      if (seen.has(k)) { duplicate++; continue; }
      seen.add(k);
      items.push(it);
    }
    const next = page.locator(nextSelector);
    const exists = await next.count() > 0;
    const disabled = exists && (await next.first().isDisabled().catch(() => false));
    if (!exists || disabled) { stop = !exists ? "button absent" : "button disabled"; break; }
    await Promise.all([next.first().click(), page.waitForLoadState("networkidle")]);
  }
  return { items, telemetry: { pattern: "next-button", pages_walked: pages, items_collected: items.length, duplicate_count: duplicate, stop_condition_observed: stop || "ceiling reached" } };
}

export async function walkInfiniteScroll<T>(
  page: Page,
  extract: () => Promise<T[]>,
  keyOf: (t: T) => string,
  idleMs = 4000
): Promise<{ items: T[]; telemetry: WalkTelemetry }> {
  const seen = new Set<string>();
  const items: T[] = [];
  let duplicate = 0;
  let pages = 0;
  let lastHeight = -1;
  let stableMs = 0;
  while (pages < HARD_CEILING) {
    pages++;
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    const h = await page.evaluate(() => document.body.scrollHeight);
    stableMs = h === lastHeight ? stableMs + 500 : 0;
    lastHeight = h;
    for (const it of await extract()) {
      const k = keyOf(it);
      if (seen.has(k)) { duplicate++; continue; }
      seen.add(k);
      items.push(it);
    }
    if (stableMs >= idleMs) break;
  }
  return { items, telemetry: { pattern: "infinite-scroll", pages_walked: pages, items_collected: items.length, duplicate_count: duplicate, stop_condition_observed: `scrollHeight stable ${idleMs}ms` } };
}

export async function walkLoadMore<T>(
  page: Page,
  extract: () => Promise<T[]>,
  keyOf: (t: T) => string,
  buttonSelector: string
): Promise<{ items: T[]; telemetry: WalkTelemetry }> {
  const seen = new Set<string>();
  const items: T[] = [];
  let duplicate = 0;
  let pages = 0;
  let stop = "";
  while (pages < HARD_CEILING) {
    pages++;
    for (const it of await extract()) {
      const k = keyOf(it);
      if (seen.has(k)) { duplicate++; continue; }
      seen.add(k);
      items.push(it);
    }
    const btn = page.locator(buttonSelector);
    if ((await btn.count()) === 0) { stop = "button absent"; break; }
    if (!(await btn.first().isVisible())) { stop = "button hidden"; break; }
    await btn.first().click();
    await page.waitForTimeout(500);
  }
  return { items, telemetry: { pattern: "load-more", pages_walked: pages, items_collected: items.length, duplicate_count: duplicate, stop_condition_observed: stop || "ceiling reached" } };
}
