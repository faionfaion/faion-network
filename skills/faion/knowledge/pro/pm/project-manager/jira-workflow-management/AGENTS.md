# Jira Workflow Management

## Summary

Configure and operate Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, and board configuration. The rule is one workflow scheme per issue type first — bespoke per-project workflows multiply maintenance cost without proportional benefit.

## Why

Jira's power is also its foot-gun: shared workflow schemes mean one project's change breaks others, automation rule loops are trivially created, and custom field sprawl slows the entire site. Explicit workflow design and automation governance prevents these compounding failures. JQL `validateQuery=strict` catches hallucinated field names before they silently return empty results.

## When To Use

- Setting up a new Jira project (Scrum, Kanban, or JSM) from scratch
- Standardizing 3+ inconsistent project workflows after acquisition or reorg
- Replacing manual triage/assignment with automation rules
- Wiring Jira into CI/CD (auto-transition on deploy, link to PR)
- Migrating from Jira Server/DC to Cloud (workflow + scheme rebuild)
- Building JQL reports for sprint health, blockers, or release scope

## When NOT To Use

- Team < 5 with simple Trello-grade needs — Jira ROI inverts at small scale
- Throwaway 2-week prototype — workflow tax exceeds value delivered
- When the goal is "make Jira look like Linear" — replace Jira instead
- Pure documentation projects — use Confluence, not Jira

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow-design.xml` | Issue types, workflow states/transitions, validators, board setup rules |
| `content/02-automation-jql.xml` | Automation rule patterns, JQL query examples, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/workflow.yaml` | Workflow statuses and transitions skeleton |
| `templates/sprint-plan.md` | Sprint planning table with goal, capacity, committed items |
| `templates/definition-of-done.md` | DoD checklist for Story/Bug issue types |
| `templates/custom-fields.yaml` | Custom field definitions (type, screen placement) |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/apply-workflow.sh` | Push workflow JSON to a Jira Cloud sandbox via REST API |
| `scripts/bulk-jql-update.py` | Bulk-transition issues matching a JQL query with rate-limit safety |
