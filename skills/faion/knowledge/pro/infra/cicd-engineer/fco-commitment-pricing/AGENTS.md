---
slug: fco-commitment-pricing
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a commitment-pricing plan (RIs / Savings Plans / 1-3yr commitments) for steady-state workloads delivering 60-75% discount, with utilization monitoring and unused-commitment alarm.
content_id: "df3d31611a50d4dc"
complexity: medium
produces: decision-record
est_tokens: 4100
tags: ["finops", "reserved-instances", "savings-plans", "cloud-cost", "commitment-pricing"]
---
# FinOps — Reserved Instances / Savings Plans Commitment

## Summary

**One-sentence:** Generates a commitment-pricing plan (RIs / Savings Plans / 1-3yr commitments) for steady-state workloads delivering 60-75% discount, with utilization monitoring and unused-commitment alarm.

**One-paragraph:** FinOps — Reserved Instances / Savings Plans Commitment — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a decision-record that the downstream agent can verify with the included validator.

**Ефективно для:**

- Cloud spend on a steady-state workload exceeds $10k/mo for at least 3 months running.
- Capacity needs are predictable within 20% over the commitment horizon.
- Finance has authority to commit to a 1-3 year term.

## Applies If (ALL must hold)

- Cloud spend on a steady-state workload exceeds $10k/mo for at least 3 months running.
- Capacity needs are predictable within 20% over the commitment horizon.
- Finance has authority to commit to a 1-3 year term.

## Skip If (ANY kills it)

- Variable / bursty workload (spot-suitable) — use `fco-spot-instances` instead.
- Pre-product / pre-PMF stage where capacity needs may pivot within 3 months.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[fco-cost-allocation]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (3-month-baseline-required, convertible-for-uncertainty, cover-base-not-peak, utilization-alert-80pct, staggered-renewal, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the decision-record + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fco-commitment-pricing` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/commitment-plan.md` | Decision record: workload + baseline + commitment shape + utilization plan |
| `templates/backup-config.example.json` | Filled decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-commitment-pricing.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[fco-cost-allocation]]
- [[fco-rightsizing]]
- [[fco-spot-instances]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
