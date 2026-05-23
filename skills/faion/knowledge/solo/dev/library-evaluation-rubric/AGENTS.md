---
slug: library-evaluation-rubric
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Library evaluation rubric (decision-record): scores for maintenance health, license, bundle-size impact, security history, ecosystem fit — picking THIS library.
content_id: "1f2cae2ab1baa5ca"
complexity: medium
produces: rubric
est_tokens: 4200
tags: [library, evaluation, dependency, rubric, dev]
---
# Library Evaluation Rubric

## Summary

**One-sentence:** Library evaluation rubric (decision-record): scores for maintenance health, license, bundle-size impact, security history, ecosystem fit — picking THIS library.

**One-paragraph:** Library evaluation rubric (decision-record): scores for maintenance health, license, bundle-size impact, security history, ecosystem fit — picking THIS library. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-library-evaluation-rubric.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Library Evaluation Rubric — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `library-evaluation-rubric` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- A new dependency is being considered and the choice is contested.
- Multiple candidate libraries cover the same need (e.g. Zod vs Yup vs Valibot).
- License or bundle-size discipline is part of the codebase contract.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Single obvious incumbent (React, TypeScript) — rubric adds no signal.
- Library is a one-time tool used only in build-time — long-term health matters less.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[hidden-tech-debt-trace]] | Workflow context: related methodology in the same family |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-library-evaluation-rubric-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-library-evaluation-rubric.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-library-evaluation-rubric.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[hidden-tech-debt-trace]]
- [[migration-impact-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (candidate count, risk surface, lock-in cost) to full-rubric / quick-rubric / pick-default. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
