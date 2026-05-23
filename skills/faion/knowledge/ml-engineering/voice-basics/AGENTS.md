# Voice Agent Basics

## Summary

**One-sentence:** Chains Whisper STT → GPT-4o reasoning → OpenAI TTS into a turn-based loop targeting ≤1000ms total latency, with VAD-based recording and 10-turn history truncation.

**One-paragraph:** Voice agents expose LLM reasoning through speech. Pipeline budgets: VAD ≤100ms, STT ≤300ms, LLM ≤500ms, TTS ≤200ms → total ≤1000ms. Records audio until VAD detects silence (webrtcvad or Silero), transcribes with Whisper specifying `language=` explicitly, reasons with GPT-4o under a system prompt that bans Markdown and caps response length, and synthesizes audio with `tts-1` (not `tts-1-hd`) for realtime. Conversation history truncated to the last 10 turns to prevent context overflow.

**Ефективно для:** інженера-агента, що додає голос до текстового пайплайну — закриває петлю між мікрофоном і динаміком з контрольованим бюджетом затримки.

## Applies If (ALL must hold)

- Customer-service / accessibility / assistant use cases where voice I/O is appropriate.
- End-to-end latency budget allows ≤1000ms (≤1500ms acceptable on tight networks).
- Microphone access is available on the host (sounddevice / pyaudio).
- The reasoning content fits 1-3 short spoken sentences per turn (no tables, code, lists).
- The deployment can run a persistent Python event loop (not stateless request/response).

## Skip If (ANY kills it)

- Sub-300ms end-to-end latency required — use OpenAI Realtime API (WebSocket) instead.
- High-security / GDPR-strict context where audio recording is unacceptable.
- Noisy environment with SNR &lt; 10 dB — Whisper accuracy degrades materially.
- Output content is structured (table, code, JSON) — voice cannot render formatting.
- Tasks that require turn-by-turn screen sharing or visual reference.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| System prompt | string ≤200 words, no Markdown | conversation designer |
| Voice id | semantic label (`assistant`, `narrator`) | content type router |
| Microphone access | sounddevice / pyaudio device handle | host setup |
| Language tag | ISO 639-1 (`en`, `uk`, `de`) | session bootstrap |
| OpenAI API key | env: `OPENAI_API_KEY` | secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/voice-implementation` | production state-machine + WebSocket wrapper that builds on this basic loop. |
| `geek/ai/multimodal-ai/tts-basics` | single-call TTS routing reused for the speak step. |
| `geek/ai/multimodal-ai/speech-to-text-basics` | Whisper STT call patterns reused for the listen step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: latency budget, VAD-based recording, response ≤50 words, history truncate ≤10, explicit language, streaming TTS | ~1000 |
| `content/02-output-contract.xml` | essential | Schema of one turn: transcribed_text, response_text, audio_path, latencies, history | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: fixed-duration recording, sync tool blocking, no interrupt, Markdown to TTS, context overflow | ~900 |
| `content/04-procedure.xml` | medium | 6-step turn procedure: record → STT → reason → strip markdown → TTS → log | ~700 |
| `content/05-examples.xml` | medium | Worked turn with VAD recording + Whisper + GPT-4o + streaming TTS | ~500 |
| `content/06-decision-tree.xml` | essential | Realtime API vs chained STT/LLM/TTS, language detect on/off, voice selection | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `record-audio` | haiku | VAD + sounddevice; mechanical. |
| `transcribe` | haiku | Whisper SDK call. |
| `reason` | sonnet | The conversational reply itself. |
| `design-system-prompt` | sonnet | One-time conversation-design pass. |

## Templates

| File | Purpose |
|------|---------|
| `templates/basic-voice-agent.py` | BasicVoiceAgent with listen / think / speak loop. |
| `templates/vad-recording.py` | webrtcvad-based recorder stopping on silence. |
| `templates/prompt-design.txt` | System prompt + per-turn prompt patterns for voice agents. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-basics.py` | Validate per-turn output JSON against 02-output-contract. | Post-turn, before pushing audio to playback. |

## Related

- [[voice-implementation]] — production state machine + WebSocket wrapper.
- [[tts-basics]] — TTS call routing.
- [[speech-to-text-basics]] — Whisper call patterns.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether to use the chained STT/LLM/TTS pipeline (latency 650-1900ms, max flexibility) or to escalate to OpenAI Realtime API (sub-300ms, tighter contract). It also picks the Whisper language tag and the voice selection. Use it during session bootstrap before the first turn.
