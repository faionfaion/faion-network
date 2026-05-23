# Voice Agents — Implementation

## Summary

**One-sentence:** Production implementation of voice agents — Realtime/Production agent classes with VAD, async tool calling, state machine, FastAPI WebSocket endpoint.

**One-paragraph:** This methodology turns the STT→LLM→TTS pipeline into a production voice agent that handles real-time conversation. Covers: Silero/WebRTC VAD (not energy thresholds), state machine (IDLE/LISTENING/PROCESSING/SPEAKING), async tool calling via thread executor, markdown stripping before TTS, sliding-window context management, latency budget (≤3s end-to-end or OpenAI Realtime API for <300ms), per-turn audit logging, and a FastAPI WebSocket endpoint for browser/mobile clients. Output: a `ProductionVoiceAgent` class + `voice_ws` FastAPI route + audit log schema.

**Ефективно для:**

- Conversational voice agent з full STT→LLM→TTS loop + multi-turn tool use.
- Browser/mobile клієнт через WebSocket — latency budget <3s end-to-end.
- Замінити energy VAD на Silero/WebRTC у production environment з фоновим шумом.
- State-machine-driven dialog: IDLE→LISTENING→PROCESSING→SPEAKING transitions.
- Realtime-API low-latency (<300ms) deployments — OpenAI native voice path.

## Applies If (ALL must hold)

- Building conversational voice agent з full STT→LLM→TTS loop.
- Exposing voice agent over WebSocket (browser, mobile, embedded device).
- Multi-turn voice conversation з tool use (function calling).
- Response latency budget ≤3s end-to-end (or OpenAI Realtime API for sub-300ms).

## Skip If (ANY kills it)

- Batch audio processing — use `[[speech-to-text-basics]]` + `[[tts-implementation]]`; VAD loop is unnecessary overhead.
- Single-turn transcription без conversation — direct Whisper call simpler.
- Phone/PSTN integration — requires SIP/RTP bridge (Twilio, Vonage) outside this scope.
- Headless server без microphone access (CI environments).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| OpenAI / provider API keys | secret | secrets manager |
| Microphone-capable runtime (browser, mobile, edge) | platform spec | client integration |
| Tool catalog (sync + async functions) | python module | service repo |
| System prompt | YAML | content repo |
| VAD config (Silero or WebRTC) | YAML | service repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[speech-to-text-basics]]` | Upstream Whisper baseline. |
| `[[tts-implementation]]` | Downstream TTS pipeline. |
| `[[openai-api-integration]]` | LLM SDK baseline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: Silero VAD, async tool executor, markdown strip, sliding context, Realtime API thresholds, per-turn audit, max_response_tokens cap | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for voice-agent-config + per-turn audit row shape | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: async-tool-registered-sync, bare-except-on-WS, energy-VAD-in-prod, no-markdown-strip | ~700 |
| `content/04-procedure.xml` | essential | Steps: pick VAD → wire state machine → register tools (sync + thread exec for async) → strip markdown → wrap WS endpoint → audit | ~900 |
| `content/06-decision-tree.xml` | essential | Routes latency / privacy / platform requirements to Realtime API vs STT+LLM+TTS path | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-vad-stack` | sonnet | Trade-off between WebRTC simplicity and Silero accuracy. |
| `wire-state-machine` | sonnet | Mechanical pattern with edge cases. |
| `tune-tool-execution` | opus | Async-vs-sync split + thread executor depth. |
| `audit-turn-schema` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/production_voice_agent.py` | ProductionVoiceAgent skeleton with state machine + tool executor + audit hook. |
| `templates/voice-agent-config.json` | Config artefact: VAD pick, latency budget, providers, tool catalog. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-implementation.py` | Validate voice-agent-config artefact against 02-output-contract. | Pre-commit + CI. |

## Related

- [[speech-to-text-basics]]
- [[speech-to-text-advanced]]
- [[tts-implementation]]
- [[voice-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides between the sub-300ms Realtime API path and the STT+LLM+TTS chain, then between Silero and WebRTC VAD, based on latency budget, privacy, and microphone environment. Walk it before wiring; choosing energy VAD in a production environment guarantees false triggers.
