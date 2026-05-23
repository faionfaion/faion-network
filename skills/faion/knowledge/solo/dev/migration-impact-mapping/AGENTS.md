---
slug: migration-impact-mapping
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Migration impact map (decision-record): codifies the 'major framework / language migration (3+ months)' decision — surface area, breakage radius, rollback path.
content_id: "386546d88c09a3a1"
complexity: deep
produces: decision-record
est_tokens: 4200
tags: [migration, framework, impact, decision, dev]
---
# Migration Impact Mapping

## Summary

**One-sentence:** Migration impact map (decision-record): codifies the 'major framework / language migration (3+ months)' decision — surface area, breakage radius, rollback path.

**One-paragraph:** Migration impact map (decision-record): codifies the 'major framework / language migration (3+ months)' decision — surface area, breakage radius, rollback path. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-migration-impact-mapping.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Migration Impact Mapping — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `migration-impact-mapping` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Proposed migration touches > 30% of files or a critical runtime boundary.
- Migration window will exceed 3 months and must be staged.
- A rollback path is needed (live-traffic dual-write, feature-flag gate, or branch revert).

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Migration scope is small (single module, one library swap) — lighter-weight ADR suffices.
- No production traffic exists yet — risk surface does not warrant the artefact.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[library-evaluation-rubric]] | Workflow context: related methodology in the same family |

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
| `fill-migration-impact-mapping-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-migration-impact-mapping.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-migration-impact-mapping.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[library-evaluation-rubric]]
- [[hidden-tech-debt-trace]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (scope, traffic, rollback cost) to staged-migration / big-bang / defer. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
