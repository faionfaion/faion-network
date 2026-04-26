# Agile Ceremonies Setup

## Summary

Defines, configures, and continuously improves the five Scrum events — Sprint Planning, Daily Standup, Sprint Review, Retrospective, and Backlog Refinement — for a team's specific size, timezone spread, and PM tool. Total ceremony overhead must stay at or below 10% of sprint capacity. Each event has a mandatory time-box, a single sprint goal, and tracked action-item closure.

## Why

Ceremonies decay without explicit structure: standups become status reports, retrospectives surface the same complaints sprint after sprint, reviews turn into internal demos without real stakeholder feedback. Time-boxing plus outcome tracking turns ceremonies from ritual into an actual feedback loop. Untracked retro actions means the team never improves.

## When To Use

- Bootstrapping Scrum for a new team: defining cadence, agendas, time-boxes, PM tool wiring.
- Migrating a waterfall or ad-hoc team to a structured ceremony rhythm.
- Tuning ceremonies that have decayed (silent retros, status-report standups, drifting reviews).
- Setting up async / hybrid ceremonies for distributed teams with wide timezone spread.
- Configuring Jira, Linear, or Azure DevOps to mirror the ceremony cadence.

## When NOT To Use

- Solo or 2-person teams — overhead exceeds value; lightweight async check-ins suffice.
- Continuous-delivery Kanban teams with WIP limits and SLA dashboards — ceremonies become anti-patterns.
- Teams with zero psychological safety — retros become blame sessions and worsen things before they help; fix safety first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ceremony-rules.xml` | Time-box table, sprint-goal rule, Definition of Ready/Done, action-item closure threshold. |
| `content/02-event-setup.xml` | Per-event agenda and tool config for Planning, Standup, Review, Retro, Refinement. |
| `content/03-remote-async.xml` | Async standup patterns, timezone rules, Geekbot config, ceremony health survey. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-planning.md` | Sprint planning artifact: goal, capacity table, backlog, risks. |
| `templates/retrospective.md` | Retro artifact: metrics, went-well, improve, action items with owners. |
| `templates/standup-bot.yaml` | Geekbot-compatible async standup configuration. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/create_sprint.sh` | Create and start a Jira sprint with goal, dates, and top ready issues via jira-cli. |
