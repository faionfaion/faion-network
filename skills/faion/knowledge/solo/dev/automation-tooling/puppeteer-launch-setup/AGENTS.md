---
slug: puppeteer-launch-setup
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Puppeteer is Google's Node.
content_id: "484c73a8de71ae0c"
tags: [puppeteer, browser-automation, headless-chrome, navigation, nodejs]
---
# Puppeteer: Launch, Navigation & Wait Strategies

## Summary

**One-sentence:** Puppeteer is Google's Node.

**One-paragraph:** Puppeteer is Google's Node.js library for controlling Chrome/Chromium via the DevTools Protocol. This methodology covers installation, browser launch configuration, page navigation, and the correct wait strategies for SPA and classic sites.

## Applies If (ALL must hold)

- Headless Chrome scripting jobs that need DevTools Protocol features (CDP sessions, request interception, coverage, tracing).
- Generating PDFs or screenshots from rendered HTML inside a Node-only pipeline.
- Light scraping where stealth is already handled (reCAPTCHA-free targets) and you want minimum dependencies.
- Running on serverless (chromium binary via @sparticuz/chromium) where Playwright bundles are too large.

## Skip If (ANY kills it)

- Cross-browser testing — use Playwright (Firefox + WebKit are first-class there; Puppeteer is Chromium-only).
- E2E test suites with parallelism, retries, fixtures — Playwright Test or Cypress give you that for free.
- Long-running scraping farms against bot-defended targets — Playwright + stealth or a managed service.

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
