---
slug: raci-matrix
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Assign one of four roles — Responsible (does the work), Accountable (single decision owner), Consulted (provides input), Informed (notified after) — to each role for each task or deliverable.
content_id: "61eafa56ea2ad28c"
tags: [raci, accountability, role-assignment, stakeholder-management, project-planning]
---
# RACI Matrix

## Summary

**One-sentence:** Assign one of four roles — Responsible (does the work), Accountable (single decision owner), Consulted (provides input), Informed (notified after) — to each role for each task or deliverable.

**One-paragraph:** Assign one of four roles — Responsible (does the work), Accountable (single decision owner), Consulted (provides input), Informed (notified after) — to each role for each task or deliverable. The rule: exactly one Accountable per task, no exceptions. Multiple Accountables collapse the escalation path and hide conflicts that only sponsors can resolve.

## Applies If (ALL must hold)

- New project kickoff with multiple roles (PM, dev lead, QA, DevOps, BA, sponsor) and recurring "who decides?" friction.
- Cross-team features where SDD task ownership is ambiguous (backend + frontend + data + ops).
- Vendor/contractor engagements: clarify what client owns vs what contractor delivers.
- Audit/compliance projects (SOC2, ISO 27001) requiring a named Accountable per control.
- Solopreneur engagements with designer, developer, and VA mix.

## Skip If (ANY kills it)

- One-person solo task with no external stakeholders — overhead with zero return.
- Pure agile teams with collective code ownership and one PO — RACI flattens to "PO=A, team=R" everywhere; use DACI for decisions instead.
- Highly emergent work where roles shift weekly — matrix decays faster than it is updated.

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
