---
slug: spike-protocol-template
tier: pro
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Time-boxed investigation tasks with explicit exit-criteria — distinct from ADR (decision recorded) and design-doc (proposal).
content_id: "5368864553184fa4"
tags: [spike-protocol-template, sdd, pro]
---

# Spike Protocol Template

## Summary

**One-sentence:** Time-boxed investigation tasks with explicit exit-criteria — distinct from ADR (decision recorded) and design-doc (proposal).

**One-paragraph:** Time-boxed investigation tasks with explicit exit-criteria. Different from ADR and design-doc. No methodology entry. Common in mature Scrum/Kanban teams. Output: spike template + entry + exit criteria + outcome capture.

## Applies If (ALL must hold)

- team using Scrum / Kanban with iteration cadence
- uncertainty in a planning area that blocks estimation
- PM/EM can grant a time-boxed investigation slot

## Skip If (ANY kills it)

- team without iteration cadence
- investigation that should be an RFC (decision-needed, not exploration)
- spike used as 'do whatever you want this week' (anti-pattern)

## Prerequisites

- identified uncertainty (technical, integration, scope)
- max time-box (default 1-3 days)
- named person to do the spike

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd` | parent skill — provides operating context for this methodology |
| `pro/sdd/internal-rfc-template` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/architecture-decision-records` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `solo/sdd/sdd/`
- peer methodology: `pro/sdd/internal-rfc-template`
- peer methodology: `solo/dev/architecture-decision-records`
- peer methodology: `solo/sdd/sdd`
- external: https://www.scrum.org/resources/blog/spike-solution-when-and-how-use-it; https://www.atlassian.com/agile/project-management/spike
