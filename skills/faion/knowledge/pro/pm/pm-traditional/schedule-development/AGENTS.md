---
slug: schedule-development
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A process for converting WBS work packages into a sequenced, resourced, and buffered schedule with an identified critical path.
content_id: "36f8f509aada22dd"
tags: [project-management, scheduling, critical-path, cpm, pert]
---
# Schedule Development

## Summary

**One-sentence:** A process for converting WBS work packages into a sequenced, resourced, and buffered schedule with an identified critical path.

**One-paragraph:** A process for converting WBS work packages into a sequenced, resourced, and buffered schedule with an identified critical path. Use three-point estimation (PERT) for any activity over 5 days, explicit dependency types (FS/SS/FF/SF), and CCPM-style project and feeding buffers. Buffers must be visible and named — never hidden inside individual task estimates.

## Applies If (ALL must hold)

- Programs with hard external deadlines (regulatory, market, contractual) requiring critical-path defense.
- Multi-team or multi-vendor work with cross-team dependencies needing FS/SS/FF links.
- Fixed-bid proposals where the schedule baseline drives the price.
- Resource-constrained programs needing leveling and conflict detection.

## Skip If (ANY kills it)

- Pure-Scrum cadence with empowered PO — sprint plan replaces schedule.
- Continuous-flow or Kanban product teams.
- Projects shorter than 2 weeks — a checklist beats a Gantt.
- Discovery or R&D where activity duration is fundamentally unknowable.

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
