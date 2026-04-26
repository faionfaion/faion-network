# Azure DevOps Boards

## Summary

Azure DevOps Boards is Microsoft's enterprise project management solution supporting four process templates (Basic, Agile, Scrum, CMMI) with tight integration to Azure Pipelines, Repos, and Test Plans. The critical constraint: use Inherited processes only, pin one process per organization, and tie commits to work items via `AB#1234` in commit messages — this gives automatic traceability from requirement to build to release without third-party glue.

## Why

Microsoft-stack organizations gain the most from ADO Boards because Entra ID (AAD), Azure Pipelines, and Repos integrate at the identity layer — PAT scopes, area-path security, and pipeline environments all share the same permission model. The Analytics OData feed enables Power BI dashboards that WIQL cannot produce for multi-sprint trends without a separate data warehouse.

## When To Use

- Microsoft-stack organizations already on Azure (Entra, Azure Pipelines, Repos, Test Plans).
- Regulated industries (CMMI process template) needing audit trails on every state transition.
- Teams wanting work-item to commit to build to release traceability without third-party glue.
- Enterprise portfolios where Epic → Feature → Story → Task hierarchy maps to OKRs or quarterly planning.
- Organizations standardizing on a single vendor to consolidate tool sprawl.

## When NOT To Use

- Pure SaaS or non-Microsoft ecosystem — ADO is heavyweight outside the Azure stack.
- Small / fast-moving startups — Linear, Shortcut, or GitHub Projects feel significantly lighter.
- Open-source projects with external contributors — onboarding to ADO creates friction.
- Teams needing a modern mobile UX — ADO Boards trails Linear, Jira, and Shortcut on UI quality.
- Heavy process customization beyond inheritance — XML "Hosted XML" is deprecated in cloud.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-setup.xml` | Process templates comparison, work-item hierarchy, board configuration, sprint and area-path setup. |
| `content/02-queries-automation.xml` | WIQL query patterns, automation rules, pipeline integration, Analytics vs WIQL trade-offs. |
| `content/03-agent-usage.xml` | Agentic workflows: ado-work-item-creator, ado-query-runner, ado-board-auditor. Gotchas (ADF, WIQL quirks, rate limits). |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-story.sh` | Bash script to create a User Story work item via REST API with title, iteration, and area path. |
| `templates/user-story.md` | User Story template with Gherkin acceptance criteria and dependency fields. |
