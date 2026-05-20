---
slug: reporting-dashboards
tier: solo
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Automated PM reporting: tool-specific dashboard configuration (Jira, Linear, ClickUp), scheduled report generation for weekly status and sprint reviews, Slack digest delivery, and BI tool integration (PowerBI, Metabase, Grafana) via API ETL.
content_id: "7b137610735ebaf5"
tags: [reporting, dashboards, automation, metrics, slack]
---
# Reporting Dashboards

## Summary

**One-sentence:** Automated PM reporting: tool-specific dashboard configuration (Jira, Linear, ClickUp), scheduled report generation for weekly status and sprint reviews, Slack digest delivery, and BI tool integration (PowerBI, Metabase, Grafana) via API ETL.

**One-paragraph:** Automated PM reporting: tool-specific dashboard configuration (Jira, Linear, ClickUp), scheduled report generation for weekly status and sprint reviews, Slack digest delivery, and BI tool integration (PowerBI, Metabase, Grafana) via API ETL. Report agents query PM tools as read-only, validate data before sending (zero committed → abort, not 0% completion), and archive every generated report. Dashboard data is only as clean as underlying PM data — garbage in, garbage out.

## Applies If (ALL must hold)

- Sprint-cadence status reporting requires manual data collection from multiple PM tools (Jira + Linear + spreadsheets), and the same numbers are computed every week.
- Stakeholders need a consolidated view across several projects without PM tool access (executives, customers, cross-team partners).
- PM tool native reports are insufficient and data needs cross-referencing with external sources (deploy frequency, error rates, support tickets).
- Automated Slack digests are required on a fixed schedule (daily standup summary, weekly status, end-of-sprint review).
- PM data must feed a BI tool (Metabase / PowerBI / Grafana) for multi-sprint trend analysis.
- Trigger phrases from a human PM that map to this methodology: "automate weekly status", "send sprint summary to Slack", "build executive dashboard", "feed Jira metrics into Metabase".

## Skip If (ANY kills it)

- Team of 1-3 people where a quick manual update is faster than building dashboard automation.
- PM tool's native dashboard covers all stakeholder needs — adding automation creates maintenance burden.
- Regulated environments needing report provenance and immutability — automated reports lack audit trails unless outputs are explicitly archived.
- Real-time operational dashboards (incident response) — PM dashboards lag by minutes to hours and are not suitable for on-call.

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

- parent skill: `solo/pm/project-manager/`
