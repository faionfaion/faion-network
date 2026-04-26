# Jira Workflow Management

## Summary

Jira workflow management covers project setup, issue-type scheme design, workflow state machines, automation rules, and JQL queries for Scrum and Kanban teams. The critical constraint: keep workflows to 5-7 statuses maximum and maintain one shared workflow per issue type — bespoke per-project workflows create scheme sprawl that breaks cross-project queries and slows the entire Jira instance.

## Why

Unconstrained Jira configuration accumulates custom fields (200-field cap), project-specific workflows, and automation rules that conflict with each other. Standardization enables org-wide JQL, shared dashboards, and automation that fires across projects. Jira's automation library has execution rate limits per Cloud tier; poorly-scoped rules burn the budget without delivering value.

## When To Use

- Bootstrapping a new Jira project for Scrum, Kanban, or Jira Service Management teams.
- Standardizing 3+ inconsistent project workflows after acquisition or reorg.
- Replacing manual triage and assignment with automation rules.
- Wiring Jira into CI/CD pipelines (auto-transition on deploy, link branches/PRs to issues).
- Migrating from Jira Server/Data Center to Cloud (workflow and scheme rebuild).

## When NOT To Use

- Team smaller than 5 with Trello-grade needs — Jira's configuration tax inverts ROI.
- Throwaway 2-week prototype — workflow overhead exceeds value.
- Goal is "make Jira look like Linear" — replace Jira rather than fight it.
- Pure documentation projects — use Confluence, not Jira.
- Compliance forbids Atlassian Cloud and budget does not cover Data Center.

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-setup.xml` | Project types, issue-type hierarchy, workflow state design, board configuration rules. |
| `content/02-automation-jql.xml` | Automation rule patterns, essential JQL queries, integration with GitHub/GitLab/CI/CD. |
| `content/03-agent-usage.xml` | Agentic workflows: workflow-author, automation-author, jql-builder, migration-mapper. Gotchas (ADF, rate limits, Cloud vs DC drift). |

## Templates

| File | Purpose |
|------|---------|
| `templates/workflow-states.yaml` | Standard development workflow statuses and transitions with validators. |
| `templates/bulk-transition.py` | Bulk JQL-driven issue transition with rate-limit safety and Retry-After handling. |
