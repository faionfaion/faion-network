# PLG Metrics and Tracking

## Summary

A metrics methodology for Product-Led Growth: the full funnel from acquisition through expansion, including activation rate, time-to-value (TTV), free-to-paid conversion, Product-Qualified Lead (PQL) scoring, net revenue retention (NRR), and cohort analysis. Every metric must have a single owner, a machine-verifiable definition tied to a single event in a single table, and a "who acts and how" runbook line attached to each dashboard tile.

## Why

Single-number product metrics hide the truth about PLG health. NRR above 100% can conceal logo churn; global TTV median hides SMB vs. Enterprise variance. PQL scores drift as the product evolves and misroute sales motion within 1-2 quarters if not recalibrated. Metric definitions that live only in dashboards (not version-controlled) diverge silently from the underlying events. Cohort analysis is the floor — every metric must be cohorted to be actionable.

## When To Use

- Standing up a PLG dashboard with activation, conversion, expansion, and retention metrics in one place
- Defining or refining the activation event ("aha moment") and time-to-value for a SaaS product
- Designing a PQL scoring model from product behavior signals
- Running cohort analysis for retention and free-to-paid conversion
- Quarterly PLG strategy review where freemium vs. trial model and gating thresholds are on the table

## When NOT To Use

- Sales-led motions where the buyer never logs in before purchase — PLG metrics produce noise
- Pre-product-market-fit startups: vanity metrics dominate, PQL scoring overfits to a tiny sample
- Self-hosted or single-tenant deployments where event telemetry is not centralized
- Hardware or one-time-purchase products without recurring usage signals
- Regulated industries where logging granular user behavior requires consent gates that break funnel completeness

## Content

| File | What's inside |
|------|---------------|
| `content/01-metric-catalog.xml` | Core PLG metrics with formulas, benchmarks, and ownership rules |
| `content/02-pql-scoring.xml` | PQL signal weights, scoring thresholds, cohort analysis rules, and agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/pql-score.py` | Signal-weighted PQL scoring function with band classification |
| `templates/dashboard.md` | Monthly PLG metrics dashboard template with acquisition/activation/monetization/expansion/retention sections |
