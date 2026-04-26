# Azure DevOps Boards

## Summary

Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API. Integrates natively with Azure Pipelines, Repos, and Test Plans. Agents operate via PAT-scoped REST API or `az boards` CLI; treat process-template definitions as YAML stored in version control.

## Why

Enterprise Microsoft-stack organisations need a single project management layer that integrates with Entra ID (SSO), Azure DevOps Pipelines (build traceability), and Power BI (Analytics OData). The CMMI template provides built-in Risk, Change Request, and Review work item types required for regulated industries. `AB#<id>` commit syntax links code changes to work items automatically.

## When To Use

- Microsoft-ecosystem organisations requiring Entra ID SSO and tenant-level governance
- Regulated or audit-heavy projects needing CMMI work item types and audit trail
- Teams using Azure Pipelines/Repos/Test Plans — Boards integrates build, PR, and release traceability
- Portfolio reporting via Azure DevOps Analytics + Power BI
- Hybrid on-prem (Azure DevOps Server) requirements where SaaS Jira is not permitted

## When NOT To Use

- Engineering-only teams preferring Linear or GitHub Projects — ADO Boards UI is heavier
- Teams primarily on GitHub — GitHub Projects v2 avoids identity and permission duplication
- Open-source or community projects — ADO licensing assumes commercial accounts
- Lightweight single-team Kanban — Trello, ClickUp, or Linear ship faster with less configuration

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Process template selection, work-item hierarchy, board config, WIP limits, Area/Iteration paths |
| `content/02-queries-and-automation.xml` | WIQL examples, automation rules, Pipeline integration, REST API patterns, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-story.md` | User Story with As-a/I-want/So-that and Gherkin acceptance criteria |
| `templates/sprint-planning.md` | Sprint planning document with capacity table, backlog, risks, DoD |
| `templates/ado-create-story.py` | Python script: create a User Story and link to a Feature parent via REST API |
