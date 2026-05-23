---
slug: freelancer-weekly-report-template
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: One-page weekly stakeholder report for solo freelancers: shipped / next / risks / asks, anchored to verifiable evidence per row, posted on a fixed cadence so the client never has to chase.
content_id: "59fa303c70f368da"
complexity: medium
produces: report
est_tokens: 4900
tags: [comms, solo, freelancing, weekly-report, stakeholder-update, cadence]
---
# Freelancer Weekly Report Template

## Summary

**One-sentence:** One-page weekly stakeholder report for solo freelancers: shipped / next / risks / asks, anchored to verifiable evidence per row, posted on a fixed cadence so the client never has to chase.

**One-paragraph:** Freelancers either over-report (Friday War-and-Peace email) or under-report (silence + monthly invoice). The template fixes a four-block weekly shape: shipped (with PR links), next (with explicit unknowns), risks (with proposed mitigations), asks (with named recipient). Output is the filled report conforming to the schema; the cadence is part of the rule set, not the artefact. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Freelancer Weekly Report Template — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `freelancer-weekly-report-template` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Active engagement of ≥2 weeks duration with a single named client.
- Operator commits to a fixed weekly cadence (day-of-week + time).

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Engagement length <2 weeks — a single closeout report is enough.
- Client explicitly opts out of weekly cadence — fall back to milestone-based reports.

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
| `fill-freelancer-weekly-report-template-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-freelancer-weekly-report-template.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-weekly-report-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[freelancer-inbound-reply-template]]
- [[freelancer-scope-change-script-library]]

## Decision tree

See `content/06-decision-tree.xml`. Decides full-cycle report vs short-update vs skip. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
