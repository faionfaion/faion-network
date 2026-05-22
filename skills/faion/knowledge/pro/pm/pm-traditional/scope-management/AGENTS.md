---
slug: scope-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Scope management defines, documents, and controls what a project will and will not deliver.
content_id: "3c7f123565e99e04"
tags: [scope, requirements, change-control, scope-creep, acceptance-criteria]
---
# Scope Management

## Summary

**One-sentence:** Scope management defines, documents, and controls what a project will and will not deliver.

**One-paragraph:** Scope management defines, documents, and controls what a project will and will not deliver. It requires a written scope statement with explicit exclusions, a signed scope baseline, and a formal change-control gate — so every addition is evaluated for cost and schedule impact before it enters the project.

## Applies If (ALL must hold)

- Fixed-price or fixed-scope contracts where scope creep damages margin.
- Regulated programs (medical, finance, government) where scope is part of compliance evidence.
- Multi-vendor programs where contracted scope per vendor must compose into one deliverable.
- Strategic transformations (ERP, CRM, cloud migration) needing formal scope statement + WBS + validated deliverables.
- Projects showing scope creep symptoms: repeated re-baselining, "while you're in there" requests, confused acceptance criteria.

## Skip If (ANY kills it)

- Pre-PMF startups iterating on hypotheses — strict scope control kills learning.
- Internal R&D or discovery sprints — locking scope before learning is anti-pattern.
- Pure agile teams with continuous discovery — backlog refinement replaces scope statements.
- One-person side projects — scope statement is overhead.
- When the root problem is unclear requirements or absent stakeholders; fix those first.

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

- parent skill: `pro/pm/pm-traditional/`
