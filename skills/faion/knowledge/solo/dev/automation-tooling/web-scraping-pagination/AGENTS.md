---
slug: web-scraping-pagination
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three pagination patterns (next-button, infinite-scroll, load-more) cover virtually all paginated sites.
content_id: "945b1c1f399eab9d"
tags: [web-scraping, pagination, infinite-scroll, browser-pool, concurrency]
---
# Web Scraping — Pagination and Memory Management

## Summary

**One-sentence:** Three pagination patterns (next-button, infinite-scroll, load-more) cover virtually all paginated sites.

**One-paragraph:** Three pagination patterns (next-button, infinite-scroll, load-more) cover virtually all paginated sites. Pair them with a browser pool or semaphore to bound memory when scraping many URLs concurrently.

## Applies If (ALL must hold)

- Scraping a listing page that spans multiple pages via a next/prev button.
- Extracting all items from a feed or social wall that uses infinite scroll.
- Handling a "Load More" button that appends items to the same DOM without navigation.
- Running concurrent scrapes across many URLs where browser memory must be bounded.

## Skip If (ANY kills it)

- Single-page sites with no pagination — add unnecessary complexity.
- APIs with offset/cursor parameters — use HTTP pagination, not DOM pagination.
- When the total item count is small enough to fit in one DOM render — no loop needed.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/automation-tooling/`
