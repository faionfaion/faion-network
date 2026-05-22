---
slug: decision-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A six-step structured evaluation framework: define decision, generate options, elicit weights individually then reconcile, route scoring by expertise, run sensitivity analysis, document with traceability.
content_id: "540833b2f15e6888"
tags: [decision-analysis, business-analysis, evaluation, selection, requirements-traceability]
---
# Decision Analysis

## Summary

**One-sentence:** A six-step structured evaluation framework: define decision, generate options, elicit weights individually then reconcile, route scoring by expertise, run sensitivity analysis, document with traceability.

**One-paragraph:** A six-step structured evaluation framework: define decision, generate options, elicit weights individually then reconcile, route scoring by expertise, run sensitivity analysis, document with traceability.

## Applies If (ALL must hold)

- Enterprise vendor/platform/package selection (CRM, ERP, ITSM, IdP) with 3+ candidates and 5-7 stakeholder groups.
- Build-vs-buy-vs-extend evaluations where Finance, Architecture, Security, and Operations each weight criteria differently.
- Approval-gate decisions in regulated environments (banking, healthcare, gov) where auditors require documented rationale.
- Investment/portfolio prioritization where the same matrix template is reused across N initiatives.
- Solution evaluation at the end of a BA cycle (BABOK KA 7) comparing candidates against elicited requirements.
- Steering committee deadlock where members are arguing intuitions rather than criteria.

## Skip If (ANY kills it)

- Decisions inside one team's autonomy (npm package choice, CI runner version) — use a 5-line ADR.
- Pure financial decisions with quantifiable cash flows — use NPV/IRR/payback, not 1-5 scoring.
- Strategic direction questions ("should we enter market X?") — use scenario planning / BABOK KA 6 strategy analysis.
- When the decision-maker has already decided and asked the BA for cover — a retrofitted matrix is theater.
- Early discovery with high uncertainty — lock weights too early creates false rigor; use opportunity-solution trees.

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

- parent skill: `pro/ba/business-analyst/`
