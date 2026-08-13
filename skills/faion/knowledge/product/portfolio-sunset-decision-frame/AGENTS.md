# Portfolio Sunset Decision Frame

## Summary

**One-sentence:** Frames a sunset decision for one product in a multi-product portfolio using revenue, maintenance cost, strategic fit, and exit cost; output is a signed decision-record with owner and date.

**One-paragraph:** Frames a sunset decision for one product in a multi-product portfolio using revenue, maintenance cost, strategic fit, and exit cost; output is a signed decision-record with owner and date. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Annual portfolio refresh: which side products to retire.
- Solo or micro-agency with ≥3 products fighting for finite attention.
- Cost-cutting review: which low-margin products to sunset vs invest in.
- Acquisition prep: trim portfolio to clean P&L before buyer due diligence.

## Applies If (ALL must hold)

- Portfolio has ≥2 products with measurable usage + revenue data.
- ≥3 months of financial data per product available.
- Sunset costs (refunds, migration paths, support tail) can be estimated.
- Named owner has authority to retire the product after sign-off.

## Skip If (ANY kills it)

- Single-product portfolio — decision frame degenerates to pivot-vs-quit.
- Acquisition LOI already signed — sunset decisions belong to the buyer.
- Cannot estimate sunset cost (legal / regulatory unknowns) — engage counsel first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-product P&L | 12 months of revenue + cost per product | accounting |
| Usage data | monthly active users per product | warehouse |
| Sunset cost estimate | refund + migration + support tail estimate | ops + legal |
| Strategic fit memo | 1 paragraph per product on portfolio fit | founder / leadership |

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
| `draft-portfolio-sunset-decision-frame` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-portfolio-sunset-decision-frame.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[founder-dependency-audit]]
- [[pivot-vs-quit-decision-template]]
- [[post-launch-72h-watch-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "decision_id": "sunset-acme-side-2026q2",
  "owner": "alex@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "product": {
    "id": "sideproduct-foo",
    "name": "FooApp"
  },
  "metrics": {
    "monthly_revenue": 320,
    "monthly_cost": 850,
    "active_users": 41,
    "evidence": "P&L 2026-05 + BI 2026-05-22"
  },
  "alternatives": [
    {
      "option": "sunset",
      "cost": 4200
    },
    {
      "option": "open-source",
      "cost": 1200
    },
    {
      "option": "sell",
      "cost": 0,
      "upside": "1x-3x ARR offer pending"
    }
  ],
  "decision": "sell",
  "rationale": "small ARR but credible buyer; sell beats sunset on NPV",
  "sunset_cost": 4200,
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
