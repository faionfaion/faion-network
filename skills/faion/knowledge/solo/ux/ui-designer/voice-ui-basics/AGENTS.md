---
slug: voice-ui-basics
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Designing a VUI starts with three primitives — intents (closed set of user goals), prompts (system speech), and error-handling (recovery paths) — so conversation flows do not loop or strand the user.
content_id: "bbfcc13f5372f068"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["voice-ui", "vui", "conversation-design", "intents", "ux"]
---
# Voice UI Basics

## Summary

**One-sentence:** Designing a VUI starts with three primitives — intents (closed set of user goals), prompts (system speech), and error-handling (recovery paths) — so conversation flows do not loop or strand the user.

**One-paragraph:** Voice UIs fail at error handling and intent ambiguity. This methodology pins three primitives: a closed intent set (≤20 high-level user goals), a prompt library (system speech with explicit slot prompts and confirmation lines), and an error-handling matrix (no-input / no-match / fallback). Every voice flow answers these three before persona, tone, or LLM augmentation is layered on.

**Ефективно для:**

- Solo founder building first Alexa / Google Assistant / Siri skill.
- Designer adding voice as a secondary interface to a mobile app.
- AI agent generating dialog flows where intent coverage must be explicit.
- Pre-launch voice-app review where conversation traps must be near-zero.

## Applies If (ALL must hold)

- Target device or platform supports VUI (Alexa, Google Assistant, Siri, custom).
- User goals can be enumerated into a closed set (≤20 intents).
- Audio testing environment is available (device, simulator, recording loop).
- Designer can author prompts in the target language.

## Skip If (ANY kills it)

- GUI-only project with no voice input.
- Open-ended LLM chat with no domain constraints — primitives fit poorly.
- Voice-only narration (audiobook, podcast) with no input.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User-goal inventory | list | Research / PM |
| VUI platform docs | URL | Alexa / Dialogflow / Siri |
| Target language list | list | Product i18n |
| Prompt-author handle | string | Designer / agent |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/spatial-ux-fundamentals` | When VUI is embedded in spatial app. |
| `solo/ux/critical-issue-triage-protocol` | Triage of voice-test findings. |

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
| `draft-intent-set` | sonnet | Per-goal judgement on intent boundary. |
| `lint-prompts` | haiku | Deterministic length + style check on prompts. |
| `error-matrix-audit` | opus | Multi-flow synthesis for error coverage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/voice-ui-basics.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/voice-ui-basics.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-ui-basics.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spatial-ux-fundamentals]]
- [[edge-case-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
