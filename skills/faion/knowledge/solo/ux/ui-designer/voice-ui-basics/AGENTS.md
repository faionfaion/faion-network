---
slug: voice-ui-basics
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A process for designing voice user interfaces (VUI): write sample dialogues first, then extract intent/slot schemas, design prompts under 20 words, build a 3-attempt error recovery chain, and validate with Wizard of Oz testing before any NLU training begins.
content_id: "bbfcc13f5372f068"
tags: [voice-ui, conversational-design, nlu, dialogue-design, error-handling]
---
# Voice UI Design Basics

## Summary

**One-sentence:** A process for designing voice user interfaces (VUI): write sample dialogues first, then extract intent/slot schemas, design prompts under 20 words, build a 3-attempt error recovery chain, and validate with Wizard of Oz testing before any NLU training begins.

**One-paragraph:** A process for designing voice user interfaces (VUI): write sample dialogues first, then extract intent/slot schemas, design prompts under 20 words, build a 3-attempt error recovery chain, and validate with Wizard of Oz testing before any NLU training begins.

## Applies If (ALL must hold)

- Designing a new voice feature for a mobile app, smart speaker skill, or IVR system
- Writing and reviewing dialogue scripts for conversational AI products
- Defining intent/slot schemas for NLU training (Alexa, Dialogflow, Rasa)
- Auditing existing voice flows for error handling gaps and confirmation strategy mismatches
- Generating utterance variations for NLU training data

## Skip If (ANY kills it)

- Complex data entry, browsing, or detailed comparison tasks — voice is the wrong modality
- Noisy environments or contexts requiring private information (credit card numbers, passwords)
- First-version MVP features where basic screen UI is not yet validated
- Platforms without microphone access or TTS output capability

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

- parent skill: `solo/ux/ui-designer/`
