# Web Scraping — Pagination and Memory Management

## Summary

**One-sentence:** Implements one of three pagination patterns (next-button, infinite-scroll, load-more) with deduplication and a bounded browser-pool / semaphore so a 10k-item scrape doesn't OOM the runner.

**One-paragraph:** Three pagination shapes cover virtually all paginated sites. Each has a different stop-condition: next-button stops when the button is absent or disabled; infinite-scroll stops when `document.body.scrollHeight` stops growing; load-more stops when the button leaves the viewport. All three require deduplication (index or hash). Concurrent multi-URL scrapes need a browser pool or `p-limit` / semaphore — without one, every URL leaks a Chromium process and the runner OOMs at ~50 URLs. Output: pagination code that produces a structured walk-report (pattern, pages_walked, items_collected, duplicate_count, pool_high_water_mark) the agent emits per source.

**Ефективно для:**

- Solo dev scraping listing pages, archives, paginated APIs without an offset/limit endpoint.
- AI-generated scraper code review — agents default to wrong stop condition (infinite-scroll on a next-button page).
- Bounded-memory pipelines: explicit p-limit / pool replaces unbounded `Promise.all`.
- Migrating Puppeteer pool code to Playwright BrowserContext.

## Applies If (ALL must hold)

- Source has a listing or search results page across multiple URLs / scrolls.
- Number of items is bounded but unknown (you scrape until "end").
- Concurrent runs across URLs are allowed (within rate limits).
- Heap / memory budget is tight (CI runner, small VPS).

## Skip If (ANY kills it)

- Source exposes an API with offset/limit — use it, don't paginate the DOM.
- Single-page source (no pagination).
- One-off scrape with &lt; 100 items — manual or quick-and-dirty is cheaper.
- Source aggressively rate-limits paged requests — see resilience first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Browser pool / locator factory | code | `web-scraping-resilience` templates |
| Page identifier (URL / cursor) | string | source |
| Item-unique key (id / hash) | string | extractor schema |
| Concurrency cap | integer | infra budget |
| Stop-condition selector | locator | source DOM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/web-scraping-agentic-workflow` | Umbrella — this is step 3.5 of that workflow. |
| `solo/dev/automation-tooling/web-scraping-element-extraction` | Per-page extraction inside the walk. |
| `solo/dev/automation-tooling/web-scraping-resilience` | Pool config + rate-limit + retry. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pattern-by-shape, stop-condition, dedupe, finally-close, semaphore-cap, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for walk-report + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: infinite-loop, leak-pages, unbounded-Promise.all, missed-dedupe | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: detect-pattern → cap-pool → walk → dedupe → emit-report | 600 |
| `content/06-decision-tree.xml` | essential | Tree: pattern? → stop-cond → dedupe → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect-pattern` | haiku | DOM heuristic: next-button selector? infinite-scroll-sentinel? load-more button? |
| `write-walker` | sonnet | Coding task: stop-condition + dedupe key. |
| `configure-pool` | haiku | Mechanical: set concurrency, finally-close. |

## Templates

| File | Purpose |
|------|---------|
| `templates/web-scraping-pagination.json` | JSON Schema for the per-walk report artefact. |
| `templates/walker.ts` | Three walker functions (next-button, infinite-scroll, load-more) in TypeScript. |
| `templates/browser-pool.ts` | Bounded browser-context pool with p-limit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-pagination.py` | Validate a walk-report JSON against schema + dedupe rule. | After each pagination walk completes. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[web-scraping-agentic-workflow]] — umbrella.
- [[web-scraping-element-extraction]] — per-page extraction inside the walk.
- [[web-scraping-resilience]] — pool + retry that this assumes.

## Decision tree

See `content/06-decision-tree.xml`. The tree first detects pattern via DOM features (next-button selector / scrollHeight growth / load-more button). It then routes to the matching walker, verifies the stop condition matches the pattern, checks dedupe applied, and verifies the concurrency cap. Leaves emit `approve`, `block-wrong-pattern`, `block-no-dedupe`, or `block-unbounded-concurrency`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/web-scraping-pagination.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/web-scraping-pagination.json",
  "type": "object",
  "required": [
    "artefact_id",
    "source",
    "pattern",
    "pages_walked",
    "items_collected",
    "duplicate_count",
    "concurrency_cap",
    "pool_high_water_mark",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^wsp-[a-z0-9-]{6,}$"
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "pattern": {
      "enum": [
        "next-button",
        "infinite-scroll",
        "load-more"
      ]
    },
    "pages_walked": {
      "type": "integer",
      "minimum": 1
    },
    "items_collected": {
      "type": "integer",
      "minimum": 0
    },
    "duplicate_count": {
      "type": "integer",
      "minimum": 0
    },
    "concurrency_cap": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50
    },
    "pool_high_water_mark": {
      "type": "integer",
      "minimum": 0
    },
    "stop_condition_observed": {
      "type": "string"
    },
    "verdict": {
      "enum": [
        "approve",
        "block-wrong-pattern",
        "block-no-dedupe",
        "block-unbounded-concurrency"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/walker.ts`

```typescript
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
```

### `templates/browser-pool.ts`

```typescript
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
```
