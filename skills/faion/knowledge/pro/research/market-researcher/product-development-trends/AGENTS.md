---
slug: product-development-trends
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A market-side trend brief that produces TAM/pricing/positioning implications from a scored signal set.
content_id: "35a8a51de6541961"
tags: [market-trends, competitive-intelligence, signal-scoring, market-implications, trend-research]
---
# Product Development Trends (Market-Side Brief)

## Summary

**One-sentence:** A market-side trend brief that produces TAM/pricing/positioning implications from a scored signal set.

**One-paragraph:** A market-side trend brief that produces TAM/pricing/positioning implications from a scored signal set. A three-stage pipeline (wide signal collection → scored synthesis → human checkpoint) writes a dated trend-report.md and a signals.jsonl audit trail so next-quarter runs diff rather than re-scrape.

## Applies If (ALL must hold)

- Quarterly market-trend refresh feeding GTM positioning, pricing tier design, or category framing
- Pre-investment decision: separating hype from durable adoption before budget is committed
- When competitive intel uncovers a methodology shift and you need to decide whether to follow or counter-position
- Annual board memo where the market lens (TAM expansion, sub-segment emergence, pricing-power shifts) is the deliverable
- Inside faion-research-agent mode=market when the team explicitly asks for a "what's changing" overlay

## Skip If (ANY kills it)

- Product roadmap or sprint planning — use researcher/product-development-trends or pm-agile
- Pure pricing benchmark — use market-researcher/pricing-research
- Single-feature validation — use user-researcher/problem-validation or continuous-discovery
- Competitive tear-down of one named rival — use competitor-analysis and competitive-intelligence
- Less than 90 days since the last trends pass with no triggering event (funding round, regulatory shift, major launch)

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
