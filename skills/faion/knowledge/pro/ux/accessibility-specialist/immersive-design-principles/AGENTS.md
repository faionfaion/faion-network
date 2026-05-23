---
slug: immersive-design-principles
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Five immersive design principles (comfort, locomotion safety, sensory budgets, agency, retreat-option) that gate VR / AR / MR experience design.
content_id: "135b80b9e0974669"
complexity: medium
produces: report
est_tokens: 4100
tags: [immersive, xr, vr, ar, comfort, a11y]
---
# Immersive Design Principles

## Summary

**One-sentence:** Five immersive design principles (comfort, locomotion safety, sensory budgets, agency, retreat-option) that gate VR / AR / MR experience design.

**One-paragraph:** Immersive (VR / AR / MR) experiences amplify both delight and exclusion. This methodology pins five principles — comfort defaults (no forced motion), safe locomotion (teleport + smooth + arm-swinger choice), sensory budgets (audio + visual + haptic capped per minute), explicit agency (no forced gaze / forced action), and a retreat-option (return-to-safe-scene shortcut). Output is an immersive-principles record per experience validated against the schema.

**Ефективно для:**

- Comfort defaults cut motion-sickness exits ≥40%.
- Safe locomotion with choice respects user preferences.
- Sensory budgets prevent overwhelm for ADHD / autism users.
- Retreat-option always available — exit is a right, not a request.

## Applies If (ALL must hold)

- VR, AR, or MR experience entering production.
- Sessions can exceed 5 minutes (where comfort matters).
- Locomotion + sensory + agency choices have not been pinned.

## Skip If (ANY kills it)

- Sub-1-minute tech demo with no production users.
- Flat 2D component — use `accessibility-first-design`.
- Pure passive video / 360 viewer with no interaction (use 360-video a11y guidance).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experience brief | Markdown | product |
| Target platforms | Quest / Vision / PSVR2 / WebXR | platform |
| Sensory inventory | audio + visual + haptic budget | design |
| Locomotion inventory | list of locomotion modes | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/immersive-record.json` | JSON skeleton for the immersive-principles record. |
| `templates/comfort-settings.json` | Default comfort settings template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-immersive-design-principles.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[vr-design-patterns]]
- [[ar-design-patterns]]
- [[spatial-accessibility]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
