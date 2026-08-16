# Productized Service Canvas

## Summary

**One-sentence:** One-page canvas that converts a bespoke recurring service into a fixed-outcome, fixed-price, fixed-timeline offer with explicit scope-in/scope-out and a repeatable SOP.

**One-paragraph:** One-page canvas that converts a bespoke recurring service into a fixed-outcome, fixed-price, fixed-timeline offer with explicit scope-in/scope-out and a repeatable SOP. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Bespoke freelancer wants to escape hourly with a fixed-outcome offer.
- Micro-agency that has delivered same outcome ≥3 times wants to standardise.
- Pre-launch sales page draft: canvas is the source for offer page copy.
- Inputs to SaaS pivot: canvas surfaces the productizable surface for a SaaS layer.

## Applies If (ALL must hold)

- You sell time-and-materials or hourly today.
- You have delivered the same outcome ≥3 times for previous clients.
- You can describe the outcome in one client-language sentence.
- You can name the buyer (role + company size + trigger event).

## Skip If (ANY kills it)

- You have not yet delivered the outcome for a paying client.
- Outcome is too custom to standardize (every engagement diverges).
- Buyer cares about hourly rate, not outcome — wrong buyer for productized offer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Past delivery log | list of ≥3 completed engagements with outcome + price | CRM / invoices |
| Buyer persona | role + company size + trigger event | founder |
| Delivery SOP draft | ordered steps from kickoff to handover | ops |
| Proof artefact | case study / testimonial from prior engagement | marketing |

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
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-productized-service-canvas` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md.j2` | Markdown skeleton conforming to the output contract |
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract Generated from `templates/artefact-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-productized-service-canvas.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[productized-service-design]]
- [[productized-service-launch]]
- [[freelancer-to-saas-time-box]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "canvas_id": "psc-acme-onboarding-2026q2",
  "owner": "alex@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "buyer": {
    "role": "VP Engineering",
    "company_size": "50-200",
    "trigger": "post-Series-A scale-up"
  },
  "outcome": "production-grade onboarding flow live in 4 weeks with conversion >35%",
  "price": {
    "currency": "USD",
    "amount": 12000,
    "model": "fixed"
  },
  "timeline": {
    "weeks": 4,
    "kickoff_to_handover": "2026-06-03 to 2026-07-01"
  },
  "scope_in": [
    "onboarding-flow design",
    "implementation",
    "instrumentation",
    "handover SOP"
  ],
  "scope_out": [
    "pricing redesign",
    "SSO",
    "marketing site changes"
  ],
  "sop": [
    {
      "step": 1,
      "name": "discovery call"
    },
    {
      "step": 2,
      "name": "audit + plan"
    },
    {
      "step": 3,
      "name": "implementation"
    },
    {
      "step": 4,
      "name": "handover + SOP"
    }
  ],
  "proof": [
    {
      "case": "case-bigco-2025",
      "outcome": "+18pp conversion",
      "evidence": "drive://cases/bigco"
    }
  ],
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
