---
slug: impl-plan-components
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Decompose an implementation plan into named components (files, modules, services, scripts) so every TASK references exactly one component and dependencies are graph-visible.
content_id: "6223ae20abbbac12"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["impl-plan", "components", "dependency-graph", "decomposition", "sdd"]
---
# Impl Plan Components

## Summary

**One-sentence:** Decompose an implementation plan into named components (files, modules, services, scripts) so every TASK references exactly one component and dependencies are graph-visible.

**One-paragraph:** Impl plans that list tasks without naming the underlying components produce dependency tangles: TASK_007 depends on TASK_002, but nobody can see whether they touch the same file. This methodology names every component upfront (file path, module name, or service), maps each TASK to one component, and emits a dependency graph. The graph is the single source of truth for execution order; cycles are rejected.

**Ефективно для:**

- Solo founder running parallel agent tasks; needs a graph to avoid file-write conflicts.
- Refactor projects where component ownership must be explicit.
- Large impl-plans (>20 tasks) where mental dependency tracking fails.
- Teams introducing CODEOWNERS-style per-file responsibility.

## Applies If (ALL must hold)

- Impl-plan has ≥5 TASK_*.md files.
- Tasks touch multiple components (files, modules, services).
- Parallel execution is planned or possible.
- Component boundaries are stable enough to enumerate.

## Skip If (ANY kills it)

- Trivial impl-plan with 1-2 tasks.
- Greenfield project where component names are not stable yet.
- Discovery / spike where the impl-plan is itself a hypothesis.
- Single-component change with no graph to draw.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| TASK_*.md files | markdown | impl-plan-task-format |
| Component inventory | list | Repo structure |
| Dependency edges | list | Manual or static analysis |
| Component naming convention | rubric | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/impl-plan-task-format` | TASK shape this methodology consumes. |
| `solo/sdd/sdd-planning/writing-implementation-plans` | Impl-plan envelope this methodology slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate-components` | haiku | Mechanical file/module listing. |
| `map-tasks` | sonnet | Per-task judgement on primary component. |
| `audit-graph` | opus | Cycle detection + parallel-execution analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/impl-plan-components.json` | JSON skeleton conforming to the output contract schema. |
| `templates/impl-plan-components.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-impl-plan-components.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[impl-plan-task-format]]
- [[writing-implementation-plans]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
