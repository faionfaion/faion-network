---
slug: business-model-research
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Business model research at the market-researcher level produces a peer-benchmark table — not a single canvas.
content_id: "243577a9242ec7d2"
tags: [business-model, benchmarking, revenue-archetypes, market-research, comp-analysis]
---
# Business Model Research (Market-Researcher Lens)

## Summary

**One-sentence:** Business model research at the market-researcher level produces a peer-benchmark table — not a single canvas.

**One-paragraph:** Business model research at the market-researcher level produces a peer-benchmark table — not a single canvas. The methodology classifies 8-15 comparables (including failed and acquihired peers) into five revenue archetypes (subscription, one-time, transaction, advertising, marketplace), extracts P25/P50/P75 distributions for ARPU, gross margin, gross logo retention, NDR, and CAC payback, then overlays the founder's plan against the distribution. The core rule: always include at least 2 dead or acquihired comparables — without them, medians overstate viability by 20-40%.

## Applies If (ALL must hold)

- Pre-spec market-side answer to "what model do peers in this category actually use?"
- Investor or board memo: produce an industry revenue-model distribution by archetype
- Pricing committee input: pull ARPU, gross margin, NDR, and rule-of-40 from a public-comp set
- Category entry decision: rank 5-15 candidate categories by median LTV:CAC and CAC payback
- M&A scoping: build a comps table mapping the target's model to nearest public proxy
- Cross-checking a researcher-mode canvas — verify the founder's chosen archetype against industry base rates

## Skip If (ANY kills it)

- Single-product canvas and unit-economics design — that is the researcher/business-model-research sibling's scope
- Markets with fewer than 3 public or well-documented private comparables — table is statistically meaningless
- Hyper-local services where public comps do not transfer — use local-market survey instead
- Pre-revenue categories with no precedent — peer benchmarking is misleading; use analogous-markets or first-principles-pricing
- Regulated verticals where revenue model is dictated by law — research the regulation, not the comps

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
