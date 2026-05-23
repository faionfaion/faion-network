# Web Scraping — Element Extraction and Data Cleaning

## Summary

**One-sentence:** Extract text, attributes, and table cells from a rendered DOM with Puppeteer ($eval/$$eval) or Playwright (locator API), then normalize via text/price/date helpers — returning null instead of crashing on parse failure.

**One-paragraph:** A scrape pipeline lives or dies on its extraction layer. Wrong API choice ($eval vs $$eval), guessed class selectors, and raw strings shipped to storage produce 60% downstream rework. This methodology pins the extraction surface: $eval for one element, $$eval for many, locator() for new Playwright code. Every extracted value passes through a normalizer (trim, collapse whitespace, parse price to float, parse date to ISO-8601). Parse failures return null with the reason logged; they never crash the scrape. Output: code (the extractor + normalizer module) + per-row validated objects.

**Ефективно для:**

- Solo dev wiring Puppeteer / Playwright into a daily scrape pipeline.
- AI-generated scraper code review — the rules anchor the LLM away from fabricated selectors.
- Data-cleaning audit: every extracted field has a documented normalizer with a fallback to null.
- Migration Puppeteer → Playwright locator API.

## Applies If (ALL must hold)

- You are using Puppeteer OR Playwright (Chromium) — not raw HTTP libraries.
- A target schema for the extracted rows exists.
- The page DOM is reasonably stable (template-driven, not random server-rendered HTML).
- You can run normalizer code inside the scraper process.

## Skip If (ANY kills it)

- Source is SSR JSON-fed — bypass the DOM, hit the JSON endpoint.
- Output is full-page text for LLM consumption — use Firecrawl / r.jina.ai markdown.
- One-off scrape — manual copy-paste is cheaper than building helpers.
- DOM is volatile / A/B-tested per request — see resilience methodology first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Browser page handle | Page / Locator | Puppeteer / Playwright |
| Target row schema | Pydantic / Zod | repo |
| Normalizer helpers | code | repo |
| Selector strategy | string | `web-scraping-agentic-workflow` step 4 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/web-scraping-agentic-workflow` | Umbrella — this is step 3 of that workflow. |
| `solo/dev/automation-tooling/web-scraping-pagination` | Same DOM context; ordered alongside this step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: $eval-vs-$$eval, prefer locator(), normalize immediately, null-on-parse-failure, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for extractor output (per-row + normalizer-applied) | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: $eval on multi, raw-string storage, crash-on-parse, regex price | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick locator → extract → normalize → null-coerce → persist | 600 |
| `content/06-decision-tree.xml` | essential | Tree: single/many/table → API choice → normalize → emit verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-locator` | sonnet | Bounded judgment on role/text/structural choice. |
| `write-normalizer` | sonnet | Coding task with deterministic transforms. |
| `lint-extracted` | haiku | Mechanical check that normalizers were applied. |

## Templates

| File | Purpose |
|------|---------|
| `templates/web-scraping-element-extraction.json` | JSON Schema for the per-row extraction artefact. |
| `templates/extractors.ts` | Reusable Playwright extractors + normalizers in TypeScript. |
| `templates/extractors.py` | Reusable Playwright extractors + normalizers in Python. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-element-extraction.py` | Validate a row JSON against the schema + normalization rule. | After each row extraction in CI fixtures. |

## Related

- [[web-scraping-agentic-workflow]] — umbrella.
- [[web-scraping-pagination]] — paged listings.
- [[web-scraping-resilience]] — rate-limit + retry.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches first on shape (single value / multi-element / table). It then forces locator() API choice for new Playwright code, $eval/$$eval for Puppeteer compatibility, and verifies a normalizer was applied. Leaves emit `approve`, `block-no-normalizer`, or `block-wrong-api`. Each leaf references a rule in `01-core-rules.xml`.
