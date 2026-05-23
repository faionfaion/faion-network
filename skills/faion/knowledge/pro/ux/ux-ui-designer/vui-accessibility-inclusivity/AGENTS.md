---
slug: vui-accessibility-inclusivity
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a VUI inclusivity report measuring WER (word-error-rate) fairness across demographic slices (accent, age, gender), enforcing reading-grade-8 prompts, visual transcript alternative, and motor/visual fallbacks.
content_id: "146aee4a9bbbf639"
complexity: medium
produces: report
est_tokens: 4000
tags: [vui, accessibility, inclusivity, asr, fairness]
---
# VUI Accessibility and Inclusivity

## Summary

**One-sentence:** Produces a VUI inclusivity report measuring WER (word-error-rate) fairness across demographic slices (accent, age, gender), enforcing reading-grade-8 prompts, visual transcript alternative, and motor/visual fallbacks.

**One-paragraph:** Voice interfaces serve diverse users only when WER is measured per demographic slice (overall accuracy hides 15-30 point subgroup gaps), prompts stay at reading grade 8 or below, every voice interaction has a visual-transcript alternative, and motor/visual impairments are accommodated with non-voice fallbacks. This methodology emits an inclusivity report consumed by QA, with hard thresholds (WER fairness gap ≤10 percentage points, grade level ≤8) and required artefacts.

**Ефективно для:**

- Pre-launch fairness audit для voice product з diverse user population.
- WER measurement across accent / age / gender slices.
- Reading-grade-8 prompt audit та simplification.
- Visual-transcript + non-voice fallback enforcement.

## Applies If (ALL must hold)

- Voice is a primary interaction modality.
- Audience includes non-native speakers, accented speech, or elderly users.
- QA can fund per-demographic recording sessions or buy benchmark dataset.

## Skip If (ANY kills it)

- Internal voice prototype with single tester.
- Pure dictation tool without dialogue.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Demographic slice list | list | research |
| Test corpus | labeled audio | QA / vendor |
| Prompt bank | JSON / Markdown | VUI designer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[voice-ui]] | dialogue + prompt vocabulary upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: wer-per-slice, wer-fairness-gap-cap, prompt-grade-8-cap, visual-transcript-alternative, non-voice-fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-slices` | haiku | Mechanical enumeration. |
| `measure-wer` | sonnet | Per-slice analysis. |
| `simplify-prompts` | sonnet | Plain-language rewrites. |

## Templates

| File | Purpose |
|------|---------|
| `templates/inclusivity-report.json` | Skeleton report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-accessibility-inclusivity.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-conversation-design]]
- [[vui-privacy-security]]
- [[vui-testing-best-practices]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by audience scope and measurement signal; remediation actions are tied to specific rule violations. Each leaf cites a rule from `01-core-rules.xml`.
