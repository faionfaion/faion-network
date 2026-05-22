---
slug: micro-mvp-cut-rubric
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A mechanical rubric for cutting any product feature to a day-sized (≤ 8 hours) slice without losing the user value.
content_id: "9402b6df39373eb9"
tags: [mvp,scoping,solo,day-sized,slice,cut-rubric]
---
# Micro-MVP Cut Rubric

## Summary

**One-sentence:** A mechanical rubric for cutting any product feature to a day-sized (≤ 8 hours) slice without losing the user value.

**One-paragraph:** Solo SaaS builders know "ship small" but mid-feature lose the discipline and start "while I'm here, I'll also..." This methodology gives a 6-axis cut rubric that mechanically reduces a feature to a day-sized slice: data model (one entity not two), surface (one page not three), permissions (owner-only not team), persistence (in-memory ok, defer DB), tests (smoke not exhaustive), UI polish (zero, ship raw). Mechanism: each axis has a "ship now" cut + a "defer to next slice" annotation. Primary output: a 1-page spec listing the cut decisions and the deferred items, with the day-sized slice ready to claim in the SDD task queue.

## Applies If (ALL must hold)

- operator is solo or 2-person team shipping daily SDD cycles
- new feature is on the roadmap with stated user outcome
- feature has been scoped past hypothesis (validation done) but pre-build
- operator has access to SDD task queue OR backlog
- daily ship cadence is a goal (not weekly / sprint)

## Skip If (ANY kills it)

- enterprise feature requiring SOC2 / regulatory traceability — can't cut to one day
- feature blocked on third-party SDK / integration with no sandbox
- feature requires data migration that itself exceeds 8 hours
- team of ≥ 3 working on the same feature — coordination overhead exceeds value
- operator is exploring, not shipping (use research-spike, not micro-MVP)

## Prerequisites (must be true before starting)

- one-line user outcome ("user can do X")
- known target user (1 person or 1 segment)
- access to existing codebase / scaffold
- one consecutive 8-hour block available (not fragmented)
- decision authority to defer the rest

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-task-decomposition` | Receives the day-sized slice as input |
| `solo/product/product-planning/micro-mvps` | Conceptual companion methodology |
| `solo/sdd/sdd/spec-writing` | Spec format for the cut slice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 6-axis cut, day-sized ceiling, deferral discipline, smoke-only tests, raw UI ship | ~1000 |
| `content/02-output-contract.xml` | essential | Cut-decision schema, deferred-list schema, slice spec format | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (scope creep mid-day, gold-plating, defer-everything, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feature_axis_assessor` | sonnet | Assess each axis: minimum slice + deferred items |
| `time_estimator` | haiku | Estimate the proposed slice against 8h ceiling |
| `slice_spec_draft` | sonnet | Produce 1-page spec with cuts + deferrals |
| `deferral_list_writer` | haiku | Format deferred items into next-slice candidates |

## Templates

| File | Purpose |
|------|---------|
| `templates/cut-rubric.md` | 6-axis cut worksheet |
| `templates/slice-spec.md` | 1-page slice spec template |
| `templates/deferral-list.md` | Next-slice candidate list |
| `templates/post-slice-retro.md` | 15-min retro after slice ships |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/slice-time-budget.py` | Estimate effort per axis | Pre-cut |
| `scripts/cut-validator.py` | Validate cut output against 8h ceiling | Post-cut |

## Related

- parent skill: `solo/product/product-planning/`
- peer methodology: `micro-mvps`, `solo/sdd/sdd/sdd-task-decomposition`
- external: [Basecamp Shape Up](https://basecamp.com/shapeup) · [Marty Cagan, Inspired](https://svpg.com/inspired-how-to-create-products-customers-love/)
