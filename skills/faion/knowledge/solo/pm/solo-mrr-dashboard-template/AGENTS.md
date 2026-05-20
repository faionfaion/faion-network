---
slug: solo-mrr-dashboard-template
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: One-sheet MRR / churn / LTV dashboard spec calibrated for a one-operator SaaS — five canonical metrics, exact Stripe-API formulas, no finance team required.
content_id: "69bd7b540ce9b3c7"
tags: [solo-mrr-dashboard-template, pm, solo]
---
# Solo MRR Dashboard Template

## Summary

**One-sentence:** A copy-pasteable single-sheet spec for MRR, gross/net churn, ARPU, LTV, and customer count — pulled directly from Stripe's API, calibrated for one operator.

**One-paragraph:** Generic `ops-metrics-basics` defines MRR conceptually but assumes a finance team to compute it. Solo SaaS operators need the actual fields: which Stripe object to read, how to handle annual plans, how to treat refunds, how to roll up by month. This methodology fixes one canonical formula per metric, so reported numbers stop drifting between investor updates, support replies, and the founder's head.

## Applies If (ALL must hold)

- product bills recurring revenue via Stripe / Paddle / Lemon Squeezy
- operator is the only person reporting financials
- MRR is between $0 and $50k
- monthly + annual plans coexist (or will soon)

## Skip If (ANY kills it)

- billing is one-off purchases (no recurring) — use a different revenue dashboard
- finance team owns the source of truth — don't fork it
- MRR > $50k and a real subscription-analytics tool (ChartMogul / Baremetrics) already runs

## Prerequisites

- read-only Stripe API key with `subscriptions:read` and `invoices:read`
- a Google Sheet / Notion / Coda surface to host the dashboard
- list of all active plans with their `interval` (`month` / `year`) and `unit_amount`

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent skill |
| `solo/product/solo-kpi-dashboard-template` | sibling — MRR is one tile in the broader KPI sheet |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: annual-divided-by-12, refunds-subtract-not-cancel, frozen-month-snapshot, single-formula-per-metric, customer-equals-subscription-not-user | ~1000 |

## Related

- parent skill: `solo/pm/project-manager`
- upstream playbook: `p1-solo-saas-builder/$0 → $4K MRR bootstrap journey`
- sibling: `solo/product/solo-kpi-dashboard-template`
