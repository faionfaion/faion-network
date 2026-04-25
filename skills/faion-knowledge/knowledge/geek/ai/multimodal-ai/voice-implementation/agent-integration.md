# Agent Integration — Voice Agents (Implementation)

## When to use
- Building a conversational voice agent with full STT → LLM → TTS loop
- Exposing a voice agent over WebSocket (browser, mobile app, embedded)
- Implementing multi-turn voice conversation with tool use (function calling)
- Adding voice I/O to an existing text-based agent pipeline
- Real-time voice interaction where response latency must be < 3 seconds

## When NOT to use
- Batch audio processing — use `speech-to-text-advanced` + `tts-implementation`; the real-time VAD loop is unnecessary overhead
- Single-turn transcription without conversation context — direct Whisper call is simpler
- Phone/PSTN integration — WebSocket pattern works but requires a SIP/RTP bridge (Twilio, Vonage) not covered here
- Environments without microphone access (CI, headless servers) — `RealtimeVoiceAgent` requires `sounddevice` with audio hardware

## Where it fails / limitations
- `RealtimeVoiceAgent._capture_audio` uses a synchronous `sounddevice` stream inside a thread — audio capture and processing on the same machine creates latency variance; in production, separate capture and processing to different processes
- Energy-based VAD (`np.sqrt(np.mean(chunk**2)) > threshold`) is a naive approximation — fails in noisy environments, background music, or HVAC noise; use Silero VAD or WebRTC VAD for production
- `_transcribe` saves audio to a temp file then transcribes — this adds 100–300ms latency; use Whisper streaming or Groq for lower latency
- `ProductionVoiceAgent._generate_response` with tool calls makes a second LLM call unconditionally — if the first response had no tool calls, the second call still runs (bug: `**kwargs` still has `tool_choice="auto"`)
- `max_response_tokens: int = 200` is too low for complex tool responses — agents frequently truncate mid-sentence
- WebSocket endpoint catches `Exception` broadly and silently closes — client receives no error explanation
- Conversation history grows unbounded — at 50 turns, the context window fills; implement sliding window or summarization

## Agentic workflow
An orchestrator sets up `ProductionVoiceAgent` with a system prompt and tool definitions. Incoming audio (bytes) arrives via WebSocket, is passed to `agent.handle_audio()`, which returns response audio bytes. The agent manages state (IDLE/LISTENING/PROCESSING/SPEAKING) to prevent concurrent turn processing. Tool functions are registered as a dict of callables — agents can call external APIs, look up data, or trigger actions during the voice turn. Session ends when max_turns is reached or client disconnects.

### Recommended subagents
- `haiku` — Audio bytes routing: receive WebSocket bytes, pass to agent, return response audio bytes
- `sonnet` — Tool function implementation: write the tool callables registered in `tool_functions` dict
- `sonnet` — System prompt design: craft the voice agent persona, response style constraints (short sentences, no markdown), tool descriptions
- `opus` — Conversation quality review: analyze conversation logs for truncation, tool-call failures, state machine errors

### Prompt pattern
```xml
<system>
You are a voice assistant. Rules:
- Keep responses under 2 sentences
- Never use markdown, bullet points, or code blocks
- Speak naturally as if talking, not writing
- If using a tool, explain what you're doing briefly before
- If uncertain, ask one clarifying question only
</system>
```

```python
# Tool registration pattern for voice agents
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    }
]
tool_functions = {"get_weather": lambda city: fetch_weather(city)}
agent = ProductionVoiceAgent(config, tools=tools, tool_functions=tool_functions)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| sounddevice | Microphone/speaker I/O via PortAudio | `pip install sounddevice` (requires `apt install portaudio19-dev`) |
| pyaudio | Alternative audio I/O | `pip install pyaudio` |
| numpy | Audio signal processing, VAD energy calc | `pip install numpy` |
| openai (Python SDK) | Whisper STT + GPT-4o LLM + TTS | `pip install openai` |
| fastapi + websockets | WebSocket server for browser/mobile clients | `pip install fastapi websockets uvicorn` |
| silero-vad | Production-quality VAD (replaces energy-based) | `pip install silero-vad` |
| webrtcvad | Google WebRTC VAD (fast, lightweight) | `pip install webrtcvad` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Realtime API | SaaS | Yes — WebSocket API | Native real-time voice; sub-300ms latency; replaces STT+LLM+TTS chain |
| Groq Whisper | SaaS | Yes — OpenAI-compatible | 10× faster STT than OpenAI; reduces STT latency from 800ms to ~80ms |
| Deepgram | SaaS | Yes — WebSocket streaming | Real-time STT; best for live microphone input |
| ElevenLabs | SaaS | Yes — Python SDK | Best TTS quality; use for final-quality voice, not real-time prototype |
| Twilio Voice | SaaS | Yes — REST + WebSocket | Phone call integration; SIP bridge for PSTN calls |
| Daily.co | SaaS | Yes — Python SDK | WebRTC media transport; better than raw WebSocket for audio |
| LiveKit | OSS/SaaS | Yes — Python SDK | WebRTC server; supports voice agent integration; self-hostable |

## Templates & scripts
See `templates.md` for `RealtimeVoiceAgent`, `ProductionVoiceAgent`, `VoiceAgentConfig`, WebSocket server.

Fix for double LLM call bug in `_generate_response`:
```python
# Only call LLM a second time if there were tool calls
if message.tool_calls:
    self.conversation_history.append(message)
    # ... execute tool calls ...
    # Get final response ONLY after tool execution
    final_response = self.client.chat.completions.create(
        model=self.config.llm_model,
        messages=self.conversation_history,
        max_tokens=self.config.max_response_tokens
    )
    message = final_response.choices[0].message
```

## Best practices
- Replace energy-based VAD with Silero VAD or WebRTC VAD for any production deployment in non-silent environments
- Use OpenAI Realtime API for lowest-latency deployments — it eliminates the STT + LLM + TTS chain and delivers ~200ms end-to-end
- Implement context window management: summarize or truncate conversation_history when it exceeds 80% of model's context limit
- Cap `max_response_tokens` at 150–200 for voice output — longer responses lose listener attention and sound robotic
- Strip markdown from LLM responses before TTS: `re.sub(r'[*_`#>]', '', text)` — asterisks and hashes are read literally
- Use sliding window on `conversation_history`: keep system prompt + last N turns + tool results; do not accumulate entire session
- Run tool functions in an executor to avoid blocking the async event loop
- Log each turn with: input_transcript, llm_response, tool_calls, audio_duration, turn_latency for quality monitoring

## AI-agent gotchas
- `AgentState` mutex is not enforced with a lock — in a multi-threaded context, state can race between LISTENING and PROCESSING; use `threading.Lock` or `asyncio.Lock`
- `ProductionVoiceAgent.handle_audio` ignores audio if `state == SPEAKING` — this is correct barge-in prevention, but the client receives no feedback; implement a visual/UI indicator
- `_speak` helper and `_synthesize` both exist and do the same thing — confusing API; agents should only call `_synthesize`
- WebSocket endpoint uses bare `except Exception` — differentiate `WebSocketDisconnect` from actual errors; log differently
- `max_turns` hard cutoff at 50 is not surfaced to the client gracefully — agent says "I need to end our conversation" which sounds jarring; implement graceful session handoff or restart
- Tool functions registered in `tool_functions` dict must be synchronous — `async def` tool functions will not be awaited and return coroutine objects; wrap with `asyncio.run()` or use sync implementations
- VAD silence timeout of 0.8s is aggressive — users with speech patterns that include longer pauses (non-native speakers, thinking pauses) will be cut off mid-thought

## References
- https://platform.openai.com/docs/guides/realtime
- https://platform.openai.com/docs/api-reference/audio
- https://platform.openai.com/docs/guides/speech-to-text
- https://cookbook.openai.com/examples/how_to_build_a_real_time_voice_agent
- https://github.com/snakers4/silero-vad
- https://livekit.io/blog/voice-ai-agents
- https://daily.co/docs
