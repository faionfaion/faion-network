# Voice Agents — Basics

## Summary

Building conversational voice agents that chain STT (Whisper) → LLM (GPT-4o) → TTS into a turn-based loop. Covers the basic architecture, latency budget per component, tool-calling integration, and the core pitfalls of fixed-duration recording and unbounded conversation history.

## Why

Voice agents expose LLM reasoning through a natural speech interface, but the sequential STT → LLM → TTS pipeline has a hard 650–1900ms minimum latency floor. Every optimization must target each stage independently; streaming and short responses are the primary levers.

## When To Use

- Customer service automation requiring natural voice interaction
- Accessibility tools where text input is not viable
- Voice-controlled CLI wrappers for internal tools
- Real-time voice assistants embedded in hardware
- Adding speech I/O to an existing text agent

## When NOT To Use

- Latency requirements below 800ms end-to-end — use OpenAI Realtime API (WebSocket) instead
- High-security contexts where audio recording raises GDPR/compliance concerns
- Noisy environments without pre-processing (SNR below 10dB) — Whisper accuracy degrades significantly
- Tasks where text output is superior (structured data, code, tables) — voice cannot render formatting

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | STT → LLM → TTS pipeline, latency table per component, BasicVoiceAgent class |
| `content/02-rules.xml` | VAD recording rule, history truncation rule, TTS response length limit, tool-call handling |

## Templates

| File | Purpose |
|------|---------|
| `templates/basic-voice-agent.py` | BasicVoiceAgent with listen/think/speak loop |
| `templates/tool-voice-agent.py` | ToolEnabledVoiceAgent with function calling |
| `templates/prompt-design.txt` | System prompt and per-turn prompt pattern for voice agents |
| `templates/vad-recording.py` | WebRTC-VAD-based recording (stops on silence) |
