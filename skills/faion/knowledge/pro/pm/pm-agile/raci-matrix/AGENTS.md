---
slug: raci-matrix
tier: pro
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A RACI matrix assigns exactly one of four roles — Responsible, Accountable, Consulted, Informed — to each stakeholder for each task or deliverable.
content_id: "61eafa56ea2ad28c"
tags: [raci-matrix, accountability, stakeholder-management, cross-functional, ownership]
---
# RACI Matrix

## Summary

**One-sentence:** A RACI matrix assigns exactly one of four roles — Responsible, Accountable, Consulted, Informed — to each stakeholder for each task or deliverable.

**One-paragraph:** A RACI matrix assigns exactly one of four roles — Responsible, Accountable, Consulted, Informed — to each stakeholder for each task or deliverable. The single testable rule: every task row must have exactly one Accountable and at least one Responsible. Multiple Accountables on a single task is the most common failure mode and re-creates the "no clear owner" problem the matrix was designed to solve.

## Applies If (ALL must hold)

- Multi-role projects with more than 3 roles and more than 10 deliverables.
- Solopreneur engagements with contractors or agencies where one human plus outsourced parties need clear per-task ownership.
- Onboarding a new hire or contractor — encodes "who owns what" in one readable table.
- Pre-mortem or kickoff for cross-functional features (PM + Eng + Design + QA + DevOps) before sprint zero.
- Incident response retros where "no one owned X" was a root cause — bake the new RACI into the runbook.

## Skip If (ANY kills it)

- Solo work with no external collaborators — overhead with zero return.
- Self-organizing Scrum teams where Definition of Done plus collective code ownership already covers accountability — RACI can undermine team agency.
- Hyper-dynamic discovery work where tasks change weekly — the matrix goes stale faster than it can be maintained.
- Senior autonomous teams operating under DACI, Advice Process, or RAPID — those frameworks fit decision rights better.

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
