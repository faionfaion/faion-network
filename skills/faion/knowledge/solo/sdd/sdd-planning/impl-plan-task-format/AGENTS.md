---
slug: impl-plan-task-format
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Define the canonical TASK_NNN-title.md format (front-matter + sections) so every implementation task is machine-parseable, agent-ready, and consistently sized.
content_id: "a3b20bd00d4e7739"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["impl-plan", "task", "format", "front-matter", "sdd"]
---
# Impl Plan Task Format

## Summary

**One-sentence:** Define the canonical TASK_NNN-title.md format (front-matter + sections) so every implementation task is machine-parseable, agent-ready, and consistently sized.

**One-paragraph:** TASK files are the atomic units of an impl-plan and the primary input to executor agents. This methodology pins the format: kebab-case slug, NNN sequential number, YAML front-matter (id, est_tokens, status, depends_on, acceptance, owner), and a fixed five-section body (Goal, Inputs, Steps, Acceptance, Notes). The format is enforced by a validator so executor agents can rely on it.

**Ефективно для:**

- Solo founder running an agent-driven SDD batch; needs parseable TASKs.
- Reviewer scanning 20+ tasks per week; consistent layout cuts review time.
- Agent generating TASKs from impl-plan + design.md; needs a target shape.
- Multi-agent orchestration where TASKs are queue items.

## Applies If (ALL must hold)

- Impl-plan is written as TASK_*.md files in a directory.
- Tasks will be consumed by an agent (executor pool, scheduler).
- Front-matter must be machine-parseable.
- Sequential numbering is stable enough to enumerate.

## Skip If (ANY kills it)

- Tasks live in an external tracker (Linear, Jira) — different format applies.
- Single-task work — overhead exceeds benefit.
- Pre-impl-plan — no tasks defined.
- Tasks executed by humans only — overhead can be relaxed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| templates/TASK_skeleton.md | markdown | This methodology |
| impl-plan.md | markdown | writing-implementation-plans |
| design.md | markdown | design-doc-structure |
| Component map | list | impl-plan-components |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/writing-implementation-plans` | Envelope holding the TASKs. |
| `solo/sdd/sdd-planning/impl-plan-components` | Component map referenced by each TASK. |

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
| `draft-task` | sonnet | Per-task content from design + components. |
| `lint-task` | haiku | Deterministic format check. |
| `audit-batch` | opus | Cross-task consistency check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/impl-plan-task-format.json` | JSON skeleton conforming to the output contract schema. |
| `templates/impl-plan-task-format.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-impl-plan-task-format.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-implementation-plans]]
- [[impl-plan-100k-rule]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
