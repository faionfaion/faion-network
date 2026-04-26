# Linear Issue Tracking

## Summary

Linear is a keyboard-first, speed-optimized issue tracker for engineering teams with a fixed hierarchy: Workspace → Team → Cycle (sprint) → Issue. Cycles provide time-boxing; Projects group issues across cycles into initiatives. Cycle assignment via API must target `nextCycle` or `futureCycle` only — never the active cycle — to protect scope. Priority is an integer enum (0–4), not a string.

## Why

Linear's opinionated, minimal workflow eliminates configuration overhead — teams are productive in under an hour. The GraphQL API is best-in-class for agents: rich query and mutation support with a stable schema. GitHub integration auto-transitions issue status when PRs are opened or merged, removing the manual "move to In Review" step. Velocity and cycle metrics are built-in without formula configuration.

## When To Use

- Building software products with engineering-focused teams valuing speed and keyboard shortcuts
- Automating cycle hygiene: moving stale issues, closing duplicates, adding labels from SDD tasks
- Syncing Linear issue state with GitHub PR status in CI pipelines
- Creating issues in bulk from structured input (SDD implementation-plan.md, CSV backlogs)
- Generating weekly velocity or cycle summary reports

## When NOT To Use

- Teams not using Linear — do not retrofit this workflow onto Jira, Trello, or GitHub Projects
- Real-time incident response — Linear's async model is too slow for live war-rooms
- One-time exploratory tasks where creating an issue adds overhead, not value
- Replacing human judgment on priority or roadmap sequencing

## Content

| File | What's inside |
|------|---------------|
| `content/01-workspace-setup.xml` | Team configuration, issue properties, cycle workflow, project and roadmap setup |
| `content/02-workflow.xml` | Triage process, GitHub integration config, keyboard shortcuts, custom views |
| `content/03-agent-usage.xml` | Agentic workflows, subagents, GraphQL issue creation script, API gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/issue-bug.md` | Bug report issue template with environment, steps to reproduce, severity |
| `templates/issue-feature.md` | Feature request issue template with problem statement and success metrics |
| `templates/create-issue.sh` | Bash script to create a Linear issue via GraphQL mutation |
| `templates/prompt-sdd-to-issues.txt` | Prompt for agent to convert SDD task blocks to Linear issue payloads |
