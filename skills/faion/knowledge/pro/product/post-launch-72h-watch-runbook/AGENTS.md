---
slug: post-launch-72h-watch-runbook
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines the 72-hour post-launch watch: signal thresholds, on-call rotation, escalation triggers, rollback gates; output is a runbook spec with named owner per signal.
content_id: "c8feeb80f684ad0e"
complexity: medium
produces: playbook-step
est_tokens: 5400
tags: [product, pro, playbook-step, launch, runbook, watch]
---
# Post-Launch 72h Watch Runbook

## Summary

**One-sentence:** Defines the 72-hour post-launch watch: signal thresholds, on-call rotation, escalation triggers, rollback gates; output is a runbook spec with named owner per signal.

**One-paragraph:** Defines the 72-hour post-launch watch: signal thresholds, on-call rotation, escalation triggers, rollback gates; output is a runbook spec with named owner per signal. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Major launch (pricing change, new tier, public marketing push) needs structured first 72h.
- Solo founder: pre-commit the watch schedule so launch sleep is bounded.
- Team launch: clarify on-call rotation + escalation paths before press hits.
- Post-mortem readiness: every signal has named owner so post-mortem can trace decisions.

## Applies If (ALL must hold)

- Launch window is bounded (≤72 hours of intensified watch).
- Signals (error rate, conversion, refund rate, support volume) are instrumented.
- On-call rotation can be staffed for the full window.
- Rollback path exists and is tested.

## Skip If (ANY kills it)

- No instrumented signals — fix observability first.
- Rollback path untested — block launch until tested.
- Solo founder with no health buffer — extend window or postpone launch.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signal list | {name, threshold, source, owner} | ops + product |
| Rollback playbook | step-by-step rollback doc with smoke test | ops |
| On-call rotation | owner per 8h slot for 72h | team / founder |
| Escalation matrix | trigger -> escalator -> action | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-post-launch-72h-watch-runbook` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-post-launch-72h-watch-runbook.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[productized-service-launch]]
- [[owner-handover-sop-kit]]
- [[north-star-vs-okr-confidence-calibration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
