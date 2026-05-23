# purpose: ProductionVoiceAgent skeleton with state machine + tool executor + audit hook.
# consumes: voice-agent-config.json + STT/LLM/TTS client instances
# produces: per-turn audit rows + spoken responses over WebSocket
# depends-on: content/01-core-rules.xml r1, r2, r3, r4, r6, r7
# token-budget-impact: ~0 LLM tokens for the wiring itself; per-turn LLM call governed by max_response_tokens
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
