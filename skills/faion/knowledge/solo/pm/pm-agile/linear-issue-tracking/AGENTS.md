---
slug: linear-issue-tracking
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Linear's opinionated, minimal workflow eliminates configuration overhead — teams are productive in under an hour.
content_id: "47d11764c93d3e16"
tags: [linear, issue-tracking, sprints, velocity, graphql, automation]
---
# Linear Issue Tracking for Engineering Teams

## Summary

**One-sentence:** Linear's opinionated, minimal workflow eliminates configuration overhead — teams are productive in under an hour.

**One-paragraph:** Linear's opinionated, minimal workflow eliminates configuration overhead — teams are productive in under an hour. The GraphQL API is best-in-class for agents: rich query and mutation support with a stable schema. GitHub integration auto-transitions issue status when PRs are opened or merged, removing the manual "move to In Review" step. Velocity and cycle metrics are built-in without formula configuration.

## Applies If (ALL must hold)

- Building software products with engineering-focused teams valuing speed and keyboard shortcuts
- Automating cycle hygiene: moving stale issues, closing duplicates, adding labels from SDD tasks
- Syncing Linear issue state with GitHub PR status in CI pipelines
- Creating issues in bulk from structured input (SDD implementation-plan.md, CSV backlogs)
- Generating weekly velocity or cycle summary reports

## Skip If (ANY kills it)

- Teams not using Linear — do not retrofit this workflow onto Jira, Trello, or GitHub Projects
- Real-time incident response — Linear's async model is too slow for live war-rooms
- One-time exploratory tasks where creating an issue adds overhead, not value
- Replacing human judgment on priority or roadmap sequencing

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

- parent skill: `solo/pm/pm-agile/`
