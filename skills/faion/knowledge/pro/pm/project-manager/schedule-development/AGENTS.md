---
slug: schedule-development
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A deterministic process for building a project schedule from WBS work packages: define activities, sequence with dependency types (FS/FF/SS/SF), estimate durations using three-point PERT, run forward and backward pass to compute Early Start/Early Finish/Late Start/Late Finish per activity, identify the critical path (zero float), and place buffers at merge points and project end using Critical Chain methods rather than per-task padding.
content_id: "36f8f509aada22dd"
tags: [scheduling, critical-path, pert, cpm, critical-chain]
---
# Schedule Development

## Summary

**One-sentence:** A deterministic process for building a project schedule from WBS work packages: define activities, sequence with dependency types (FS/FF/SS/SF), estimate durations using three-point PERT, run forward and backward pass to compute Early Start/Early Finish/Late Start/Late Finish per activity, identify the critical path (zero float), and place buffers at merge points and project end using Critical Chain methods rather than per-task padding.

**One-paragraph:** A deterministic process for building a project schedule from WBS work packages: define activities, sequence with dependency types (FS/FF/SS/SF), estimate durations using three-point PERT, run forward and backward pass to compute Early Start/Early Finish/Late Start/Late Finish per activity, identify the critical path (zero float), and place buffers at merge points and project end using Critical Chain methods rather than per-task padding.

## Applies If (ALL must hold)

- Building the initial schedule from a WBS at kickoff (activity definition through CPM baseline)
- Re-baselining after a change-control event (scope add, vendor slip, milestone shift)
- Producing PERT three-point estimates for stakeholder communications
- Solopreneur weekly capacity planning across multiple parallel projects

## Skip If (ANY kills it)

- Pure agile teams with fixed-cadence sprints — velocity and roadmap replace CPM; critical path is overhead
- Highly creative / R&D work where activity duration is unknowable — use rolling-wave or Kanban instead
- Tasks under 2 weeks with a single owner — a checklist suffices
- Fixed-deadline projects where you back-plan from end date — use reverse-pass / time-boxed scope planning

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
