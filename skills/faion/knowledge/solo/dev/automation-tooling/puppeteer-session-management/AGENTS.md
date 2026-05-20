---
slug: puppeteer-session-management
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers cookie get/set/delete, localStorage/sessionStorage manipulation, HTTP request interception (block, modify headers, mock responses), and response capture for data extraction pipelines.
content_id: "fc438b2f3024b42a"
tags: [puppeteer, cookies, request-interception, session, browser-automation]
---
# Puppeteer: Session, Cookies & Request Interception

## Summary

**One-sentence:** Covers cookie get/set/delete, localStorage/sessionStorage manipulation, HTTP request interception (block, modify headers, mock responses), and response capture for data extraction pipelines.

**One-paragraph:** Covers cookie get/set/delete, localStorage/sessionStorage manipulation, HTTP request interception (block, modify headers, mock responses), and response capture for data extraction pipelines.

## Applies If (ALL must hold)

- Automating authenticated workflows where re-login on every run is too slow or triggers CAPTCHA.
- Blocking images/fonts/stylesheets to get a 3-5x speedup on DOM-only scraping tasks.
- Mocking external API responses for deterministic test runs.
- Adding auth headers (Bearer tokens) to requests without touching the page JS.

## Skip If (ANY kills it)

- Sites that detect cookie injection as a session anomaly — some auth systems re-verify on suspicious cookie patterns; test first.
- When the goal is intercepting encrypted traffic (HTTPS MITM) — Puppeteer interception works at the protocol level but does not decrypt independently of the browser's TLS stack.

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
