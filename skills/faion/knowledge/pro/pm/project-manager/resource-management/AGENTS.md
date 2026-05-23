---
slug: resource-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Identify required skills per work package, plan to 75-80% effective capacity (never 100%), level overloads via delay/split/add/cut, monitor utilization weekly with stretch bench.
content_id: "c287bf8e68309063"
complexity: medium
produces: spec
est_tokens: 4700
tags: [resource-planning, capacity, utilization, team-management, leveling]
---
# Resource Management

## Summary

**One-sentence:** Identify required skills per work package, plan to 75-80% effective capacity (never 100%), level overloads via delay/split/add/cut, monitor utilization weekly with stretch bench.

**One-paragraph:** Identify required skills and quantities per work package, assess real availability capped at 75-80% effective capacity, map resources to activities, level overloads via delay/split/add/cut/extend options, develop the team, and monitor utilization weekly against plan. Resources include human, physical, material, financial — human dominates and never assumes 100% capacity. Cross-train backups for critical skills; bus factor below 2 is a P1 risk.

**Ефективно для:**

- Multi-team programmes with shared engineers across projects
- Onboarding / offboarding wave shifting skill mix within 30-60 days
- Agency / consulting context billing by utilization
- Capacity planning ahead of quarterly OKR commitments

## Applies If (ALL must hold)

- Multi-team programs where the same engineers are claimed by 2+ projects
- Onboarding or offboarding wave shifting skill mix within 30-60 days
- Agency or consulting context billing by utilization
- Mid-project resource crisis (key person quit, contractor delayed)
- Capacity planning ahead of quarterly OKR commitments

## Skip If (ANY kills it)

- Stable single team under 8 people — informal allocation works
- Pure agile teams committed to whole-team ownership — utilization tracking erodes safety
- One-week sprint of throwaway research
- Organisations where utilization % is a performance metric — creates burnout and gaming

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster | YAML | HR / engineering management |
| Calendar / PTO | iCal / API | Google / Microsoft calendar |
| Skill matrix | YAML | self + manager input with last-used dates |
| Cost rates | CSV | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[schedule-development]] | Resource demand is sequenced against the schedule |
| [[raci-matrix]] | Role assignments anchor the skill-matching step |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: cap-effective-capacity-80, bus-factor-min-2, skill-matrix-last-used, reconcile-with-schedule-cost, stretch-bench | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-capacity` | haiku | Mechanical subtraction in script — calendar - meetings - PTO |
| `match-skill` | sonnet | Skill × availability × cost scoring with rationale |
| `propose-leveling` | sonnet | Per-option cost + schedule impact |

## Templates

| File | Purpose |
|------|---------|
| `templates/resource-plan.md` | Resource plan with summary table, calendar grid, skill matrix, resource risks |
| `templates/resource-request.md` | Resource request form with role, skills, dates, justification, impact-if-not-filled |
| `templates/capacity.yaml` | Per-person weekly capacity input schema for the planner script |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/capacity.py` | Compute effective hours per person per week from roster, PTO, and meeting load | Weekly cron; pre-sprint planning |
| `scripts/validate-resource-management.py` | Validate resource plan invariants (80% cap, bus factor) | Pre-commit on resource-plan changes |

## Related

- parent skill: `pro/pm/project-manager/`
- [[schedule-development]]
- [[raci-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
