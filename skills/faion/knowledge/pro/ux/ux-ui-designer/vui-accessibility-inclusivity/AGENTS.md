---
slug: vui-accessibility-inclusivity
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for designing voice interfaces that serve diverse user populations: non-native speakers, accented speech, elderly users, and those with motor or visual impairments.
content_id: "146aee4a9bbbf639"
tags: [vui, accessibility, inclusivity, asr, fairness]
---
# VUI Accessibility and Inclusivity

## Summary

**One-sentence:** A methodology for designing voice interfaces that serve diverse user populations: non-native speakers, accented speech, elderly users, and those with motor or visual impairments.

**One-paragraph:** A methodology for designing voice interfaces that serve diverse user populations: non-native speakers, accented speech, elderly users, and those with motor or visual impairments. Apply word-error-rate (WER) fairness evaluation across demographic slices, keep prompt language at reading grade 8 or below, and always provide a visual transcript alternative. Voice is an accessibility modality, not an add-on feature.

## Applies If (ALL must hold)

- Building voice agents or IVR for diverse user bases: non-native speakers, elderly users, motor- or visually-impaired users.
- Auditing an existing voice product for ASR error rate by demographic group.
- Localizing a voice agent into a new language or regional dialect.
- Designing voice as the accessibility alternative to a touch UI (kiosk, automotive, hands-busy context).

## Skip If (ANY kills it)

- Single-locale, single-accent, narrow-demographic prototype — full diversity testing can wait until validation.
- Heavy ambient-noise contexts where ASR fails for everyone — fix the audio pipeline (echo cancel, beamforming) first.
- Phone-tree IVR with rigid menu prompts — touch-tone fallback is the inclusive design path; accent-handling is secondary.

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
