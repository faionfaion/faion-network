---
slug: ecommerce-checkout-ba-pack
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Reusable BA pack for any e-commerce checkout: user-flow, edge-case catalogue, NFR thresholds, regulatory checklist, payment-provider integration spec.
content_id: "757eb9b554880f3f"
complexity: deep
produces: spec
est_tokens: 4900
tags: [ba, pro, ecommerce, checkout, payments, reusable-pack]
---
# E-commerce Checkout BA Pack

## Summary

**One-sentence:** Reusable BA pack for any e-commerce checkout: user-flow, edge-case catalogue, NFR thresholds, regulatory checklist, payment-provider integration spec.

**One-paragraph:** E-commerce Checkout BA Pack pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Greenfield Shopify / Medusa / custom build BA scoping.
- Checkout-redesign engagement for a Stripe / Adyen / Mollie merchant.
- Cross-border launch needing VAT / OSS / IOSS rules.
- PSP migration where existing flow must be re-specified.

## Applies If (ALL must hold)

- Engagement scope includes designing or rebuilding an e-commerce checkout flow.
- The store accepts at least one card / wallet / BNPL payment method.
- There is at least one tax/VAT/GST regime in play (B2C cross-border or domestic VAT).
- Stakeholders include both product and finance / accounting.

## Skip If (ANY kills it)

- Pre-order / waitlist flow with no actual money capture at this stage.
- B2B invoicing only (no card / wallet capture).
- Pure marketplace where checkout is delegated to seller storefronts.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing checkout flow doc | markdown / Figma | Client repo |
| Payment-provider contracts | pdf | Client legal |
| Tax / VAT regime list | csv | Finance / accounting |
| Refund / chargeback policy | markdown | Customer success |
| Browser / device matrix | csv | Analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ecommerce-checkout-ba-pack` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ecommerce-checkout-ba-pack.md` | Markdown spec skeleton with required sections + placeholders |
| `templates/ecommerce-checkout-ba-pack.schema.json` | JSON Schema for the structured spec output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ecommerce-checkout-ba-pack.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
