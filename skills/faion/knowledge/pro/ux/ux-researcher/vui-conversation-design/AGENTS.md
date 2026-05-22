---
slug: vui-conversation-design
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: VUI conversation design structures intent-based dialog flows for voice interfaces: defining intents, slots, prompt classes (open, directed, option, confirmation), happy paths, and all repair branches (no-match, no-input, max-retry, escape-to-human).
content_id: "50b47ba24bfb8d6a"
tags: [voice-ui, conversation-design, dialog-flow, intent-design, repair-paths]
---
# VUI Conversation Design

## Summary

**One-sentence:** VUI conversation design structures intent-based dialog flows for voice interfaces: defining intents, slots, prompt classes (open, directed, option, confirmation), happy paths, and all repair branches (no-match, no-input, max-retry, escape-to-human).

**One-paragraph:** VUI conversation design structures intent-based dialog flows for voice interfaces: defining intents, slots, prompt classes (open, directed, option, confirmation), happy paths, and all repair branches (no-match, no-input, max-retry, escape-to-human). The method applies to Alexa Skills, Google Actions, IVR systems, and in-app voice features that use a defined intent+entity NLU model.

## Applies If (ALL must hold)

- Authoring intent-based dialog flows with defined intents and slots.
- Writing prompt copy in all four classes (open, directed, option, confirmation) and tagging for analytics.
- Migrating a chatbot script to voice where brevity, prosody, and turn-taking change the requirements.
- Adding repair coverage (no-match, no-input, escalation) to an existing dialog graph.

## Skip If (ANY kills it)

- LLM-only freestyle conversation without pre-defined intents — that needs RAG-driven or agentic dialog methodology.
- Pure GUI form-filling — no turn-taking benefit from VUI design patterns.
- Asynchronous chat (email, ticketing) where real-time constraint is absent.
- One-shot commands with no follow-up (smart-home toggle) — dialog flow is degenerate.

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

- parent skill: `pro/ux/ux-researcher/`
