---
slug: llm-powered-conversational-ai
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a conversational-AI design spec for an LLM-core voice/text interface (ASR → LLM → TTS) replacing rule-based intent-slot NLU, with latency budget, safety filters, fallback escalation.
content_id: "41a3d8ba41910cbb"
complexity: deep
produces: spec
est_tokens: 4900
tags: [conversational-ai, voice-ui, llm, asr, tts]
---
# LLM-Powered Conversational AI

## Summary

**One-sentence:** Produces a conversational-AI design spec for an LLM-core voice/text interface (ASR → LLM → TTS) replacing rule-based intent-slot NLU, with latency budget, safety filters, fallback escalation.

**One-paragraph:** LLM-core conversational interfaces handle multi-part queries and ambiguity that rule-based NLU cannot, but introduce latency (ASR + LLM + TTS) and hallucination risk. This methodology produces a design spec covering the three-stage pipeline (ASR provider + LLM model + TTS voice), latency budget per stage (cumulative <2.5 s for voice, <4 s for text), safety filters (jailbreak detection + factual grounding), and a fallback escalation to human + rule-based when confidence drops below threshold.

**Ефективно для:** voice-UX engineer, що замінює rule-based чат-бота на LLM-core pipeline і потребує latency + safety + fallback specs.

## Applies If (ALL must hold)

- Replacing a rule-based chatbot whose intent-slot model fails on multi-part queries.
- Building a voice agent where users phrase the same intent many different ways.
- Latency budget allows ASR + LLM + TTS round-trip (voice <2.5 s, text <4 s).

## Skip If (ANY kills it)

- Domain is high-stakes (medical / legal advice) without expert validation pipeline.
- Conversation is single-turn and deterministic — rule-based is cheaper.
- No safety / grounding pipeline available — hallucination risk too high to ship.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ASR provider creds | secret | secrets manager |
| LLM model + endpoint | config | engineering |
| TTS voice config | config | engineering |
| Safety policy (jailbreak + grounding sources) | YAML | trust + safety |
| Fallback escalation target | config | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[multimodal-vui-design]] | Voice + visual sync rules. |
| [[ai-design-assistant-patterns]] | Assistant pattern catalogue. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-spec` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/convo-spec.json` | JSON skeleton: modality + providers + latency + safety + fallback + audit. |
| `templates/safety-policy.yaml` | Jailbreak detector + grounding source list + refusal templates. |
| `templates/_smoke-test.json` | Filled voice-tier1 conversational AI spec. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llm-powered-conversational-ai.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[multimodal-vui-design]]
- [[ai-design-assistant-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the spec; mis-routing leads to producing the wrong artefact shape.
