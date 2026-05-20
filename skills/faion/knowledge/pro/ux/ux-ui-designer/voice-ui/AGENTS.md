---
slug: voice-ui
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for designing speech-controlled interfaces — voice assistants, app voice commands, IVR systems — by writing sample dialogues first, then defining intents/slots, authoring prompts, and designing a 3-tier error-recovery ladder before any NLU training begins.
content_id: "86dd9e9bf58a407b"
tags: [voice-ui, conversational-design, nlu, dialogue-design, accessibility]
---
# Voice UI Design: Dialogue-First Methodology for Voice Assistants and Commands

## Summary

**One-sentence:** A methodology for designing speech-controlled interfaces — voice assistants, app voice commands, IVR systems — by writing sample dialogues first, then defining intents/slots, authoring prompts, and designing a 3-tier error-recovery ladder before any NLU training begins.

**One-paragraph:** A methodology for designing speech-controlled interfaces — voice assistants, app voice commands, IVR systems — by writing sample dialogues first, then defining intents/slots, authoring prompts, and designing a 3-tier error-recovery ladder before any NLU training begins. Voice interfaces fail when copied from visual UI patterns: users do not know what to say, prompts are robotic, errors are dead ends. Writing dialogues before code forces natural language and exposes missing intents early. Error ladders (rephrase → examples → fallback) reduce abandonment; explicit confirmation strategy prevents irreversible actions without user awareness.

## Applies If (ALL must hold)

- Designing a voice assistant, Alexa/Google skill, or IVR flow end-to-end.
- Adding voice commands to an existing app for hands-free or accessibility use.
- Migrating a legacy NLU bot (Dialogflow, Lex) to an LLM-powered runtime.
- Defining acceptance criteria for a voice feature in a spec or design doc.
- Auditing transcripts of an existing voice product for verbosity or missing error paths.

## Skip If (ANY kills it)

- Visual UI work where voice is cosmetic — invest in the core visual flow first.
- Highly private data entry (financial account numbers, medical detail) without strong auth design.
- Noisy or shared environments where ASR reliability cannot be guaranteed.
- Browsing or exploratory tasks — visual lists outperform voice for discovery.
- Rapid prototype stage before basic ASR integration is confirmed working.

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
