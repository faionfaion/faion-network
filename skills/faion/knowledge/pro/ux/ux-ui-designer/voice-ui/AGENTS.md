---
slug: voice-ui
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a voice-UI specification authoring sample dialogues first, then defining intents/slots, prompts, and a 3-tier error-recovery ladder (rephrase → examples → fallback) before any NLU training begins.
content_id: "86dd9e9bf58a407b"
complexity: medium
produces: spec
est_tokens: 4200
tags: [voice-ui, conversational-design, nlu, dialogue-design, accessibility]
---
# Voice UI Design: Dialogue-First Methodology

## Summary

**One-sentence:** Produces a voice-UI specification authoring sample dialogues first, then defining intents/slots, prompts, and a 3-tier error-recovery ladder (rephrase → examples → fallback) before any NLU training begins.

**One-paragraph:** Voice interfaces fail when copied from visual UI patterns: users do not know what to say, prompts are robotic, errors are dead ends. This methodology forces dialogue-first design — write sample conversations before code, derive intents/slots from real wording, ship a 3-tier error-recovery ladder, and make confirmation strategy explicit for irreversible actions. Output is a spec consumed by Alexa Skills Kit / Google Actions / custom LLM voice (Realtime API, Gemini Live, Pipecat).

**Ефективно для:**

- Designing voice assistant, app voice command, або IVR з нуля.
- Authoring sample dialogues BEFORE NLU/intent training.
- Designing 3-tier error-recovery ladder для voice prompts.
- Explicit confirmation strategy для irreversible actions (delete, send, pay).

## Applies If (ALL must hold)

- Product ships voice-controlled interactions (assistant, command, IVR).
- Voice is a primary modality — not just a fallback.
- Team can iterate on prompts before model training.

## Skip If (ANY kills it)

- Voice as marketing checkbox only — no real intent coverage.
- Pure dictation tool with no dialogue (use STT methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case description | Markdown | PM |
| Target platforms | list (alexa / google / custom-llm) | engineering |
| Sensitive-action list | list | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vui-conversation-design]] | state-machine vocabulary upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: dialogues-before-code, error-ladder-3-tier, prompt-grade-8-and-short, explicit-confirmation-irreversible, barge-in-allowed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `author-dialogues` | sonnet | Natural-language drafting. |
| `extract-intents` | haiku | Mechanical NLU schema. |
| `write-prompts` | sonnet | Tone + length tuning. |
| `error-ladder` | sonnet | Escalation design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/voice-spec.json` | Skeleton voice-spec |
| `templates/dialogue-template.md` | Dialogue-authoring template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-ui.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[vui-conversation-design]]
- [[vui-accessibility-inclusivity]]
- [[vui-privacy-security]]
- [[vui-testing-best-practices]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by intent reversibility + utterance coverage; enforces confirmation for irreversible actions and 3-tier ladder for the rest. Each leaf cites a rule from `01-core-rules.xml`.
