---
slug: user-story-mapping
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A two-dimensional arrangement of user stories along a horizontal user-journey axis (activities → tasks) and a vertical priority axis (essential → nice-to-have), producing a story map that reveals the complete user experience and enables slice-based release planning.
content_id: "c615a84e28b6c652"
tags: [user-stories, story-mapping, release-planning, requirements, babok]
---
# User Story Mapping

## Summary

**One-sentence:** A two-dimensional arrangement of user stories along a horizontal user-journey axis (activities → tasks) and a vertical priority axis (essential → nice-to-have), producing a story map that reveals the complete user experience and enables slice-based release planning.

**One-paragraph:** A two-dimensional arrangement of user stories along a horizontal user-journey axis (activities → tasks) and a vertical priority axis (essential → nice-to-have), producing a story map that reveals the complete user experience and enables slice-based release planning. The BA owns scope definition: turning the map into formal artifacts (BRD, BPMN, traceability matrix, JIRA epics).

## Applies If (ALL must hold)

- Sprint-zero or pre-discovery session where the BA must convert a fuzzy idea into a stakeholder-signed release plan.
- Brownfield project with a flat 200+ ticket backlog needing journey context before re-prioritization.
- Compliance/regulated project where each story must trace to a process step, regulation clause, and acceptance criterion.
- Vendor migration: the existing journey is the backbone, gap analysis fills the cells.
- Stakeholder alignment with mixed business + IT audience who need to agree on a release slice.

## Skip If (ANY kills it)

- Maintenance backlog of isolated bug fixes and tech debt — no journey, use WSJF or RICE instead.
- Pure API/platform product with no end-user persona — model with C4 + use cases.
- Team already on a stable release cadence with a healthy backlog and clear roadmap — rebuilding the map is sunk cost.
- One-off internal automation (single user, single happy path) — a 5-step checklist beats a wall map.
- Stakeholders cannot commit 2-4 contiguous hours — a half-attended map produces false consensus.

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

- parent skill: `pro/ba/business-analyst/`
