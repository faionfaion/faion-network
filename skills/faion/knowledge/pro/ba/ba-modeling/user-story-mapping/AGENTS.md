---
slug: user-story-mapping
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Arranges user stories along two dimensions: horizontal (user journey activities and tasks in narrative verb-phrases) and vertical (priority from essential to nice-to-have).
content_id: "c615a84e28b6c652"
tags: [user-story-mapping, release-planning, agile, user-journey, backlog]
---
# User Story Mapping

## Summary

**One-sentence:** Arranges user stories along two dimensions: horizontal (user journey activities and tasks in narrative verb-phrases) and vertical (priority from essential to nice-to-have).

**One-paragraph:** Arranges user stories along two dimensions: horizontal (user journey activities and tasks in narrative verb-phrases) and vertical (priority from essential to nice-to-have). The result shows the complete user experience and enables release slicing into a walking skeleton (R1) plus enhancement releases. Map lives as YAML-in-git; renderers produce Markdown, Mermaid, and Miro outputs from that single source.

## Applies If (ALL must hold)

- Flat backlog of 50-500 items with no journey context — agents reverse-engineer activities from titles.
- New product or module kick-off with personas and goals but no scope yet.
- Release planning for a 3-6 month roadmap that needs a walking-skeleton cut with thin-slice defense.
- Migration or replatforming — current journey mapped first, target journey overlaid to surface gaps.
- Stakeholder workshop prep — agents pre-populate a draft map so the workshop debates cuts, not vocabulary.
- Auditing an existing Jira backlog for journey coverage gaps.

## Skip If (ANY kills it)

- Single-feature work (one screen, one form) — write 3 stories with AC and ship; mapping overhead exceeds value.
- Pure platform / API-only services with no end-user journey — use interface-analysis and use-case-modeling.
- Hard-deadline regulated work where scope is already defined by regulation.
- Pre-PMF zero-to-one where the journey changes weekly — prototype + customer development instead.
- Pure infrastructure / DevOps backlogs — non-user activities do not belong on a story map.

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

- parent skill: `pro/ba/ba-modeling/`
