---
slug: impl-plan-components
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structural reference for implementation-plan.
content_id: "6223ae20abbbac12"
tags: [implementation-plan, structure, wave-analysis, task-decomposition, dependency-graph]
---
# Implementation Plan Components

## Summary

**One-sentence:** Structural reference for implementation-plan.

**One-paragraph:** Structural reference for implementation-plan.md sections: prerequisites, dependency graph, wave analysis, critical path, task breakdown, risk assessment, and rollout.

## Applies If (ALL must hold)

- Writing or reviewing an implementation-plan.md — as the structural reference.
- Validating a generated plan against the canonical component list before marking it Draft.
- Adapting the template to a specific project type (API-only, frontend-only, full-stack).
- Onboarding an executor agent: wave analysis and dependency graph define the scheduling contract.

## Skip If (ANY kills it)

- As a substitute for writing-implementation-plans/ — that file explains the methodology (100k rule, INVEST, wave algorithm); this file shows the structural components.
- When the plan is already written and approved — this is authoring guidance, not execution guidance.

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
