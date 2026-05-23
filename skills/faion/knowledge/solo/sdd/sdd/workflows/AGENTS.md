---
slug: workflows
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Reusable end-to-end SDD workflow templates (spec-workflow, design-workflow, implementation-workflow, review-workflow) that bind phase methodologies to a runnable orchestration with named owners and gate hand-offs.
content_id: "5855a9b1517a6537"
complexity: medium
produces: spec
est_tokens: 4000
tags: [sdd, workflows, phases, llm, agents]
---
# SDD Workflows

## Summary

**One-sentence:** Reusable end-to-end SDD workflow templates (spec-workflow, design-workflow, implementation-workflow, review-workflow) that bind phase methodologies to a runnable orchestration with named owners and gate hand-offs.

**One-paragraph:** Reusable end-to-end SDD workflow templates (spec-workflow, design-workflow, implementation-workflow, review-workflow) that bind phase methodologies to a runnable orchestration with named owners and gate hand-offs. The methodology pins the artefact: a workflows.json catalog of available workflows, each with input artefacts, output artefacts, agents involved, and the gate that closes the workflow.

**Ефективно для:**

- Operators standing up SDD on a new project — pick a workflow, get a phase delivery loop.
- Reviewers who need to know which workflow produced an artefact.
- Pool executors that pick a workflow by name and execute it deterministically.
- Audit surface: every artefact knows which workflow produced it.

## Applies If (ALL must hold)

- Project uses SDD lifecycle and needs a runnable orchestration per phase.
- Workflow catalog is shared across multiple features.
- An executor / agent pool consumes workflow definitions.

## Skip If (ANY kills it)

- Ad-hoc one-off feature with no need for a reusable workflow.
- Team prefers per-feature bespoke orchestration.
- Workflow definitions cannot be persisted (no place to store catalog).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Phase methodology list | list | SDD docs |
| Agent / model roster | yaml | Pool config |
| Gate definitions | yaml | quality-gates-confidence |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-workflow-overview` | Defines the phase model that each workflow implements. |
| `solo/sdd/sdd/quality-gates-confidence` | Provides the gate definitions consumed by every workflow. |

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
| `draft-workflows` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-workflows` | haiku | Schema check + threshold checks; deterministic. |
| `review-workflows` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/workflows.json` | JSON skeleton conforming to the output contract schema. |
| `templates/workflows.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-workflows.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[sdd-workflow-overview]]
- [[quality-gates-confidence]]
- [[task-creation-parallelization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
