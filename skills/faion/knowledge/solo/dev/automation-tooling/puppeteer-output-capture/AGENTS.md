---
slug: puppeteer-output-capture
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Puppeteer can capture full-page screenshots, element-scoped screenshots, and PDF exports directly from rendered HTML.
content_id: "263244e6bd3dd697"
tags: [puppeteer, screenshot, pdf-generation, browser-automation, nodejs]
---
# Puppeteer: Screenshot & PDF Capture

## Summary

**One-sentence:** Puppeteer can capture full-page screenshots, element-scoped screenshots, and PDF exports directly from rendered HTML.

**One-paragraph:** Puppeteer can capture full-page screenshots, element-scoped screenshots, and PDF exports directly from rendered HTML. This methodology covers all screenshot options (type, quality, clip, base64) and PDF configuration (format, margins, headers/footers).

## Applies If (ALL must hold)

- Generating PDFs or screenshots from rendered HTML inside a Node-only pipeline.
- Automated visual regression artifacts — capturing page state before/after a change.
- Producing invoice/report PDFs from a web app's print-stylesheet layout.
- Sending screenshots as evidence in monitoring/alerting workflows.

## Skip If (ANY kills it)

- Static HTML with no JS rendering — a simpler HTML-to-PDF library (e.g. WeasyPrint for Python) avoids the Chromium dependency.
- High-volume thumbnail generation at scale — a dedicated service like Puppeteer clusters or Browserless is more cost-efficient.

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
