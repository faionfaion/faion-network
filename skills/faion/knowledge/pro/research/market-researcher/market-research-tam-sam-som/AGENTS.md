---
slug: market-research-tam-sam-som
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: TAM/SAM/SOM sizing quantifies market opportunity through three nested estimates using top-down, bottom-up, and competitor-based methods.
content_id: "c5f8c78a7fe4875b"
tags: [market-sizing, tam-sam-som, market-research, investor-pitch, gating]
---
# Market Research — TAM/SAM/SOM

## Summary

**One-sentence:** TAM/SAM/SOM sizing quantifies market opportunity through three nested estimates using top-down, bottom-up, and competitor-based methods.

**One-paragraph:** TAM/SAM/SOM sizing quantifies market opportunity through three nested estimates using top-down, bottom-up, and competitor-based methods. The core rule: always triangulate with both top-down and bottom-up; if the two diverge more than 2x, flag it as a research gap rather than averaging the numbers. The market-researcher lens produces three audience-specific cuts from the same canonical base: an investor cut, a GTM cut, and a pricing cut.

## Applies If (ALL must hold)

- Seed/Series-A pitch deck market slide needs three numbers, three sources, one chart
- GTM segmentation kickoff: SAM split per channel so the marketer can allocate CAC budget
- Pricing-tier sizing: each tier needs its own ARPU × addressable-count math
- Re-sizing after a pivot, geography expansion, or new pricing page
- Board update comparing SOM-actual vs. SOM-plan for the trailing quarter

## Skip If (ANY kills it)

- Hobby projects, internal tooling, free OSS — investor audience absent, sizing is theatre
- Two-sided marketplaces pre-launch — supply liquidity dominates raw market size
- Replacement for win/loss interviews — TAM/SAM/SOM does not explain why deals close
- Already-shipping products where bottom-up cohort revenue forecasts are stronger
- Solo freemium-with-no-paid-plan — SAM × ARPU collapses to zero

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

- parent skill: `pro/research/market-researcher/`
