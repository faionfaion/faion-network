---
slug: user-story-mapping
tier: solo
group: product
domain: product-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: User story mapping arranges stories into a two-dimensional model: user activities as the horizontal backbone (left-to-right = user journey) and tasks stacked vertically by priority within each activity.
content_id: "c615a84e28b6c652"
tags: [story-mapping, user-journey, release-planning, backbone, skeleton]
---
# User Story Mapping

## Summary

**One-sentence:** User story mapping arranges stories into a two-dimensional model: user activities as the horizontal backbone (left-to-right = user journey) and tasks stacked vertically by priority within each activity.

**One-paragraph:** User story mapping arranges stories into a two-dimensional model: user activities as the horizontal backbone (left-to-right = user journey) and tasks stacked vertically by priority within each activity. The walking skeleton is exactly one task per activity, forming an end-to-end working flow that becomes the earliest shippable version. Release slices are horizontal cuts that span the full backbone. Flat backlogs lose the context of user workflows: stories get prioritized in isolation without seeing whether the full journey is covered. A story map makes missing steps visible, prevents releases that cover only one column of the journey, and creates a shared picture for cross-functional teams before sprint planning.

## Applies If (ALL must hold)

- Designing an end-to-end user journey across multiple activities.
- Slicing a backlog into shippable releases when a flat list lost journey context.
- Cross-functional alignment before sprint planning (engineering, design, PM need a shared picture).
- Identifying the walking skeleton for an MVP — pairs with mvp-scoping.

## Skip If (ANY kills it)

- Pure technical work (infrastructure, refactors, platform changes) — no user-facing backbone exists.
- Tiny single-flow features — direct user stories with acceptance criteria suffice.
- Teams without shared journey understanding yet — do user-journey-mapping or JTBD interviews first.

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

- parent skill: `solo/product/product-planning/`
