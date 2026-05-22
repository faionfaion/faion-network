---
slug: jira-workflow-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Jira workflow management covers project setup, issue-type scheme design, workflow state machines, automation rules, and JQL queries for Scrum and Kanban teams.
content_id: "bccd99f4c2a7b0d7"
tags: [jira, workflow, automation, issue-tracking, jql]
---
# Jira Workflow Management

## Summary

**One-sentence:** Jira workflow management covers project setup, issue-type scheme design, workflow state machines, automation rules, and JQL queries for Scrum and Kanban teams.

**One-paragraph:** Jira workflow management covers project setup, issue-type scheme design, workflow state machines, automation rules, and JQL queries for Scrum and Kanban teams. Keep workflows to 5-7 statuses maximum and maintain one shared workflow per issue type across all projects to prevent scheme sprawl that breaks cross-project queries and slows performance.

## Applies If (ALL must hold)

- Bootstrapping a new Jira project for Scrum, Kanban, or Jira Service Management teams.
- Standardizing 3+ inconsistent project workflows after acquisition or reorg.
- Replacing manual triage and assignment with automation rules.
- Wiring Jira into CI/CD pipelines (auto-transition on deploy, link branches/PRs to issues).
- Migrating from Jira Server/Data Center to Cloud (workflow and scheme rebuild).

## Skip If (ANY kills it)

- Team smaller than 5 with Trello-grade needs — Jira's configuration tax inverts ROI.
- Throwaway 2-week prototype — workflow overhead exceeds value.
- Goal is "make Jira look like Linear" — replace Jira rather than fight it.
- Pure documentation projects — use Confluence, not Jira.
- Compliance forbids Atlassian Cloud and budget does not cover Data Center.

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
