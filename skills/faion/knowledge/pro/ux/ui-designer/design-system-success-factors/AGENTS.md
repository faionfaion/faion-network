---
slug: design-system-success-factors
tier: pro
group: ux
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Four-pillar rubric (ownership / usable components / strong docs / measured adoption) to grade a design system's health and pinpoint the weakest pillar before more components ship.
content_id: "da0563d1346d0276"
complexity: medium
produces: rubric
est_tokens: 4900
tags: [design-systems, rubric, governance, adoption-metrics, design-ops]
---
# Design System Success Factors

## Summary

**One-sentence:** Four-pillar rubric (ownership / usable components / strong docs / measured adoption) to grade a design system's health and pinpoint the weakest pillar before more components ship.

**One-paragraph:** Four-pillar rubric (ownership / usable components / strong docs / measured adoption) to grade a design system's health and pinpoint the weakest pillar before more components ship. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Quarterly health check of an in-flight design system.
- Justifying headcount by showing weakest-pillar evidence.
- Comparing two candidate systems before adoption.
- Triaging where to invest the next sprint of design-ops capacity.
- Catching 'phantom adoption' (cited but not actually used) before a roadmap claim.

## Applies If (ALL must hold)

- The triggering activity for design-system-success-factors appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/` parent skill context | vocabulary, neighbouring methodologies |
| [[design-system-governance]] | upstream context this methodology builds on |
| [[design-system-impact-queue]] | upstream context this methodology builds on |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-design-system-success-factors-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-system-success-factors.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |


## Related

- [[design-system-governance]]
- [[design-system-impact-queue]]
- [[design-system-changelog-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
