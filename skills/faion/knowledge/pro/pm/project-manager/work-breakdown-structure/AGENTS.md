---
slug: work-breakdown-structure
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A deliverable-oriented hierarchical decomposition of project scope into work packages — noun-based nodes (outputs), not verbs (activities).
content_id: "c3bcfc94a7e4ecc3"
tags: [wbs, scope, project-planning, deliverables, estimation]
---
# Work Breakdown Structure

## Summary

**One-sentence:** A deliverable-oriented hierarchical decomposition of project scope into work packages — noun-based nodes (outputs), not verbs (activities).

**One-paragraph:** A deliverable-oriented hierarchical decomposition of project scope into work packages — noun-based nodes (outputs), not verbs (activities). Each level represents 100% of its parent (100% rule). Leaf nodes (work packages) satisfy the 8-80 hour rule and carry a Dictionary entry with acceptance criteria, owner, and dependencies. The WBS is the scope baseline; schedule and cost are derived from it, not contained in it.

## Applies If (ALL must hold)

- Translating an approved scope statement or SOW into an estimable, assignable work-package tree before scheduling and costing
- Bidding on fixed-scope work requiring bottom-up estimation
- Validating the 100% rule on a hand-drafted plan: diff WBS against scope statement
- Re-baselining after a change request — mutate only the affected branch

## Skip If (ANY kills it)

- Pure Scrum or Kanban teams where the product backlog is the decomposition — an extra WBS creates two sources of truth
- Discovery or research projects where less than 30% of scope is known — the WBS below level 2 will be fabricated
- Solo work on a feature under 2 weeks — a checklist is simpler
- Projects with emergent deliverables (innovation, R&D, platform exploration) — use rolling-wave planning instead

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
