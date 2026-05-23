---
slug: ops-pricing-strategy
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a value-based pricing spec: cost floor, customer-value ceiling, willingness-to-pay research, pricing model (subscription / usage / hybrid), and 60-day test plan — replaces gut-feel pricing.
content_id: "2e5ce948ea43dbb7"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["pricing", "value-based-pricing", "monetization", "saas", "solo"]
---
# Pricing Strategy

## Summary

**One-sentence:** Generates a value-based pricing spec: cost floor, customer-value ceiling, willingness-to-pay research, pricing model (subscription / usage / hybrid), and 60-day test plan — replaces gut-feel pricing.

**One-paragraph:** Pricing Strategy produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder pricing v1 or repricing existing tiers who needs a value-based spec with cost floor, value ceiling, WTP research, model choice, and 60-day test plan — before underpricing the offer for 12 months.

## Applies If (ALL must hold)

- Cost-of-delivery quantified (cost floor known)
- ≥10 customer or prospect interviews available for WTP signal
- Founder authority to change pricing within 60 days

## Skip If (ANY kills it)

- Commodity product with reference price already set by market
- Pre-product (no value evidence yet) — defer until WTP signal exists
- Marketplace-set pricing (Steam, App Store) — model is fixed

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cost-of-delivery per customer / month | USD | billing + infra |
| Customer + prospect interview transcripts / notes | doc | research log |
| Competitor pricing snapshot (≥3) | table | manual scrape |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-financial-planning` | Pricing drives top-line projection. |
| `ops-subscription-models` | Pricing model interacts with subscription tier design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-cost-floor-known, r2-value-ceiling-from-research, r3-explicit-model, r4-60-day-test-plan, r5-grandfather-existing-customers, r6-named-owner | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-pricing-strategy` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-pricing-strategy` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-pricing-strategy` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-pricing-strategy.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-pricing-strategy.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-pricing-strategy.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-financial-planning]]
- [[ops-subscription-models]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
