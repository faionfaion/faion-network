---
slug: competitive-intelligence-methods
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A two-sub-methodology bundle — competitor landscape mapping and competitive-intelligence feature analysis — run as a sequential pipeline: landscape first (2x2 positioning + whitespace identification across 15-20 competitors covering all four types), then feature-matrix drill-down (Y/P/N + 0-3 quality score with evidence URL per cell, gap-validation critic with forced skip budget).
content_id: "cfa4c3388aad196c"
tags: [competitive-intelligence, feature-matrix, competitor-landscape, gap-validation, market-research]
---
# Competitive Intelligence Methods

## Summary

**One-sentence:** A two-sub-methodology bundle — competitor landscape mapping and competitive-intelligence feature analysis — run as a sequential pipeline: landscape first (2x2 positioning + whitespace identification across 15-20 competitors covering all four types), then feature-matrix drill-down (Y/P/N + 0-3 quality score with evidence URL per cell, gap-validation critic with forced skip budget).

**One-paragraph:** A two-sub-methodology bundle — competitor landscape mapping and competitive-intelligence feature analysis — run as a sequential pipeline: landscape first (2x2 positioning + whitespace identification across 15-20 competitors covering all four types), then feature-matrix drill-down (Y/P/N + 0-3 quality score with evidence URL per cell, gap-validation critic with forced skip budget).

## Applies If (ALL must hold)

- Pre-MVP wedge selection: need the 2x2 + gap list before writing a spec.
- Quarterly competitive review: deltas in funding, pricing, positioning, hiring across top 15-20 competitors.
- New-feature go/no-go: deciding whether feature X is table-stakes, opportunity, or moat-building.
- Pricing repositioning: anchoring price tier on a fresh per-competitor pricing scrape.
- Pitch deck or investor update: defensible "competitive landscape" slide with sourced rows.

## Skip If (ANY kills it)

- Sub-week tactical decisions (single ad copy, single landing-page test) — matrices are too coarse.
- True greenfield with fewer than 3 competitors — feature matrix collapses to 1 column; use jobs-to-be-done.
- Highly regulated B2B (defense, banking core) where competitor data is private and any public pull is misleading.
- Late-stage scaling where customer-success and retention data dominate — feature matrix produces feature-bloat backlog.
- After product-market fit — optimizing on feature matrix is how startups become "Salesforce-but-cheaper" forever.

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
