---
slug: ba-planning
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: BABOK Knowledge Area 1 defines the five seeding tasks that govern all BA work: plan BA approach, plan stakeholder engagement, plan BA governance, plan BA information management, and identify BA performance improvements.
content_id: "4442ac0007c37656"
tags: [ba, babok, planning, governance, monitoring]
---
# Business Analysis Planning

## Summary

**One-sentence:** BABOK Knowledge Area 1 defines the five seeding tasks that govern all BA work: plan BA approach, plan stakeholder engagement, plan BA governance, plan BA information management, and identify BA performance improvements.

**One-paragraph:** BABOK Knowledge Area 1 defines the five seeding tasks that govern all BA work: plan BA approach, plan stakeholder engagement, plan BA governance, plan BA information management, and identify BA performance improvements. Each task produces one artifact with its own approver, cadence, and lifecycle. Without KA1, downstream methodologies (stakeholder-analysis, ba-governance, requirements-lifecycle, elicitation-techniques) use inconsistent assumptions and produce incoherent outputs.

## Applies If (ALL must hold)

- A new initiative crosses from discovery to planned delivery and needs an explicit BA approach, stakeholder map, governance, information management, and performance plan.
- Programs that must demonstrate BABOK conformance to certifying bodies or internal QA (CCBA/CBAP audits, IIBA-aligned PMOs).
- Hybrid plan-driven + change-driven engagements where per-task baselined vs. living artifact declarations are needed.
- Activating sibling ba-core methodologies — KA1 is their prerequisite seeding ceremony.
- When introducing BA performance metrics (rework rate, requirement defect density, elicitation throughput).

## Skip If (ANY kills it)

- Solo MVP, prototype, or research spike — five KA1 tasks are heavier than the work itself; use a one-page lean canvas.
- Pure backlog-driven Scrum where the Definition of Ready already encodes the BA approach.
- Continuous-discovery contexts where requirements churn weekly — KA1 baselines go stale faster than they can be reviewed.
- When the sponsor will not name a governance approver — without one, KA1 governance becomes decorative.

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
