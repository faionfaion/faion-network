---
slug: vui-accessibility-inclusivity
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for designing voice user interfaces that work equitably across accents, dialects, speech impediments, age groups, and languages.
content_id: "146aee4a9bbbf639"
tags: [voice-ui, accessibility, inclusivity, wcag, asr]
---
# VUI Accessibility and Inclusivity

## Summary

**One-sentence:** Methodology for designing voice user interfaces that work equitably across accents, dialects, speech impediments, age groups, and languages.

**One-paragraph:** Methodology for designing voice user interfaces that work equitably across accents, dialects, speech impediments, age groups, and languages. The core rule: never build a voice-only path — always pair every voice interaction with a visual or touch alternative.

## Applies If (ALL must hold)

- Designing or auditing a VUI or voice assistant feature
- Evaluating speech recognition training data for diversity gaps
- Adding multimodal feedback (visual, haptic) to a voice interface
- Writing error-recovery dialogue scripts for voice flows
- Specifying accent calibration or pronunciation correction features
- Conducting inclusive usability testing with diverse voice participants

## Skip If (ANY kills it)

- Pure GUI components with no voice interaction — use standard accessibility checklist instead
- Backend ASR model training (this methodology covers UX design, not ML training pipelines)
- Text-based chatbots with no speech I/O — different interaction model

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

- parent skill: `pro/ux/accessibility-specialist/`
