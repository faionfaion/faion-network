# Agent Integration — Voice Agents

## When to use
- Building phone-based AI agents: inbound/outbound call center, appointment scheduling, support
- Web or mobile app requires real-time voice conversation (browser WebRTC)
- Replacing IVR (Interactive Voice Response) menus with natural conversational AI
- Voice accessibility feature: hands-free interface for existing agent workflows
- Live translation agent: real-time speech-to-speech across 100+ languages

## When NOT to use
- Text chat is sufficient — voice adds latency, cost, and infrastructure complexity for no UX gain
- Latency budget is below 300ms end-to-end — no current production stack achieves this reliably
- Audio quality is unpredictable (noisy environment, poor microphone) — accuracy degrades significantly
- Use case requires precise multi-step confirmation (legal, medical consent) — voice ambiguity introduces risk; use structured text forms instead
- Self-hosted required with <$500/month infra budget — LiveKit self-hosting requires real-time media server expertise

## Where it fails / limitations
- Total pipeline latency (STT + LLM + TTS) = 600-1500ms; users perceive this as sluggish vs text chat
- Barge-in handling (user interrupts agent mid-speech) requires VAD tuning — poorly tuned VAD causes the agent to either not listen or cut itself off constantly
- Phone PSTN integration via Twilio/Retell adds 100-200ms of additional latency vs WebRTC
- Speech-to-speech models (GPT-4o Realtime) bypass STT/TTS but have no tool-call support during streaming — forced to wait for model to finish before executing tools
- Emotional detection accuracy is 60-70% in noisy conditions — don't act on low-confidence signals
- Concurrent session scaling requires careful infra: 100 simultaneous WebRTC sessions needs dedicated media server capacity
- Transcript accuracy degrades for non-native speakers, accents, or mixed-language speech; no current API handles code-switching reliably

## Agentic workflow
Voice agents are real-time event-driven pipelines, not request-response agents. Audio arrives in 100-200ms chunks from WebRTC/WebSocket; each chunk flows through VAD → STT → LLM → TTS and back as audio. An orchestrator subagent maintains conversation state (history, context, tool results) and is invoked on each user turn completion (detected by VAD/turn detection). Tool calls happen between turns: the agent pauses TTS synthesis, executes the tool (CRM lookup, calendar booking), then resumes. Use managed platforms (Retell, Vapi) to avoid building the media layer; build custom only for LiveKit self-hosted deployments.

### Recommended subagents
- `faion-sdd-executor-agent` — can design the conversation flow and tool integration for a voice agent pipeline

### Prompt pattern
```python
# Voice agent system prompt pattern
SYSTEM_PROMPT = """You are a friendly customer support agent for Acme Corp.
Keep responses under 2 sentences — long responses feel unnatural over voice.
Do not use lists, markdown, or special characters — they don't render in speech.
When you need information, call the appropriate tool before responding.
If unsure, say "Let me check that for you" to acknowledge while you look it up.
"""

# Tool call during conversation (Retell example)
tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Lookup order status by order ID.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"]
            }
        }
    }
]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `livekit-agents` | Self-hosted voice agent framework (Python) | `pip install livekit-agents` / [docs](https://docs.livekit.io/agents/) |
| `retell-sdk` | Retell AI Python/JS SDK | `pip install retell-sdk` / [docs](https://docs.retellai.com/) |
| `vapi-python` | Vapi Python SDK | `pip install vapi-python` / [docs](https://docs.vapi.ai/) |
| `twilio` | PSTN/SIP telephony integration | `pip install twilio` / [docs](https://www.twilio.com/docs) |
| `openai` | GPT-4o Realtime API (WebRTC/WebSocket) | `pip install openai` / [realtime docs](https://platform.openai.com/docs/guides/realtime) |
| `elevenlabs` | ElevenLabs TTS + Conversational AI SDK | `pip install elevenlabs` / [docs](https://elevenlabs.io/docs) |
| `ffmpeg` | Audio format conversion for telephony | system package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Retell AI | SaaS | Yes | Best for phone agents; $0.07-0.12/min; handles full pipeline |
| Vapi | SaaS | Yes | Rapid prototyping; $0.05-0.10/min; good webhook support |
| ElevenLabs Conversational AI | SaaS | Yes | ~500ms latency; premium voice quality; $0.50/min |
| LiveKit | OSS + SaaS | Yes | Self-hosted or cloud; WebRTC media server; most flexible |
| Bland.ai | SaaS | Yes | Outbound campaigns; $0.09/min; bulk scheduling |
| OpenAI Realtime API | SaaS | Partial | Speech-to-speech; 128K context; no streaming tool calls |
| Twilio ConversationRelay | SaaS | Yes | PSTN bridge for any AI backend; pairs with LiveKit/Retell |
| Synthflow | SaaS | Yes | Enterprise telephony; <100ms latency; custom pricing |

## Templates & scripts
```python
# retell_agent.py — minimal Retell webhook handler (≤45 lines)
from fastapi import FastAPI, Request
from retell import Retell
import os

app = FastAPI()
client = Retell(api_key=os.environ["RETELL_API_KEY"])

SYSTEM_PROMPT = """You are an appointment scheduler for Acme Clinic.
Keep responses short (1-2 sentences). Confirm all details before booking."""

@app.post("/retell-webhook")
async def retell_webhook(request: Request):
    payload = await request.json()
    event_type = payload.get("event")

    if event_type == "call_started":
        return {"response_id": payload["response_id"], "content": "Hello! How can I help you today?"}

    if event_type == "call_analyzed":
        # Post-call: save transcript, trigger CRM update
        transcript = payload.get("transcript", "")
        await save_transcript(payload["call_id"], transcript)
        return {"status": "ok"}

    if event_type == "agent_response":
        conversation = payload.get("transcript", [])
        response = await generate_response(conversation)
        return {"response_id": payload["response_id"], "content": response}

    return {"status": "ignored"}

async def generate_response(conversation: list) -> str:
    # Call your LLM with system prompt + conversation history
    from openai import AsyncOpenAI
    openai = AsyncOpenAI()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation
    resp = await openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return resp.choices[0].message.content
```

## Best practices
- Keep LLM response length to 1-3 sentences — long responses are unnatural over voice and increase TTS latency
- Strip markdown, bullet points, and special characters from LLM output before TTS synthesis
- Implement barge-in: detect user speech during agent TTS output and interrupt immediately via VAD
- Use filler phrases ("Let me check that for you") while tool calls execute — silence >1s feels like a disconnect
- Log full transcripts + turn latencies per call; p95 latency per component reveals where to optimize
- Set a conversation timeout (15-20 mins) to prevent runaway agent sessions consuming telephony minutes
- Test with real phone numbers and real accents before launch — simulator accuracy differs significantly from production
- Use webhooks for post-call processing (CRM updates, quality scoring) rather than blocking the call thread

## AI-agent gotchas
- Voice system prompts must explicitly forbid markdown — LLMs generate `**bold**` text even when not instructed to
- Tool calls during voice must complete in <2s or the agent sounds unresponsive; cache frequent lookups (order status, user data)
- GPT-4o Realtime API requires WebRTC peer connection — cannot be called from a standard Python async context without a media bridge
- Retell/Vapi charge per minute of call time, not per LLM token — cost model is different from text agents; budget accordingly
- PSTN calls add ~150ms latency vs WebRTC; budget for this in latency requirements
- VAD false positives (background noise triggers turn detection) cause the agent to respond mid-user-sentence; tune `endpointing_delay` to 400-600ms
- Outbound campaigns via Bland/Retell require compliance with TCPA (US) and GDPR — do not autodial without explicit consent workflows

## References
- [Retell AI Documentation](https://docs.retellai.com/)
- [LiveKit Agents Framework](https://docs.livekit.io/agents/)
- [Vapi Documentation](https://docs.vapi.ai/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [ElevenLabs Conversational AI](https://elevenlabs.io/docs/agents-platform/overview)
- [Twilio ConversationRelay](https://www.twilio.com/en-us/products/conversational-ai/conversationrelay)
- [Building Voice Agents — LiveKit Blog](https://blog.livekit.io/building-voice-agents/)
