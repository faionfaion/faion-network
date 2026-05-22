---
slug: llm-powered-conversational-ai
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design and implementation methodology for conversational AI systems using LLMs — system prompt authoring with explicit topic boundaries, guardrail rules, fallback and escalation logic, and red-team testing for jailbreak vectors.
content_id: "cfe94ee1911fd184"
tags: [conversational-ai, llm, system-design, guardrails, safety]
---
# LLM-Powered Conversational AI

## Summary

**One-sentence:** Design and implementation methodology for conversational AI systems using LLMs — system prompt authoring with explicit topic boundaries, guardrail rules, fallback and escalation logic, and red-team testing for jailbreak vectors.

**One-paragraph:** Design and implementation methodology for conversational AI systems using LLMs — system prompt authoring with explicit topic boundaries, guardrail rules, fallback and escalation logic, and red-team testing for jailbreak vectors. Every production system prompt must define: allowed topics (list), forbidden topics (list), escalation triggers, and persona constraints.

## Applies If (ALL must hold)

- Building a voice or chat assistant handling multi-part, ambiguous, or contextually dependent queries
- Replacing a rule-based IVR or FAQ bot where query diversity exceeds what a decision tree covers
- Designing a customer support agent that must maintain conversation history
- Integrating a conversational layer into an existing product (search, onboarding, help center)
- Prototyping dialogue flows before committing to a production NLU platform

## Skip If (ANY kills it)

- Transaction-critical flows (payments, medical orders) without deterministic validation after each LLM turn
- Real-time phone IVR where latency >2s is unacceptable
- Regulated industries where every utterance must be pre-approved (financial advice, clinical diagnosis)
- Query space is small and fully enumerable — rule-based VUI is cheaper and more reliable
- Products without a moderation or content policy layer

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

- parent skill: `geek/ux/ux-ui-designer/`
