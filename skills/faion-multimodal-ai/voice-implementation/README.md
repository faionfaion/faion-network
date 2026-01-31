---
id: voice-implementation
name: "Voice Agents - Implementation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Voice Agents - Implementation

Advanced implementation patterns for production voice agents.

## Real-time Voice Agent

```python
import asyncio
import queue
import threading
from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np

@dataclass
class VADConfig:
    threshold: float = 0.02
    min_speech_duration: float = 0.5
    silence_duration: float = 0.8

class RealtimeVoiceAgent:
    """Voice agent with real-time streaming."""

    def __init__(
        self,
        system_prompt: str,
        voice: str = "nova",
        vad_config: VADConfig = None
    ):
        self.system_prompt = system_prompt
        self.voice = voice
        self.vad_config = vad_config or VADConfig()

        self.client = OpenAI()
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_speaking = False

    def start(self):
        """Start the voice agent."""
        self.is_listening = True

        # Start audio capture thread
        capture_thread = threading.Thread(target=self._capture_audio)
        capture_thread.start()

        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio)
        process_thread.start()

        return capture_thread, process_thread

    def stop(self):
        """Stop the voice agent."""
        self.is_listening = False

    def _capture_audio(self):
        """Capture audio from microphone."""
        import sounddevice as sd

        def callback(indata, frames, time, status):
            if self.is_listening and not self.is_speaking:
                self.audio_queue.put(indata.copy())

        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype='float32',
            callback=callback,
            blocksize=1600  # 100ms blocks
        ):
            while self.is_listening:
                sd.sleep(100)

    def _process_audio(self):
        """Process captured audio with VAD."""
        audio_buffer = []
        speech_detected = False
        silence_frames = 0

        while self.is_listening:
            try:
                audio_chunk = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Simple VAD: energy-based
            energy = np.sqrt(np.mean(audio_chunk ** 2))

            if energy > self.vad_config.threshold:
                speech_detected = True
                silence_frames = 0
                audio_buffer.append(audio_chunk)
            elif speech_detected:
                silence_frames += 1
                audio_buffer.append(audio_chunk)

                # Check if speech ended
                if silence_frames > self.vad_config.silence_duration * 10:
                    if len(audio_buffer) > self.vad_config.min_speech_duration * 10:
                        # Process utterance
                        audio_data = np.concatenate(audio_buffer)
                        self._handle_utterance(audio_data)

                    audio_buffer = []
                    speech_detected = False
                    silence_frames = 0

    def _handle_utterance(self, audio_data: np.ndarray):
        """Process a complete utterance."""
        self.is_speaking = True

        try:
            # Transcribe
            transcript = self._transcribe(audio_data)
            print(f"User: {transcript}")

            if transcript.strip():
                # Generate response
                response = self._generate_response(transcript)
                print(f"Agent: {response}")

                # Speak response
                self._speak(response)

        finally:
            self.is_speaking = False

    def _transcribe(self, audio_data: np.ndarray) -> str:
        """Transcribe audio data."""
        import tempfile
        import wave

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

            with open(f.name, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            Path(f.name).unlink()

        return result.text

    def _generate_response(self, user_input: str) -> str:
        """Generate LLM response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history,
            max_tokens=150  # Keep responses short for voice
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _speak(self, text: str):
        """Speak text with streaming."""
        import pyaudio

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )

        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=self.voice,
            input=text,
            response_format="pcm"
        ) as response:
            for chunk in response.iter_bytes(chunk_size=1024):
                stream.write(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
```

## Production Voice Agent

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
import logging
import asyncio

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
    vad_threshold: float = 0.02
    silence_timeout: float = 1.0
    max_turns: int = 50

class ProductionVoiceAgent:
    """Production-ready voice agent."""

    def __init__(
        self,
        config: VoiceAgentConfig,
        tools: List[Dict] = None,
        tool_functions: Dict[str, Callable] = None
    ):
        self.config = config
        self.tools = tools or []
        self.tool_functions = tool_functions or {}
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

        self.state = AgentState.IDLE
        self.conversation_history = [
            {"role": "system", "content": config.system_prompt}
        ]
        self.turn_count = 0

    async def start_session(self):
        """Start voice session."""
        self.state = AgentState.IDLE
        self.conversation_history = [
            {"role": "system", "content": self.config.system_prompt}
        ]
        self.turn_count = 0
        self.logger.info("Voice session started")

    async def end_session(self):
        """End voice session."""
        self.state = AgentState.IDLE
        self.logger.info(f"Voice session ended after {self.turn_count} turns")

    async def handle_audio(self, audio_data: bytes) -> Optional[bytes]:
        """Handle incoming audio and return response audio."""
        if self.state == AgentState.SPEAKING:
            return None

        if self.turn_count >= self.config.max_turns:
            self.logger.warning("Max turns reached")
            return await self._speak("I need to end our conversation now. Goodbye!")

        self.state = AgentState.LISTENING

        try:
            # Transcribe
            transcript = await self._transcribe(audio_data)
            if not transcript.strip():
                self.state = AgentState.IDLE
                return None

            self.logger.info(f"User: {transcript}")
            self.state = AgentState.PROCESSING

            # Generate response
            response = await self._generate_response(transcript)
            self.logger.info(f"Agent: {response}")

            # Synthesize speech
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
        """Transcribe audio data."""
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_data)
            f.flush()

            with open(f.name, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model=self.config.stt_model,
                    file=audio_file
                )

            Path(f.name).unlink()

        return result.text

    async def _generate_response(self, user_input: str) -> str:
        """Generate LLM response with tool support."""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Call LLM
        kwargs = {
            "model": self.config.llm_model,
            "messages": self.conversation_history,
            "max_tokens": self.config.max_response_tokens
        }

        if self.tools:
            kwargs["tools"] = self.tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            self.conversation_history.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name in self.tool_functions:
                    result = self.tool_functions[func_name](**args)
                else:
                    result = {"error": f"Unknown function: {func_name}"}

                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Get final response
            response = self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message

        assistant_message = message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    async def _synthesize(self, text: str) -> bytes:
        """Synthesize speech."""
        response = self.client.audio.speech.create(
            model=self.config.tts_model,
            voice=self.config.voice,
            input=text
        )

        # Collect all chunks
        audio_data = b""
        for chunk in response.iter_bytes():
            audio_data += chunk

        return audio_data

    async def _speak(self, text: str) -> bytes:
        """Quick helper to speak a message."""
        return await self._synthesize(text)

    def get_conversation_summary(self) -> str:
        """Get summary of conversation."""
        messages = [
            m for m in self.conversation_history
            if m["role"] in ["user", "assistant"]
        ]
        return "\n".join([
            f"{m['role'].title()}: {m['content'][:100]}..."
            for m in messages[-10:]  # Last 10 messages
        ])
```

## WebSocket Voice Agent Server

```python
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

@app.websocket("/voice")
async def voice_endpoint(websocket: WebSocket):
    """WebSocket endpoint for voice agent."""
    await websocket.accept()

    config = VoiceAgentConfig(
        system_prompt="You are a helpful voice assistant.",
        voice="nova"
    )
    agent = ProductionVoiceAgent(config)
    await agent.start_session()

    try:
        while True:
            # Receive audio data
            audio_data = await websocket.receive_bytes()

            # Process and get response
            response_audio = await agent.handle_audio(audio_data)

            if response_audio:
                await websocket.send_bytes(response_audio)

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        await agent.end_session()
        await websocket.close()
```

## Best Practices

1. **State Management**
   - Track agent state clearly
   - Prevent concurrent operations
   - Handle interruptions

2. **Audio Processing**
   - Use proper VAD for detection
   - Handle silence appropriately
   - Process in chunks

3. **Response Generation**
   - Keep responses concise
   - Use streaming where possible
   - Handle tool calls efficiently

4. **Error Recovery**
   - Graceful degradation
   - Retry on transient failures
   - Log all errors

5. **Performance**
   - Use async/await
   - Stream audio when possible
   - Cache common responses

## References

- [OpenAI Audio API](https://platform.openai.com/docs/guides/speech-to-text)
- [Real-time Voice Agents](https://cookbook.openai.com/examples/how_to_build_a_real_time_voice_agent)
