# Agent Integration — Voice Agents (Basics)

## When to use
- Customer service automation requiring natural voice interaction (IVR replacement)
- Accessibility tools where text input is not viable (mobility impairment, eyes-free situations)
- Voice-controlled CLI wrappers for internal tools
- Real-time voice assistants embedded in hardware (kiosks, IoT devices)
- Voice-enabled chatbots where adding speech I/O to an existing text agent is the goal

## When NOT to use
- Low-latency requirements below 800ms end-to-end — the STT → LLM → TTS pipeline has ~650-1900ms minimum with current APIs
- High-security contexts where audio recording raises GDPR/compliance concerns
- Noisy environments without pre-processing (factory floor, open office) — Whisper accuracy degrades significantly below SNR 10dB
- Tasks where text output is superior (structured data, code, tables) — voice cannot render formatting

## Where it fails / limitations
- Echo cancellation is not handled by the code in README — speaker output captured by microphone creates a feedback loop; requires OS-level echo cancellation or hardware solution
- `pygame.mixer` for TTS playback is not interrupt-safe — if the agent speaks a long response, the user cannot interrupt mid-sentence
- VAD (voice activity detection) is absent in the basic example — agent records for a fixed duration, missing variable-length speech
- Conversation history grows unboundedly across turns — will hit context limits after 20-50 turns on GPT-4o
- Tool calls in `ToolEnabledVoiceAgent.process()` are awaited synchronously — long-running tool calls stall the voice response
- `sounddevice` requires system audio permissions and PortAudio — not available in headless server environments

## Agentic workflow
Voice agents require a persistent event loop, not a request/response agent pattern. For agent integration, treat voice as an I/O transport layer: the STT output becomes a text message sent to a Claude subagent, and the subagent's text response is passed to TTS. This decouples the reasoning logic from the audio stack. Claude subagents work well for designing the conversation flow, scripting system prompts, and building tool definitions — but the audio loop itself must run in a persistent Python process.

### Recommended subagents
- Custom conversation-design agent — given a use case description, produce the system prompt, tool definitions, and response length guidelines for a voice agent
- `faion-sdd-execution` — scaffold the voice agent class with proper VAD, interrupt handling, and context window management

### Prompt pattern
```
Design a voice agent for the following use case: {use_case}.
Produce:
1. System prompt (max 200 words, natural spoken language, no markdown)
2. List of tool definitions (JSON schema) the agent needs
3. Response length guideline (target word count per turn)
4. Conversation termination triggers (phrases that end the session)
```

```
The user said (via STT): "{transcribed_text}"
Conversation context: {last_3_turns}
Respond in 1-3 short sentences suitable for TTS. Avoid lists, markdown, or code.
If you need to call a tool, do so silently and respond with the result.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | Whisper STT + OpenAI TTS; GPT-4o reasoning | `pip install openai` · platform.openai.com/docs/guides/speech-to-text |
| `sounddevice` | Cross-platform audio recording/playback | `pip install sounddevice` · python-sounddevice.readthedocs.io |
| `pyaudio` | Alternative audio I/O; better VAD integration | `pip install pyaudio` · people.csail.mit.edu/hubert/pyaudio |
| `webrtcvad` | WebRTC-based VAD for detecting speech vs. silence | `pip install webrtcvad` · github.com/wiseman/py-webrtcvad |
| `pydub` | Audio format conversion, trimming, normalization | `pip install pydub` · github.com/jiaaro/pydub |
| `elevenlabs` | High-quality TTS with voice cloning | `pip install elevenlabs` · elevenlabs.io/docs |
| `deepgram` | Real-time streaming STT (lower latency than Whisper API) | `pip install deepgram-sdk` · developers.deepgram.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Whisper API | SaaS | Yes — SDK | Best general STT; $0.006/min; 25MB file limit |
| OpenAI TTS | SaaS | Yes — SDK | 6 voices; tts-1 (fast) and tts-1-hd (quality) |
| ElevenLabs | SaaS | Yes — REST/SDK | Best voice quality; voice cloning; multilingual |
| Deepgram | SaaS | Yes — WebSocket | Real-time streaming STT; <300ms latency; speaker diarization |
| AssemblyAI | SaaS | Yes — SDK | STT + LeMUR (LLM on transcripts); async processing |
| OpenAI Realtime API | SaaS | Yes — WebSocket | Native STT+LLM+TTS in one connection; lowest latency option |
| Twilio | SaaS | Yes — REST | Telephony integration; converts phone calls to audio streams |

## Templates & scripts
See `templates.md` for `BasicVoiceAgent` and `ToolEnabledVoiceAgent` classes.

Inline: simple VAD-based recording (stop when silence detected):
```python
import webrtcvad, sounddevice as sd, collections, numpy as np

def record_until_silence(sample_rate: int = 16000, silence_ms: int = 1000) -> bytes:
    vad = webrtcvad.Vad(2)  # aggressiveness 0-3
    frame_ms, frame_bytes = 30, sample_rate * 30 // 1000 * 2
    silence_frames = silence_ms // 30
    ring = collections.deque(maxlen=silence_frames)
    frames = []
    with sd.RawInputStream(samplerate=sample_rate, channels=1, dtype='int16') as s:
        while True:
            data, _ = s.read(frame_bytes // 2)
            frame = bytes(data)
            is_speech = vad.is_speech(frame, sample_rate)
            ring.append(is_speech)
            frames.append(frame)
            if len(frames) > silence_frames and not any(ring):
                break
    return b"".join(frames)
```

## Best practices
- Use OpenAI Realtime API (WebSocket) for lowest end-to-end latency — it bypasses the STT → LLM → TTS round-trip
- Keep TTS responses under 50 words per turn — longer responses feel unnatural and cannot be interrupted
- Implement interrupt detection: if new audio is detected during TTS playback, stop playback and process the interrupt
- Use `tts-1` (not `tts-1-hd`) for real-time conversation; `tts-1-hd` for pre-generated audio where latency is not critical
- Truncate conversation history to last 10 turns to prevent context overflow; summarize older context into system prompt
- Specify language explicitly in Whisper calls (`language="uk"`, `language="en"`) to avoid language detection latency and errors
- For telephony (Twilio): encode audio as mulaw 8kHz, not PCM 16kHz — Twilio's native format

## AI-agent gotchas
- The STT → LLM → TTS pipeline is sequential; parallelizing STT and LLM is not possible — minimize per-step latency instead
- `client.audio.speech.create()` returns a streaming response; always use `stream_to_file()` or stream directly to avoid buffering the full audio in memory
- Tool calls inside a voice turn must complete before TTS can begin — long-running tools (web search, DB queries) should return a "thinking" audio response first
- Whisper occasionally mis-transcribes proper nouns and domain terms — use the `prompt` parameter to hint at expected vocabulary
- Fixed-duration recording (`sd.rec(duration * sr)`) truncates long responses and records silence for short ones — always use VAD-based recording in production

## References
- https://platform.openai.com/docs/guides/speech-to-text
- https://platform.openai.com/docs/guides/text-to-speech
- https://platform.openai.com/docs/guides/realtime
- https://elevenlabs.io/docs/api-reference/text-to-speech
- https://developers.deepgram.com/docs/getting-started
- https://cookbook.openai.com/examples/how_to_build_a_real_time_voice_agent
