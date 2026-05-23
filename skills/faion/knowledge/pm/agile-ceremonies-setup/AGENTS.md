# Agile Ceremonies Setup

## Summary

**One-sentence:** Configure the five Scrum events sized to team + timezone + tooling so ceremony overhead stays below 10% of sprint capacity with action-item closure tracked.

**One-paragraph:** Agile ceremonies (planning / daily standup / refinement / review / retrospective) ought to consume <10% of sprint capacity. This methodology configures the five events to fit team size, timezone spread, and PM-tool conventions. Output is a ceremonies configuration artefact (per-event purpose, time-box, attendees, output, owner) plus templates per ceremony. Retrospective action items carry owner + due-date and are tracked across sprints.

**Ефективно для:**

- New Scrum teams establishing their cadence.
- Teams whose ceremonies have drifted into theatre.
- Distributed teams across multiple timezones.
- Teams whose retro actions never close.

## Applies If (ALL must hold)

- Team runs (or wants to run) Scrum or Scrum-ish cadence.
- Sprint length is fixed (1, 2, or 3 weeks).
- Team has a PM-tool home (Jira / Linear / GitHub Projects).
- Team has named Scrum Master or equivalent facilitator.

## Skip If (ANY kills it)

- Continuous-flow (Kanban) team — different ceremony shape.
- Solo developer — ceremonies cost more than they return.
- Team without facilitator authority — ceremonies degrade quickly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team list + timezones | table | PM |
| Sprint cadence decision | decision-record | team |
| PM-tool access | API token / app | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | PO and stakeholder reviews depend on engagement plan. |
| `communications-management` | Channels for standup + ceremony output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — ceremony purpose stated, time-box per event, retro action owner+due, ceremony overhead <10%, attendees bounded | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ceremonies config artefact | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns — drifted retros, no-purpose standups, time-boxes ignored, no closure | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: assess → configure → bootstrap → measure → tune | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping config state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-config` | haiku | Template fill from team list. |
| `measure-overhead` | sonnet | Compute ceremony hours vs sprint capacity. |
| `retro-action-synthesis` | opus | Cross-sprint pattern recognition for systemic actions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-planning.md` | Sprint planning template. |
| `templates/retrospective.md` | Retro template with mandatory action items. |
| `templates/standup-bot.yaml` | Standup bot config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agile-ceremonies-setup.py` | Schema-validate the config artefact. | Pre-commit + on config changes. |
| `scripts/create_sprint.sh` | Scaffold a new sprint folder with planning + retro from templates. | At sprint start. |

## Related

- [[agile-hybrid-approaches]]
- [[communications-management]]
- [[stakeholder-engagement]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agile-ceremonies-setup input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
