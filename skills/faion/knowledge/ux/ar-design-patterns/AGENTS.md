# AR Design Patterns

## Summary

**One-sentence:** Produces an AR interaction spec covering placement, occlusion-aware UI, gesture grammar, lighting estimation, and reset-on-track-loss for handheld + headset AR apps.

**One-paragraph:** AR design patterns blend digital content with the real world: stable placement via plane detection or anchors, occlusion-aware UI that respects real-world depth, gesture grammar consistent across iOS ARKit / Android ARCore / WebXR, lighting estimation for material realism, and a reset-on-track-loss path so users never see jittering or floating UI. Output is a per-screen interaction spec.

**Ефективно для:**

- Handheld AR (iOS/Android) — placement + gesture spec до імплементації.
- AR overlays для field-service / remote-assistance: occlusion-aware UI.
- Cross-platform AR app: уніфікувати gesture grammar між ARKit/ARCore/WebXR.
- Lighting estimation для realism — matte vs glossy materials.

## Applies If (ALL must hold)

- Building an AR experience on ARKit, ARCore, WebXR, or a unified runtime (Unity AR Foundation).
- Users interact with virtual content placed in physical space.
- Cross-platform consistency or specific platform's interaction grammar matters.

## Skip If (ANY kills it)

- Pure VR — different design constraints (use vr-design-patterns).
- Single-shot AR filter (face effect) — overkill spec for a 5-second moment.
- Marker-only AR with no plane/anchor tracking — placement spec is moot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target runtime | ARKit | ARCore | WebXR | Unity | product brief |
| Screen inventory | list | product brief |
| Gesture grammar baseline | table | platform HIG |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[immersive-design-principles]] | Comfort/presence baseline this builds on |
| [[spatial-ux-fundamentals]] | Reference frames + spatial affordances |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ar-screen-spec.md` | Per-screen AR interaction spec with anchoring/occlusion/lighting/grammar |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ar-design-patterns.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[immersive-design-principles]]
- [[vr-design-patterns]]
- [[spatial-ui-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
