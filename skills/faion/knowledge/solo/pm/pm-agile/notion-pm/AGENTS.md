---
slug: notion-pm
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Notion PM uses interconnected databases (Projects, Tasks, Sprints) with relation and rollup fields to build a customizable agile workspace.
content_id: "ae344d00cc415537"
tags: [notion, agile, pm, sprint, database]
---
# Notion PM

## Summary

**One-sentence:** Notion PM uses interconnected databases (Projects, Tasks, Sprints) with relation and rollup fields to build a customizable agile workspace.

**One-paragraph:** Notion PM uses interconnected databases (Projects, Tasks, Sprints) with relation and rollup fields to build a customizable agile workspace. Tasks must exist as individual database pages — not as sub-bullets inside sprint documents — to be queryable via the API. Use a single Tasks database with Sprint as a relation field; never create a new database per sprint, which fragments history and breaks velocity computation.

## Applies If (ALL must hold)

- Small agile team (2–10 people) wanting sprint planning, backlog, and docs in one tool
- When sprint retrospectives, meeting notes, and task tracking need inline cross-references
- When workflow is still evolving — Notion databases restructure faster than Jira or Linear
- Solopreneur or micro-team where full sprint tooling (velocity charts, burndowns) is overkill
- When stakeholders need read-only project status via shareable page without PM tool accounts

## Skip If (ANY kills it)

- Teams with mature Scrum practices needing native burndown charts, velocity tracking, and sprint analytics
- High-velocity engineering teams with 10+ members — database performance degrades with large datasets
- When issues need tight Git/PR integration (auto-close on merge, branch naming)
- Organizations needing SOC2/HIPAA compliant issue tracking with field-level audit logs

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
