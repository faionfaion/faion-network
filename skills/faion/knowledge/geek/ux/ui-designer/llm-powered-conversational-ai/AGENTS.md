# LLM-Powered Conversational AI

## Summary

Design and implement voice/text conversational interfaces backed by an LLM core (ASR → LLM → TTS pipeline) rather than rule-based NLU. The LLM handles complex, multi-part queries, maintains conversation history, resolves ambiguity, and generates natural continuations — capabilities that traditional intent-slot systems cannot match.

## Why

Rule-based VUI breaks on any query outside its predefined intent list. LLMs interpret open-ended phrasing, ask clarifying questions, and maintain context across turns. The result is a conversational experience that degrades gracefully instead of failing hard. The tradeoff is latency, cost, and hallucination risk — which must be managed with guardrails and a bounded persona scope.

## When To Use

- Replacing a rule-based chatbot that fails on complex or multi-part queries
- Building a voice agent where users phrase the same intent in many different ways
- Implementing natural follow-up handling across multi-turn conversations
- Prototyping an ASR → LLM → TTS pipeline for a product voice feature
- Adding ambiguity clarification to a conversational flow

## When NOT To Use

- Narrow command set (3–10 intents) — rule-based NLU is simpler, faster, cheaper, and more reliable
- Response must be deterministic and auditable (medical dosage, legal status) — LLM variability is a liability
- Latency budget is under 300ms end-to-end — the ASR → LLM → TTS stack has irreducible latency
- Product needs autonomous action execution without human confirmation — guardrail architecture must come first
- High background noise or non-standard accents at scale — ASR accuracy is the bottleneck, not LLM quality

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | ASR → LLM → TTS pipeline stages, guardrail pattern, persona scope rule |
| `content/02-agent-integration.xml` | Subagent roles, prompt patterns, service/tool catalog, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-system-prompt.txt` | System prompt template for voice agent persona with scope boundary |
| `templates/guardrail-validator-prompt.txt` | Guardrail agent prompt for validating tool calls before execution |
| `templates/pipeline.py` | Minimal ASR → LLM → TTS pipeline implementation |
