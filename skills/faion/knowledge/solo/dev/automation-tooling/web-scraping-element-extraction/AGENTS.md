---
slug: web-scraping-element-extraction
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Extract text, attributes, and table data from DOM elements using Puppeteer ($eval/$$eval) and Playwright (locator API).
content_id: "91461b1f43ef4f04"
tags: [web-scraping, dom-extraction, puppeteer, playwright, data-cleaning]
---
# Web Scraping — Element Extraction and Data Cleaning

## Summary

**One-sentence:** Extract text, attributes, and table data from DOM elements using Puppeteer ($eval/$$eval) and Playwright (locator API).

**One-paragraph:** Extract text, attributes, and table data from DOM elements using Puppeteer ($eval/$$eval) and Playwright (locator API). Normalize extracted strings with text, price, and date helpers before persisting.

## Applies If (ALL must hold)

- Extracting product names, prices, image URLs, or listing data from a scraped page.
- Pulling structured rows from HTML tables (price tables, comparison grids, report exports).
- Collecting all attribute values (href, src, data-*) from a set of matched elements.
- Cleaning raw text before writing to a JSONL dataset or database.

## Skip If (ANY kills it)

- When the page is JS-rendered and the DOM is not yet settled — wait for network idle or a sentinel element first.
- When the site offers a structured API — parsing JSON is faster and more stable than DOM extraction.
- When you need cross-page aggregation — that belongs in pagination logic, not extraction.

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
