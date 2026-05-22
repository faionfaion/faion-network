---
slug: market-research-tam-sam-som
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three nested market size calculations (TAM = total addressable, SAM = serviceable available, SOM = realistically obtainable) computed via three independent methods (top-down from reports, bottom-up from customer counts, competitor-based from revenue proxies) and triangulated.
content_id: "c5f8c78a7fe4875b"
tags: [market-sizing, tam-sam-som, market-research, sizing, revenue-forecasting]
---
# Market Research: TAM/SAM/SOM Triangulation

## Summary

**One-sentence:** Three nested market size calculations (TAM = total addressable, SAM = serviceable available, SOM = realistically obtainable) computed via three independent methods (top-down from reports, bottom-up from customer counts, competitor-based from revenue proxies) and triangulated.

**One-paragraph:** Three nested market size calculations (TAM = total addressable, SAM = serviceable available, SOM = realistically obtainable) computed via three independent methods (top-down from reports, bottom-up from customer counts, competitor-based from revenue proxies) and triangulated. Lock the ICP definition before any number is fetched. Round aggressively — two significant figures max. Express SOM as a customer count first, dollars second.

## Applies If (ALL must hold)

- Pre-spec phase: sanity check whether a niche clears a revenue floor (e.g. SOM > $1M ARR in 3 years).
- Pitch decks, investor memos, grant applications requiring a numerical market frame.
- Pricing or positioning decisions where segment economics matter (SAM × ARPU sets the envelope).
- Comparing two adjacent niches before committing to MVP scope.
- Annual roadmap review as market segment shifts (new geography, new tier, post-funding).

## Skip If (ANY kills it)

- Hobby projects, internal tools, free OSS — sizing adds zero signal.
- Replacement for actual customer interviews — TAM/SAM/SOM is not problem validation.
- Already-shipping products with real ARR — extrapolate from cohorts, not market reports.
- Two-sided marketplaces in pre-launch — supply/demand dynamics dominate raw market size.
- Deep-tech with a 10-year horizon — the market category may not exist yet.
- Regulated markets pre-license (medical, fintech) — addressable share depends on regulator decisions.

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

- parent skill: `pro/research/researcher/`
