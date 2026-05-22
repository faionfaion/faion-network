---
slug: competitive-intelligence
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Point-in-time competitor snapshots go stale within weeks.
content_id: "d67f5064b0d6f498"
tags: [competitive-intelligence, market-intelligence, battlecards, agents, ci-pipeline]
---
# Competitive Intelligence

## Summary

**One-sentence:** Point-in-time competitor snapshots go stale within weeks.

**One-paragraph:** Point-in-time competitor snapshots go stale within weeks. Continuous CI pipelines that separate mechanical collection (Haiku) from strategic synthesis (Opus) achieve 85-95% time reduction and measurably improve sales win rates. Battlecards older than 14 days with confident tone are worse than no battlecard.

## Applies If (ALL must hold)

- Live B2B/SaaS market where competitors ship weekly and pricing changes often.
- Sales team needs current battlecards (deal cycle > 30 days exposes stale data fast).
- Product roadmap decisions blocked on feature parity or differentiation gaps.
- Funding round, M&A, or executive hire signals need to surface within 24h.
- You already have 3+ named direct competitors plus stable URLs to track.

## Skip If (ANY kills it)

- Pre-PMF or category-creation phase—competitors are not the bottleneck, customer interviews are.
- Fewer than 5 known competitors—manual quarterly snapshot beats infrastructure overhead.
- Highly regulated/closed markets (defense, sealed bids) where public signals are noise.
- Personal projects with no GTM motion—output has no consumer.
- When the team will not act on alerts (CI without a sales/product action loop is theater).

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
