---
slug: schedule-development
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Convert WBS work packages into a sequenced, resourced, buffered schedule with critical path identified via CPM, PERT estimates, and CCPM-style visible buffers.
content_id: "22d0aedf00ba48d2"
complexity: medium
produces: spec
est_tokens: 4200
tags: [schedule, critical-path, cpm, pert, ccpm]
---
# Schedule Development

## Summary

**One-sentence:** Convert WBS work packages into a sequenced, resourced, buffered schedule with critical path identified via CPM, PERT estimates, and CCPM-style visible buffers.

**One-paragraph:** Schedule development takes the WBS and produces a network of verb-led activities with explicit FS/SS/FF/SF dependencies, three-point (PERT) estimates for activities over 5 days, named resources, and CCPM-style buffers held visible at project and feeding-chain level. Critical-path analysis identifies the longest dependency chain; buffer health is monitored weekly. Schedules not refreshed weekly stop reflecting reality and silently mislead the team.

**Ефективно для:**

- Programmes with hard external deadlines needing critical-path defence.
- Multi-team work with cross-team dependencies needing FS/SS/FF links.
- Fixed-bid proposals where the schedule baseline drives the price.
- Resource-constrained programmes needing levelling and conflict detection.

## Applies If (ALL must hold)

- Hard external deadline (regulatory / market / contractual) anchors the work.
- Multi-team or multi-vendor dependencies need explicit FS/SS/FF links.
- Fixed-bid or fixed-scope contract requires a defended schedule baseline.
- Resource-constrained programme needs levelling + buffer monitoring.

## Skip If (ANY kills it)

- Pure-Scrum cadence with empowered PO — sprint plan replaces schedule.
- Continuous-flow / Kanban product team.
- Project shorter than 2 weeks — checklist beats Gantt.
- Discovery / R&D where duration is fundamentally unknowable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| WBS work packages | outline + dictionary | wbs-creation |
| Resource calendar | spreadsheet / planner export | resource-management |
| Holiday/leave roster | ICS / table | HR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `wbs-creation` | Provides the work packages that become activities. |
| `scope-management` | Locks scope so schedule is not redone every change. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — verb-led activities, dependency types, PERT thresholds, visible buffers, weekly refresh | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for activity-list artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns — single-point estimates, hidden padding, stale critical path, ignored resource conflicts | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: define → sequence → estimate → resource → buffer → refresh | 900 |
| `content/05-examples.xml` | optional | Worked activity-list snippet with critical path highlighted | 600 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping schedule state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `convert-wbs-to-activities` | sonnet | Verb conversion + decomposition judgment. |
| `pert-estimates` | sonnet | Three-point reasoning per activity. |
| `compute-critical-path` | haiku | Deterministic topological computation. |
| `buffer-sizing` | opus | Cross-chain reasoning + variance synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/activity-list.md` | Activity list template with PERT + dependency columns. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-schedule-development.py` | Schema-validate the activity-list JSON artefact. | Pre-commit + before baseline lock. |
| `scripts/cpm.py` | Compute critical path from activity-list CSV. | On schedule change. |

## Related

- [[wbs-creation]]
- [[scope-management]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the schedule-development input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
