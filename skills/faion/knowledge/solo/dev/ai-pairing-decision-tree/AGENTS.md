---
slug: ai-pairing-decision-tree
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-task decision record routing the work to one of {solo-dev, AI-pair, full-agent} based on stakes, reversibility, novelty, and supervision budget.
content_id: "67ffaddd4c5bfe33"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [dev, solo, ai-pairing, decision-tree, task-routing]
---
# AI Pairing Decision Tree

## Summary

**One-sentence:** Per-task decision record routing the work to one of {solo-dev, AI-pair, full-agent} based on stakes, reversibility, novelty, and supervision budget.

**One-paragraph:** Defaulting every task to AI pairing burns context and produces sloppy commits on irreversible work; defaulting every task to solo writing burns hours on boilerplate. The decision tree asks four observable questions (stakes, reversibility, novelty-to-the-codebase, supervision-budget) and routes the task; the artefact is the per-task decision record so the choice is auditable. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- AI Pairing Decision Tree — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `ai-pairing-decision-tree` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Solo dev evaluating an upcoming task and choosing the writing mode.
- Task is non-trivial: ≥30 min of focused work or ≥1 file changed.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- One-off throwaway script with no commit — pick whatever is fastest.
- Task is bounded boilerplate the IDE template handles — no decision needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[software-developer]] | Baseline dev discipline — what 'solo writing' means |

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
| `fill-ai-pairing-decision-tree-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-ai-pairing-decision-tree.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pairing-decision-tree.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[ai-over-reliance-self-audit]]
- [[ai-prompt-as-commit-artifact]]
- [[ai-prompt-patterns-test-ideation]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (stakes, reversibility, novelty, supervision_budget) → solo / ai-pair / full-agent. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
