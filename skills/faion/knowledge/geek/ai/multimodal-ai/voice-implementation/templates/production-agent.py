"""ProductionVoiceAgent with state machine, tool support, session management."""
import json
import logging
import re
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

from openai import OpenAI


class AgentState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"


@dataclass
class VoiceAgentConfig:
    system_prompt: str
    voice: str = "nova"
    stt_model: str = "whisper-1"
    llm_model: str = "gpt-4o"
    tts_model: str = "tts-1"
    max_response_tokens: int = 200
    silence_timeout: float = 1.0
    max_turns: int = 50
    max_history_turns: int = 10


class ProductionVoiceAgent:
    """Production voice agent with state machine and tool support."""

    def __init__(self, config: VoiceAgentConfig,
                 tools: list[dict] | None = None,
                 tool_functions: dict[str, Callable] | None = None):
        self.config = config
        self.tools = tools or []
        self.tool_functions = tool_functions or {}
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)
        self.state = AgentState.IDLE
        self.conversation_history: list[dict] = [
            {"role": "system", "content": config.system_prompt}
        ]
        self.turn_count = 0

    async def start_session(self) -> None:
        self.state = AgentState.IDLE
        self.conversation_history = [{"role": "system", "content": self.config.system_prompt}]
        self.turn_count = 0

    async def handle_audio(self, audio_data: bytes) -> Optional[bytes]:
        if self.state == AgentState.SPEAKING:
            return None  # barge-in prevention
        if self.turn_count >= self.config.max_turns:
            return await self._synthesize("I need to end our conversation now. Goodbye!")

        self.state = AgentState.LISTENING
        try:
            transcript = await self._transcribe(audio_data)
            if not transcript.strip():
                self.state = AgentState.IDLE
                return None

            self.state = AgentState.PROCESSING
            response = await self._generate_response(transcript)
            self.state = AgentState.SPEAKING
            audio_response = await self._synthesize(response)
            self.turn_count += 1
            self.state = AgentState.IDLE
            return audio_response
        except Exception as e:
            self.logger.error(f"Error handling audio: {e}")
            self.state = AgentState.IDLE
            return None

    async def _transcribe(self, audio_data: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_data)
            f.flush()
            with open(f.name, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model=self.config.stt_model, file=audio_file)
            Path(f.name).unlink()
        return result.text

    async def _generate_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        self._truncate_history()

        kwargs: dict[str, Any] = {
            "model": self.config.llm_model,
            "messages": self.conversation_history,
            "max_tokens": self.config.max_response_tokens
        }
        if self.tools:
            kwargs["tools"] = self.tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        # Second LLM call only when tool calls occurred
        if message.tool_calls:
            self.conversation_history.append(message)
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = (self.tool_functions[func_name](**args)
                          if func_name in self.tool_functions
                          else {"error": f"Unknown: {func_name}"})
                self.conversation_history.append({
                    "role": "tool", "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=self.conversation_history,
                max_tokens=self.config.max_response_tokens
            )
            message = response.choices[0].message

        text = self._strip_markdown(message.content or "")
        self.conversation_history.append({"role": "assistant", "content": text})
        return text

    async def _synthesize(self, text: str) -> bytes:
        response = self.client.audio.speech.create(
            model=self.config.tts_model, voice=self.config.voice, input=text)
        return b"".join(response.iter_bytes())

    def _truncate_history(self) -> None:
        """Keep system prompt + last max_history_turns pairs."""
        system = [m for m in self.conversation_history if m["role"] == "system"]
        turns = [m for m in self.conversation_history if m["role"] != "system"]
        self.conversation_history = system + turns[-(self.config.max_history_turns * 2):]

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """Strip markdown before TTS — asterisks and hashes are read literally."""
        return re.sub(r"[*_`#>]", "", text).strip()
