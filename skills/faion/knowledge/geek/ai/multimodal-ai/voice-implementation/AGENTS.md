# Voice Agents — Implementation

## Summary

Production implementation of voice agents: RealtimeVoiceAgent with energy-based VAD and threading, ProductionVoiceAgent with state machine (IDLE/LISTENING/PROCESSING/SPEAKING) and async tool calling, and a FastAPI WebSocket endpoint for browser/mobile clients.

## Why

The basic STT → LLM → TTS loop must be wrapped in explicit state management to prevent concurrent turn processing, and conversation history must be capped to avoid context overflow. Energy-based VAD is a prototype approximation — production deployments require Silero VAD or WebRTC VAD for reliable speech detection in real environments.

## When To Use

- Building a conversational voice agent with full STT → LLM → TTS loop
- Exposing a voice agent over WebSocket (browser, mobile, embedded)
- Implementing multi-turn voice conversation with tool use (function calling)
- Adding voice I/O to an existing text-based agent pipeline
- Real-time voice interaction where response latency must be under 3 seconds

## When NOT To Use

- Batch audio processing — use speech-to-text-basics + tts-implementation; the VAD loop is unnecessary overhead
- Single-turn transcription without conversation — direct Whisper call is simpler
- Phone/PSTN integration — requires a SIP/RTP bridge (Twilio, Vonage) not covered here
- Environments without microphone access (CI, headless servers)

## Content

| File | What's inside |
|------|---------------|
| `content/01-realtime-agent.xml` | RealtimeVoiceAgent with VADConfig, audio capture thread, energy-based VAD, utterance processing |
| `content/02-production-agent.xml` | ProductionVoiceAgent with state enum, async handle_audio, tool calling, context window management |
| `content/03-rules.xml` | VAD replacement rule, context window cap, markdown stripping before TTS, async tool functions rule |

## Templates

| File | Purpose |
|------|---------|
| `templates/realtime-agent.py` | RealtimeVoiceAgent with threaded capture and VAD processing |
| `templates/production-agent.py` | ProductionVoiceAgent with state machine, tool support, session management |
| `templates/websocket-server.py` | FastAPI WebSocket endpoint wiring ProductionVoiceAgent |
| `templates/system-prompt.txt` | Voice agent system prompt: 2-sentence rule, no markdown, tool explanation pattern |
