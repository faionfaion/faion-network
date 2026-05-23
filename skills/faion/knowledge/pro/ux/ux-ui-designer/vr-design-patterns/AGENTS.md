---
slug: vr-design-patterns
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a VR-design pattern spec: visible ground plane + stable horizon, teleport-first locomotion for novices, world-anchored UI, accessibility fallbacks (seated mode, subtitles, one-handed control) — to ship a comfortable, inclusive VR app.
content_id: "6543f00fc9abea0c"
complexity: medium
produces: spec
est_tokens: 4100
tags: [vr, immersive, ux-design, interaction-design, comfort]
---
# VR Design Patterns

## Summary

**One-sentence:** Produces a VR-design pattern spec: visible ground plane + stable horizon, teleport-first locomotion for novices, world-anchored UI, accessibility fallbacks (seated mode, subtitles, one-handed control) — to ship a comfortable, inclusive VR app.

**One-paragraph:** User-centered VR design starts with comfort: place a visible ground plane and stable horizon to anchor the vestibular system, choose teleportation-first locomotion for novices (smooth optional), anchor UI to the world rather than the head, and ship accessibility fallbacks (seated mode, subtitles, one-handed control). This methodology emits a VR-pattern spec validated by a comfort checklist. Violations correlate with motion sickness and store rejection.

**Ефективно для:**

- Pre-launch comfort audit для VR app on Quest, PSVR2, Vision Pro.
- Locomotion design рішення (teleport vs smooth) для novice vs experienced users.
- Seated-mode + one-handed control parity check.
- Store-review pre-submission for VR comfort + accessibility.

## Applies If (ALL must hold)

- App is a VR (not pure AR) experience.
- Locomotion or scene motion is part of the experience.
- Users include first-time VR users (consumer audience).

## Skip If (ANY kills it)

- Pure AR overlay app — different comfort envelope.
- Stationary cockpit-only experience without locomotion.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scene inventory | Markdown | design |
| Locomotion design | doc | game design |
| Audience profile | persona doc | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-accessibility]] | input modalities + seated parity foundation |
| [[immersive-design-principles]] | broader immersive vocabulary |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: stable-horizon-ground, teleport-first-locomotion, world-anchored-ui, seated-mode-and-one-hand, subtitles-default-on-discoverable, snap-turn-default-comfort | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scene-audit` | haiku | Boolean checks per scene. |
| `locomotion-policy` | sonnet | Audience-aware default selection. |
| `a11y-audit` | haiku | Required-fallback presence check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vr-pattern-spec.json` | Skeleton VR-pattern spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vr-design-patterns.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[spatial-accessibility]]
- [[spatial-ux-fundamentals]]
- [[spatial-interaction-patterns]]
- [[immersive-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by audience and per-scene comfort signals; enforces locomotion + anchoring + accessibility defaults. Each leaf cites a rule from `01-core-rules.xml`.
