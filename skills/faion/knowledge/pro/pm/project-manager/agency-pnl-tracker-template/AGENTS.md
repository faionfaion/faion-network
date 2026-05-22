---
slug: agency-pnl-tracker-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d997bd8241c0e04c"
summary: Micro-agency P&L template with project / retainer / productized revenue lines, contractor costs, and weekly cash-flow + utilization views.
tags: [pnl, agency, finance, cash-flow, utilization, micro-agency, retainer]
---
# Micro-Agency P&L Tracker Template

## Summary

**One-sentence:** Micro-agency P&L template with project / retainer / productized revenue lines, contractor costs, and weekly cash-flow + utilization views.

**One-paragraph:** Generic SaaS-flavored financial planning hides the levers a micro-agency founder pulls weekly (utilization, contractor margin, retainer concentration). Mechanism: spreadsheet (or Notion DB) with three revenue lines (project, retainer, productized) and three cost categories (contractor, fixed ops, founder draw) per month. Weekly view rolls up: hours utilization per team member, retainer concentration (top-3 client revenue share), contractor margin per role, runway in months. Monthly close updates a single dashboard. Outputs: Friday cash-flow + utilization snapshot, monthly P&L statement, quarterly retainer-concentration audit.

## Applies If (ALL must hold)

- micro-agency or freelance team (1-10 people including contractors)
- mix of project + retainer revenue (or planning to add retainer)
- founder is responsible for finance (no full-time bookkeeper / CFO)
- accounting software in use (Xero, QuickBooks, Wave, FreeAgent) for source-of-truth — tracker complements, doesn't replace

## Skip If (ANY kills it)

- SaaS / product company — use SaaS unit economics templates instead
- enterprise / 50+ person agency — multi-tier finance ops needed, not a single spreadsheet
- pre-revenue freelancer — keep it simpler, single sheet hours x rate is enough
- founder uses a full ERP — template is redundant

## Prerequisites (must be true before starting)

- 3 months of historical revenue + expense data
- time-tracking data per team member (Toggl, Harvest, Clockify)
- contractor rates per role + their billable hourly to clients
- list of active retainer clients with monthly value
- target weekly check-in time (Friday 17:00 is the canonical Friday cash-flow slot)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/cost-estimation` | Source of project cost baselines |
| `pro/product/product-operations/account-health-scoring-model` | Health score per client informs retainer-concentration risk |
| `pro/research/researcher/agency-revenue-mix-audit-template` | Quarterly deeper dive consumes the P&L data |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 3-revenue-line structure, weekly utilization, retainer concentration cap, contractor-margin floor, monthly close discipline | ~900 |
| `content/02-output-contract.xml` | essential | Weekly snapshot schema, monthly P&L schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (revenue-line confusion, utilization fiction, single-client risk, hidden contractor cost, end-of-month reconciliation lag, vanity gross over net) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `weekly_snapshot_rollup` | haiku | Template fill from time-tracking + invoicing data |
| `concentration_risk_alert` | sonnet | Cross-client analysis: top-3 share threshold |
| `contractor_margin_audit` | sonnet | Per-role profitability check |
| `quarter_close_synthesis` | opus | Cross-month narrative for quarterly review |

## Templates

| File | Purpose |
|------|---------|
| `templates/pnl-spreadsheet.md` | Sheet structure: revenue lines, cost categories, weekly + monthly views |
| `templates/friday-snapshot.md` | Friday 5-min check-in template |
| `templates/monthly-close-checklist.md` | Steps to lock the month + update the dashboard |
| `templates/retainer-concentration-alert.md` | Trigger template when top-1 client exceeds threshold |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-weekly-snapshot.py` | Pull time + invoicing → produce Friday snapshot | Weekly Friday morning |
| `scripts/check-retainer-concentration.py` | Compute top-1 / top-3 client revenue share, alert if &gt; thresholds | Monthly + on new retainer signing |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `cost-estimation`, `quarterly-retainer-review-script`, `agency-revenue-mix-audit-template`
- external: [Profit First (Mike Michalowicz)](https://mikemichalowicz.com/profit-first/) · [BTAR - Bill The Agency Resource](https://bookkeepingstandard.com/) · [Forecast - Agency P&L templates](https://www.forecast.app/blog)
