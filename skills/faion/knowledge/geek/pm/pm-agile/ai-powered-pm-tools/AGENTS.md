# AI-Powered PM Tools 2026

## Summary

Selection and integration guide for AI-augmented project management tools (Jira+Rovo, ClickUp Brain, Monday.com AI agents) in Agile contexts. Concrete trigger: when your team spends > 2h/sprint writing stories, grooming backlogs, or producing retrospective summaries that an AI agent can draft as starting input.

## Why

AI work breakdown, ceremony automation, and sprint velocity prediction eliminate repetitive PM overhead. Tools differ in API composability — Jira/Linear/GitHub Projects expose REST/GraphQL that Claude subagents can drive; vendor-embedded AI (Rovo, ClickUp Autopilot) is not yet API-composable. Understanding which layer to automate prevents building the wrong thing.

## When To Use

- Backlog grooming generates repetitive subtasks and acceptance criteria a model can draft
- Sprint planning takes > 1h because estimates and breakdowns happen verbally without preparation
- Retrospective summaries must be produced quickly from issue data after each sprint
- Evaluating Jira, Linear, ClickUp, or GitHub Projects for AI feature adoption
- Integrating a Claude subagent with a PM API (Jira REST v3, Linear GraphQL, GitHub Projects GraphQL)

## When NOT To Use

- Team forming (< 3 sprints): AI tooling before stable team dynamics disrupts trust-building
- Cross-squad dependency management: AI work breakdown tools are single-project scoped
- SAFe/healthcare/defense Agile: AI-generated artifacts require compliance review not supported by current tooling
- Retrospective ceremonies that already run well and lightweight: adding tooling adds overhead without benefit
- New teams with fewer than 6 sprints of history: velocity prediction produces noise, not signal

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-comparison.xml` | Feature comparison of Jira+Rovo, Monday.com, ClickUp, Wrike, Linear; API composability matrix |
| `content/02-agile-integration.xml` | Sprint planning and retrospective prompt patterns; agent workflow; CLI tools; gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-planning-prompt.txt` | XML prompt for AI-assisted story breakdown with ACs and DoD |
| `templates/retrospective-prompt.txt` | XML prompt for sprint retrospective summary from issue data |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/linear-sprint-summary.sh` | Bash: fetch active cycle tasks from Linear GraphQL API |
