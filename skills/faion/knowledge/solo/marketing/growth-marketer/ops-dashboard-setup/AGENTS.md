# Dashboard Setup

## Summary

A framework for centralizing business metrics into a single, actionable view. Covers
dashboard design principles, metric selection (5-10 max), data source connections, and
reporting cadences (daily pulse, weekly review, monthly report). The core rule: every
metric on a dashboard must be one you can act on — lagging vanity metrics belong in
archives, not on the dashboard.

## Why

Metrics scattered across tools (Stripe, Google Analytics, CRM, product analytics)
create decision lag. A single dashboard surface reduces time-to-insight from hours
to seconds, enables pattern detection across correlated metrics (e.g., CAC vs LTV),
and makes weekly reviews actionable rather than archaeological.

## When To Use

- No single view of business health exists across revenue, customers, and marketing
- Weekly review meetings waste time hunting for numbers across tools
- Setting up a new SaaS or product business that needs an initial metrics system
- Quarterly planning requires trend visibility across multiple metric categories
- Switching analytics tools and need to rebuild reporting infrastructure

## When NOT To Use

- Business has fewer than 10 customers — a simple spreadsheet outperforms a dashboard
- Metrics are undefined or inconsistently tracked — fix data collection first
- No one will review the dashboard regularly — a stale dashboard is worse than none
- Dashboard tool requires data warehouse setup that hasn't been built yet

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-principles.xml` | Dashboard types, design principles, metric selection criteria, layout pattern |
| `content/02-metric-categories.xml` | Revenue metrics (MRR, churn, LTV:CAC), customer metrics, marketing funnel metrics |
| `content/03-reporting-templates.xml` | Monthly metrics tracker structure, channel performance table, insights format |

## Templates

| File | Purpose |
|------|---------|
| `templates/monthly-metrics-tracker.md` | Spreadsheet structure: revenue, customers, unit economics, marketing |
| `templates/dashboard-spec.md` | Dashboard specification: purpose, audience, metrics, visualizations |
| `templates/monthly-report.md` | Monthly report template: executive summary, KPIs, channel performance |
