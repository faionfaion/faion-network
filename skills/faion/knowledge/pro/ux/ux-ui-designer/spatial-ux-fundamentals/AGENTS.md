---
slug: spatial-ux-fundamentals
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a spatial-spec mapping every panel and control to one of three field zones — near (0.3-1.0 m), mid (1.0-3.0 m), far (3.0 m+) — with anchoring, occlusion, and sight-line annotations enforced via lint.
content_id: "845db2e8bdce2a5f"
complexity: medium
produces: spec
est_tokens: 4200
tags: [spatial-computing, vr, ux-design, ergonomics, hmd]
---
# Spatial UX Fundamentals

## Summary

**One-sentence:** Produces a spatial-spec mapping every panel and control to one of three field zones — near (0.3-1.0 m), mid (1.0-3.0 m), far (3.0 m+) — with anchoring, occlusion, and sight-line annotations enforced via lint.

**One-paragraph:** Spatial UX organises content in three physical zones: near field (0.3-1.0 m, primary interactions and controls), mid field (1.0-3.0 m, content consumption and work surfaces), far field (3.0 m+, ambient context only — no interactive controls). Anchoring modes (head-locked-with-decay, world-locked, hand-attached) and occlusion/sight-line constraints round out the spec. This methodology emits a JSON spatial-spec validated by a lint script that flags elements outside their correct band or interactive controls placed in the far field.

**Ефективно для:**

- Drafting first-pass spatial UX вимог для Vision Pro / Quest / HoloLens apps.
- Re-mapping 2D mobile/desktop flow до near/mid/far field zones.
- Спільний spatial vocabulary між PM / engineering / 3D artists.
- Pre-prototype review для reach + occlusion + sight-line ризиків.

## Applies If (ALL must hold)

- Stationary or seated/standing immersive use is the target.
- Designing for a head-mounted display (visionOS, Quest, PSVR2, HoloLens).
- Active interaction with spatial content is part of the experience.

## Skip If (ANY kills it)

- Phone AR snap-on banner overlays — world-scale constraints do not apply.
- Desktop 3D viewers (CAD, Blender) — different ergonomic envelope.
- Lean-back 360 video — passive viewing has no reach design.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI element list | JSON / Markdown | design |
| Target HMD | enum | PM |
| Anthropometric edge cases | list | a11y research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | self-contained methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: three-field-zones, no-interactive-in-far-field, default-content-distance, anchor-primary-hand-or-decay, chin-region-forbidden, recenter-affordance-required | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assign-zones` | haiku | Numeric clamp. |
| `anchor-decisions` | sonnet | Light judgment on primary vs reference. |
| `lint-spec` | haiku | Mechanical check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-spec.json` | Skeleton spatial spec |
| `templates/spatial-spec-linter.py` | Lint script for zone + anchor + chin-region violations |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-ux-fundamentals.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[spatial-ui-patterns]]
- [[spatial-interaction-patterns]]
- [[spatial-accessibility]]
- [[vr-design-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by element role and enforces zone + anchor rules; recenter-affordance check fires on every spec. Each leaf cites a rule from `01-core-rules.xml`.
