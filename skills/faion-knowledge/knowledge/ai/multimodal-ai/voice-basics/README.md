---
id: voice-basics
name: "Voice Agents - Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Voice Agents - Basics

## Overview

Voice agents combine Speech-to-Text, LLM reasoning, and Text-to-Speech to create conversational AI systems that can interact through voice. They power virtual assistants, customer service bots, and interactive voice response systems.

## When to Use

- Customer service automation
- Virtual assistants
- Voice-controlled applications
- Interactive voice response (IVR)
- Accessibility tools
- Real-time translation
- Voice-enabled chatbots

## Key Concepts

### Voice Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VOICE AGENT                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    STT      │  │    LLM      │  │    TTS      │         │
│  │  (Whisper)  │──▶│  (GPT-4o)  │──▶│  (OpenAI)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│        ▲                                    │               │
│        │                                    ▼               │
│  ┌─────────────┐                    ┌─────────────┐         │
│  │ Microphone  │                    │  Speaker    │         │
│  └─────────────┘                    └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Latency Components

| Component | Typical Latency | Target |
|-----------|-----------------|--------|
| VAD | 50-100ms | <100ms |
| STT | 200-500ms | <300ms |
| LLM | 300-1000ms | <500ms |
| TTS | 100-300ms | <200ms |
| **Total** | 650-1900ms | <1000ms |

## Basic Voice Agent

```python
from openai import OpenAI
import sounddevice as sd
import numpy as np
import tempfile
import wave
from pathlib import Path

client = OpenAI()

class BasicVoiceAgent:
    """Simple voice agent with STT + LLM + TTS."""

    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant.",
        voice: str = "nova",
        sample_rate: int = 16000
    ):
        self.system_prompt = system_prompt
        self.voice = voice
        self.sample_rate = sample_rate
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

    def listen(self, duration: float = 5.0) -> str:
        """Record audio from microphone and transcribe."""
        print("Listening...")

        # Record audio
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio.tobytes())

            # Transcribe
            with open(f.name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            Path(f.name).unlink()

        return transcript.text

    def think(self, user_input: str) -> str:
        """Process input and generate response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def speak(self, text: str):
        """Convert text to speech and play."""
        import pygame

        response = client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text
        )

        # Save and play
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            response.stream_to_file(f.name)

            pygame.mixer.init()
            pygame.mixer.music.load(f.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            Path(f.name).unlink()

    def chat(self, duration: float = 5.0):
        """Full conversation turn."""
        # Listen
        user_input = self.listen(duration)
        print(f"You: {user_input}")

        # Think
        response = self.think(user_input)
        print(f"Agent: {response}")

        # Speak
        self.speak(response)

        return response

    def run(self, turns: int = 5):
        """Run interactive conversation."""
        print("Voice Agent started. Speak after the prompt.")

        for _ in range(turns):
            input("Press Enter to speak...")
            self.chat()

        print("Conversation ended.")
```

## Voice Agent with Tools

```python
from typing import List, Dict, Callable
import json

class ToolEnabledVoiceAgent:
    """Voice agent with tool/function calling capabilities."""

    def __init__(
        self,
        system_prompt: str,
        tools: List[Dict],
        tool_functions: Dict[str, Callable],
        voice: str = "nova"
    ):
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_functions = tool_functions
        self.voice = voice
        self.client = OpenAI()
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

    async def process(self, user_input: str) -> str:
        """Process user input with potential tool calls."""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Initial LLM call
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            self.conversation_history.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Execute tool
                if function_name in self.tool_functions:
                    result = self.tool_functions[function_name](**arguments)
                else:
                    result = {"error": f"Unknown function: {function_name}"}

                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Get final response
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.conversation_history,
                tools=self.tools
            )
            message = response.choices[0].message

        assistant_message = message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

# Example tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Set a reminder",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "time": {"type": "string", "description": "Time in natural language"}
                },
                "required": ["message", "time"]
            }
        }
    }
]

def get_weather(location: str) -> dict:
    return {"location": location, "temperature": 72, "condition": "sunny"}

def set_reminder(message: str, time: str) -> dict:
    return {"status": "set", "message": message, "time": time}

tool_functions = {
    "get_weather": get_weather,
    "set_reminder": set_reminder
}
```

## Best Practices

1. **Latency Optimization**
   - Use streaming for STT and TTS
   - Keep responses concise
   - Consider response caching

2. **Conversation Design**
   - Use clear, natural language
   - Handle interruptions gracefully
   - Provide feedback during processing

3. **Error Handling**
   - Graceful degradation
   - Retry on transient failures
   - Clear error messages

4. **Voice Selection**
   - Match voice to use case
   - Consider user preferences
   - Test with real users

5. **Turn Management**
   - Detect conversation end
   - Handle silence appropriately
   - Limit conversation length

## Common Pitfalls

1. **High Latency** - Not streaming components
2. **Echo** - Not handling speaker output
3. **Interruption Handling** - Not stopping playback
4. **Long Responses** - TTS takes too long
5. **No Context Limits** - Token overflow
6. **Poor VAD** - Missing or false triggers

## References

- [OpenAI Audio API](https://platform.openai.com/docs/guides/speech-to-text)
- [Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Real-time Voice Agents](https://cookbook.openai.com/examples/how_to_build_a_real_time_voice_agent)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Process voice input | haiku | File handling and format conversion |
| Implement voice synthesis | sonnet | Integration and quality control |

