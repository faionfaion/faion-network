---
slug: jira-workflow-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Configure Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, board configuration, API token scope.
content_id: "9a8b7c6d5e4f3a2b"
complexity: medium
produces: config
est_tokens: 4200
tags: [jira, workflow, automation, jql, project-management]
---
# Jira Workflow Management

## Summary

**One-sentence:** Configure Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, board configuration, API token scope.

**One-paragraph:** Configure Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, board configuration, API token scope.

**Ефективно для:**

- Команд, що уже на Atlassian-стеку (Confluence + Jira + Bitbucket).
- Enterprise проектів, що потребують fine-grained permissions per role.
- JSM-команд, що поєднують service-desk з dev workflow.
- Scaled-Agile (SAFe) розгортань з кількома команд-рівнями.

## Applies If (ALL must hold)

- Team uses Atlassian Cloud or Data Center with admin access.
- Workflow customisation needed beyond default Scrum/Kanban.
- API token scoped to minimum (read:jira-work + write:jira-work).
- JQL queries can be authored or imported.

## Skip If (ANY kills it)

- &lt;10-person engineering-only team — Linear is faster.
- GitHub-first team — use GitHub Projects v2.
- Microsoft stack — use ADO Boards.
- Free-tier Jira with strict limits — workflow customisation blocked.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Why Jira was picked. |
| [[change-control]] | Workflow changes routed through CR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `issue-type-scheme-author` | sonnet | Design issue-type scheme + screens. |
| `workflow-designer` | sonnet | States + transitions + conditions + validators. |
| `automation-rule-author` | haiku | Emit Jira automation rule YAML. |
| `jql-query-author` | haiku | Compose saved JQL queries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/jira-workflow.yaml` | Workflow definition: states, transitions, conditions, validators. |
| `templates/jql-queries.yaml` | Day-1 saved JQL queries. |
| `templates/automation-rules.yaml` | Automation rule set. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jira-workflow-management.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[azure-devops-boards]]
- [[gitlab-boards]]
- [[pm-tool-selection]]
- [[cross-tool-migration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (atlassian_tier, team_size, workflow_complexity) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
