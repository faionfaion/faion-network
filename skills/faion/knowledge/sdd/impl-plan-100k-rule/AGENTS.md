# Impl Plan 100k Rule

## Summary

**One-sentence:** Cap any single implementation-plan task at ~100k tokens of estimated agent work so the executor can finish in one session without compaction loss.

**One-paragraph:** Tasks that exceed the agent context budget get partially executed and compacted away, losing context the next session needs. This methodology pins a 100k-token cap per TASK_*.md: estimate inputs + likely tool calls + output budget, split tasks that exceed it. The cap aligns with Sonnet/Opus working set; deep-research tasks at 200k+ still split. Estimates are stored in the front-matter; the impl-plan validator rejects any task with no estimate or one over 100k.

**Ефективно для:**

- Solo founder running long-horizon SDD batches where session limits matter.
- Agent pool orchestrator scheduling tasks against a token budget.
- Refactor projects where one 'simple' task secretly touches 30 files.
- Teams using 1M-context models but want predictable session cost.

## Applies If (ALL must hold)

- Tasks are executed by an LLM-driven agent (Claude Code, Aider, similar).
- Sessions have a token cap (context window or quota).
- Impl-plan exists in TASK_*.md form with front-matter.
- Estimates can be computed from inputs + output budget.

## Skip If (ANY kills it)

- Tasks are executed by humans only — no token budget.
- Single-shot agent run with no budget concern (e.g. local prototype).
- Discovery / spike where the output is the learning, not the artefact.
- Pre-impl-plan — no tasks defined yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| TASK_*.md files | markdown | impl-plan-task-format |
| Token-estimate formula | rubric | Internal |
| Input artefact list | list | TASK front-matter |
| Output budget per task | integer | TASK front-matter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/impl-plan-task-format` | TASK file shape that carries the estimate. |
| `solo/sdd/sdd-planning/impl-plan-components` | Component-level decomposition that feeds the estimate. |

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
| `estimate-task` | haiku | Mechanical token arithmetic from inputs. |
| `split-oversized` | sonnet | Decompose oversized task into 2+ sub-tasks. |
| `audit-plan` | opus | Multi-task synthesis across an impl-plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/impl-plan-100k-rule.json` | JSON skeleton conforming to the output contract schema. |
| `templates/impl-plan-100k-rule.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-impl-plan-100k-rule.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[impl-plan-task-format]]
- [[impl-plan-components]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
