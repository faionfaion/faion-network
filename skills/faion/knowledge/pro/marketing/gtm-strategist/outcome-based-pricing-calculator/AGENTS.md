---
slug: outcome-based-pricing-calculator
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "168bced160f9372a"
summary: A structured outcome-based-pricing calculator for solo freelancers and micro-agencies that anchors price to delivered outcome value (revenue lift, cost saved, risk reduced) instead of hours, with a defensible discount-to-confidence ladder.
tags: [pricing, agency, freelance, value-pricing, outcome-based, retainer]
---

# Outcome-Based Pricing Calculator

## Summary

**One-sentence:** Build a defensible outcome-based price for a freelance or micro-agency engagement by quantifying delivered outcome value, multiplying by a confidence-weighted capture rate, and laying out a discount-to-floor ladder the founder can use live in a sales call.

**One-paragraph:** `ops-financial-basics` is too thin for agency pricing — most founders default to hours-based rates because they cannot defend a value-based price under questioning. Outcome-based pricing requires three explicit inputs: the customer's expected outcome value (revenue lift, cost saved, churn averted, time reclaimed), the confidence with which the outcome will be achieved, and the share of value captured (typical agency capture: 5-25% of outcome value, with the lower end on speculative outcomes and the upper end on guaranteed outcomes). The calculator outputs (a) a defensible asking price, (b) a confidence-weighted floor below which the deal is not worth taking, (c) a 3-step discount ladder for negotiation, and (d) the discovery-call questions required to populate the inputs honestly. Primary output: a one-page pricing memo per prospect plus a saved calculator state checked into the agency's shared pricing repo.

## Applies If (ALL must hold)

- engagement is project-based or scoped-retainer (not hourly time-and-materials)
- outcome can be quantified by at least one of: revenue change, cost change, time-saved-at-fully-loaded-rate, risk-reduced-at-actuarial-value
- prospect is decision-maker OR has authority to recommend within 1 step
- engagement scope is bounded (deliverable list, success criteria) at the pricing conversation

## Skip If (ANY kills it)

- engagement is genuinely time-and-materials with no defined deliverable — keep hourly rates, do not retrofit outcome framing
- prospect explicitly refuses to disclose any outcome estimate — outcome-based pricing requires the prospect's number, even a rough one
- engagement is a fixed-vendor-list government contract — outcome pricing rarely survives procurement; use the procurement template instead
- you cannot estimate confidence honestly because you have never delivered the outcome class before — price as time-and-materials at a learning-engagement discount; do not bluff a confidence number

## Prerequisites

- discovery-call transcript or notes covering: business model, current metrics for the outcome dimension, decision authority, budget reference points
- portfolio of 2+ comparable past outcomes (your own or your agency's) with quantified results
- access to industry benchmarks for the outcome dimension (CAC, churn, conversion rate) when prospect cannot supply baselines
- a defined floor: the lowest price below which the engagement is not worth taking (covers cost + opportunity cost + minimum margin)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | Foundational pricing models; this methodology specialises one of them |
| `pro/marketing/conversion-optimizer/agency-case-study-template` | Case studies provide the comparable-outcomes input |
| `pro/marketing/gtm-strategist/agency-proposal-template-system` | Proposal where the outcome-based price lands |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: prospect's-number, confidence-honest, capture-rate-banded, floor-discipline, discount-ladder | ~900 |
| `content/02-output-contract.xml` | essential | Pricing memo schema with inputs, computation, defensible price, floor, ladder | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: anchor-from-thin-air, ego-confidence, capture-rate-greed, no-floor, accept-floor-on-call, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_outcome_value_estimate_from_discovery_notes` | sonnet | Bounded extraction; must cite prospect quotes |
| `propose_confidence_band_from_comparables` | sonnet | Cross-portfolio judgment |
| `compute_price_and_floor` | haiku | Deterministic formula once inputs are set |
| `draft_discount_ladder` | sonnet | Per-step bounded judgment on concessions |

## Templates

| File | Purpose |
|------|---------|
| `templates/pricing-memo.md` | One-page memo per prospect with all inputs, computation, asking-price, floor, ladder |
| `templates/outcome-calc.yaml` | YAML calculator with inputs and formula so the computation is auditable |
| `templates/discovery-questions.md` | Questions to ask in discovery to populate each input |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-price.py` | Reads outcome-calc.yaml, applies confidence and capture-rate, outputs price + floor + ladder | Before sending proposal |
| `scripts/win-loss-calibration.py` | Walks closed deals, compares predicted vs realised outcome and capture, surfaces calibration error | Quarterly |

## Related

- parent skill: `pro/marketing/gtm-strategist/SKILL.md`
- peer methodologies: `solo/marketing/gtm-strategist/ops-pricing-strategy`, `pro/marketing/gtm-strategist/retainer-conversion-script`
- external: [Ron Baker, Implementing Value Pricing (Wiley, 2010)] · [Blair Enns, Pricing Creativity (RockBench, 2018)] · [Patrick Campbell, ProfitWell pricing playbooks] · [Hermann Simon, Confessions of the Pricing Man (Springer, 2015)]
