---
slug: spatial-interaction-patterns
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an interaction-pattern specification for spatial (AR/VR/MR) apps: state machines for direct-manipulation, ray-cast selection, gaze+dwell, voice, and gesture — with primary + fallback modality per interaction.
content_id: "aba67744189197d0"
complexity: medium
produces: spec
est_tokens: 4200
tags: [spatial-interaction, input-modalities, xr-design, accessibility, gesture-design]
---
# Spatial Interaction Patterns

## Summary

**One-sentence:** Produces an interaction-pattern specification for spatial (AR/VR/MR) apps: state machines for direct-manipulation, ray-cast selection, gaze+dwell, voice, and gesture — with primary + fallback modality per interaction.

**One-paragraph:** Spatial interactions split across five input modalities (hand-tracking, controllers, gaze+dwell, voice, gesture). A robust app declares one primary + one fallback per critical interaction, models it as an explicit state machine, and validates inter-platform parity. This methodology emits a JSON spec mapping each interaction to (primary, fallback, state-machine, accessibility-notes). Mis-modeled state machines (no cancel state, no error state) are the most common failure mode after platform-review submission.

**Ефективно для:**

- Specifying hand-tracking + controller fallbacks для cross-platform XR app.
- Declaring state machine per interaction (idle/hover/select/cancel/error).
- Cross-platform parity audit: same interaction works on visionOS + Quest.
- Gesture-design review для bespoke gestures поза стандартним pinch/grab.

## Applies If (ALL must hold)

- App ships interactive 3D content beyond pure passive viewing.
- Multi-modal input is intended (hand + voice or controller + gaze).
- Cross-platform reach matters (visionOS + Quest minimum).

## Skip If (ANY kills it)

- Passive 360 video player — gaze-only suffices.
- Single-modality jam project — state-machine overhead too high.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interaction inventory | list | design |
| Target platforms | list | PM |
| Accessibility floor | spatial-accessibility report | a11y lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-accessibility]] | two-modality requirement is enforced here |
| [[spatial-ux-fundamentals]] | field-zone semantics referenced by spec |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: primary-plus-fallback-modality, state-machine-explicit, gesture-vocabulary-closed, platform-parity, voice-as-equal-modality | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate-interactions` | haiku | Mechanical listing. |
| `model-state-machines` | sonnet | State design with cancel/error coverage. |
| `parity-audit` | haiku | Boolean check per platform. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interaction-spec.json` | Skeleton interaction spec |
| `templates/state-machine.dot` | Graphviz template for one interaction state machine |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-interaction-patterns.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[spatial-accessibility]]
- [[spatial-ux-fundamentals]]
- [[spatial-ui-patterns]]
- [[vr-design-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by interaction class (select/manipulation/navigation) → picks modalities; checks state-machine completeness. Each leaf cites a rule from `01-core-rules.xml`.
