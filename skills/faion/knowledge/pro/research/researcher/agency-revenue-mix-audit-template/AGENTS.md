---
slug: agency-revenue-mix-audit-template
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Revenue-mix audit template that classifies an agency's last-12-months revenue by type (project, retainer, productized, referral, owner-billed) and surfaces dependence risks + valuation-multiplier impact.
content_id: "51b5885f27fc48d1"
complexity: medium
produces: spec
est_tokens: 4900
tags: [agency, revenue-mix, audit, research, pro]
---
# Agency Revenue Mix Audit Template

## Summary

**One-sentence:** Revenue-mix audit template that classifies an agency's last-12-months revenue by type (project, retainer, productized, referral, owner-billed) and surfaces dependence risks + valuation-multiplier impact.

**One-paragraph:** Revenue-mix audit template that classifies an agency's last-12-months revenue by type (project, retainer, productized, referral, owner-billed) and surfaces dependence risks + valuation-multiplier impact. The methodology pins inputs to citable sources, runs ≥3 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Agency founder pre-broker audit before exit conversations.
- Annual revenue-mix review to track owner-dependency reduction.
- Mix-shift planning when retainer % must rise to lift valuation.
- Investor / acquirer due-diligence prep.

## Applies If (ALL must hold)

- The triggering activity for agency revenue mix audit template appears in the user's workload at least once per cycle.
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
| `pro/research/researcher/` parent skill context | vocabulary, neighbouring methodologies |
| [[agency-valuation-rubric]] | upstream context this methodology builds on |
| [[business-model-planning]] | upstream context this methodology builds on |

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
| `fill-agency-revenue-mix-audit-template-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-revenue-mix-audit-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |


## Related

- [[agency-valuation-rubric]]
- [[business-model-planning]]
- [[risk-assessment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
