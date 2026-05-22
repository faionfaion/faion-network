---
slug: azure-devops-boards
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API.
content_id: "0016db00e9ec3678"
tags: [azure-devops, boards, project-management, kanban, scrum]
---
# Azure DevOps Boards

## Summary

**One-sentence:** Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API.

**One-paragraph:** Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API. Integrates natively with Azure Pipelines, Repos, and Test Plans. Agents operate via PAT-scoped REST API or az boards CLI; treat process-template definitions as YAML stored in version control.

## Applies If (ALL must hold)

- Microsoft-ecosystem organisations requiring Entra ID SSO and tenant-level governance.
- Regulated or audit-heavy projects needing CMMI work item types and audit trail.
- Teams using Azure Pipelines/Repos/Test Plans — Boards integrates build, PR, and release traceability.
- Portfolio reporting via Azure DevOps Analytics + Power BI.
- Hybrid on-prem (Azure DevOps Server) requirements where SaaS Jira is not permitted.

## Skip If (ANY kills it)

- Engineering-only teams preferring Linear or GitHub Projects — ADO Boards UI is heavier.
- Teams primarily on GitHub — GitHub Projects v2 avoids identity and permission duplication.
- Open-source or community projects — ADO licensing assumes commercial accounts.
- Lightweight single-team Kanban — Trello, ClickUp, or Linear ship faster with less configuration.

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

- parent skill: `pro/pm/project-manager/`
