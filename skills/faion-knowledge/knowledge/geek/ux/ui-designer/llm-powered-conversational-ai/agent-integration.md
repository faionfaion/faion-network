# Agent Integration — LLM-Powered Conversational AI

## When to use
- Replacing or augmenting a rule-based chatbot or voice assistant that fails on complex, multi-part queries
- Building a product assistant that must handle natural conversation history (not just single-turn Q&A)
- Implementing voice agents where users phrase the same intent in many different ways
- Adding clarification and ambiguity resolution to a conversational flow (LLMs interpret where rule-based systems fail)
- Prototyping an LLM-based VUI pipeline: ASR → LLM → TTS stack for a product feature

## When NOT to use
- The interaction is a narrow, well-defined command set (3–10 intents) — rule-based NLU is simpler, faster, cheaper, and more reliable
- The response must be deterministic and auditable (medical dosage, legal status) — LLM variability is a liability
- The voice channel has high background noise or non-standard accents at scale — ASR accuracy is the bottleneck, not LLM quality
- Latency budget is <300ms end-to-end — streaming helps but the ASR→LLM→TTS stack has irreducible latency
- The product needs to execute actions autonomously without human confirmation — LLM action calls require guardrail architecture first

## Where it fails / limitations
- LLM hallucination in conversational context produces confident wrong answers — without retrieval grounding, factual reliability is low
- Conversation history grows with each turn; at ~10–15 turns the context window cost and latency increase significantly
- Persona consistency degrades over long conversations without explicit persona reinforcement in the system prompt
- Off-topic escalation is an unsolved problem — LLMs engage with out-of-scope queries when they should decline
- TTS introduces latency; streaming TTS (chunk-by-chunk) required for perceived responsiveness
- Emotion/tone detection is imprecise — aggressive frustration and mild impatience produce different user needs but similar ASR output
- Function/tool calling in voice context requires explicit validation before execution — LLM may call wrong function from ambiguous audio

## Agentic workflow
A Claude subagent (Sonnet) acts as the conversational LLM core: it receives the ASR transcript, conversation history, and system persona prompt, generates a response, and outputs both a spoken text and an optional structured action (tool call). A Haiku subagent handles TTS integration (submitting the response to Amazon Polly or Google TTS), format conversion, and logging. A guardrail agent (Haiku) validates tool calls against an allowlist before execution. Human review of conversation logs is required periodically to detect persona drift and off-topic escalation patterns.

### Recommended subagents
- General Claude subagent (Sonnet) — conversation turn generation, intent understanding, ambiguity clarification
- General Claude subagent (Haiku) — TTS submission, log formatting, guardrail validation, off-topic detection

### Prompt pattern
```
System: You are [persona name], a [role] for [product]. You help users [core use cases].
You must:
- Never claim capabilities outside [allowed domain list]
- Ask one clarifying question at a time when the request is ambiguous
- Escalate to human support when the user is frustrated or the query is outside your scope
- Keep responses under 2 sentences for voice delivery
- Always confirm before executing actions (booking, purchasing, deleting)

Conversation history:
[last 5 turns as role/content pairs]

Current user input: [ASR transcript]
```

```
You are a guardrail validator for a voice agent.
The LLM has proposed this tool call: [tool_name, parameters]
Allowed tools: [allowlist]
Allowed parameter ranges: [constraints]
Check:
1. Is the tool in the allowlist?
2. Are all parameters within allowed ranges?
3. Does the action match what the user asked for in the transcript?
Output: { approved: true/false, reason: "...", safe_to_execute: true/false }
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai-whisper` | Local ASR (speech-to-text) | `pip install openai-whisper` / github.com/openai/whisper |
| `whisper.cpp` | C++ port of Whisper — lower latency, on-device | github.com/ggerganov/whisper.cpp |
| `pyttsx3` | Local TTS for development/testing | `pip install pyttsx3` |
| `pyaudio` | Microphone capture for real-time ASR | `pip install pyaudio` |
| Pipecat | OSS voice agent framework (ASR→LLM→TTS pipeline) | `pip install pipecat-ai` / pipecat.ai |
| LiveKit Agents | Real-time voice agent SDK | `pip install livekit-agents` / livekit.io/agents |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Whisper (cloud) | SaaS | Yes — REST API | High-accuracy ASR; 90%+ on standard accents |
| AssemblyAI | SaaS | Yes — REST API | Real-time streaming ASR; speaker diarization |
| Deepgram | SaaS | Yes — REST API | Low-latency streaming ASR; best for real-time voice |
| Amazon Polly | SaaS | Yes — REST API | Neural TTS; SSML support; voice persona selection |
| Google Text-to-Speech | SaaS | Yes — REST API | WaveNet/Neural2 voices; streaming output |
| ElevenLabs | SaaS | Yes — REST API | Ultra-realistic TTS; voice cloning; streaming |
| Anthropic Claude API | SaaS | Yes — REST API | Conversational LLM core; streaming messages API |
| OpenAI Realtime API | SaaS | Yes — WebSocket | End-to-end voice: ASR+LLM+TTS in one WebSocket |
| Vapi | SaaS | Yes — REST API | Managed voice agent infrastructure; phone call support |

## Templates & scripts
See `templates.md` for the conversation flow specification template and system persona prompt template.

Minimal ASR→LLM→TTS pipeline (Python):
```python
import anthropic, boto3, io, sys
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

PERSONA = (
    "You are a helpful assistant. Keep responses under 2 sentences. "
    "Ask one clarifying question when the request is ambiguous."
)

def transcribe(audio_data: bytes) -> str:
    """Transcribe audio via Whisper (or swap for Deepgram/AssemblyAI)."""
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(io.BytesIO(audio_data))
    return result["text"]

def generate_response(history: list[dict], user_text: str) -> str:
    client = anthropic.Anthropic()
    history.append({"role": "user", "content": user_text})
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system=PERSONA,
        messages=history,
    )
    reply = msg.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply

def speak(text: str) -> None:
    polly = boto3.client("polly", region_name="us-east-1")
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    audio = AudioSegment.from_mp3(io.BytesIO(response["AudioStream"].read()))
    play(audio)
```

## Best practices
- Define the persona's scope boundary explicitly in the system prompt — "I can only help with [X], [Y], [Z]" prevents topic drift
- Always confirm before executing real-world actions (booking, deleting, purchasing) — one LLM turn of confirmation is cheap; bad action execution is not
- Use streaming TTS output (chunk text as it generates) to keep perceived latency under 1 second
- Log every conversation turn with the ASR confidence score — low-confidence transcripts explain the most common LLM errors
- Set a conversation history window (5–10 turns) and summarize older context — unbounded history increases cost and latency without proportional benefit
- Validate function call parameters against schema before execution, every time — never trust LLM-generated parameter values directly
- Monitor escalation rate weekly — if >10% of conversations escalate to human, the persona boundary or the LLM's capability is mismatched to user expectations

## AI-agent gotchas
- ASR introduces noise that degrades LLM intent recognition — "book a flight" may transcribe as "buck a flight"; require the LLM to confirm ambiguous transcripts before acting
- Streaming responses must be buffered to sentence boundaries before TTS submission — partial sentence TTS sounds unnatural and breaks understanding
- Tool call guardrail agent must see the original user transcript, not just the LLM-generated tool call — the LLM may hallucinate parameters not mentioned by the user
- Long system prompts increase latency and cost; keep persona prompt under 200 tokens, use retrieval for knowledge
- Human-in-loop checkpoint: review conversation logs weekly for hallucinated facts, persona drift, and off-topic escalation patterns — do not rely on automated metrics alone
- Emotional tone detection is unreliable; use explicit escalation triggers (user says "agent", "human", "frustrated") rather than sentiment scoring

## References
- OpenAI Whisper: https://github.com/openai/whisper
- Anthropic streaming messages: https://docs.anthropic.com/en/api/messages-streaming
- Pipecat voice AI framework: https://pipecat.ai
- LiveKit Agents: https://livekit.io/agents
- NNGroup conversational AI: https://www.nngroup.com/articles/llm-conversation-design/
- OpenAI Realtime API: https://platform.openai.com/docs/guides/realtime
