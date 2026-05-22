---
slug: ar-design-patterns
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AR must blend seamlessly with the real world.
content_id: "f87d0aa0ebdaf898"
tags: [ar, design, spatial-computing, placement, accessibility]
---
# AR Design Patterns

## Summary

**One-sentence:** AR must blend seamlessly with the real world.

**One-paragraph:** AR must blend seamlessly with the real world. Design context-aware AR experiences with surface detection, object recognition, and placement strategies that respect physical boundaries.

## Applies If (ALL must hold)

- Designing handheld AR (ARKit/ARCore) or headset AR (Vision Pro, Quest passthrough, HoloLens) experiences.
- Use cases: navigation overlays, product visualization (e-commerce), training/maintenance, shared annotations, contextual data labels.
- Defining placement strategies (surface detection, object recognition, world anchoring) and content scale rules.
- Authoring guardrails for "respect reality": occlusion, lighting integration, safe boundaries.

## Skip If (ANY kills it)

- 2D mobile features that only need a camera (QR scanning, barcode lookup)—AR overhead is unjustified.
- Marketing one-shots without a follow-up plan—AR demos rot when SDK versions change.
- Fully immersive VR—different ergonomic rules; use vr-design-patterns or spatial-design-tools.
- Public unsupervised contexts where safety / occlusion of real hazards (stairs, traffic) is unmanageable.

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

- parent skill: `pro/ux/ux-ui-designer/`
