---
slug: puppeteer-page-interaction
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers all user-facing interaction in Puppeteer: CSS/XPath element selection, click/type/keyboard/mouse simulation, all form input types, multi-tab handling, iFrame access, dialog handling, file downloads, and mobile device emulation.
content_id: "32cf7ff2b420a1fc"
tags: [puppeteer, dom-interaction, form-automation, browser-automation, nodejs]
---
# Puppeteer: Page Interaction, Forms & Advanced Patterns

## Summary

**One-sentence:** Covers all user-facing interaction in Puppeteer: CSS/XPath element selection, click/type/keyboard/mouse simulation, all form input types, multi-tab handling, iFrame access, dialog handling, file downloads, and mobile device emulation.

**One-paragraph:** Covers all user-facing interaction in Puppeteer: CSS/XPath element selection, click/type/keyboard/mouse simulation, all form input types, multi-tab handling, iFrame access, dialog handling, file downloads, and mobile device emulation.

## Applies If (ALL must hold)

- Automating form fills, multi-step wizards, or login flows that require simulated human input.
- Extracting data from pages that require interaction before content loads.
- Testing UI components that open new tabs, show browser dialogs, or render inside iFrames.
- Emulating mobile devices for responsive-site scraping or testing.

## Skip If (ANY kills it)

- Pure HTML scraping with no JS rendering — use a simple HTTP client + cheerio, avoid the browser overhead.
- Cross-browser interaction tests — Playwright covers Firefox and WebKit natively.

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
