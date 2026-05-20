---
slug: ops-dashboard-setup
tier: solo
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A framework for centralizing business metrics into a single, actionable view.
content_id: "bc0b5fbc7556bdd3"
tags: [dashboard, metrics, reporting, kpis, business-operations]
---
# Dashboard Setup

## Summary

**One-sentence:** A framework for centralizing business metrics into a single, actionable view.

**One-paragraph:** A framework for centralizing business metrics into a single, actionable view. Covers dashboard design principles, metric selection (5-10 max), data source connections, and reporting cadences (daily pulse, weekly review, monthly report). The core rule: every metric on a dashboard must be one you can act on — lagging vanity metrics belong in archives, not on the dashboard.

## Applies If (ALL must hold)

- No single view of business health exists across revenue, customers, and marketing
- Weekly review meetings waste time hunting for numbers across tools
- Setting up a new SaaS or product business that needs an initial metrics system
- Quarterly planning requires trend visibility across multiple metric categories
- Switching analytics tools and need to rebuild reporting infrastructure

## Skip If (ANY kills it)

- Business has fewer than 10 customers — a simple spreadsheet outperforms a dashboard
- Metrics are undefined or inconsistently tracked — fix data collection first
- No one will review the dashboard regularly — a stale dashboard is worse than none
- Dashboard tool requires data warehouse setup that hasn't been built yet

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/marketing/growth-marketer/`
