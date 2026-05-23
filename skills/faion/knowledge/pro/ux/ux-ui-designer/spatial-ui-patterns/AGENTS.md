---
slug: spatial-ui-patterns
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a pattern-taxonomy spec for 3D user interfaces in AR/VR/MR: panel-type assignment (world-locked / head-locked / body-locked / hand-attached), comfort distance ≥1 m, FoV occupancy ≤40°, touch targets ≥60×60 pt at 1 m.
content_id: "74a68d691e50df2e"
complexity: medium
produces: spec
est_tokens: 4100
tags: [spatial-ui, ar-vr-mr, panel-types, window-management, ergonomics]
---
# Spatial UI Patterns

## Summary

**One-sentence:** Produces a pattern-taxonomy spec for 3D user interfaces in AR/VR/MR: panel-type assignment (world-locked / head-locked / body-locked / hand-attached), comfort distance ≥1 m, FoV occupancy ≤40°, touch targets ≥60×60 pt at 1 m.

**One-paragraph:** Spatial UI is a four-panel taxonomy: world-locked (reference content), head-locked (forbidden in visionOS, limited in Quest), body-locked (primary UI), hand-attached (tools). Comfort constraints — distance ≥1 m, FoV occupancy ≤40°, touch targets ≥60×60 pt at 1 m — apply per panel type. This methodology emits a spec mapping each panel to its type, distance, size, and anchoring, validated against the per-platform constraint set. Head-locked UI in production builds is the most-rejected pattern in store reviews.

**Ефективно для:**

- Mapping every panel to one of four types (world-locked / head-locked / body-locked / hand-attached).
- Enforcing comfort distance ≥1 m і FoV occupancy ≤40° для primary UI.
- Cross-platform parity: panels work на visionOS і Quest однаково.
- Pre-store-review audit для panel-type compliance.

## Applies If (ALL must hold)

- Designing UI for an HMD app shipping on visionOS, Quest, or HoloLens.
- Existing UI was ported from mobile/desktop and needs panel-type assignment.
- Store review flagged head-locked UI in a prior release.

## Skip If (ANY kills it)

- Passive 360 video player — no UI panels.
- Pure passthrough overlay with no app UI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI inventory | list of panels | design |
| Target platforms | list | PM |
| Use-case content type | enum | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-ux-fundamentals]] | field-zone definitions are inputs to panel placement |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: panel-type-mandatory, head-locked-forbidden-default, comfort-distance-min-1m, fov-occupancy-cap, touch-target-min-60pt-at-1m | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assign-types` | haiku | Mechanical taxonomy pick. |
| `size-and-distance` | haiku | Numeric clamp. |
| `fov-budgeting` | sonnet | Aggregate reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/panel-spec.json` | Skeleton panel spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-ui-patterns.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[spatial-ux-fundamentals]]
- [[spatial-interaction-patterns]]
- [[vr-design-patterns]]
- [[immersive-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by panel role (primary / tool / reference / safety-telemetry) and applies the panel-type rule; FoV-occupancy gate fires when sum exceeds 40%. Each leaf cites a rule from `01-core-rules.xml`.
