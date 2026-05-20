---
slug: voice-agents
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production voice AI agents built on real-time STT → LLM → TTS pipelines.
content_id: "8a9f65938ff14348"
tags: [voice-agents, real-time-ai, telephony, speech-to-text, text-to-speech]
---
# Voice Agents

## Summary

**One-sentence:** Production voice AI agents built on real-time STT → LLM → TTS pipelines.

**One-paragraph:** Production voice AI agents built on real-time STT → LLM → TTS pipelines. Use managed platforms (Retell AI, Vapi, ElevenLabs) for phone and web voice agents. Total pipeline latency target is 600-800ms; anything above 1.5s feels broken. Keep LLM responses to 1-3 sentences and strip all markdown before TTS synthesis.

## Applies If (ALL must hold)

- Building phone-based AI agents: inbound/outbound call center, appointment scheduling, support
- Web or mobile app requires real-time voice conversation (browser WebRTC)
- Replacing IVR (Interactive Voice Response) menus with natural conversational AI
- Voice accessibility feature: hands-free interface for existing agent workflows
- Live translation agent: real-time speech-to-speech across 100+ languages

## Skip If (ANY kills it)

- Text chat is sufficient — voice adds latency, cost, and infrastructure complexity for no UX gain
- Latency budget is below 300ms end-to-end — no current production stack achieves this reliably
- Audio quality is unpredictable (noisy environment, poor microphone) — accuracy degrades significantly
- Use case requires precise multi-step confirmation (legal, medical consent) — voice ambiguity introduces risk; use structured text forms instead
- Self-hosted required with <$500/month infra budget — LiveKit self-hosting requires real-time media server expertise

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

- parent skill: `geek/ai/ml-engineer/`
