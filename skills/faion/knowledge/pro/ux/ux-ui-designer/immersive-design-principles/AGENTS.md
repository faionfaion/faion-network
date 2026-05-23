---
slug: immersive-design-principles
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an immersive (AR/VR/MR/XR) experience spec balancing presence + comfort with concrete budgets for FOV usage, locomotion, session length, vestibular safety, and accessibility.
content_id: "135b80b9e0974669"
complexity: medium
produces: spec
est_tokens: 4500
tags: [immersive-design, vr, ar, mr, xr, comfort]
---
# Immersive Design Principles

## Summary

**One-sentence:** Produces an immersive (AR/VR/MR/XR) experience spec balancing presence + comfort with concrete budgets for FOV usage, locomotion, session length, vestibular safety, and accessibility.

**One-paragraph:** Immersive experiences balance presence (feeling there) with comfort (no nausea, no fatigue). Concrete budgets: FOV target 90-110°, locomotion vestibular-safe (teleport, smooth with vignette), session length capped by use case (consumer 15-30 min, enterprise 25 min + break), spatial audio for presence, accessibility paths (seated, single-handed, mono-vision, low-vision). The spec lists every budget + accessibility path + comfort gate.

**Ефективно для:**

- AR/VR/MR/XR продукт з longer-than-30s session — budgets обов'язкові.
- Locomotion design: teleport vs smooth з vignette — vestibular safety.
- Spatial audio для presence — і a11y fallback на subtitles.
- Seated / single-handed / low-vision paths — а11y від day 1.

## Applies If (ALL must hold)

- Designing an immersive experience longer than 30 seconds.
- Locomotion or sustained interaction is in scope.
- User population includes a non-trivial accessibility tail.

## Skip If (ANY kills it)

- Short AR filter or quick scene with no locomotion — overkill spec.
- Pure passive 360 video — use video UX, not immersive principles.
- Existing system with established comfort patterns — apply as audit, not rewrite.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use case + audience | consumer / enterprise / education | product brief |
| Target hardware | headset list | platform |
| Accessibility audit | spatial-accessibility methodology output | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-accessibility]] | Accessibility paths sourced here |
| [[ar-design-patterns]] | AR-specific patterns when AR is in scope |

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
| `templates/immersive-spec.md` | Immersive experience spec covering locomotion + comfort + a11y + FOV |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-immersive-design-principles.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[enterprise-xr-applications]]
- [[ar-design-patterns]]
- [[vr-design-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
