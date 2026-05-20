---
slug: solo-kpi-dashboard-template
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Concrete dashboard spec — metrics, queries, tools, refresh cadence — for a $0–50k ARR solo SaaS to run a 30-minute Friday pulse without a BI engineer.
content_id: "acae0ebb1ca231d0"
tags: [solo-kpi-dashboard-template, product, solo]
---
# Solo KPI Dashboard Template

## Summary

**One-sentence:** A copy-pasteable KPI dashboard spec for a solo SaaS at $0–50k ARR — six metrics, exact queries, tool choices, refresh cadence.

**One-paragraph:** Generic ops-dashboard methodology assumes a team and a stack (BI, warehouse, dashboarding tool). A solo operator at sub-$50k ARR needs the opposite: a fixed, minimal dashboard that takes 30 minutes to build, runs on Plausible + Stripe + Postgres directly, and is reviewable Friday afternoon in 10 minutes. This template hard-codes the six metrics that matter at this stage (signups, activation, MRR, gross churn, support tickets, weekly active accounts), the exact SQL or API call to compute each, and the refresh rule. It is deliberately narrow.

## Applies If (ALL must hold)

- product is a paid SaaS with self-serve signup
- ARR is between $0 and $50k
- there is one operator (solo founder)
- billing runs on Stripe / Paddle / Lemon Squeezy

## Skip If (ANY kills it)

- ARR is over $50k and a real BI tool (Metabase / Mode / Hex) is justified
- product is non-SaaS (one-off purchases, marketplace, agency)
- a paid analytics team already maintains a dashboard — don't duplicate

## Prerequisites

- read-only Stripe API key
- Plausible / Posthog / GA4 site already configured
- read-only Postgres connection (or equivalent)
- a Notion / Coda / Google Sheets surface to host the dashboard

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent skill |
| `solo/pm/solo-mrr-dashboard-template` | MRR is one of the six tiles; uses that spec |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: six-tiles-max, sql-or-api-only, friday-30-min, one-source-of-truth, no-vanity-metrics | ~900 |

## Related

- parent skill: `solo/product/product-planning`
- upstream playbook: `p1-solo-saas-builder/Friday metrics check & MRR pulse`
- sibling: `solo/pm/solo-mrr-dashboard-template`
