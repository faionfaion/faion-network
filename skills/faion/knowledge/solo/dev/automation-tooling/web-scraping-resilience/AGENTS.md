---
slug: web-scraping-resilience
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a resilience config artefact (jitter, exp-backoff retry, safeExtract, anti-detect headers, crash-recover) that wraps the scrape pipeline against bans, transient failures, and browser crashes.
content_id: "c1b14efa6030fdb2"
complexity: medium
produces: config
est_tokens: 4000
tags: [web-scraping, rate-limiting, retry, error-handling, anti-detection]
---
# Web Scraping — Resilience

## Summary

**One-sentence:** Produces a resilience config that wraps the scrape pipeline with jittered rate-limit, exponential-backoff retry capped at 5, safeExtract fallbacks, browser-crash recovery, and anti-detection headers.

**One-paragraph:** Production scrapers need three layers that the development-grade pipeline lacks. (1) Rate-limit with random jitter — fixed-interval requests are a fingerprint sites ban on. (2) Exponential-backoff retry capped at 5 attempts — re-throw on the final to allow caller logging. (3) safeExtract that wraps every page.$eval with timeout + default — a single failing element should not crash the row. Add browser-crash recovery (detect "Target closed" / "Session closed", relaunch) and anti-detection headers (Accept-Language, override navigator.webdriver, stealth plugin where supported). Output is a config artefact + code wrappers; the per-run scrape consumes the config rather than copy-pasting these settings each time.

**Ефективно для:**

- Solo dev whose dev-grade scraper started getting 429-banned in production.
- AI-assisted code review — the rules block "just retry on failure" loops without backoff.
- Long-running scrapes (overnight cron) where a single browser crash should not abort.
- Sources with mild bot-detection (Cloudflare's basic JS challenge level).

## Applies If (ALL must hold)

- Scrape runs unattended (cron, scheduled task).
- Source produces transient failures (timeouts, 5xx, 429).
- Browser-based scraper (Puppeteer / Playwright).
- A target rate exists (requests per minute per domain).

## Skip If (ANY kills it)

- Source has an SLA-backed public API — use it, this is overkill.
- Hardline anti-bot (Cloudflare Turnstile, CAPTCHA at every page) — fundamental rethink needed, not just resilience.
- One-off ad-hoc scrape — manual retry is cheaper.
- Source explicitly forbids scraping AND no legal exception — stop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target requests/min per domain | int | source policy / robots.txt |
| Browser handle | Puppeteer / Playwright | runtime |
| Anti-detection plugin | npm pkg | playwright-stealth / puppeteer-extra |
| Logger | code | repo |
| Concurrency cap | int | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/web-scraping-agentic-workflow` | Umbrella — resilience is the production-hardening layer. |
| `solo/dev/automation-tooling/web-scraping-pagination` | Pool config consumed by this layer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: jitter, exp-backoff cap 5, safeExtract, crash-recover, anti-detect headers, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for resilience config artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tight loop, no jitter, infinite retry, webdriver visible | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: probe rate-limit → wire jitter → wire retry → wrap extracts → arm crash-recover | 700 |
| `content/06-decision-tree.xml` | essential | Tree: error-class? → action (jitter, retry, recover, alarm) → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `set-rate-limit` | haiku | Mechanical: requests/min cap + jitter window. |
| `wire-retry` | sonnet | Coding task: exp-backoff with jitter. |
| `wrap-safe-extract` | sonnet | Helper authoring with sensible defaults. |

## Templates

| File | Purpose |
|------|---------|
| `templates/web-scraping-resilience.json` | JSON Schema for the resilience config artefact. |
| `templates/safe-extract.ts` | safeExtract + retryWithBackoff helpers in TypeScript. |
| `templates/anti-detect.ts` | Header set + navigator.webdriver override + stealth plugin wiring. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-resilience.py` | Validate the resilience config JSON against schema + consistency rules. | On scrape start; nightly in CI. |

## Related

- [[web-scraping-agentic-workflow]] — umbrella.
- [[web-scraping-pagination]] — pool config consumed here.
- [[web-scraping-element-extraction]] — safeExtract wraps it.

## Decision tree

See `content/06-decision-tree.xml`. The tree classifies the error class observed during the run (transient 5xx, 429 rate-limit, timeout, browser crash, captcha) and routes to the matching action: jitter+retry, back-off doubled, page recover, browser relaunch, or human-escalate. Leaves emit `apply`, `escalate-human`, or `block-fatal`. Each leaf references a rule in `01-core-rules.xml`.
