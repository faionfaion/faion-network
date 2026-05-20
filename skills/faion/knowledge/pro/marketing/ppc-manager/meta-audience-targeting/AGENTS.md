---
slug: meta-audience-targeting
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Meta audience construction: demographics, interests, custom audiences (pixel/CRM/engagement), lookalikes, exclusions, reach estimation.
content_id: "1c76070a6845a8c9"
tags: [meta-audiences, targeting-api, custom-audiences, lookalike-audiences, audience-exclusion]
---
# Meta Audience Targeting: Demographics, Interests, Custom Audiences, and Lookalikes

## Summary

**One-sentence:** Meta audience construction: demographics, interests, custom audiences (pixel/CRM/engagement), lookalikes, exclusions, reach estimation.

**One-paragraph:** Meta audience construction: demographics, interests, custom audiences (pixel/CRM/engagement), lookalikes, exclusions, reach estimation. Core rule: exclude recent purchasers from prospecting.

## Applies If (ALL must hold)

- Building or auditing any Meta ad set audience via the Marketing API
- Creating custom audiences from pixel events, customer lists, or engagement sources
- Generating lookalike audiences from a qualified source audience
- Constructing full-funnel audience stacks (cold → warm → hot)
- Estimating reach before launching using the `reachestimate` endpoint
- Setting up Special Ad Category campaigns (housing, credit, employment) with restricted targeting

## Skip If (ANY kills it)

- Campaign or ad set creation structure — use `ads-meta-campaign-setup` for the full three-tier setup
- Budget allocation across audiences — use `ads-budget-optimization`
- Instagram-specific placement targeting — use `instagram-ads` for placement-level API details
- Audience analysis or reporting post-launch — this covers construction only

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
