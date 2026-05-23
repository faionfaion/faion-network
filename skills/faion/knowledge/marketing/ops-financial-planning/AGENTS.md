# Financial Planning

## Summary

**One-sentence:** Generates a solopreneur financial plan: 3-month + 12-month cash-flow projection, runway months = cash / burn, reinvestment allocation (reserve 20% + split reinvestment vs founder pay), and monthly reconciliation cadence.

**One-paragraph:** Financial Planning produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder with ≥1 month of revenue history who needs a 12-month forward financial plan with runway, reserve, reinvestment split, and monthly reconciliation — before runway surprise kills the business.

## Applies If (ALL must hold)

- ≥1 month of revenue history (even $0)
- Burn rate computable (tools + contractors + tax estimate)
- Founder commits to monthly reconciliation

## Skip If (ANY kills it)

- Pre-revenue with zero validated MRR signal — different methodology (validation first)
- Already on professional CFO retainer — they do this
- Enterprise multi-entity finance — out of scope

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last 3 months of revenue + expenses | CSV | billing + bank exports |
| Current cash balance | USD | bank |
| Tax estimate (% of revenue) per jurisdiction | % | accountant or local rate |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-pricing-strategy` | Pricing changes drive top-line projection. |
| `ops-subscription-models` | Sub model drives churn + LTV in projection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-3m-and-12m-projection, r2-runway-months-tracked, r3-reserve-20-pct-of-revenue, r4-reinvestment-vs-pay-split, r5-monthly-reconciliation, r6-tax-estimate-included | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-financial-planning` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-financial-planning` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-financial-planning` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-financial-planning.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-financial-planning.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-financial-planning.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-pricing-strategy]]
- [[ops-subscription-models]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
