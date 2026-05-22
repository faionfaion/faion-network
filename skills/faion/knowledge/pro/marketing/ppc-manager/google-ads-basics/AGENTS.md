---
slug: google-ads-basics
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OAuth 2.
content_id: "83f18ccf24d0e2e1"
tags: [google-ads-api, authentication, account-hierarchy, python-client, oauth]
---
# Google Ads API — Basics

## Summary

**One-sentence:** OAuth 2.

**One-paragraph:** OAuth 2.0 + developer token auth, account hierarchy (MCC → Customer → Campaign → Ad Group), GAQL queries, and credential storage best practices.

## Applies If (ALL must hold)

- Authenticating a Python app to the Google Ads API for the first time
- Setting up google-ads.yaml or dict-based credentials
- Querying the account hierarchy or listing campaigns with metrics
- Updating campaign status (ENABLED, PAUSED, REMOVED)

## Skip If (ANY kills it)

- Search, Display, Shopping, or PMax campaign creation — use the campaign-type-specific methodologies
- Conversion tracking setup — use ads-conversion-tracking methodology
- Reporting and automation — use google-ads-reporting methodology
- Single-account hobby spend under $500/month — Google Ads UI plus auto-rules is cheaper than building API plumbing
- One-off creative/copy decisions where human judgement dominates and there is no batching benefit
- Smart Bidding tuning during 2-3 week learning phase — let the algorithm finish before agents nudge bids
- Anything needing developer-token Standard Access if you only have Test or Basic — apply for upgrade first

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
