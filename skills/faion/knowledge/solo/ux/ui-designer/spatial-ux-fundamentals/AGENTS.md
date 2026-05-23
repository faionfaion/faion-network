---
slug: spatial-ux-fundamentals
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Designing for spatial (XR / Vision Pro / Quest) starts with three primitives — comfort zones, spatial affordances, and depth hierarchy — that prevent user fatigue and disorientation in the first 10 minutes of use.
content_id: "845db2e8bdce2a5f"
complexity: deep
produces: spec
est_tokens: 4200
tags: ["spatial-ux", "xr", "vision-pro", "quest", "primitives"]
---
# Spatial UX Fundamentals

## Summary

**One-sentence:** Designing for spatial (XR / Vision Pro / Quest) starts with three primitives — comfort zones, spatial affordances, and depth hierarchy — that prevent user fatigue and disorientation in the first 10 minutes of use.

**One-paragraph:** Spatial UX fails when 2D heuristics are ported into 3D. This methodology pins three primitives: comfort zones (arm-reach inner, working-distance middle, peripheral outer with field-of-view limits), spatial affordances (depth + occlusion + parallax communicate interactivity, not just color/shape), and depth hierarchy (z-distance maps to attention, not just z-index). Every spatial UI component answers these three before motion and aesthetics layer on.

**Ефективно для:**

- Solo designer building first Vision Pro / Quest app and needing primitive guardrails.
- Founder evaluating whether to ship a spatial version of an existing 2D product.
- AI agent generating spatial UI variants that need primitive constraints baked in.
- Cross-platform design where 2D handoff must adapt to spatial without redesign.

## Applies If (ALL must hold)

- Target device is a spatial headset (Vision Pro, Quest, Mixed-Reality).
- First-time spatial design — primitives are not assumed knowledge.
- Designer or agent will produce spatial UI variants in the next 30 days.
- Design tool supports 3D / Z-depth output (Reality Composer, Figma plugin, Unity).

## Skip If (ANY kills it)

- Mobile or desktop 2D project — primitives do not apply.
- Late-stage spatial polish where primitives are already established.
- Voice-only XR — use voice-ui-basics methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target device + field of view | string + degrees | Device manufacturer spec |
| Use-case duration estimate | minutes | Product design |
| User-physical-context model | seated / standing / mobile | Session research |
| 3D design tool URL | URL | Tool picker |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/spatial-design-tools` | Tools used to author the primitives. |
| `solo/ux/edge-case-checklist` | Edge cases consumed at handoff. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-comfort-zone` | sonnet | Per-flow judgement on comfort-zone placement. |
| `validate-spatial-spec` | haiku | Deterministic check on z-distance + FoV thresholds. |
| `multi-flow-spatial-audit` | opus | Cross-flow synthesis for an app. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-ux-fundamentals.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/spatial-ux-fundamentals.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-ux-fundamentals.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[voice-ui-basics]]
- [[edge-case-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
