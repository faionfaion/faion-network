---
slug: browser-automation-overview
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A routing layer for headless browser tasks: compare Puppeteer vs Playwright using the feature matrix, pick one, then load the appropriate sibling methodology (`puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`).
content_id: "6a4adc6cf5506ced"
tags: [browser-automation, puppeteer, playwright, routing, headless]
---
# Browser Automation Overview

## Summary

**One-sentence:** A routing layer for headless browser tasks: compare Puppeteer vs Playwright using the feature matrix, pick one, then load the appropriate sibling methodology (`puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`).

**One-paragraph:** A routing layer for headless browser tasks: compare Puppeteer vs Playwright using the feature matrix, pick one, then load the appropriate sibling methodology (`puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`). This file does not contain implementation patterns — it is the decision layer only.

## Applies If (ALL must hold)

- Choosing between Puppeteer and Playwright for a new automation, scraping, or E2E project.
- Onboarding a project that needs headless browser tasks (PDF, screenshots, form fill, scraping, E2E).
- Triaging an existing browser-automation codebase: which tool is in use and where are the gaps.
- Routing an agent to the correct sibling skill before producing any code.
- Centralizing browser-automation knowledge for a single agent that will fan out to one of three sibling skills.

## Skip If (ANY kills it)

- Deep implementation: jump directly to `puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`.
- Mobile app automation (Appium, Detox, Maestro) — browser-only scope.
- API-only testing — use `api-testing` patterns; a browser is wasteful.
- Browser fingerprinting / strong anti-bot evasion at scale — out of scope here.
- For accessibility audits — Lighthouse / axe-core have purpose-built drivers; Playwright integration is fine but the audit logic is not in this file.

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
