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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-implementation.py` | Validate voice-agent-config artefact against 02-output-contract. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[speech-to-text-basics]]
- [[speech-to-text-advanced]]
- [[tts-implementation]]
- [[voice-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides between the sub-300ms Realtime API path and the STT+LLM+TTS chain, then between Silero and WebRTC VAD, based on latency budget, privacy, and microphone environment. Walk it before wiring; choosing energy VAD in a production environment guarantees false triggers.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/production_voice_agent.py`

```python
from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class AgentState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"


@dataclass
class VoiceAgentConfig:
    vad: str = "silero"
    stack: str = "stt_llm_tts"
    latency_budget_ms: int = 2500
    sliding_window_turns: int = 12
    max_response_tokens: int = 180


@dataclass
class ProductionVoiceAgent:
    """State-machine-driven voice agent. Rules: r1-r7 of voice-implementation."""

    config: VoiceAgentConfig
    stt: Any
    llm: Any
    tts: Any
    vad: Any
    tools: dict[str, Callable[..., Any]] = field(default_factory=dict)
    state: AgentState = AgentState.IDLE
    history: list[dict] = field(default_factory=list)
    log: logging.Logger = field(default_factory=lambda: logging.getLogger("voice-agent"))

    _MD_RE = re.compile(r"[*_`#>]")

    def _strip_markdown(self, text: str) -> str:
        # rule r3: never feed raw markdown to TTS
        return self._MD_RE.sub("", text)

    async def _call_tool(self, name: str, **kwargs) -> Any:
        # rule r2: blocking tools go through a thread executor
        fn = self.tools[name]
        if asyncio.iscoroutinefunction(fn):
            return await fn(**kwargs)
        return await asyncio.to_thread(fn, **kwargs)

    def _slide_history(self) -> None:
        # rule r4: cap history to sliding_window_turns
        keep = self.config.sliding_window_turns
        if len(self.history) > keep:
            self.history = self.history[-keep:]

    async def handle_turn(self, audio_bytes: bytes) -> dict:
        t0 = time.monotonic()
        self.state = AgentState.PROCESSING
        transcript = await self.stt.transcribe(audio_bytes)
        llm_resp = await self.llm.chat(
            history=self.history,
            user=transcript,
            tools=list(self.tools),
            max_response_tokens=self.config.max_response_tokens,
        )
        tool_calls = []
        for call in llm_resp.get("tool_calls", []):
            result = await self._call_tool(call["name"], **call["args"])
            tool_calls.append({"name": call["name"], "result": result})
        text = self._strip_markdown(llm_resp["text"])
        self.state = AgentState.SPEAKING
        audio = await self.tts.synthesize(text)
        self.history.append({"user": transcript, "assistant": text})
        self._slide_history()
        self.state = AgentState.IDLE
        # rule r6: log all five fields
        audit = {
            "input_transcript": transcript,
            "llm_response": text,
            "tool_calls": tool_calls,
            "audio_duration": getattr(audio, "duration_s", None),
            "turn_latency_ms": int((time.monotonic() - t0) * 1000),
        }
        self.log.info("voice-turn", extra=audit)
        return {"audio": audio, "audit": audit}
```

### `templates/voice-agent-config.json`

```json
{
  "vad": "silero",
  "stack": "stt_llm_tts",
  "latency_budget_ms": 2500,
  "tool_executor": {
    "mode": "thread"
  },
  "context": {
    "sliding_window_turns": 12,
    "max_response_tokens": 180
  },
  "tts_markdown_stripped": true,
  "audit": {
    "fields": [
      "input_transcript",
      "llm_response",
      "tool_calls",
      "audio_duration",
      "turn_latency_ms"
    ]
  }
}
```
