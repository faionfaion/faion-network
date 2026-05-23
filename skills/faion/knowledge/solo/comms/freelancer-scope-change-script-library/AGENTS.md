---
slug: freelancer-scope-change-script-library
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Library of 10-15 reusable scripts for the four canonical scope-change conversations (small ask, big ask, mission-creep, emergency) so the freelancer never improvises under pressure.
content_id: "fc13a0b002233040"
complexity: medium
produces: spec
est_tokens: 4900
tags: [comms, solo, freelancing, scope-change, scripts, negotiation]
---
# Freelancer Scope-Change Script Library

## Summary

**One-sentence:** Library of 10-15 reusable scripts for the four canonical scope-change conversations (small ask, big ask, mission-creep, emergency) so the freelancer never improvises under pressure.

**One-paragraph:** Faion has a difficult-conversations methodology but no domain-specific scope-change scripts. Freelancers default to either 'no problem' (mission-creep) or 'we need to talk' (panic spike). The library codifies a script per situation type with a fixed shape: empathy line → impact line → option set (price/timeline tradeoff) → next-step. Output is a script entry conforming to the schema; the artefact is a versioned library, not a single message. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Freelancer Scope-Change Script Library — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `freelancer-scope-change-script-library` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Active project where the client has just asked for additional scope.
- Operator wants a pre-vetted phrasing rather than drafting under time pressure.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Internal-team work without commercial scope boundaries — use a project planning methodology instead.
- Outright project termination — escalate to legal/contract review.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[communicator]] | Parent skill — shared comms vocabulary and tone discipline |

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
| `fill-freelancer-scope-change-script-library-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-freelancer-scope-change-script-library.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-scope-change-script-library.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[freelancer-inbound-reply-template]]
- [[freelancer-weekly-report-template]]

## Decision tree

See `content/06-decision-tree.xml`. Routes the caller to one of four situation-type scripts (small-ask / big-ask / mission-creep / emergency). Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
