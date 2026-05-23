---
slug: writing-implementation-plans
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Bridge approved design.md into an executable impl-plan.md that breaks AD-X decisions into ordered, token-budgeted task rows grouped by wave, with a per-task acceptance criterion and a per-wave gate.
content_id: "2994d2ea09432fba"
complexity: deep
produces: spec
est_tokens: 4300
tags: [implementation, planning, sdd, tasks, waves]
---
# Writing Implementation Plans

## Summary

**One-sentence:** Bridge approved design.md into an executable impl-plan.md that breaks AD-X decisions into ordered, token-budgeted task rows grouped by wave, with a per-task acceptance criterion and a per-wave gate.

**One-paragraph:** Bridge approved design.md into an executable impl-plan.md that breaks AD-X decisions into ordered, token-budgeted task rows grouped by wave, with a per-task acceptance criterion and a per-wave gate. The methodology pins the artefact: every row carries task-id, owns-files, depends-on, est_tokens, owner-model, AC, and the wave number; total budget is summed and checked against the global cap.

**Ефективно для:**

- Features large enough that one task is insufficient.
- Pool executors that consume impl-plan rows as task seeds.
- Reviewers checking that estimated work fits the global token cap.
- Audit surface: every task row references back to AD-X and FR-X.

## Applies If (ALL must hold)

- Approved design.md exists.
- Total work is ≥3 tasks.
- Token budget cap is known.

## Skip If (ANY kills it)

- Single-task feature.
- Design is still in flux.
- No budget cap defined; impl-plan cannot be sized.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| design.md | markdown | Design phase |
| Token budget cap | integer | Pool config |
| Model roster | yaml | Pool config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/writing-design-documents` | Provides AD-X decisions that this plan decomposes. |
| `solo/sdd/sdd/task-creation-parallelization` | Provides wave / dependency / size rules consumed here. |

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
| `draft-writing-implementation-plans` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-writing-implementation-plans` | haiku | Schema check + threshold checks; deterministic. |
| `review-writing-implementation-plans` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/writing-implementation-plans.json` | JSON skeleton conforming to the output contract schema. |
| `templates/writing-implementation-plans.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-writing-implementation-plans.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-design-documents]]
- [[task-creation-parallelization]]
- [[sdd-workflow-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
