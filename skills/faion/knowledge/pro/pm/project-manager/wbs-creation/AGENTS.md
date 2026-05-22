---
slug: wbs-creation
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule.
content_id: "a8221dfd16c637b7"
tags: [wbs, scope, decomposition, 100-rule, dictionary]
---
# WBS Creation

## Summary

**One-sentence:** Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule.

**One-paragraph:** Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule. Each node in the tree is a noun (an output), not a verb (an activity). The lowest level items — work packages — are estimable (8-80 hours), assignable to one owner, and have explicit acceptance criteria documented in a WBS Dictionary.

## Applies If (ALL must hold)

- Predictive/waterfall projects with fixed scope at kickoff (agency contracts, ERP rollouts, hardware launches)
- Hybrid delivery: WBS at program level, sprints underneath each work package
- Cost-loaded schedules and EVM tracking — WBS is the spine for cost accounts
- Migration projects (data, system, vendor) where every artefact must be enumerated
- Compliance projects (SOC2, HIPAA, ISO 27001) where 100% rule maps to control coverage

## Skip If (ANY kills it)

- Pure-agile teams driven by a product backlog — WBS calcifies what should flex
- Discovery / R&D where deliverables are emergent — use a hypothesis backlog instead
- Fast-moving startup product work where scope changes weekly — overhead exceeds value
- Solo work on a feature under 2 weeks — a checklist beats a WBS

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
