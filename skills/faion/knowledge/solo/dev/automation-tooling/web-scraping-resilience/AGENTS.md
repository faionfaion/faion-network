---
slug: web-scraping-resilience
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production scrapers need three layers: rate limiting with random jitter to avoid IP bans, exponential-backoff retry for transient failures, and safe extraction helpers that return defaults instead of crashing.
content_id: "c1b14efa6030fdb2"
tags: [web-scraping, rate-limiting, retry, error-handling, anti-detection]
---
# Web Scraping — Resilience: Rate Limiting, Retries, and Error Handling

## Summary

**One-sentence:** Production scrapers need three layers: rate limiting with random jitter to avoid IP bans, exponential-backoff retry for transient failures, and safe extraction helpers that return defaults instead of crashing.

**One-paragraph:** Production scrapers need three layers: rate limiting with random jitter to avoid IP bans, exponential-backoff retry for transient failures, and safe extraction helpers that return defaults instead of crashing. Anti-detection headers and webdriver property overrides reduce bot-detection false positives.

## Applies If (ALL must hold)

- Any scraper that runs on a schedule against a live site.
- Scrapers that process more than a handful of URLs in a batch.
- Sites that enforce rate limits, CAPTCHAs, or bot-detection middleware.
- Long-running scrape jobs where a single crash should not abort the entire run.

## Skip If (ANY kills it)

- One-off dev experiments against local test servers — overhead exceeds value.
- Sites behind hard interactive CAPTCHAs (Cloudflare Turnstile) where no header trick helps — budget for a real anti-bot service instead.

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
