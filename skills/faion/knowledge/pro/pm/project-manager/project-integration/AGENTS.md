---
slug: project-integration
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The PM acts as integrator across all knowledge areas (scope, schedule, cost, quality, risk, resources, communications, procurement) through a single version-controlled integrated plan.
content_id: "e52338361d3020d7"
tags: [integration-management, change-control, project-charter, cross-functional, status-tracking]
---
# Project Integration Management

## Summary

**One-sentence:** The PM acts as integrator across all knowledge areas (scope, schedule, cost, quality, risk, resources, communications, procurement) through a single version-controlled integrated plan.

**One-paragraph:** The PM acts as integrator across all knowledge areas (scope, schedule, cost, quality, risk, resources, communications, procurement) through a single version-controlled integrated plan. Every change request triggers cross-area impact analysis before approval; status colour is derived from numeric thresholds, not PM narrative; and closure is treated as integration's last mile — formal acceptance plus lessons learned plus archive.

## Applies If (ALL must hold)

- Programs with 2+ workstreams whose decisions interact (scope vs. schedule vs. cost vs. vendor).
- Initiation phase: drafting the project charter to authorize work and bind sponsor commitment.
- Change-heavy environments where every CR has cross-area impact simultaneously.
- Multi-team or multi-vendor delivery where local optimization harms whole-system performance.
- Project closure: final integration, lessons learned, formal acceptance, contract closeout.

## Skip If (ANY kills it)

- Single-team, single-stream work with a stable backlog — Scrum or Kanban already integrates within the team.
- Short tactical engagements under 4 weeks with no inter-area trade-offs — overhead exceeds value.
- Pure research or discovery phases with no committed scope — wait until charter signal is real.
- Solo-developer projects — keep artifacts lightweight (one-page charter, weekly check); the integrator is one person.

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
