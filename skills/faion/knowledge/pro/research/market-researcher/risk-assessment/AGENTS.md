---
slug: risk-assessment
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Market-risk assessment identifies, scores, and mitigates demand, competition, pricing, trend, and channel risks before committing to a segment or pricing strategy.
content_id: "b423b8f400bec9a7"
tags: [risk-assessment, market-research, demand-risk, competitive-risk, pricing-risk]
---
# Risk Assessment (Market-Researcher Lens)

## Summary

**One-sentence:** Market-risk assessment identifies, scores, and mitigates demand, competition, pricing, trend, and channel risks before committing to a segment or pricing strategy.

**One-paragraph:** Market-risk assessment identifies, scores, and mitigates demand, competition, pricing, trend, and channel risks before committing to a segment or pricing strategy. Every risk row must cite a paragraph or table from an existing market research file — no row may rely on general knowledge. This ensures the register stays grounded in evidence and can be automatically validated.

## Applies If (ALL must hold)

- Pre-entry go/no-go on a new market segment when TAM/SAM/SOM exists but demand evidence is thin
- Pricing strategy decision: before locking a price point, score demand-elasticity and anchor-competitor risk
- Launch-readiness review for a positioning or category bet
- After a competitor raises a Series B or ships a copycat: re-score competitive-displacement and pricing-pressure rows
- Channel-dependence audit when more than 40% of pipeline comes from one channel
- Pivot evaluation: comparing two segment options requires a structured market-risk delta

## Skip If (ANY kills it)

- Pure technical, team, financial, or operational risk — use the generic `researcher/risk-assessment` variant or `pro/pm/pm-traditional/risk-management/`
- Idea stage with fewer than 5 problem interviews — demand-risk score is uncalibrated; run continuous discovery first
- B2B deals where risk is per-account, not per-market — use account-level deal-risk frameworks
- Solo side projects under $1k of committed spend — overhead exceeds expected loss

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
