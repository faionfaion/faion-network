---
slug: web-scraping-pagination
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a pagination-walk artefact and a bounded-memory browser pool config implementing one of three patterns (next-button, infinite-scroll, load-more) for a paginated source.
content_id: "945b1c1f399eab9d"
complexity: medium
produces: code
est_tokens: 3700
tags: [web-scraping, pagination, infinite-scroll, browser-pool, concurrency]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-pagination.py` | Validate a walk-report JSON against schema + dedupe rule. | After each pagination walk completes. |

## Related

- [[web-scraping-agentic-workflow]] — umbrella.
- [[web-scraping-element-extraction]] — per-page extraction inside the walk.
- [[web-scraping-resilience]] — pool + retry that this assumes.

## Decision tree

See `content/06-decision-tree.xml`. The tree first detects pattern via DOM features (next-button selector / scrollHeight growth / load-more button). It then routes to the matching walker, verifies the stop condition matches the pattern, checks dedupe applied, and verifies the concurrency cap. Leaves emit `approve`, `block-wrong-pattern`, `block-no-dedupe`, or `block-unbounded-concurrency`. Each leaf references a rule in `01-core-rules.xml`.
