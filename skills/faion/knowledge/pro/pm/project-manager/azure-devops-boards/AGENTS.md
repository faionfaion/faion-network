---
slug: azure-devops-boards
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Azure DevOps Boards configuration spec (process template, hierarchy, board columns, WIP limits, area/iteration paths, REST API agent access) for Microsoft-stack enterprise teams.
content_id: "0016db00e9ec3678"
complexity: medium
produces: config
est_tokens: 4100
tags: [azure-devops, boards, project-management, kanban, scrum]
---
# Azure DevOps Boards

## Summary

**One-sentence:** Azure DevOps Boards configuration spec (process template, hierarchy, board columns, WIP limits, area/iteration paths, REST API agent access) for Microsoft-stack enterprise teams.

**One-paragraph:** Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API. Integrates natively with Azure Pipelines, Repos, and Test Plans. Agents operate via PAT-scoped REST API or `az boards` CLI; treat process-template definitions as YAML stored in version control.

**Ефективно для:**

- Microsoft-ecosystem організацій з Entra ID SSO + tenant governance.
- Regulated/audit-heavy проектів, що вимагають CMMI work-item types та повний audit trail.
- Команд із Azure Pipelines/Repos/Test Plans — Boards дає build, PR і release traceability.
- Portfolio reporting через Azure DevOps Analytics + Power BI.

## Applies If (ALL must hold)

- Organisation has an Azure DevOps Services or Server tenant with Entra ID.
- Team needs Boards + Pipelines/Repos integration (AB#&lt;id&gt; commit linking).
- Regulated workflow OR formal change-request governance required.
- Agents authenticated with scoped PAT (Work Items: Read &amp; Write, no Full-access).

## Skip If (ANY kills it)

- Pure GitHub stack — use GitHub Projects v2; avoid identity duplication.
- Engineering-only ≤10-person team — Linear is faster, lighter UI.
- Open-source or community project — ADO licensing assumes commercial accounts.
- Single-team lightweight Kanban — Trello / ClickUp ship in hours, not days.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADO project URL | `https://dev.azure.com/{org}/{project}` | platform admin |
| PAT (scoped: Work Items r/w, no full) | secret | 1Password / Azure Key Vault |
| Process template choice | enum {Basic, Agile, Scrum, CMMI} | governance decision |
| Area/Iteration tree | YAML | architecture team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Upstream decision picking ADO over Jira/Linear/etc. |
| [[jira-workflow-management]] | Peer reference for the alternative if Jira route is taken instead. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: template-inheritance, area-vs-iteration, WIP-limit, PAT-scope, AB-linking, skip-this-methodology | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema for the config artefact (process, board columns, swimlanes, area/iteration tree) | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick template → import tree → configure board → wire PAT → validate | 800 |
| `content/06-decision-tree.xml` | essential | ADO vs alternatives + template choice routing | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `template-pick` | sonnet | Judgment over governance constraints vs team weight. |
| `tree-author` | haiku | Mechanical YAML emission for area/iteration tree. |
| `board-wire` | sonnet | WIP + swimlane + card-style synthesis. |
| `validate-and-commit` | haiku | Run the validator, commit the YAML. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ado-boards-config.yaml` | YAML skeleton for process + area/iteration + board columns + swimlanes. |
| `templates/wiql-saved-queries.yaml` | Example saved WIQL queries the team should ship from day 1. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-devops-boards.py` | Validate the YAML config against the schema | Pre-commit on every config change |

## Related

- [[jira-workflow-management]]
- [[gitlab-boards]]
- [[pm-tool-selection]]
- [[cross-tool-migration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps three observables (ecosystem ∈ Microsoft/GitHub/Atlassian, regulatory profile, team size) to apply / pick alternative / skip. Each leaf references a rule from `01-core-rules.xml`.
