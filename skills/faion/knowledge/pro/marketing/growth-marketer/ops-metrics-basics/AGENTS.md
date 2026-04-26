# Ops Metrics Basics

## Summary

A practical metrics management system for solopreneurs and small teams: choose 5-10 actionable metrics, implement collection from existing data sources, set targets and alerts, and establish a review cadence (daily pulse, weekly review, monthly deep-dive). Includes all core SaaS metric formulas (MRR, ARR, churn, LTV, CAC, ARPU, net retention).

## Why

Operating on gut feeling produces late signals. A minimal metrics stack with automated collection, green/yellow/red status, and a fixed review rhythm converts data into timely decisions without requiring a data team. The discipline is choosing fewer metrics, not more.

## When To Use

- Early-stage product that has some paying users but no formal metrics system.
- Solo operator who needs to answer "how is business?" with real numbers on demand.
- Team misaligned on what constitutes good/bad performance for the current phase.
- Setting up Stripe → Sheets → Looker Studio pipeline for the first time.

## When NOT To Use

- Pre-revenue product — no payment data means the core metrics are undefined.
- Enterprises with dedicated BI teams — this pattern targets lean operations, not warehouse-scale analytics.
- When you want deep behavioral analytics — use product analytics tools (Mixpanel, Amplitude) instead of this ops-level framework.

## Content

| File | What's inside |
|------|---------------|
| `content/01-metric-selection.xml` | Metric categories (north star, leading, lagging, input, output), solopreneur essential metrics table. |
| `content/02-tracking-and-review.xml` | Data sources, tracking stack options, target-setting, alert triggers, review cadence. |
| `content/03-formulas-and-antipatterns.xml` | All core SaaS metric formulas with definitions, common mistakes table. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-review.md` | Weekly review template: metrics table, went-well, needs-attention, next-week actions. |
