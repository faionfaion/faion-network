---
slug: google-ads-reporting
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GAQL-based reporting, scheduled automation, and error handling patterns for Google Ads accounts.
content_id: "7fad4d1a8505d80b"
tags: [google-ads, gaql, reporting, automation, api]
---
# Google Ads Reporting and Automation — GAQL, Batch Ops, Error Handling

## Summary

**One-sentence:** GAQL-based reporting, scheduled automation, and error handling patterns for Google Ads accounts.

**One-paragraph:** GAQL-based reporting, scheduled automation, and error handling patterns for Google Ads accounts. Use search_stream for large queries, always include segments.date, divide cost_micros by 1,000,000 before presenting, and pin the API version. Read-only reporting agents feed a warehouse; mutation agents (auto-pause, bid change) require strict guardrails and human approval before executing.

## Applies If (ALL must hold)

- Scheduled daily or weekly performance reports across multiple Google Ads accounts (MCC)
- Threshold-based alerting: high CPA, low CTR, paused-by-mistake, budget pacing exceptions
- Bulk read pipelines feeding a warehouse, Looker Studio, or Slack from raw GAQL
- Auto-pausing low performers with strict guardrails and a per-run paused-list log
- Change-history monitoring for compliance via change_event

## Skip If (ANY kills it)

- A single dashboard the team already opens in Looker — agent overhead not justified
- Features requiring the UI only (some recommendations, brand-suitability controls)
- Smart Bidding interventions during the learning phase — threshold-based agents can sabotage learning
- Real-time intra-day decisions — conversion data lags 1-3 hours and stabilizes after ~3 days

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

- parent skill: `pro/marketing/ppc-manager/`
