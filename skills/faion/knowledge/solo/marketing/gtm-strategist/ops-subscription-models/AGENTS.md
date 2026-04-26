# Subscription Models

## Summary

A framework for designing and operating subscription businesses: choose model type (SaaS,
membership, replenishment, curation), structure tiers with strategic feature allocation,
instrument MRR/churn/LTV metrics, automate billing recovery (dunning), and manage the
full customer lifecycle from trial through win-back. Net Revenue Retention above 100% is
the goal — meaning expansion revenue offsets churn.

## Why

One-time sales require constant new acquisition; subscriptions create compounding recurring
revenue. The mechanism: annual plans reduce churn (cash in, less friction to cancel), dunning
automation recovers 20–40% of failed payments that would otherwise be silent churn, and
lifecycle interventions (at-risk triggers, save offers) extend LTV at near-zero marginal cost.

## When To Use

- Launching a SaaS, digital membership, or content platform.
- Converting an existing one-time-purchase product to recurring revenue.
- Churn rate is above 5%/month and root cause is unclear.
- Expansion revenue (upgrades) is zero — missing upsell/tier paths.
- Setting up billing infrastructure for the first time (Stripe, Paddle).

## When NOT To Use

- One-time high-value services (consulting, agency work) where recurring isn't the model.
- Products with naturally episodic demand (event software, seasonal tools).
- When product has not yet demonstrated retention past 90 days — subscription without retention is an expensive churn machine.
- Physical product subscriptions without reliable supply chain — replenishment model requires fulfillment reliability.

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-and-tiers.xml` | Subscription types; billing frequency trade-offs; Good-Better-Best, Freemium, Usage+Base tier structures; feature allocation table. |
| `content/02-metrics-and-billing.xml` | Essential metrics formulas (MRR, ARR, churn, LTV, NRR); billing best practices; dunning sequence (Day 0–10); payment recovery flow. |
| `content/03-lifecycle-and-examples.xml` | Customer lifecycle stages and interventions; SaaS and membership site examples with tier decisions and results. |

## Templates

| File | Purpose |
|------|---------|
| `templates/subscription-model-doc.md` | Model design document: type, billing, tiers, metric targets, lifecycle automation plan. |
| `templates/dunning-emails.txt` | 3-email payment recovery sequence (Day 1, Day 3, Day 7). |
