---
slug: browser-automation
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Headless browser automation using Playwright (preferred) or Puppeteer for E2E testing, web scraping, screenshot/PDF generation, and form automation.
content_id: "d8c859d1a4403ff4"
tags: [browser, automation, testing, scraping, playwright, puppeteer]
---
# Browser Automation

## Summary

**One-sentence:** Headless browser automation using Playwright (preferred) or Puppeteer for E2E testing, web scraping, screenshot/PDF generation, and form automation.

**One-paragraph:** Headless browser automation using Playwright (preferred) or Puppeteer for E2E testing, web scraping, screenshot/PDF generation, and form automation. Use role= and text= locators; always wait on conditions, never fixed timeouts; persist auth via context.storageState; block images/fonts/analytics on scraping runs.

## Applies If (ALL must hold)

- E2E testing of web apps (Playwright test suite, preview verification).
- Scraping public sites that have no usable API.
- Programmatic screenshot/PDF generation for reports, OG cards, invoice rendering.
- Form fill and submit automation for portals lacking an API.
- Visual regression on component library builds.

## Skip If (ANY kills it)

- The site offers a REST/GraphQL/RSS API — always prefer the API; browser automation is brittle and slow.
- Sites with strong anti-bot protection (Cloudflare Turnstile, PerimeterX) — fight cost exceeds value.
- High-throughput scraping (>100 pages/sec) — use HTTP-only (httpx, scrapy) instead.
- Tasks requiring credentials you don't legitimately own.
- Behind-VPN or zero-trust portals where headless browser fingerprint trips MFA.

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

- parent skill: `solo/dev/software-developer/`
