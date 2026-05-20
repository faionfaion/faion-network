---
slug: continuous-discovery-habits
tier: pro
group: product
domain: product-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Teresa Torres' framework: a product trio (PM + Design Lead + Tech Lead) runs weekly customer touchpoints and maps all signals into an Opportunity Solution Tree (OST).
content_id: "29f987d4a7c8494e"
tags: [discovery, product-trio, opportunity-solution-tree, torres, customer-research]
---
# Continuous Discovery Habits

## Summary

**One-sentence:** Teresa Torres' framework: a product trio (PM + Design Lead + Tech Lead) runs weekly customer touchpoints and maps all signals into an Opportunity Solution Tree (OST).

**One-paragraph:** Teresa Torres' framework: a product trio (PM + Design Lead + Tech Lead) runs weekly customer touchpoints and maps all signals into an Opportunity Solution Tree (OST). Every node is classified as outcome, opportunity, solution, or assumption test. Opportunities are scored on reach × frequency × severity × addressability. Selected opportunities spawn falsifiable assumption tests before any build. Discovery output traces to delivery via opp_id in SDD specs and PR titles.

## Applies If (ALL must hold)

- Active product with paying users where weekly discovery output must convert into roadmap moves
- Quarterly OKR cycle where each Outcome must trace to opportunities, then to assumption tests
- Backlog grooming: rejecting feature requests disguised as solutions and recasting as opportunities
- Roadmap negotiation where the OST provides a defensible structure for "why not feature X"
- Solo/small-team where agents fill discovery gaps by mining tickets, analytics, and sales calls
- Post-launch when shipped features aren't moving the Outcome — to diagnose the broken assumption

## Skip If (ANY kills it)

- Pre-PMF or zero-user products — no signal volume to support a weekly cadence; use customer-development or problem-validation first
- Crisis triage (active outage, churn cliff, security incident) — pause discovery, resume after
- Hardware / regulated medical / enterprise sales with 6–18 month cycles — adapt to monthly windows
- Stakeholder culture demanding validation from a single interview — pick a different framework
- Pure platform/infra teams whose users are other engineers — adapt with DX telemetry instead

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

- parent skill: `pro/product/product-planning/`
