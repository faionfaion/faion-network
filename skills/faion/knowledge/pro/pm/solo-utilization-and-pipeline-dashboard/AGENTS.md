---
slug: solo-utilization-and-pipeline-dashboard
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Lightweight utilization-and-pipeline dashboard (spreadsheet or Notion) for a freelance practice — drives rate decisions and prevents feast-or-famine.
content_id: "c76521c31dae8ca2"
tags: [solo-utilization-and-pipeline-dashboard, pm, pro]
---
# Solo Utilization & Pipeline Dashboard

## Summary

**One-sentence:** A lightweight utilization-and-pipeline dashboard that tracks billable %, realised $/hr, and pipeline coverage so a freelancer can make defensible rate-raise and capacity decisions quarterly.

**One-paragraph:** Generic `reporting-dashboards` methodologies are tool-focused (Looker / Tableau / Mode). A freelance practice doesn't need a tool — it needs the right four metrics: weekly utilization %, realised $/hr (billed revenue / total worked hours, INCLUDING admin), pipeline coverage (signed + qualified next-90d revenue / target), and rate trend over time. This methodology fixes those four, the exact formulas, and the quarterly review cadence that turns the numbers into a rate decision.

## Applies If (ALL must hold)

- the operator earns from billable services (T&M, fixed-price, retainer)
- the operator wants rate decisions to be defensible against their own data
- the operator already tracks hours somewhere (Toggl / Harvest / a sheet)
- engagements are long enough that pipeline coverage is meaningful (4+ weeks)

## Skip If (ANY kills it)

- revenue is product-led (SaaS / digital downloads) — utilization doesn't apply
- the operator is fully booked on a single retainer and has no pipeline to track
- a real PSA (Harvest Forecast, Float, Productive) is already in place — use it
- the operator is in a salaried role; utilization is their employer's problem

## Prerequisites

- a time-tracking habit (any tool) covering at least the last 4 weeks
- a written floor rate and target rate
- an opportunity log (signed / qualified / unqualified pipeline rows)
- a clear definition of "weekly capacity hours" (e.g., 30 billable target)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent skill |
| `pro/pm/capacity-planning-realistic` | sibling — feeds the weekly-capacity-hours input |
| `pro/marketing/rate-raise-conversation-script` | downstream — consumer of rate-trend output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: four-metrics-fixed, realised-rate-includes-admin, pipeline-90d-window, quarterly-review-cadence, rate-decision-tied-to-data | ~1000 |

## Related

- parent skill: `pro/pm/project-manager`
- upstream playbook: `p3-technical-freelancer/Quarterly rate adjustment review`
- sibling: `pro/marketing/rate-raise-conversation-script`
