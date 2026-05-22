---
slug: hourly-rate-floor-calculation
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Compute the per-hour billable rate a freelancer / contractor must charge to hit a target take-home income at realistic billable utilization (40-60%), not 100%.
content_id: "c019147611b282aa"
tags: [pricing, freelance, utilization, rate-card, runway, gross-up]
---
# Hourly Rate Floor Calculation

## Summary

**One-sentence:** Compute the per-hour billable rate a freelancer / contractor must charge to hit a target take-home income at realistic billable utilization (40-60%), not 100%.

**One-paragraph:** Freelancers consistently under-price because they divide their target income by 2080 hours and use that number as their hourly. Real billable utilization for a sustainable solo practice is 40-60% — the other 40-60% goes to sales, admin, learning, and unpaid project waste. This methodology defines the floor calculation: target_take_home → gross_up_for_taxes → gross_up_for_overhead → divide_by_billable_hours → utilization_correction. Mechanism: a 7-step worksheet, geography-specific tax + overhead assumptions, and a confidence-band output ("floor", "stretch", "non-negotiable bottom"). Primary output: a single number — the minimum sustainable hourly — plus the assumptions table so future re-pricing can recompute without redoing discovery.

## Applies If (ALL must hold)

- operator bills hourly for ≥ 50% of income OR is about to start hourly work
- operator has a target take-home income figure (annual or monthly)
- operator is solo or 1099-style contractor (W-2 calculations are different)
- operator is in a stable tax jurisdiction with known effective rates
- operator does NOT have employer-provided benefits covering healthcare / pension

## Skip If (ANY kills it)

- pure fixed-price business — use `from-hourly-to-fixed-transition` and ops-pricing-strategy instead
- W-2 employee with stable salary — rate floor concept doesn't map
- target income unknown ("just whatever I can get") — fix target first
- operator uses tax-equalization (multi-country payroll) — needs specialist advice
- operator has &lt; 6 months' bookkeeping data — no overhead baseline to gross up against

## Prerequisites (must be true before starting)

- target annual take-home income (post-tax)
- estimated effective tax rate for the jurisdiction (income + self-employment + VAT/GST if billable)
- 6-12 months of overhead spend (tools, insurance, healthcare, office, training)
- estimated unpaid time per quarter (sales, admin, learning, dead leads)
- realistic billable utilization estimate (default 50% if no data)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | Optional: position the floor within a tiered SaaS pricing structure |
| `pro/marketing/gtm-strategist/from-hourly-to-fixed-transition` | Receives the floor as the effective-hourly anchor for fixed-price math |
| `solo/launch-operations/runway-calc` | Sanity-check the income target against current burn |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: utilization &lt; 100%, gross-up taxes, gross-up overhead, three-band output, geography-specific | ~1000 |
| `content/02-output-contract.xml` | essential | Floor / stretch / bottom band schema, assumption table, recompute trigger | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (100% utilization fantasy, forgotten benefits, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gross_up_taxes_compute` | haiku | Pure arithmetic with jurisdiction lookup |
| `overhead_baseline_summarizer` | sonnet | Read 12-month expense data, classify business vs personal |
| `utilization_estimator` | sonnet | Pattern-match operator history to billable-hours band |
| `floor_calculation_synth` | sonnet | Combine inputs into 3-band output with assumption trail |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-floor-worksheet.md` | 7-step calculation template with assumption fields |
| `templates/overhead-categories.md` | Standard overhead bucket list (tools, insurance, training, etc.) |
| `templates/utilization-bands.md` | Solo / agency utilization benchmark table |
| `templates/jurisdiction-tax-table.md` | Sample effective-rate table for US, UK, EU, UA, PT |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/floor-calc.py` | Compute floor / stretch / bottom from inputs | Initial pricing |
| `scripts/recompute-trigger.py` | Compare current assumptions vs cached worksheet | Quarterly review |

## Related

- parent skill: `pro/marketing/gtm-strategist/`
- peer methodologies: `from-hourly-to-fixed-transition`, `ops-pricing-strategy`
- external: [Freelancer's Rate Calculator (Brennan Dunn)](https://doubleyourfreelancingrate.com/) · [IRS self-employment tax guide](https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes)
