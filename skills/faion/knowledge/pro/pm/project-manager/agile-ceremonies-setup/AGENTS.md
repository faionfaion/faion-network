---
slug: agile-ceremonies-setup
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Defines, configures, and continuously improves the five Scrum events — Sprint Planning, Daily Standup, Sprint Review, Retrospective, and Backlog Refinement — for a team's specific size, timezone spread, and PM tool.
content_id: "41e9f58c7ac55250"
tags: [scrum, ceremonies, sprint-planning, retrospectives, agile]
---
# Agile Ceremonies Setup

## Summary

**One-sentence:** Defines, configures, and continuously improves the five Scrum events — Sprint Planning, Daily Standup, Sprint Review, Retrospective, and Backlog Refinement — for a team's specific size, timezone spread, and PM tool.

**One-paragraph:** Defines, configures, and continuously improves the five Scrum events — Sprint Planning, Daily Standup, Sprint Review, Retrospective, and Backlog Refinement — for a team's specific size, timezone spread, and PM tool. Total ceremony overhead must stay at or below 10% of sprint capacity. Each event has a mandatory time-box, a single sprint goal, and tracked action-item closure.

## Applies If (ALL must hold)

- Bootstrapping Scrum for a new team: defining cadence, agendas, time-boxes, PM tool wiring.
- Migrating a waterfall or ad-hoc team to a structured ceremony rhythm.
- Tuning ceremonies that have decayed (silent retros, status-report standups, drifting reviews).
- Setting up async / hybrid ceremonies for distributed teams with wide timezone spread.
- Configuring Jira, Linear, or Azure DevOps to mirror the ceremony cadence.

## Skip If (ANY kills it)

- Solo or 2-person teams — overhead exceeds value; lightweight async check-ins suffice.
- Continuous-delivery Kanban teams with WIP limits and SLA dashboards — ceremonies become anti-patterns.
- Teams with zero psychological safety — retros become blame sessions and worsen things before they help; fix safety first.

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
