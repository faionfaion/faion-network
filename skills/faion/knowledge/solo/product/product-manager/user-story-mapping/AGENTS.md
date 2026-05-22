---
slug: user-story-mapping
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Arrange user stories into a two-dimensional map: backbone activities run left-to-right (user journey), tasks are stacked vertically under each activity by priority.
content_id: "c615a84e28b6c652"
tags: [user-stories, mapping, release-planning, journey, mvp]
---
# User Story Mapping

## Summary

**One-sentence:** Arrange user stories into a two-dimensional map: backbone activities run left-to-right (user journey), tasks are stacked vertically under each activity by priority.

**One-paragraph:** Arrange user stories into a two-dimensional map: backbone activities run left-to-right (user journey), tasks are stacked vertically under each activity by priority. The map exposes a "walking skeleton" (one task per activity, end-to-end) and horizontal release slices, making scope decisions visual and defensible. Use verb phrases for backbone items; 5-10 activities is the target range.

## Applies If (ALL must hold)

- Decomposing a new product or major feature where the user journey spans 3+ steps and the team needs a shared mental model.
- Slicing releases from a large feature backlog by identifying a walking skeleton then incremental slices.
- Discovery to delivery handoff: turning interview transcripts into structured backbone and tasks before sprint planning.
- Onboarding a new contributor who needs to understand the product end-to-end in one diagram.

## Skip If (ANY kills it)

- Single isolated feature with no journey (e.g. "add audit log endpoint") — go directly to a story or spec.
- Maintenance / bug-fix work where the journey is already stable and mapped.
- Linear data-pipeline products with no user-facing journey; use technical sequence diagrams instead.
- When the team will not maintain the map — stale story maps actively mislead.

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

- parent skill: `solo/product/product-manager/`
