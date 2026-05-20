---
slug: hybrid-delivery
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Hybrid delivery is a framework for programs that combine predictive (waterfall) and agile delivery modes when neither alone fits.
content_id: "9023d6bf3361c079"
tags: [hybrid, agile, waterfall, program-management, governance]
---
# Hybrid Delivery: Combining Predictive and Agile Approaches

## Summary

**One-sentence:** Hybrid delivery is a framework for programs that combine predictive (waterfall) and agile delivery modes when neither alone fits.

**One-paragraph:** Hybrid delivery is a framework for programs that combine predictive (waterfall) and agile delivery modes when neither alone fits. The boundary between modes is defined explicitly in a program.yaml work-graph: top-level milestones (predictive arm) decompose into epics, which decompose into team backlogs (agile arm). Both arms use their own vocabulary and rituals; a translation layer converts between them for steering-committee reporting.

## Applies If (ALL must hold)

- Programs with hardware + software components where physical-world milestones are predictive and digital iteration is agile.
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates on top of agile execution.
- Enterprise transformation rollouts: portfolio-level milestones and budget cycles with Scrum/Kanban delivery teams.
- Vendor + internal team mixes where vendor contracts are fixed-bid and internal teams iterate.
- DevOps + Agile delivery with monthly/quarterly ops/finance/security governance reviews.

## Skip If (ANY kills it)

- Pure software-only product teams with autonomous backlog and no compliance gates — full Scrum or Kanban is simpler.
- Tiny teams (under 10) where ceremony overhead exceeds coordination value — pick one mode.
- Pure fixed-scope delivery where iteration adds risk without value — stay predictive.
- "We do hybrid" without explicit boundaries — that is incoherence, not hybrid; refuse and force a real method choice.

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

- parent skill: `pro/pm/project-manager/`
