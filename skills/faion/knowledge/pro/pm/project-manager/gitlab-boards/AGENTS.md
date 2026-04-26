# GitLab Boards

## Summary

GitLab Issue Boards provide kanban-style project management integrated with GitLab's DevOps platform. Boards visualize issues through scoped labels (`workflow::*`, `priority::*`, `type::*`), WIP limits, iterations, and CI-driven automation — giving engineering teams a unified DevOps + PM plane without a separate tracker.

## Why

Teams already on GitLab for source control and CI/CD eliminate context-switching by managing work inside the same system that runs their pipelines. Scoped labels enforce mutual exclusivity per state machine (one `workflow::*` at a time), CI jobs move cards on MR events, and the Service Desk routes external requests into the same board — all accessible via REST and GraphQL for agent-driven automation.

## When To Use

- Engineering teams using GitLab for source control and CI/CD wanting one unified platform
- Self-hosted or compliance-constrained orgs (defense, finance, healthcare) where GitLab CE/EE on-prem is the only option
- Group-of-projects needing cross-repo visibility via group-level boards
- DevSecOps pipelines where vulnerabilities should auto-become issues on the same board
- Teams using GitLab Iterations for sprint cadence and Roadmaps (Premium) for portfolio views

## When NOT To Use

- Teams not using GitLab for code — Linear, Jira, or GitHub Projects fit better
- Heavy custom-field requirements with cross-issue rollups and pivot dashboards — GitLab boards are deliberately simple
- Marketing or non-engineering teams needing rich content management — Asana, Notion, or ClickUp fit better
- Free-tier projects needing WIP limits, scoped iterations, or roadmap timelines — those are Premium/Ultimate features
- Highly regulated portfolios needing EVM, official gantts, or PMO-grade reporting — GitLab is light on EVM

## Content

| File | What's inside |
|------|---------------|
| `content/01-board-setup.xml` | Board types, scoped label taxonomy, board configuration rules, WIP limits |
| `content/02-workflow.xml` | Agentic automation patterns, subagent roles, prompt pattern for triage-router |
| `content/03-tools-and-references.xml` | CLI tools, SaaS integrations, best practices, AI-agent gotchas, references |

## Templates

| File | Purpose |
|------|---------|
| `templates/labels.yaml` | Scoped label taxonomy (workflow, priority, type, severity) ready to apply via gitlabform |
| `templates/issue-bug.md` | Bug report issue template for `.gitlab/issue_templates/` |
| `templates/issue-feature.md` | Feature request issue template |
| `templates/mr-default.md` | Default merge request template |
| `templates/stale-in-progress.py` | Script: audit project for issues idle in `workflow::in-progress` beyond N days |
