---
slug: data-driven-requirements
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Apply data analytics to requirements engineering.
content_id: "b45eb25f7aa0f50e"
tags: [data-driven, analytics, requirements, evidence-based, metrics]
---
# Data-Driven Requirements Engineering

## Summary

**One-sentence:** Apply data analytics to requirements engineering.

**One-paragraph:** Apply data analytics to requirements engineering. Use evidence-based approaches to prioritization and validation. This is the BA-core variant covering fundamentals; deeper metric-layer and A/B-power material lives in the business-analyst sibling.

## Applies If (ALL must hold)

- The team has at least one production system emitting structured events for 90+ days, and someone can already pull a baseline number from it.
- Stakeholders disagree on priority and the disagreement is resolvable by a metric (usage, revenue, error rate).
- A requirement under discussion has a measurable current state and a plausibly measurable target.
- Recurring rework or post-launch "we shipped the wrong thing" is attributed to opinion-based prioritization.
- BA is being asked for evidence by a finance/risk/steerco audience.

## Skip If (ANY kills it)

- Pre-product or pre-launch with no users — any "data" will be a vanity sample; use qualitative discovery instead.
- The org has zero data infrastructure: no event tracking, no warehouse, no BI — build the minimum infra first before claiming the practice.
- One-off compliance/legal/contractual requirements where the answer is "must, by date X."
- Pure UX/brand/accessibility floor work where the metric is downstream perception.
- Two-day decisions where running a baseline query costs more than shipping and reverting.
- Teams that won't agree on a single metric definition.

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

- parent skill: `pro/ba/ba-core/`
