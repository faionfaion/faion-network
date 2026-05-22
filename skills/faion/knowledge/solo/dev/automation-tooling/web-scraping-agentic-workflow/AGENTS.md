---
slug: web-scraping-agentic-workflow
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A scrape agent probes SSR vs JS-render, selects the right tool (httpx+selectolax or Playwright), validates every row against a schema, stores to a versioned JSONL dataset, and detects schema drift between runs.
content_id: "481ac2a3a37b6383"
tags: [web-scraping, agentic-workflow, schema-validation, dataset-storage, firecrawl]
---
# Web Scraping — Agentic Workflow and Tool Selection

## Summary

**One-sentence:** A scrape agent probes SSR vs JS-render, selects the right tool (httpx+selectolax or Playwright), validates every row against a schema, stores to a versioned JSONL dataset, and detects schema drift between runs.

**One-paragraph:** A scrape agent probes SSR vs JS-render, selects the right tool (httpx+selectolax or Playwright), validates every row against a schema, stores to a versioned JSONL dataset, and detects schema drift between runs. Use managed services (Firecrawl, Jina Reader) when the agent only needs clean text.

## Applies If (ALL must hold)

- Sites without an official API or RSS feed where you need product, price, or listing data on a schedule.
- Research workflows: gathering a corpus of pages for an LLM to summarize or fine-tune on.
- Monitoring: tracking changes to a competitor pricing page, regulator publication, or status board.
- Aggregating content from JS-rendered SPAs that curl cannot see.
- One-off backfills of public data into a structured dataset.

## Skip If (ANY kills it)

- The site offers an official API or RSS — use it. Cheaper, more reliable, and ToS-clean.
- Targets where the ToS forbids scraping and you have no fair-use defense.
- Authenticated account data of users who did not consent.
- Data behind hard anti-bot walls (Cloudflare Turnstile interactive, Akamai Bot Manager) without a stealth service budget.
- Sub-second latency requirements — scraping is inherently slow.

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
