---
slug: puppeteer-stealth-proxy
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers puppeteer-extra-plugin-stealth for automated bot-detection evasion, manual navigator property overrides, single-proxy configuration, and rotating proxy pool patterns.
content_id: "c6fae0d76c10ffdd"
tags: [puppeteer, stealth, proxy, bot-detection, browser-automation]
---
# Puppeteer: Stealth Mode & Proxy Support

## Summary

**One-sentence:** Covers puppeteer-extra-plugin-stealth for automated bot-detection evasion, manual navigator property overrides, single-proxy configuration, and rotating proxy pool patterns.

**One-paragraph:** Covers puppeteer-extra-plugin-stealth for automated bot-detection evasion, manual navigator property overrides, single-proxy configuration, and rotating proxy pool patterns. Includes limitations and arms-race caveats for production scraping.

## Applies If (ALL must hold)

- Scraping targets with basic bot-detection that checks navigator properties.
- Pipelines that must distribute requests across multiple IP addresses to avoid rate-limiting.
- Any flow that requires appearing as a regular browser to bypass simple fingerprinting.

## Skip If (ANY kills it)

- Long-running scraping farms against Cloudflare Enterprise or Datadome-defended targets — stealth plugin lags behind detection; switch to Playwright + playwright-extra/stealth or a managed service like Bright Data.
- Anything involving credentials, CAPTCHAs, or 2FA in a fully automated loop — human-in-the-loop checkpoints are required (see puppeteer-agent-workflow).

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
