---
slug: azure-devops-boards
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Azure DevOps Boards is Microsoft's enterprise project management solution supporting four process templates (Basic, Agile, Scrum, CMMI) with tight integration to Azure Pipelines, Repos, and Test Plans.
content_id: "0016db00e9ec3678"
tags: [azure-devops, project-management, microsoft-stack, enterprise, wiql]
---
# Azure DevOps Boards

## Summary

**One-sentence:** Azure DevOps Boards is Microsoft's enterprise project management solution supporting four process templates (Basic, Agile, Scrum, CMMI) with tight integration to Azure Pipelines, Repos, and Test Plans.

**One-paragraph:** Azure DevOps Boards is Microsoft's enterprise project management solution supporting four process templates (Basic, Agile, Scrum, CMMI) with tight integration to Azure Pipelines, Repos, and Test Plans. The critical constraint: use Inherited processes only, pin one process per organization, and tie commits to work items via AB#1234 in commit messages — this gives automatic traceability from requirement to build to release without third-party glue.

## Applies If (ALL must hold)

- Microsoft-stack organizations already on Azure (Entra, Azure Pipelines, Repos, Test Plans).
- Regulated industries (CMMI process template) needing audit trails on every state transition.
- Teams wanting work-item to commit to build to release traceability without third-party glue.
- Enterprise portfolios where Epic → Feature → Story → Task hierarchy maps to OKRs or quarterly planning.
- Organizations standardizing on a single vendor to consolidate tool sprawl.

## Skip If (ANY kills it)

- Pure SaaS or non-Microsoft ecosystem — ADO is heavyweight outside the Azure stack.
- Small / fast-moving startups — Linear, Shortcut, or GitHub Projects feel significantly lighter.
- Open-source projects with external contributors — onboarding to ADO creates friction.
- Teams needing a modern mobile UX — ADO Boards trails Linear, Jira, and Shortcut on UI quality.
- Heavy process customization beyond inheritance — XML "Hosted XML" is deprecated in cloud.

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

- parent skill: `pro/pm/pm-agile/`
