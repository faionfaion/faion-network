---
id: voice-agents
name: "Voice Agents"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Voice Agents

Production voice AI agents: real-time voice assistants, telephony integration, conversational AI.

## Market Overview (2025-2026)

| Metric | Value |
|--------|-------|
| Speech recognition market | $29.28B by 2026 |
| Call center AI market | $2.41B (2025) → $10.07B (2032) |
| CAGR | 22.7% |
| North America market share | 36.92% (2024) |

## Architecture

```
User Speech → STT → LLM → TTS → Agent Speech
     ↑                              ↓
     └──────── Audio Stream ────────┘
```

**Voice Pipeline Components:**

| Component | Purpose | Latency Target |
|-----------|---------|----------------|
| STT (Speech-to-Text) | Transcribe user speech | <200ms |
| VAD (Voice Activity Detection) | Detect speech boundaries | <50ms |
| LLM | Generate response | <500ms |
| TTS (Text-to-Speech) | Synthesize speech | <200ms |
| Turn Detection | Detect end of user turn | <100ms |

**Total target latency:** <600-800ms for natural conversation

## Platform Comparison

| Platform | Latency | Pricing | Best For |
|----------|---------|---------|----------|
| [Retell AI](https://www.retellai.com) | ~600ms | $0.07-0.12/min | Production phone agents |
| [ElevenLabs](https://elevenlabs.io/conversational-ai) | ~500ms | $0.50/min | Premium voice quality |
| [LiveKit](https://livekit.io) | <100ms | Self-hosted / Cloud | Custom infrastructure |
| [Vapi](https://vapi.ai) | <500-700ms | $0.05-0.10/min | Rapid prototyping |
| [Bland.ai](https://www.bland.ai) | ~800ms | $0.09/min | Outbound campaigns |
| [Synthflow](https://synthflow.ai) | <100ms | Custom | Enterprise telephony |

## Connection Methods

| Method | Use Case | Latency |
|--------|----------|---------|
| WebRTC | Browser/mobile apps | Lowest |
| WebSocket | Server-to-server | Low |
| SIP | VoIP/telephony | Carrier-grade |
| PSTN | Traditional phone | Standard |

## 2025-2026 Trends

1. **Emotional Intelligence** - Agents detect emotions (urgency, hesitation) and adjust responses
2. **Multilingual Real-time** - Seamless translation across 100+ languages
3. **Proactive Agents** - Anticipate user needs before being asked
4. **Hybrid Human-AI** - AI handles routine, humans handle complex/emotional
5. **MCP Integration** - Model Context Protocol for tool calling
6. **Speech-to-Speech Models** - Direct audio models (GPT-4o Realtime) bypass STT/TTS pipeline

## Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and platform comparison |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples for each platform |
| [templates.md](templates.md) | Production templates |
| [llm-prompts.md](llm-prompts.md) | System prompts for voice agents |

## Quick Start Decision

```
Need phone integration?
├─ Yes → Retell AI or Vapi (fastest setup)
├─ Self-hosted required? → LiveKit
├─ Premium voice quality? → ElevenLabs
└─ No → OpenAI Realtime API + WebRTC
```

## References

- [Retell AI Docs](https://docs.retellai.com/)
- [ElevenLabs Agents Platform](https://elevenlabs.io/docs/agents-platform/overview)
- [LiveKit Agents](https://docs.livekit.io/agents/)
- [Vapi Documentation](https://docs.vapi.ai/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [Twilio ConversationRelay](https://www.twilio.com/en-us/products/conversational-ai/conversationrelay)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Voice interface design | sonnet | UX pattern |
| Real-time processing | sonnet | Performance optimization |
| Conversation flow | sonnet | Dialog design |
