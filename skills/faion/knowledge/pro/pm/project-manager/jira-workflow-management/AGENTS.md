---
slug: jira-workflow-management
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure and operate Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, and board configuration.
content_id: "bccd99f4c2a7b0d7"
tags: [jira, workflow, project-management, automation, jql]
---
# Jira Workflow Management

## Summary

**One-sentence:** Configure and operate Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, and board configuration.

**One-paragraph:** Configure and operate Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, and board configuration. The rule is one workflow scheme per issue type first — bespoke per-project workflows multiply maintenance cost without proportional benefit.

## Applies If (ALL must hold)

- Setting up a new Jira project (Scrum, Kanban, or JSM) from scratch
- Standardizing 3+ inconsistent project workflows after acquisition or reorg
- Replacing manual triage/assignment with automation rules
- Wiring Jira into CI/CD (auto-transition on deploy, link to PR)
- Migrating from Jira Server/DC to Cloud (workflow + scheme rebuild)
- Building JQL reports for sprint health, blockers, or release scope

## Skip If (ANY kills it)

- Team < 5 with simple Trello-grade needs — Jira ROI inverts at small scale
- Throwaway 2-week prototype — workflow tax exceeds value delivered
- When the goal is "make Jira look like Linear" — replace Jira instead
- Pure documentation projects — use Confluence, not Jira

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
