---
slug: productized-service-canvas
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: One-page canvas that converts a bespoke recurring service into a fixed-outcome, fixed-price, fixed-timeline offer with explicit scope-in/scope-out and a repeatable SOP.
content_id: "91732d06d5e94711"
complexity: medium
produces: spec
est_tokens: 5400
tags: [product, pro, spec, productized-service, canvas]
---
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
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

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
