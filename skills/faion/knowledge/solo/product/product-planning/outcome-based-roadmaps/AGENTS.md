---
slug: outcome-based-roadmaps
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An outcome-based roadmap replaces feature commitments with measurable metric targets as the unit of planning.
content_id: "7b806f2f25577504"
tags: [roadmap, outcome-driven, quarterly-planning, metric-focused, product-strategy]
---
# Outcome-Based Roadmaps

## Summary

**One-sentence:** An outcome-based roadmap replaces feature commitments with measurable metric targets as the unit of planning.

**One-paragraph:** An outcome-based roadmap replaces feature commitments with measurable metric targets as the unit of planning. Each quarterly slot carries a verb+metric+delta+timeframe outcome ("Reduce churn from 8% to 5% by Q2"), a list of candidate solutions marked "to-validate", and an explicit "not doing" list. Solutions are mutable mid-quarter; outcomes are frozen once set. This format keeps the roadmap valid across experiments and prevents stakeholders from treating it as a delivery contract.

## Applies If (ALL must hold)

- Quarterly planning where the best solution is still uncertain.
- Stakeholders conflate feature lists with contractual commitments.
- Discovery loop is active and the roadmap must survive the next experiment.
- Multiple teams or contractors need goal alignment without locking solutions.

## Skip If (ANY kills it)

- Contractually committed deliverables (RFPs, enterprise SLAs, regulatory deadlines)—use a timeline roadmap.
- Pure execution phase with fully scoped and validated work—use a sprint/release plan.
- No metrics pipeline; outcome roadmaps require trustworthy baselines to be meaningful.
- Pre-PMF zero-to-one stage where finding any user is the priority, not moving a metric.

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

- parent skill: `solo/product/product-planning/`
