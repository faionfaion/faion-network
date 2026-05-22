---
slug: vui-conversation-design
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design multi-turn voice conversations as state machines with explicit intents, entities, and prompts.
content_id: "50b47ba24bfb8d6a"
tags: [vui, conversation-design, dialog, voice-agent, intent-routing]
---
# VUI Conversation Design

## Summary

**One-sentence:** Design multi-turn voice conversations as state machines with explicit intents, entities, and prompts.

**One-paragraph:** Design multi-turn voice conversations as state machines with explicit intents, entities, and prompts. Structure dialog flows for happy paths and edge cases (missing entity, ambiguous input, no match), cap reprompts at 3, and ground every prompt in ≤12 spoken words. Separate voice scripts from screen prompts; test in realistic environments (kitchen noise, traffic).

## Applies If (ALL must hold)

- Building Alexa Skills, Google Actions, Siri shortcuts, or custom voice assistants on top of LLMs.
- Designing IVR replacements with intent + entity routing (banking, support, scheduling).
- Hands-busy / eyes-busy contexts: cooking, driving, factory floor, surgery, accessibility.
- Adding a voice channel to an existing chatbot — the dialog model differs significantly from text.
- LLM-powered conversational agents that need a deterministic dialog skeleton on top of free-form generation.

## Skip If (ANY kills it)

- Privacy-sensitive flows (passwords, medical results) where overheard speech is unacceptable.
- High-precision input (URLs, codes, IDs longer than ~6 chars) — voice degrades sharply.
- Markets with low ambient assistant adoption — discovery and habit formation cost outpaces value.
- Tasks requiring visual scanning (tables, comparison shopping, long lists).

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
