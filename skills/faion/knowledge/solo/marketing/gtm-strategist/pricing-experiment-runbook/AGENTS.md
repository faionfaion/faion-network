---
slug: pricing-experiment-runbook
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "308bb84809d51c45"
summary: A step-by-step pricing-experiment runbook for Stripe-based solo SaaS that pre-commits the test design (variant, audience, duration, success metric), pins grandfathering rules, handles billing edge cases (proration, refunds, currency, taxes), and forces an explicit go / no-go decision after the test window.
tags: [pricing, stripe, experiment, ab-test, grandfathering, solo-saas]
---

# Pricing Experiment Runbook (Stripe Solo)

## Summary

**One-sentence:** Run a pricing experiment on a Stripe-based solo SaaS without breaking existing customers — pre-commit the design, pin grandfathering, handle billing edges (proration, currency, taxes, dispute risk), and force a go / no-go at the end.

**One-paragraph:** `ops-pricing-strategy` covers pricing models in the abstract; this runbook covers the operational mechanics of actually changing a price on Stripe in production. Failures are concrete: grandfathered customers accidentally re-billed at the new price, currency-conversion errors at the EU VAT moment, refund-storm from a poorly-announced increase, an A/B test that statistically never closes because the volume is too low. The runbook pins six gates: (1) pre-commit the experiment design (variant, audience, exposure rule, duration), (2) pin grandfathering policy (which customers stay on the old price and for how long), (3) configure Stripe correctly (new Price object, no Plan deletion, coupon stack for grandfathering), (4) instrument the measurement (trial-to-paid, MRR delta per variant, refund rate, support-ticket volume), (5) handle currency / tax edges explicitly, (6) force a go / no-go decision document on the final day. Primary output: a one-page Pricing Experiment Plan plus a Stripe configuration checklist plus a post-experiment decision memo.

## Applies If (ALL must hold)

- product is on Stripe Billing (Subscriptions or Checkout) with at least 30 active subscriptions
- founder has Stripe Dashboard access AND Stripe-API access (curl / SDK)
- proposed pricing change is a real change (price, tier structure, billing period) not a copy edit
- founder controls landing page and pricing page (can make timely changes)

## Skip If (ANY kills it)

- fewer than 30 active subscriptions — statistical inference is unreliable; iterate qualitatively first
- pricing change is contractually negotiated with each customer (enterprise) — handle per-contract, not as an experiment
- product uses a non-Stripe processor — the Stripe-specific steps do not apply; adapt the principles but use the provider's docs
- founder is in the middle of a Stripe Radar dispute spike — pricing changes amplify dispute risk; stabilise first

## Prerequisites

- Stripe Test Mode environment that mirrors live (subscriptions, products, prices)
- a documented baseline of MRR, trial-to-paid, churn rate over the last 90 days
- a recipient list for the customer-facing announcement (existing customers, trial users, prospects)
- tax setup verified (Stripe Tax enabled OR manual VAT/GST in invoice rendering correct)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | Pricing-strategy decisions sit one level above this runbook |
| `pro/marketing/growth-marketer/ab-testing-setup` | A/B-test setup mechanics |
| `pro/marketing/growth-marketer/statistics-basics` | Significance thresholds; what counts as a closed test |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-commit plan, grandfathering policy, Stripe correctness, currency-tax discipline, forced go/no-go | ~900 |
| `content/02-output-contract.xml` | essential | Experiment Plan schema, Stripe-config checklist, decision-memo schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: grandfathering miss, currency drift, statistically-never-closes, refund storm, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `experiment_design_pre_commit` | opus | Cross-input synthesis of audience + variant + duration + metric |
| `stripe_config_checklist_generation` | haiku | Template fill once experiment design is set |
| `customer_announcement_drafting` | sonnet | Tone-sensitive copy with grandfathering details |
| `post_experiment_decision_memo` | opus | Cross-metric synthesis: significance + business impact + qualitative signals |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-plan.md` | One-page plan with all required fields |
| `templates/stripe-config-checklist.md` | Step-by-step Stripe Dashboard + API checklist |
| `templates/grandfather-coupon.json` | Stripe coupon JSON template for grandfathering existing customers |
| `templates/customer-announcement.md` | Email template for the customer-facing announcement |
| `templates/decision-memo.md` | Post-experiment go / no-go memo skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/stripe-pre-flight.py` | Reads Stripe API and validates: new Price exists, old Price still active, grandfather coupon attached to existing customers, no orphaned subscriptions | T-1 day before experiment start |
| `scripts/experiment-readout.py` | Pulls Stripe events for the experiment window, computes per-variant trial-to-paid, refund rate, MRR delta | On the final day of the experiment |

## Related

- parent skill: `solo/marketing/gtm-strategist/SKILL.md`
- peer methodologies: `solo/marketing/gtm-strategist/ops-pricing-strategy`, `solo/marketing/gtm-strategist/ops-subscription-models`
- external: [Stripe Billing migration docs] · [Patrick Campbell, ProfitWell pricing experiment playbooks] · [Patio11 (Patrick McKenzie) writeups on SaaS pricing experiments]
