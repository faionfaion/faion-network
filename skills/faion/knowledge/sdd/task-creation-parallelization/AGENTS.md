# Task Creation and Parallelization

## Summary

**One-sentence:** Decompose an approved design and impl-plan into INVEST-shaped tasks grouped into parallel waves, each task bounded by a token budget and an explicit dependency list so a worker pool can execute waves concurrently.

**One-paragraph:** Decompose an approved design and impl-plan into INVEST-shaped tasks grouped into parallel waves, each task bounded by a token budget and an explicit dependency list so a worker pool can execute waves concurrently. The methodology pins the artefact: a tasks.json whose entries carry id, depends_on, wave, est_tokens, owner-model, and acceptance criteria, plus a wave graph that is acyclic and balanced.

**Ефективно для:**

- SDD batches large enough to need a wave-based executor.
- Solo founders running a self-replenishing background-agent pool.
- Pipelines where each task has a per-task token budget separate from the global budget.
- Audit surface: tasks.json is the single source of truth for who runs what when.

## Applies If (ALL must hold)

- Approved design.md + impl-plan.md exist.
- Work scope is ≥3 tasks; smaller scopes do not benefit from waving.
- An executor pool exists that can consume the wave structure.

## Skip If (ANY kills it)

- Single-task feature — write one task directly.
- Tasks have hidden global state that prevents parallel execution.
- No executor pool — wave graph is just paper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| design.md | markdown | design phase |
| impl-plan.md | markdown | impl-plan phase |
| token budget | integer | Pool config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/writing-implementation-plans` | Provides the structured plan that this methodology decomposes. |

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
| `draft-task-creation-parallelization` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-task-creation-parallelization` | haiku | Schema check + threshold checks; deterministic. |
| `review-task-creation-parallelization` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-creation-parallelization.json` | JSON skeleton conforming to the output contract schema. |
| `templates/task-creation-parallelization.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-creation-parallelization.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-implementation-plans]]
- [[sdd-workflow-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
