---
slug: playwright-automation
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cross-browser automation library (Chromium/Firefox/WebKit) for E2E testing, agentic web tasks, and headless scraping with auth reuse via storageState.
content_id: "c81e6644c6f45d57"
tags: [playwright, e2e-testing, browser-automation, scraping, testing]
---
# Playwright Automation

## Summary

**One-sentence:** Cross-browser automation library (Chromium/Firefox/WebKit) for E2E testing, agentic web tasks, and headless scraping with auth reuse via storageState.

**One-paragraph:** Cross-browser automation library (Chromium/Firefox/WebKit) for E2E testing, agentic web tasks, and headless scraping with auth reuse via storageState. The concrete rule: always prefer getByRole > getByLabel > getByText > CSS selectors — role-based locators survive UI tweaks; CSS selectors die on the next sprint. Never use page.waitForTimeout; use locator auto-wait or expect(locator).toBeVisible({timeout}).

## Applies If (ALL must hold)

- Cross-browser E2E tests (Chromium/Firefox/WebKit) with auto-waiting and trace viewer
- Agentic web tasks: login flows, form filling, scraping requiring JS execution
- Visual regression testing via toHaveScreenshot() snapshots
- API testing alongside UI in one session (page.request)
- Replacing legacy Selenium/Cypress suites for speed and reliability
- Authenticating once, reusing storageState across many headless agent runs

## Skip If (ANY kills it)

- Pure HTTP scraping where the target renders server-side (use httpx/fetch, 100x cheaper)
- Mobile-app E2E testing (use Appium, Detox, Maestro)
- Sub-millisecond unit tests of UI components (use Vitest + Testing Library)
- Targets with hard bot-detection (Cloudflare Turnstile aggressive mode)
- Long-lived stateful sessions (hours): better suited to a real browser profile

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
