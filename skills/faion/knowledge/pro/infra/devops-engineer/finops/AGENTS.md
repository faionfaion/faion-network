---
slug: finops
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a FinOps cycle spec for the Inform → Optimize → Operate phases: tagging coverage, anomaly detection, rightsizing cadence, and commitment strategy with per-team accountability.
content_id: "72aecea18e96a3e9"
complexity: deep
produces: config
est_tokens: 4500
tags: [finops, cost, rightsizing, commitments, cloud-cost]
---
# FinOps Operating Cycle

## Summary

**One-sentence:** Generates a FinOps cycle spec for the Inform → Optimize → Operate phases: tagging coverage, anomaly detection, rightsizing cadence, and commitment strategy with per-team accountability.

**One-paragraph:** Generates a FinOps cycle spec for the Inform → Optimize → Operate phases: tagging coverage, anomaly detection, rightsizing cadence, and commitment strategy with per-team accountability. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший FinOps cycle: tagging baseline + anomaly alert.
- Quarterly rightsizing + commitment review.
- Per-team showback / chargeback model.
- FinOps Foundation framework mapping.

## Applies If (ALL must hold)

- Cloud spend exceeds $10k/month and is non-trivial in the org budget.
- At least one named FinOps owner (or accountable role) exists or will be hired.
- Cost data is exportable (billing CSV / FOCUS / CUR / GCP billing export).

## Skip If (ANY kills it)

- Cloud spend <$1k/month — overhead not justified.
- No accountable role and none planned — process will not stick.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing export | CUR / FOCUS / billing CSV | Finance / FinOps |
| Team tagging baseline | tag plan | Platform |
| Commitment strategy draft | RI/SP/CUD plan | Finance / FinOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | upstream context not required |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-finops` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[finops-devops-cost-alerts]]
- [[devops-platform-policy-finops]]
- [[dora-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
