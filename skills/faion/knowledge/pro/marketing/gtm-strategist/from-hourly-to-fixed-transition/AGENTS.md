---
slug: from-hourly-to-fixed-transition
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A framework for moving an active book of business off hourly billing to fixed-price or productized engagements without revenue collapse.
content_id: "2a9444c76250d19d"
tags: [pricing, freelance, productized, transition, retainer, cash-flow]
---
# From Hourly to Fixed-Price Transition

## Summary

**One-sentence:** A framework for moving an active book of business off hourly billing to fixed-price or productized engagements without revenue collapse.

**One-paragraph:** Defines the sequence in which a freelancer or small studio replaces hourly engagements with fixed-price ones — starting with the highest-margin existing client, running a controlled 2-3 client overlap window, productizing the first repeatable scope into a fixed offer, and re-pricing remaining hourly clients in a single round. Mechanism: a 12-week three-phase rollout (Audit → Pilot → Convert) gated on per-client gross-margin calculations and a "cash bridge" buffer covering 6-8 weeks of trough revenue. Primary output: a transition plan with per-client decisions (convert / sunset / retain hourly), a productized SKU spec, and a documented cash bridge.

## Applies If (ALL must hold)

- operator currently bills ≥ 60% of revenue hourly
- operator has ≥ 3 active clients OR ≥ 4 quarters of stable hourly work
- monthly hourly revenue ≥ $3,000 (transition overhead exceeds value below this)
- operator has detected at least 2 repeatable scopes across past engagements
- operator has 6 weeks of personal runway OR a cash buffer ≥ 1.5× monthly burn

## Skip If (ANY kills it)

- operator has &lt; 2 clients — too narrow to absorb a single sunset
- already 100% fixed-price — transition is over; use pricing-experiments instead
- operator's work is genuinely non-repeatable (one-off forensics, novel R&D)
- runway &lt; 4 weeks — cannot afford pilot trough; needs immediate cash, not transition
- existing clients on enforceable hourly contracts with &gt; 6 months left

## Prerequisites (must be true before starting)

- per-client revenue + delivered-hours table for last 4 quarters
- per-client gross-margin estimate (revenue minus operator-time at desired effective hourly)
- catalog of past engagements with scope similarity tags
- statement of operator's target effective hourly rate (anchor for fixed pricing)
- written 6-8 week cash bridge (savings, line of credit, or new-client pipeline)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/hourly-rate-floor-calculation` | Effective-hourly anchor for fixed-price math |
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | Productized SKU shape and tier ladder |
| `pro/research/researcher/competitor-analysis` | Reality-check on market-rate ceiling for the productized SKU |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: margin-first selection, overlap window, productize one scope, single re-price round, cash bridge | ~1000 |
| `content/02-output-contract.xml` | essential | Transition plan schema, productized SKU spec, cash bridge requirements | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (sunset cascade, premature productizing, scope creep on fixed, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `client_margin_table_compute` | haiku | Pure arithmetic over revenue / hours data |
| `productize_scope_synthesis` | opus | Cross-engagement pattern recognition; high consequence |
| `cash_bridge_stress_test` | sonnet | Bounded scenario math with discrete cases |
| `client_communication_draft` | sonnet | Re-pricing message templates with operator tone |

## Templates

| File | Purpose |
|------|---------|
| `templates/transition-plan.md` | Per-client decision sheet with margin + action |
| `templates/productized-sku-spec.md` | Fixed-scope offer with deliverables + exclusions |
| `templates/repricing-email.md` | Client message for hourly-to-fixed conversion |
| `templates/cash-bridge-worksheet.md` | 8-week trough projection |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/margin-analyzer.py` | Compute per-client gross margin at target effective rate | Audit phase |
| `scripts/transition-risk-scorer.py` | Score sunset-vs-convert risk per client | Pilot phase |

## Related

- parent skill: `pro/marketing/gtm-strategist/`
- peer methodology: `hourly-rate-floor-calculation`, `ops-pricing-strategy`
- external: [Productize Yourself (Brennan Dunn)](https://doubleyourfreelancingrate.com/) · [Hourly Billing Is Nuts (Jonathan Stark)](https://jonathanstark.com/htbo)
