# Voice Agent Code Examples

Production code examples for major voice AI platforms.

## OpenAI Realtime API (WebSocket)

### Basic WebSocket Connection

```python
import asyncio
import websockets
import json
import base64

class OpenAIRealtimeClient:
    """OpenAI Realtime API WebSocket client."""

    def __init__(self, api_key: str, model: str = "gpt-4o-realtime-preview"):
        self.api_key = api_key
        self.model = model
        self.ws = None

    async def connect(self):
        """Establish WebSocket connection."""
        url = f"wss://api.openai.com/v1/realtime?model={self.model}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }
        self.ws = await websockets.connect(url, extra_headers=headers)

        # Configure session
        await self.ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": "You are a helpful voice assistant.",
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                }
            }
        }))

    async def send_audio(self, audio_chunk: bytes):
        """Send audio chunk to server."""
        await self.ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": base64.b64encode(audio_chunk).decode()
        }))

    async def receive_events(self):
        """Receive and handle events from server."""
        async for message in self.ws:
            event = json.loads(message)
            yield event

    async def close(self):
        """Close WebSocket connection."""
        if self.ws:
            await self.ws.close()


# Usage
async def main():
    client = OpenAIRealtimeClient(api_key="sk-...")
    await client.connect()

    # Send audio and handle responses
    async for event in client.receive_events():
        if event["type"] == "response.audio.delta":
            audio_data = base64.b64decode(event["delta"])
            # Play audio_data
        elif event["type"] == "response.text.delta":
            print(event["delta"], end="")
```

### With Function Calling

```python
async def configure_session_with_tools(ws):
    """Configure session with function calling."""
    await ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],
            "instructions": "You are a booking assistant. Use tools to check availability and book appointments.",
            "voice": "nova",
            "tools": [
                {
                    "type": "function",
                    "name": "check_availability",
                    "description": "Check available time slots for a service",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "service": {"type": "string", "description": "Service type"},
                            "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                        },
                        "required": ["service", "date"]
                    }
                },
                {
                    "type": "function",
                    "name": "book_appointment",
                    "description": "Book an appointment",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "service": {"type": "string"},
                            "date": {"type": "string"},
                            "time": {"type": "string"},
                            "customer_name": {"type": "string"}
                        },
                        "required": ["service", "date", "time", "customer_name"]
                    }
                }
            ]
        }
    }))


async def handle_function_call(ws, event):
    """Handle function call from the model."""
    call_id = event["call_id"]
    name = event["name"]
    args = json.loads(event["arguments"])

    # Execute function
    if name == "check_availability":
        result = {"slots": ["09:00", "10:00", "14:00", "15:00"]}
    elif name == "book_appointment":
        result = {"confirmed": True, "confirmation_number": "ABC123"}
    else:
        result = {"error": "Unknown function"}

    # Send result back
    await ws.send(json.dumps({
        "type": "conversation.item.create",
        "item": {
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps(result)
        }
    }))

    # Trigger response generation
    await ws.send(json.dumps({"type": "response.create"}))
```

## Retell AI

### Python SDK

```python
from retell import Retell
import asyncio

# Initialize client
client = Retell(api_key="your-retell-api-key")

# Create agent
agent = client.agent.create(
    voice_id="11labs-Adrian",
    llm_websocket_url="wss://your-llm-server.com/llm",
    agent_name="Support Agent",
    response_engine={
        "type": "retell_llm",
        "llm_model": "gpt-4o",
        "system_prompt": "You are a helpful customer support agent."
    },
    language="en-US",
    voice_speed=1.0,
    volume=1.0,
    ambient_sound="coffee-shop",
    enable_backchannel=True,
    backchannel_words=["mm-hmm", "right", "okay"],
    end_call_after_silence_ms=30000
)

print(f"Created agent: {agent.agent_id}")


# Create phone call
call = client.call.create_phone_call(
    from_number="+15551234567",
    to_number="+15559876543",
    agent_id=agent.agent_id,
    metadata={"customer_id": "12345"}
)

print(f"Call initiated: {call.call_id}")


# List calls with pagination
calls = client.call.list(limit=50)
for call in calls:
    print(f"{call.call_id}: {call.call_status}")
```

### Custom LLM WebSocket Server

```python
from fastapi import FastAPI, WebSocket
from dataclasses import dataclass
import json

app = FastAPI()

@dataclass
class RetellRequest:
    interaction_type: str  # "call_details", "update_only", "response_required"
    transcript: list
    response_id: int

@app.websocket("/llm")
async def llm_websocket(websocket: WebSocket):
    """Retell LLM WebSocket endpoint."""
    await websocket.accept()

    try:
        async for data in websocket.iter_text():
            request = json.loads(data)

            if request["interaction_type"] == "call_details":
                # Initial call setup
                config = {
                    "response_type": "config",
                    "config": {
                        "auto_reconnect": True,
                        "call_details": True
                    }
                }
                await websocket.send_json(config)

            elif request["interaction_type"] == "response_required":
                # Generate LLM response
                transcript = request.get("transcript", [])
                response_id = request["response_id"]

                # Your LLM logic here
                response_text = await generate_response(transcript)

                # Stream response word by word
                words = response_text.split()
                for i, word in enumerate(words):
                    await websocket.send_json({
                        "response_type": "response",
                        "response_id": response_id,
                        "content": word + " ",
                        "content_complete": i == len(words) - 1,
                        "end_call": False
                    })

    except Exception as e:
        print(f"WebSocket error: {e}")


async def generate_response(transcript: list) -> str:
    """Generate response using your LLM."""
    # Integrate with OpenAI, Claude, etc.
    messages = [{"role": t["role"], "content": t["content"]} for t in transcript]
    # ... call LLM API
    return "This is the response from the LLM."
```

## ElevenLabs Conversational AI

### WebSocket Client

```python
import websockets
import json
import asyncio

class ElevenLabsConversationalClient:
    """ElevenLabs Conversational AI WebSocket client."""

    def __init__(self, agent_id: str, api_key: str = None):
        self.agent_id = agent_id
        self.api_key = api_key
        self.ws = None

    async def connect(self):
        """Connect to ElevenLabs WebSocket."""
        url = f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id={self.agent_id}"
        headers = {}
        if self.api_key:
            headers["xi-api-key"] = self.api_key

        self.ws = await websockets.connect(url, extra_headers=headers)

        # Wait for conversation_initiation_metadata
        response = await self.ws.recv()
        metadata = json.loads(response)
        return metadata

    async def send_audio(self, audio_chunk: bytes):
        """Send audio chunk (base64 encoded)."""
        import base64
        await self.ws.send(json.dumps({
            "user_audio_chunk": base64.b64encode(audio_chunk).decode()
        }))

    async def receive_events(self):
        """Receive events from the agent."""
        async for message in self.ws:
            event = json.loads(message)
            event_type = event.get("type")

            if event_type == "audio":
                # Audio response from agent
                yield {
                    "type": "audio",
                    "data": event["audio_event"]["audio_base_64"]
                }
            elif event_type == "agent_response":
                # Text response
                yield {
                    "type": "text",
                    "data": event["agent_response_event"]["agent_response"]
                }
            elif event_type == "user_transcript":
                # User speech transcription
                yield {
                    "type": "transcript",
                    "data": event["user_transcription_event"]["user_transcript"]
                }

    async def interrupt(self):
        """Interrupt the agent (user barge-in)."""
        await self.ws.send(json.dumps({"type": "interrupt"}))


# Usage
async def run_conversation():
    client = ElevenLabsConversationalClient(
        agent_id="your-agent-id",
        api_key="your-api-key"  # Optional for public agents
    )

    metadata = await client.connect()
    print(f"Connected: {metadata}")

    # Handle events
    async for event in client.receive_events():
        if event["type"] == "audio":
            # Play audio
            pass
        elif event["type"] == "text":
            print(f"Agent: {event['data']}")
        elif event["type"] == "transcript":
            print(f"User: {event['data']}")
```

## LiveKit Agents

### Voice Agent with Telephony

```python
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.agents.llm import ChatContext, ChatMessage
from livekit.agents.voice import VoiceAgent
from livekit.plugins import openai, silero, deepgram, cartesia

async def entrypoint(ctx: JobContext):
    """Voice agent entrypoint."""

    # Initialize components
    vad = silero.VAD.load()
    stt = deepgram.STT()
    llm = openai.LLM(model="gpt-4o")
    tts = cartesia.TTS(voice="79a125e8-cd45-4c13-8a67-188112f4dd22")

    # Create chat context with system prompt
    chat_ctx = ChatContext()
    chat_ctx.append(
        role="system",
        text="""You are a helpful voice assistant for Acme Corp.

Your responsibilities:
- Answer questions about our products
- Help schedule appointments
- Provide order status updates

Keep responses concise (1-2 sentences) for natural conversation.
Be friendly but professional."""
    )

    # Create voice agent
    agent = VoiceAgent(
        vad=vad,
        stt=stt,
        llm=llm,
        tts=tts,
        chat_ctx=chat_ctx,
        allow_interruptions=True,
        interrupt_speech_duration=0.5,
        min_endpointing_delay=0.5,
    )

    # Connect to room
    await ctx.connect()

    # Start agent
    agent.start(ctx.room)

    # Wait for participant
    await agent.say("Hello! Welcome to Acme Corp. How can I help you today?")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )
```

### With Function Calling

```python
from livekit.agents.llm import FunctionContext, FunctionTool

# Define tools
async def check_order_status(order_id: str) -> str:
    """Check the status of an order."""
    # Your order lookup logic
    return f"Order {order_id} is currently being shipped and will arrive in 2-3 days."

async def schedule_callback(
    phone_number: str,
    preferred_time: str,
    reason: str
) -> str:
    """Schedule a callback from a human agent."""
    # Your scheduling logic
    return f"Callback scheduled for {preferred_time}. A representative will call you at {phone_number}."

# Create function context
fnc_ctx = FunctionContext()

fnc_ctx.add_function(
    FunctionTool(
        name="check_order_status",
        description="Check the status of a customer's order",
        parameters={
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to look up"
                }
            },
            "required": ["order_id"]
        },
        callable=check_order_status
    )
)

fnc_ctx.add_function(
    FunctionTool(
        name="schedule_callback",
        description="Schedule a callback from a human agent",
        parameters={
            "type": "object",
            "properties": {
                "phone_number": {"type": "string"},
                "preferred_time": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["phone_number", "preferred_time", "reason"]
        },
        callable=schedule_callback
    )
)

# Use in agent
llm = openai.LLM(model="gpt-4o", fnc_ctx=fnc_ctx)
```

## Vapi

### Create Assistant via API

```python
import requests

VAPI_API_KEY = "your-vapi-api-key"

def create_assistant():
    """Create a Vapi assistant."""
    response = requests.post(
        "https://api.vapi.ai/assistant",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "name": "Support Assistant",
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "en"
            },
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful customer support agent. Keep responses brief and helpful."
                    }
                ],
                "temperature": 0.7,
                "maxTokens": 150,
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": "transfer_to_human",
                            "description": "Transfer the call to a human agent",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "reason": {
                                        "type": "string",
                                        "description": "Reason for transfer"
                                    }
                                },
                                "required": ["reason"]
                            }
                        }
                    }
                ]
            },
            "voice": {
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM"
            },
            "firstMessage": "Hello! Thanks for calling support. How can I help you today?",
            "endCallMessage": "Thank you for calling. Have a great day!",
            "silenceTimeoutSeconds": 30,
            "maxDurationSeconds": 600,
            "backgroundSound": "office"
        }
    )
    return response.json()


def start_call(assistant_id: str, phone_number: str):
    """Start an outbound call."""
    response = requests.post(
        "https://api.vapi.ai/call",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "assistantId": assistant_id,
            "customer": {
                "number": phone_number
            },
            "phoneNumberId": "your-phone-number-id"
        }
    )
    return response.json()
```

### Webhook Handler

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

app = FastAPI()

class VapiMessage(BaseModel):
    type: str
    call: Optional[Dict[str, Any]] = None
    transcript: Optional[str] = None
    functionCall: Optional[Dict[str, Any]] = None

@app.post("/vapi/webhook")
async def vapi_webhook(request: Request):
    """Handle Vapi webhooks."""
    data = await request.json()
    message_type = data.get("message", {}).get("type")

    if message_type == "function-call":
        # Handle function call
        function_call = data["message"]["functionCall"]
        name = function_call["name"]
        parameters = function_call["parameters"]

        if name == "transfer_to_human":
            # Implement transfer logic
            return {
                "result": "Transfer initiated to human agent.",
                "forwardToPhoneNumber": "+15551234567"
            }
        elif name == "lookup_account":
            # Implement account lookup
            account_id = parameters.get("account_id")
            return {
                "result": f"Account {account_id} found. Balance: $150.00"
            }

    elif message_type == "end-of-call-report":
        # Call ended - save transcript, analytics, etc.
        call_id = data["message"]["call"]["id"]
        transcript = data["message"]["transcript"]
        duration = data["message"]["call"]["duration"]
        # Save to database...

    return {"status": "ok"}
```

## Twilio ConversationRelay

### FastAPI WebSocket Handler

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
import json
from openai import OpenAI

app = FastAPI()
openai_client = OpenAI()

@app.post("/voice/incoming")
async def incoming_call():
    """Handle incoming Twilio call with ConversationRelay."""
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Connect>
            <ConversationRelay
                url="wss://your-server.com/conversation"
                voice="Google.en-US-Neural2-F"
                language="en-US"
                transcriptionProvider="google"
                speechModel="phone_call"
                interruptible="true"
                welcomeGreeting="Hello! How can I help you today?"
            />
        </Connect>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")


@app.websocket("/conversation")
async def conversation_relay(websocket: WebSocket):
    """Handle ConversationRelay WebSocket."""
    await websocket.accept()

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep responses concise."}
    ]

    try:
        async for data in websocket.iter_text():
            event = json.loads(data)
            event_type = event.get("type")

            if event_type == "setup":
                # Connection established
                call_sid = event.get("callSid")
                print(f"Call connected: {call_sid}")

            elif event_type == "prompt":
                # User speech transcribed
                user_text = event.get("voicePrompt")
                print(f"User: {user_text}")

                messages.append({"role": "user", "content": user_text})

                # Generate response
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=150
                )

                assistant_text = response.choices[0].message.content
                messages.append({"role": "assistant", "content": assistant_text})

                print(f"Agent: {assistant_text}")

                # Send response back to Twilio
                await websocket.send_json({
                    "type": "text",
                    "token": assistant_text
                })

            elif event_type == "interrupt":
                # User interrupted
                print("User interrupted agent")

            elif event_type == "error":
                print(f"Error: {event.get('description')}")

    except Exception as e:
        print(f"WebSocket error: {e}")
```

## Real-time VAD Implementation

### Energy-based VAD

```python
import numpy as np
from dataclasses import dataclass
from typing import Optional, Callable
import asyncio

@dataclass
class VADConfig:
    threshold: float = 0.02
    min_speech_ms: int = 250
    silence_ms: int = 700
    sample_rate: int = 16000
    frame_ms: int = 30

class EnergyVAD:
    """Energy-based Voice Activity Detection."""

    def __init__(
        self,
        config: VADConfig = None,
        on_speech_start: Optional[Callable] = None,
        on_speech_end: Optional[Callable] = None
    ):
        self.config = config or VADConfig()
        self.on_speech_start = on_speech_start
        self.on_speech_end = on_speech_end

        self.is_speaking = False
        self.speech_frames = 0
        self.silence_frames = 0
        self.audio_buffer = []

        self.frame_samples = int(self.config.sample_rate * self.config.frame_ms / 1000)
        self.min_speech_frames = int(self.config.min_speech_ms / self.config.frame_ms)
        self.silence_frames_threshold = int(self.config.silence_ms / self.config.frame_ms)

    def process_frame(self, audio_frame: np.ndarray) -> Optional[np.ndarray]:
        """Process audio frame and detect speech boundaries."""
        # Calculate RMS energy
        energy = np.sqrt(np.mean(audio_frame ** 2))
        is_speech = energy > self.config.threshold

        if is_speech:
            self.speech_frames += 1
            self.silence_frames = 0
            self.audio_buffer.append(audio_frame)

            if not self.is_speaking and self.speech_frames >= self.min_speech_frames:
                self.is_speaking = True
                if self.on_speech_start:
                    self.on_speech_start()

        else:
            if self.is_speaking:
                self.silence_frames += 1
                self.audio_buffer.append(audio_frame)

                if self.silence_frames >= self.silence_frames_threshold:
                    # Speech ended
                    self.is_speaking = False
                    result = np.concatenate(self.audio_buffer)
                    self.audio_buffer = []
                    self.speech_frames = 0
                    self.silence_frames = 0

                    if self.on_speech_end:
                        self.on_speech_end()

                    return result
            else:
                self.speech_frames = 0

        return None

    def reset(self):
        """Reset VAD state."""
        self.is_speaking = False
        self.speech_frames = 0
        self.silence_frames = 0
        self.audio_buffer = []
```

## Audio Streaming Utilities

### WebSocket Audio Streamer

```python
import asyncio
import sounddevice as sd
import numpy as np
from typing import AsyncGenerator

class AudioStreamer:
    """Real-time audio capture and streaming."""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_ms: int = 100
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = int(sample_rate * chunk_ms / 1000)
        self.queue = asyncio.Queue()
        self.is_running = False

    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio capture."""
        if self.is_running:
            # Convert to int16 for transmission
            audio_int16 = (indata * 32767).astype(np.int16)
            asyncio.run_coroutine_threadsafe(
                self.queue.put(audio_int16.tobytes()),
                self.loop
            )

    async def start(self) -> AsyncGenerator[bytes, None]:
        """Start streaming audio chunks."""
        self.is_running = True
        self.loop = asyncio.get_event_loop()

        stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32',
            blocksize=self.chunk_size,
            callback=self._audio_callback
        )

        with stream:
            while self.is_running:
                try:
                    chunk = await asyncio.wait_for(self.queue.get(), timeout=0.2)
                    yield chunk
                except asyncio.TimeoutError:
                    continue

    def stop(self):
        """Stop streaming."""
        self.is_running = False


class AudioPlayer:
    """Real-time audio playback."""

    def __init__(self, sample_rate: int = 24000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.queue = asyncio.Queue()
        self.is_running = False

    async def play(self, audio_data: bytes):
        """Queue audio for playback."""
        await self.queue.put(audio_data)

    async def start(self):
        """Start playback loop."""
        import pyaudio

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )

        self.is_running = True

        try:
            while self.is_running:
                try:
                    chunk = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    stream.write(chunk)
                except asyncio.TimeoutError:
                    continue
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def stop(self):
        """Stop playback."""
        self.is_running = False
```
