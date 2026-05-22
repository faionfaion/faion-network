---
slug: llm-powered-conversational-ai
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design and implement voice/text conversational interfaces backed by an LLM core (ASR → LLM → TTS pipeline) rather than rule-based NLU.
content_id: "cfe94ee1911fd184"
tags: [conversational-ai, voice-ui, llm, asr, tts]
---
# LLM-Powered Conversational AI

## Summary

**One-sentence:** Design and implement voice/text conversational interfaces backed by an LLM core (ASR → LLM → TTS pipeline) rather than rule-based NLU.

**One-paragraph:** Design and implement voice/text conversational interfaces backed by an LLM core (ASR → LLM → TTS pipeline) rather than rule-based NLU. The LLM handles complex, multi-part queries, maintains conversation history, resolves ambiguity, and generates natural continuations — capabilities that traditional intent-slot systems cannot match.

## Applies If (ALL must hold)

- Replacing a rule-based chatbot that fails on complex or multi-part queries
- Building a voice agent where users phrase the same intent in many different ways
- Implementing natural follow-up handling across multi-turn conversations
- Prototyping an ASR → LLM → TTS pipeline for a product voice feature
- Adding ambiguity clarification to a conversational flow

## Skip If (ANY kills it)

- Narrow command set (3–10 intents) — rule-based NLU is simpler, faster, cheaper, and more reliable
- Response must be deterministic and auditable (medical dosage, legal status) — LLM variability is a liability
- Latency budget is under 300ms end-to-end — the ASR → LLM → TTS stack has irreducible latency
- Product needs autonomous action execution without human confirmation — guardrail architecture must come first
- High background noise or non-standard accents at scale — ASR accuracy is the bottleneck, not LLM quality

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

- parent skill: `geek/ux/ui-designer/`
