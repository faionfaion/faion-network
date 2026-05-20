---
slug: voice-implementation
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production implementation of voice agents: RealtimeVoiceAgent with energy-based VAD and threading, ProductionVoiceAgent with state machine (IDLE/LISTENING/PROCESSING/SPEAKING) and async tool calling, and a FastAPI WebSocket endpoint for browser/mobile clients.
content_id: "7edf0a729e6512ee"
tags: [voice, production, websocket, fastapi, realtime]
---
# Voice Agents - Implementation

## Summary

**One-sentence:** Production implementation of voice agents: RealtimeVoiceAgent with energy-based VAD and threading, ProductionVoiceAgent with state machine (IDLE/LISTENING/PROCESSING/SPEAKING) and async tool calling, and a FastAPI WebSocket endpoint for browser/mobile clients.

**One-paragraph:** Production implementation of voice agents: RealtimeVoiceAgent with energy-based VAD and threading, ProductionVoiceAgent with state machine (IDLE/LISTENING/PROCESSING/SPEAKING) and async tool calling, and a FastAPI WebSocket endpoint for browser/mobile clients.

## Applies If (ALL must hold)

- Building a conversational voice agent with full STT to LLM to TTS loop
- Exposing a voice agent over WebSocket (browser, mobile, embedded)
- Implementing multi-turn voice conversation with tool use (function calling)
- Adding voice I/O to an existing text-based agent pipeline
- Real-time voice interaction where response latency must be under 3 seconds

## Skip If (ANY kills it)

- Batch audio processing - use speech-to-text-basics + tts-implementation; the VAD loop is unnecessary overhead
- Single-turn transcription without conversation - direct Whisper call is simpler
- Phone/PSTN integration - requires a SIP/RTP bridge (Twilio, Vonage) not covered here
- Environments without microphone access (CI, headless servers)

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

- parent skill: `geek/ai/multimodal-ai/`
