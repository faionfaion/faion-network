---
slug: user-story-mapping
tier: pro
group: business-analyst
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Two-axis story map (user journey × release slices) producing a backlog with explicit walking-skeleton, MVP, and release-N horizons so teams ship value rather than features.
content_id: "4b2597950ce82b41"
complexity: medium
produces: spec
est_tokens: 2700
tags: [user-story-mapping, backlog, mvp, release-planning, journey]
---
# User Story Mapping

## Summary

**One-sentence:** A two-axis story map (user journey horizontal × release slices vertical) producing a backlog with walking-skeleton, MVP, and subsequent release horizons.

**One-paragraph:** Flat backlogs hide the user journey; teams build features in arbitrary order and miss the walking skeleton. Story mapping makes the journey explicit (horizontal) and the release slices visible (vertical). Output: a structured backlog with a named walking-skeleton release (smallest end-to-end usable path), an MVP release (smallest valuable path), and subsequent releases. Every story carries acceptance criteria + traceability to a use case.

**Ефективно для:**

- Pre-build backlog formation on greenfield products.
- Re-baselining a stalled backlog where priority is unclear.
- Cross-team alignment on release sequencing.
- Stakeholder demo planning aligned to user journey.

## Applies If (ALL must hold)

- a user journey or use-case set exists
- team will work in iterations / sprints
- PO or BA can own the map and review weekly
- the engagement has ≥2 releases planned

## Skip If (ANY kills it)

- single-release engagement — flat backlog is fine
- no journey definition yet — produce use cases first
- team uses pure flow (Kanban) with no release concept

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| use-case spec or journey definition | MD / wiki | use-case-modeling |
| named PO / owner | org chart | PM |
| release cadence definition | wiki | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[use-case-modeling]] | Provides the journey backbone. |
| [[stakeholder-analysis]] | Named actors anchor the journey. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: journey backbone first, walking-skeleton named, MVP named, every story has AC, traceability to use case | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for story-map artefact: journey, slices, stories, AC | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: feature-first map, missing walking skeleton, AC-less stories, lost traceability, stale map | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: lay journey → identify slices → name walking skeleton + MVP → write AC → review | 700 |
| `content/05-examples.xml` | essential | Worked example: 3-step journey × 2-release map excerpt | 500 |
| `content/06-decision-tree.xml` | essential | Tree on release count + journey availability + PO availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `journey_layout` | sonnet | Convert use cases into journey backbone. |
| `slice_drafting` | sonnet | Identify viable release slices. |
| `ac_writing` | sonnet | Acceptance criteria per story. |
| `traceability_audit` | haiku | Mechanical AC ↔ use-case link check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-map.md` | Markdown skeleton with journey + slices + stories. |
| `templates/story-row.csv` | Header for individual story rows. |
| `templates/_smoke-test.md` | Minimum viable story map. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-story-mapping.py` | Validates story map against the JSON Schema. | After story-writing session; pre-commit. |

## Related

- [[use-case-modeling]]
- [[stakeholder-analysis]]
- [[definition-of-done-library]]
- [[scope-drift-early-warning-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
