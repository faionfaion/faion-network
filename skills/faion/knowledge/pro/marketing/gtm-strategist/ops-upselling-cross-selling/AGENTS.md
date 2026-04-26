# Upselling & Cross-Selling

## Summary

A trigger-based expansion revenue framework: detect usage signals (account at 80% of limit, advanced feature use, team growth), match each trigger to a specific upgrade offer framed around the customer's own data point ("900 of 1,000 subscribers"), present with one-click upgrade and prorated billing, and track Net Revenue Retention monthly. Expansion costs 5–25x less to generate than new-logo revenue.

## Why

Expansion off an existing customer base is the highest-ROI growth lever once new-logo CAC exceeds 30% of LTV. Generic "want to upgrade?" CTAs convert 3–5x worse than usage-anchored offers. Trigger-based automation (at 80% limit, after first success, at renewal) ensures timing is right without manual tracking across hundreds of accounts.

## When To Use

- Existing customer base of 100+ paying accounts where new-logo CAC has crept above 30% of LTV
- NRR sub-100% and an expansion lever is needed to offset churn before adding top-of-funnel spend
- Pricing has metered tiers (seats, usage, feature gates) that naturally produce upsell triggers
- Catalog of 2+ adjacent products where current customers are obvious cross-sell candidates

## When NOT To Use

- Pre-PMF or unstable pricing — upsell offers train customers on prices that may change, generating churn risk
- Customers in active support escalation — wrong moment, damages trust and depresses CSAT
- One-and-done products without recurring usage signal (single-purchase ebooks) — referral or repeat-buy is the right lever
- When activation rate is the real problem — expansion off a low-activation base just lifts a tiny denominator

## Content

| File | What's inside |
|------|---------------|
| `content/01-triggers-and-timing.xml` | Upsell trigger signals, cross-sell opportunity mapping, good vs. bad timing table |
| `content/02-offer-framing.xml` | Value-based positioning do/don't examples, friction reduction, upgrade experience steps |
| `content/03-examples-and-gotchas.xml` | SaaS usage-limit and course cross-sell case examples; AI-agent gotchas for expansion messaging |

## Templates

| File | Purpose |
|------|---------|
| `templates/upsell-usage-email.md` | Usage-limit upsell email template anchored to customer's actual usage data |
| `templates/upsell-feature-email.md` | Feature-based upsell email with free trial CTA |
| `templates/crosssell-email.md` | Cross-sell email for adjacent product with loyalty discount |
| `templates/expansion-dashboard.md` | Monthly expansion MRR summary: by type, top opportunities |
| `templates/triggers.py` | Expansion trigger detector: usage threshold + advanced feature usage signals |
