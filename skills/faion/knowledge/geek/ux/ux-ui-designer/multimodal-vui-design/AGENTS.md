---
slug: multimodal-vui-design
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for voice-first UI that also exposes visual / haptic affordances — modality matrix, fallback ladder, recognition error model, persona voice constraints.
content_id: "586d55b2e1eeecaf"
complexity: deep
produces: spec
est_tokens: 4900
tags: [vui, voice-ui, multimodal, speech-recognition, asr-tts]
---

# Multimodal VUI Design Spec

## Summary

**One-sentence:** Spec for voice-first UI that also exposes visual / haptic affordances — modality matrix, fallback ladder, recognition error model, persona voice constraints.

**One-paragraph:** Spec for voice-first UI that also exposes visual / haptic affordances — modality matrix, fallback ladder, recognition error model, persona voice constraints. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying multimodal vui design spec. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for multimodal vui design spec across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- voice is a primary interaction modality (not just dictation), with visual or haptic affordances supporting it
- the experience runs on a device with ASR + TTS available (smart speaker, in-car, wearable, phone)
- the team owns voice prompt, wake-word policy, and recognition-error handling

## Skip If (ANY kills it)

- voice is only an accessibility option, not a primary modality — use a11y methodology instead
- single-utterance command set with no follow-up turns — use simpler intent-design methodology
- voice is rendered by a third-party platform (Alexa, Google Assistant) with no UX control — use platform-specific docs

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ASR + TTS capability sheet | vendor + model + language list | ml-engineering |
| Persona voice constraints | tone, age range, language style | brand |
| Recognition error budget | WER target + recovery turns | ml-engineering |
| Visual or haptic surface inventory | what affordances support voice | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[llm-powered-conversational-ai]] | Conversational backbone |
| [[wcag-22-checklist]] | A11y baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `modality_matrix_design` | sonnet | Per task: voice / visual / haptic mapping. |
| `error_recovery_design` | opus | ASR / TTS / intent-mismatch recovery ladder. |
| `voice_persona_check` | sonnet | Brand fit on TTS samples. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui-spec.md` | Spec skeleton for multimodal VUI |
| `templates/modality-matrix.json` | Per-task modality matrix skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in VUI spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multimodal-vui-design.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[llm-powered-conversational-ai]]
- [[ai-spatial-computing]]
- [[generative-ui-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
