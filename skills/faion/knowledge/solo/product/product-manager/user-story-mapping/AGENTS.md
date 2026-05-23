---
slug: user-story-mapping
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Build a user story map (backbone of activities → user tasks → stories), slice the map into MVP / Release-1 / Release-2 horizontally so scope decisions are visible and shippable.
content_id: "a9e31c3e93d54a28"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["story-mapping", "ux", "release-planning", "scope-cutting", "user-journey"]
---
# User Story Mapping

## Summary

**One-sentence:** Build a user story map (backbone of activities → user tasks → stories), slice the map into MVP / Release-1 / Release-2 horizontally so scope decisions are visible and shippable.

**One-paragraph:** Replaces flat backlogs with a 2-D map: the horizontal axis is the user journey (left → right), the vertical axis is alternative stories per task (top → bottom). A horizontal slice across the map is a coherent release. Visible scope-cutting beats invisible deprioritisation in a flat list.

**Ефективно для:**

- Solo PM with a feature touching ≥2 user steps and ≥1 dev-week of scope — needs a visual artefact to decide what ships in v1 without losing the bigger journey.

## Applies If (ALL must hold)

- Feature touches ≥2 sequential user tasks.
- Scope cuts will happen and need to be visible to stakeholders.
- Team includes ≥1 designer / engineer who needs the journey context.

## Skip If (ANY kills it)

- Single-step feature (a setting, a flag, a fix).
- Pre-discovery — user journey not validated.
- Solo dev shipping a 1-day change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User persona | markdown | Research |
| Journey hypotheses | list | Discovery output |
| Capacity available for v1 | estimate | Team plan |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/mvp-scoping` | Capacity constraints that drive the v1 slice. |
| `solo/product/product-manager/spec-writing` | Downstream artefact for each prioritised story. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-user-story-mapping` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-user-story-mapping` | haiku | Schema check + threshold checks; deterministic. |
| `review-user-story-mapping` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-story-mapping.json` | JSON skeleton conforming to the output contract schema. |
| `templates/user-story-mapping.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-story-mapping.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[mvp-scoping]]
- [[spec-writing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
