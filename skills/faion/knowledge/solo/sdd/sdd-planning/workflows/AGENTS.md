---
slug: workflows
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Navigation hub for the three-phase SDD lifecycle: Spec Phase (requirements) → Design Phase (technical blueprint) → Execution Phase (implementation).
content_id: "5855a9b1517a6537"
tags: [sdd, workflows, lifecycle, navigation, phase-map]
---
# SDD Workflows Navigation Hub

## Summary

**One-sentence:** Navigation hub for the three-phase SDD lifecycle: Spec Phase (requirements) → Design Phase (technical blueprint) → Execution Phase (implementation).

**One-paragraph:** Navigation hub for the three-phase SDD lifecycle: Spec Phase (requirements) → Design Phase (technical blueprint) → Execution Phase (implementation). Provides phase-by-phase input/output tables, a complete workflow path, and links to the detailed phase files. This file routes; it does not instruct.

## Applies If (ALL must hold)

- Starting work on a feature without knowing which SDD phase is active
- Bootstrapping a new project: constitution through first execution
- Switching phases mid-feature (spec approved, starting design)
- Explaining the SDD system to a new agent or contributor

## Skip If (ANY kills it)

- Already in a specific phase and know what to do — go directly to the phase file
- As a substitute for phase-specific workflow files: this file is navigation, not instructions
- Looking for document templates — those live in template-spec, template-design, template-task

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
