# Productized Service Design

## Summary

**One-sentence:** Designs the full productized-service offer (SOP, deliverables, pricing model, guarantees, refund policy, escalation); output is a service design spec ready for launch.

**One-paragraph:** Designs the full productized-service offer (SOP, deliverables, pricing model, guarantees, refund policy, escalation); output is a service design spec ready for launch. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Canvas (see productized-service-canvas) approved — next step is full design.
- Pre-launch readiness: lock SOP, deliverables, guarantees, refund policy before first sale.
- Scale-up: hire-and-onboard signal — design spec is what a new delivery hire reads day-1.
- Audit existing productized offer: identify gaps in SOP / guarantees / escalation.

## Applies If (ALL must hold)

- Productized canvas already validated for this offer.
- ≥3 prior engagements delivered the same outcome.
- Pricing model decided (fixed / retainer / milestone).
- Founder available to draft SOP + guarantees with named ops owner.

## Skip If (ANY kills it)

- Canvas not validated — apply productized-service-canvas first.
- No prior outcome delivered — design is hypothetical.
- Pricing model undecided — block until decided.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved canvas | canvas spec id | PM / founder |
| Delivery cost data | labor + tools cost per engagement | ops |
| Refund policy draft | 1 paragraph + edge cases | legal |
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
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-productized-service-design` | sonnet | Output drafting needs structure + light judgement. |
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
| `scripts/validate-productized-service-design.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[productized-service-canvas]]
- [[productized-service-launch]]
- [[owner-handover-sop-kit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "design_id": "psd-acme-onboarding-2026q2",
  "owner": "ops@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "canvas_ref": "psc-acme-onboarding-2026q2",
  "sop": [
    {
      "step": 1,
      "name": "kickoff",
      "deliverable": "kickoff doc"
    },
    {
      "step": 2,
      "name": "discovery",
      "deliverable": "audit memo"
    },
    {
      "step": 3,
      "name": "impl",
      "deliverable": "shipped flow"
    },
    {
      "step": 4,
      "name": "handover",
      "deliverable": "ops SOP + dashboard"
    }
  ],
  "deliverables": [
    "audit memo",
    "shipped onboarding flow",
    "instrumentation dashboard",
    "handover SOP"
  ],
  "pricing": {
    "model": "fixed",
    "amount": 12000,
    "currency": "USD"
  },
  "guarantees": [
    "+15pp conversion OR refund 50%",
    "deliver within 4 weeks OR 10% credit"
  ],
  "refund_policy": {
    "window_days": 14,
    "conditions": [
      "deliverable missed",
      "guarantee unmet"
    ]
  },
  "escalation": [
    {
      "trigger": "client unresponsive 5 days",
      "escalator": "founder",
      "action": "pause + reassign"
    }
  ],
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
