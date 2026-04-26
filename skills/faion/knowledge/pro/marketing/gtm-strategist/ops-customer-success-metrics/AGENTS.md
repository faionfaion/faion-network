# Customer Success Metrics

## Summary

A measurement framework for SaaS and B2B products with 50+ paying accounts: compute a weighted 0–100 health score from product usage (30%), feature adoption (25%), support sentiment (20%), engagement (15%), and payment health (10%); track NPS, CSAT, time-to-value, adoption rate, expansion rate, and Net Revenue Retention monthly; automate alerts at score thresholds; and review cohort patterns to identify churn signals before they become cancellations.

## Why

Without a health score, churn is invisible until the cancellation email arrives. Leading indicators (usage decay, support escalations, feature abandonment) precede cancellation by 30–90 days — enough time to intervene. NRR below 100% means new-logo acquisition must outrun a leaking bucket; health scoring converts that from a reactive sprint into a proactive weekly triage.

## When To Use

- B2B/SaaS with more than 50 paying accounts where manual relationship management no longer scales
- Net Revenue Retention below 100% and you need to systematize early-warning signals
- Onboarding a CS function and need an objective health score to triage book-of-business
- Replacing gut-feel quarterly reviews with a measurable monthly cadence

## When NOT To Use

- Pre-PMF or fewer than ~20 customers — talking to every customer directly beats any score
- Pure self-serve consumer products where 1:1 outreach has negative ROI
- When event tracking is not instrumented — health scores on unreliable data produce false alerts and erode trust
- When the team cannot act on alerts — a score with nobody to follow up is theater

## Content

| File | What's inside |
|------|---------------|
| `content/01-health-score.xml` | Component weights, scoring rubric (usage/feature/support/engagement/payment), health bucket thresholds and actions |
| `content/02-key-metrics.xml` | NPS, CSAT, time-to-value, feature adoption, expansion rate, NRR definitions with formulas and targets |
| `content/03-automation-and-gotchas.xml` | Alert automation flow, monthly review process, leading vs. lagging indicators, AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-dashboard.md` | Monthly health distribution table, at-risk accounts list, expansion-ready list |
| `templates/metric-tracking.md` | Monthly metrics table: NPS, CSAT, TTV, adoption, expansion, NRR vs. targets |
| `templates/health.py` | Weighted health score function (0–100) and bucket classifier |
