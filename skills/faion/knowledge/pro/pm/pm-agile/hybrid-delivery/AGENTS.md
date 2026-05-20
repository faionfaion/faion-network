---
slug: hybrid-delivery
tier: pro
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A delivery model that combines predictive (waterfall/stage-gate) and agile methods within a single program, assigning each by component risk profile.
content_id: "9023d6bf3361c079"
tags: [hybrid, delivery-model, waterfall, agile, enterprise-delivery]
---
# Hybrid Delivery

## Summary

**One-sentence:** A delivery model that combines predictive (waterfall/stage-gate) and agile methods within a single program, assigning each by component risk profile.

**One-paragraph:** A delivery model that combines predictive (waterfall/stage-gate) and agile methods within a single program, assigning each by component risk profile. The canonical pattern: use predictive for planning, contracting, regulatory submissions, and hardware; use agile for software execution, testing, and iteration. Pure agile and pure waterfall each fail in mixed-reality programs. Hardware/software products need physical milestones alongside iterative firmware; regulated industries need gate evidence alongside fast cycles; enterprise portfolios need quarterly budget cycles alongside two-week sprints. Hybrid is not a compromise — it is an explicit, architected two-cadence model with a defined translation layer between them.

## Applies If (ALL must hold)

- Programs with hardware and software components (medical device, automotive, IoT).
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates and V-model evidence.
- Enterprise transformation rollouts: portfolio level uses milestones, delivery teams use Scrum/Kanban.
- Vendor plus internal team mixes where vendor work is fixed-bid (predictive) and internal is iterative.
- Cloud platforms running DevOps + Agile for delivery while ops/finance/security gate quarterly.

## Skip If (ANY kills it)

- Pure software product team with autonomous backlog and no compliance — full Scrum or Kanban is simpler.
- Startup with fewer than 10 people — ceremony overhead exceeds coordination value.
- Pure fixed-scope construction build where iteration adds risk without value — stay predictive.
- "We do hybrid" with no explicit written boundary — that is incoherence, not a method.

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

- parent skill: `pro/pm/pm-agile/`
