# Maintain Mode SOPs Solo

## Summary

**One-sentence:** Produces a maintain-mode SOP spec (weekly check + monthly tax + quarterly review + on-call rule) for a solo-owned product moving from build-mode to maintain-mode.

**Ефективно для:** Solopreneurs whose product stopped growing but still serves paying customers and need a low-touch ops SOP to keep it alive without lighting hair on fire weekly.

**One-paragraph:** A solo product that finished its growth chapter still needs care — uptime, support, billing edge cases, dependency upgrades, tax filings. Without a written maintain-mode SOP the operator either over-invests (build-mode habits keep firing) or under-invests (silently rotting). This methodology produces an SOP spec: weekly 30-min check, monthly tax / billing reconciliation, quarterly dependency upgrade window, on-call rule for incidents. Output is consumed by the operator's calendar + status page.

## Applies If (ALL must hold)

- Product has crossed PMF or stopped growing and is in maintain-mode.
- Product has paying customers (MRR > 0) AND zero growth-investment is planned for ≥6 months.
- Operator is the single point of failure for ops, billing, support.
- Operator can dedicate ≥30 minutes / week to maintain-mode tasks.

## Skip If (ANY kills it)

- Product is still in build-mode (growth tasks dominate).
- Product has no paying customers — sunset playbook instead.
- Operator cannot guarantee ≥30 min/week — sunset or hand-off instead.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| MRR + churn snapshot | currency + % | Stripe / Lemonsqueezy |
| dependency list | array | package manifest |
| support inbox | URL | Help Scout / Front / email |
| status page URL | URL | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/multi-product-portfolio-management` | Parent — multi-product portfolio context. |
| `solo/product/subscription-lifecycle-edge-cases` | Downstream — billing edge cases the SOP must cover. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scaffold_sop_spec` | haiku | Template-fill from prereqs. |
| `calibrate_cadence` | sonnet | Bounded judgement: weekly vs bi-weekly vs monthly cadence per task. |
| `ops_drift_review` | opus | Cross-month synthesis on drift from spec. |

## Templates

| File | Purpose |
|---|---|
| `templates/maintain-mode-sops-solo.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/maintain-mode-sops-solo.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-maintain-mode-sops-solo.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[multi-product-portfolio-management]] — related methodology.
- [[subscription-lifecycle-edge-cases]] — related methodology.
- [[sunset-failed-product-playbook]] — related methodology.
- [[portfolio-triage-indie]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
