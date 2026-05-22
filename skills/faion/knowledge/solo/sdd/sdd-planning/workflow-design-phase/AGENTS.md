---
slug: workflow-design-phase
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Step-by-step procedures for the SDD design phase: writing design documents (spec → AD-X → file table → data models → API contracts → testing strategy), writing implementation plans (context load → complexity analysis → work units → 100k rule → dependency graph → wave analysis), creating TASK_NNN.
content_id: "9ada230815e8b4d7"
tags: [sdd, workflow, design, planning]
---
# Workflow: Design Phase

## Summary

**One-sentence:** Step-by-step procedures for the SDD design phase: writing design documents (spec → AD-X → file table → data models → API contracts → testing strategy), writing implementation plans (context load → complexity analysis → work units → 100k rule → dependency graph → wave analysis), creating TASK_NNN.

**One-paragraph:** Step-by-step procedures for the SDD design phase: writing design documents (spec → AD-X → file table → data models → API contracts → testing strategy), writing implementation plans (context load → complexity analysis → work units → 100k rule → dependency graph → wave analysis), creating TASK_NNN.md files from the plan, and running parallelization analysis. Prerequisite: spec.md must be approved before starting.

## Applies If (ALL must hold)

- Approved spec.md exists and the feature needs a technical blueprint before coding starts.
- Choosing between 2+ architecture options with real trade-offs.
- Codebase has existing patterns that new work must follow — design phase surfaces them.
- Feature spans multiple services or data models requiring explicit data flow.

## Skip If (ANY kills it)

- Spec is still Draft or unapproved — design decisions will be based on shifting requirements.
- Tiny bugfixes or single-file changes where a full design doc adds zero value.
- Pure infrastructure changes (server config, CI tweaks) that do not affect application architecture.
- Greenfield spikes where the goal is learning, not committing to an approach.

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

- parent skill: `solo/sdd/sdd-planning/`
