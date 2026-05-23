# Task Creation Principles

## Summary

**One-sentence:** Pin the four principles for creating implementation tasks (atomic, testable, owned, estimated) so every TASK_*.md can be picked up by an executor agent with no back-channel.

**One-paragraph:** Tasks that violate atomicity, testability, ownership, or estimation force executors back to the author for clarification — defeating async execution. This methodology enumerates the four principles, gives a self-check rubric, and ties to the impl-plan-task-format validator. Every TASK passes the rubric before it lands in the queue; failures are split, rewritten, or assigned before execution starts.

**Ефективно для:**

- Solo founder authoring TASKs for an agent pool that runs unattended.
- Reviewer pre-vetting a queue before it ships to executors.
- Migration projects where TASKs must survive multi-week pauses.
- Teams introducing agent-driven SDD execution.

## Applies If (ALL must hold)

- TASKs are consumed by an executor agent (or human running async).
- Author cannot guarantee real-time clarification of ambiguity.
- Impl-plan exists in TASK_*.md form.
- Acceptance criteria can be expressed as binary checks.

## Skip If (ANY kills it)

- TASKs executed by author in real time — no async overhead.
- Single-task feature — overhead exceeds benefit.
- Pre-impl-plan — no TASKs yet.
- Tasks intentionally exploratory (spike) — different rubric.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| impl-plan-task-format spec | markdown | impl-plan-task-format |
| TASK_*.md drafts | markdown | Author |
| AC rubric | rubric | ac-quality-rubric |
| Component map | list | impl-plan-components |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/impl-plan-task-format` | TASK shape this methodology audits. |
| `solo/sdd/sdd-planning/impl-plan-100k-rule` | Estimation cap this methodology enforces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `self-check` | haiku | Deterministic rubric pass. |
| `split-non-atomic` | sonnet | Decompose multi-component TASKs. |
| `audit-queue` | opus | Multi-task synthesis across the queue. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-creation-principles.json` | JSON skeleton conforming to the output contract schema. |
| `templates/task-creation-principles.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-creation-principles.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[impl-plan-task-format]]
- [[impl-plan-100k-rule]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
