---
slug: schedule-development
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Deterministic CPM scheduling from WBS: define activities, sequence with FS/FF/SS/SF, PERT-estimate, forward+backward pass, identify critical + near-critical paths, Critical-Chain buffers.
content_id: "22d0aedf00ba48d2"
complexity: deep
produces: spec
est_tokens: 4700
tags: [scheduling, critical-path, pert, cpm, critical-chain]
---
# Schedule Development

## Summary

**One-sentence:** Deterministic CPM scheduling from WBS: define activities, sequence with FS/FF/SS/SF, PERT-estimate, forward+backward pass, identify critical + near-critical paths, Critical-Chain buffers.

**One-paragraph:** Deterministic process: define activities (verb+noun, 3-7 per WBS work package), sequence with explicit dependency types (FS default; SS/FF/SF justified), three-point PERT estimation, run forward and backward pass for ES/EF/LS/LF, identify critical path (float=0) AND near-critical paths (float<2 days), place buffers at merge points and project end via Critical Chain (Goldratt) rather than per-task padding. Effort hours are not duration days; model resource availability explicitly. Use business-calendar libraries for date math.

**Ефективно для:**

- Building initial schedule from a WBS at kickoff
- Re-baselining after an approved change-control event
- Producing PERT three-point estimates for stakeholder communications
- Solopreneur weekly capacity planning across parallel projects

## Applies If (ALL must hold)

- Building the initial schedule from a WBS at kickoff
- Re-baselining after a change-control event
- Producing PERT three-point estimates for stakeholder communications
- Solopreneur weekly capacity planning across multiple parallel projects

## Skip If (ANY kills it)

- Pure agile teams with fixed-cadence sprints — velocity and roadmap replace CPM
- Highly creative / R&D work where activity duration is unknowable
- Tasks under 2 weeks with a single owner — a checklist suffices
- Fixed-deadline projects where you back-plan from end date — use reverse-pass

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| WBS work packages | YAML | scope baseline |
| Dependencies | YAML | predecessor edges with type + lag |
| Calendars | YAML | working days, holidays per resource |
| Effort estimates | YAML | three-point per activity |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | WBS work packages feed the activity list |
| [[resource-management]] | Effective capacity feeds duration computation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: fs-by-default, track-near-critical-paths, lock-baseline, effort-not-duration, explicit-predecessors | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-activities` | sonnet | Verb+noun naming from WBS |
| `compute-cpm` | haiku | Pure DAG arithmetic in script |
| `monte-carlo` | haiku | N=10000 simulation in script over PERT triples |

## Templates

| File | Purpose |
|------|---------|
| `templates/activity-list.md` | Activity table with ID, duration, dependencies, and resource columns |
| `templates/dependencies.yaml` | Predecessor edges with type (FS/FF/SS/SF) + lag |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/critical-path.py` | CPM forward/backward pass using networkx; validates DAG, computes ES/EF/LS/LF and float | On schedule baseline or rebaseline |
| `scripts/validate-schedule-development.py` | Validate schedule invariants (DAG, business calendar, near-critical surfaced) | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[resource-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
