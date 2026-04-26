# Implementation Plan Components

## Summary

Structural reference for every section an `implementation-plan.md` must contain: prerequisites,
dependency graph, wave analysis (tasks grouped by dependency level for parallel execution),
phase breakdown, per-task entries with INVEST validation, critical path, risk assessment,
testing plan, and rollout strategy. Defines what each section must contain and shows worked examples.

## Why

Implementation plans without a dependency graph and wave analysis produce sequential execution
where parallel work was possible, and executor agents discover missing dependencies at runtime.
The wave analysis table is the scheduling contract the executor must respect: tasks in the same
wave have no unmet dependencies and may run in parallel. The critical path determines which
tasks block everything else and must not slip.

## When To Use

- Writing or reviewing an `implementation-plan.md` — as the structural reference
- Validating a generated plan against the canonical component list before marking it Draft
- Adapting the template to a specific project type (API-only, frontend-only, full-stack)
- Onboarding an executor agent: wave analysis and dependency graph define the scheduling contract

## When NOT To Use

- As a substitute for `writing-implementation-plans/` — that file explains the methodology
  (100k rule, INVEST, wave algorithm); this file shows the structural components
- When the plan is already written and approved — this is authoring guidance, not execution guidance

## Content

| File | What's inside |
|------|---------------|
| `content/01-sections.xml` | All required plan sections with purpose, structure, and worked examples |
| `content/02-wave-analysis.xml` | Wave algorithm, dependency types (FS/SS/FF/SF), checkpoint types, parallelization |
| `content/03-checklist.xml` | Phase-by-phase authoring checklist: complexity analysis, dependency graph, wave, critical path, risk, rollout |

## Templates

| File | Purpose |
|------|---------|
| `templates/impl-plan-template.md` | Canonical implementation-plan.md template with all sections and placeholder text |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/validate-deps.sh` | Topological sort validator — detects cycles in task dependency list |
| `scripts/extract-waves.py` | Extract wave → tasks mapping from implementation-plan.md wave analysis table |
