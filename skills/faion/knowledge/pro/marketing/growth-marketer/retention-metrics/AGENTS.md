# Retention Metrics

## Summary

Retention metrics quantify how many users return over time. Core set: D1/D7/D30 cohort retention rates, DAU/MAU engagement ratio, monthly churn rate, and a churn-risk score per user. Every metric requires a locked SQL definition — "DAU" computed differently across reports produces uncomparable numbers.

## Why

Aggregate retention ("D30 = 15%") hides cohort trends and segment regressions. Without cohort-level retention you cannot tell whether the product is improving, whether a traffic-source change is diluting quality, or whether a feature experiment moved the needle. The churn-risk score gives operators time to intervene before users cancel.

## When To Use

- Standing up retention reporting for the first time — generate D1/D7/D30 cohort tables.
- Weekly digest automation: WoW deltas, at-risk cohort flags, DAU/MAU trend.
- Benchmarking against industry norms (B2B SaaS, social, mobile, ecom) to set realistic targets.
- Building a churn-risk model: feature engineering per user from event data.
- Pre-A/B-test power planning — knowing baseline cohort variance is required to size experiments.

## When NOT To Use

- One-off transactional products (single-purchase utility, gift) — retention is the wrong primitive; use LTV + repeat-purchase.
- Pre-PMF: cohorts smaller than 100 users produce noise, not signal.
- B2B products with monthly or quarterly usage — D1/D7 retention misleads; use feature-event retention or contract-tied metrics.
- Heavily seasonal products where cohort comparison across periods is invalid without de-seasonalizing.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-metrics.xml` | Definitions, benchmarks by product type, engagement ratios, monthly churn targets |
| `content/02-checklist.xml` | Implementation checklist: define active user, cohort cadence, segmentation, dashboarding, churn prediction |
| `content/03-churn-prediction.xml` | Churn-risk scoring logic, risk tiers, agent workflow rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/cohort-matrix.py` | Python snippet: compute acquisition cohort retention matrix from a DataFrame |
| `templates/retention-loop-design.md` | Retention loop design template: trigger, action, reward, investment, metrics |
| `templates/engagement-dashboard.md` | Weekly engagement dashboard template: retention rates, DAU/MAU, loop health, churn analysis |
