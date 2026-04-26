# Google Ads Reporting & Optimization

## Summary

A data-driven optimization cycle for Google Ads accounts: monitor key metrics, analyze segments (device, daypart, location, audience), triage search terms weekly, and execute targeted actions. The cycle is Monitor → Analyze → Diagnose → Optimize. Quality Score tracks ad relevance and predicts CPA spikes 1-2 weeks ahead. Never make major structural changes more than once a month — frequent changes reset Smart Bidding learning.

## Why

Google Ads generates more signals than any human can review manually. Without a structured reporting cycle, advertisers make changes based on gut feeling, miss expensive non-converting search terms, and misread aggregate metrics that mask per-segment problems. A weekly search-terms triage alone often reduces CPA by 10-20% by eliminating wasted spend on irrelevant queries.

## When To Use

- Recurring weekly or monthly performance reports across multiple Google Ads accounts
- Search-terms triage: identifying expensive non-converting queries to add as negatives at scale
- Cross-segment diagnosis: device, daypart, location, and audience performance breakdowns
- Post-campaign attribution and budget reallocation reviews
- KPI threshold monitoring with alerts (CPA exceeded, impression share dropped, QS drop)

## When NOT To Use

- Real-time bid management — Google Ads' own automated bidding has more signal access and is faster
- Attribution across non-Google channels — use a multi-touch tool (GA4 + Looker, Triple Whale)
- Creative-quality scoring — requires design judgment, not metrics
- Strategic budget allocation across channels — use `ads-budget-optimization` instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-reports-metrics.xml` | Essential reports, key metrics, Quality Score breakdown, segment analysis |
| `content/02-optimization-cycle.xml` | Search terms analysis, optimization actions by symptom, reporting schedule |
| `content/03-agent-rules.xml` | GAQL gotchas: micros, conversion float, impression share fraction, privacy threshold |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-checklist.md` | Weekly optimization checklist: spend, conversions, CPA, actions taken |
| `templates/performance-report.md` | Period-over-period performance report template with campaign table |
| `templates/weekly-report.py` | GAQL helper: campaign metrics last N days, search terms for negatives |
