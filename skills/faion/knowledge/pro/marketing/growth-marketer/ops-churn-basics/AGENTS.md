# Churn Basics

## Summary

Churn measurement is the prerequisite for any retention intervention. Three metrics must be reported together: customer churn rate, MRR churn rate, and Net Revenue Retention (NRR). Voluntary and involuntary churn (failed payments) must be tracked separately — they have different root causes and fixes. A health score (login frequency + feature usage + support sentiment) provides leading indicators before the cancel event.

## Why

At 5% monthly churn, half of customers leave every year. Reducing from 5% to 3% roughly doubles LTV. But acting on churn requires knowing when it happens (cohort timing), why it happens (exit survey), and who is at risk (health score). Without measurement and segmentation, prevention work is guesswork. This methodology provides the measurement and segmentation layer; `ops-churn-prevention` covers interventions.

## When To Use

- Subscription/usage-based business needing a baseline churn rate before prevention work.
- Quarterly review or board prep requiring customer churn, MRR churn, NRR, and segment breakdowns.
- Diagnosing whether retention pain is acquisition-mix, new-cohort onboarding, or aging-cohort decay.
- Precursor to `ops-churn-prevention` and `cohort-basics`.

## When NOT To Use

- One-off transactional businesses without subscriptions — measure repeat-purchase rate instead.
- Free B2C with no revenue — focus on retention curves directly.
- Pre-revenue products — churn is meaningless until cohort sizes stabilize.
- Annual-only contracts with fewer than 2 renewal cycles — sample too small for a stable rate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-measurement.xml` | Churn types, formulas, benchmarks, health score model, common mistakes |
| `content/02-checklist.xml` | Definition, measurement, analysis, segmentation, impact, and monitoring steps |

## Templates

| File | Purpose |
|------|---------|
| `templates/monthly-churn.sql` | Voluntary vs involuntary customer + MRR churn SQL (warehouse-native) |
| `templates/churn-report.md` | Monthly churn analysis dashboard template |
