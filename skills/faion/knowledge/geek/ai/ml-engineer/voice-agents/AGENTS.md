# Voice Agents

## Summary

Production voice AI agents built on real-time STT → LLM → TTS pipelines. Use managed platforms (Retell AI, Vapi, ElevenLabs) for phone and web voice agents. Total pipeline latency target is 600-800ms; anything above 1.5s feels broken. Keep LLM responses to 1-3 sentences and strip all markdown before TTS synthesis.

## Why

Voice agents replace IVR menus and phone support with natural conversational AI. The market is growing at 22.7% CAGR. Managed platforms absorb the hardest infrastructure problems (WebRTC, VAD, barge-in, telephony integration) so that teams can focus on conversation design and tool integration. Building the media layer from scratch (LiveKit) is only justified when self-hosting is required or latency requirements are below 300ms.

## When To Use

- Phone-based AI agents: inbound/outbound call center, appointment scheduling, support
- Web or mobile app requires real-time voice conversation (browser WebRTC)
- Replacing IVR menus with natural conversational AI
- Voice accessibility feature: hands-free interface for existing workflows
- Live translation: real-time speech-to-speech across 100+ languages

## When NOT To Use

- Text chat is sufficient — voice adds latency, cost, and infra complexity for no UX gain
- Latency budget is below 300ms end-to-end — no current production stack achieves this reliably
- Audio quality is unpredictable (noisy environment, poor microphone) — accuracy degrades significantly
- Use case requires precise multi-step confirmation (legal, medical consent) — voice ambiguity introduces risk
- Self-hosted required with less than $500/month infra budget — LiveKit self-hosting requires real-time media server expertise

## Content

| File | What's inside |
|------|---------------|
| `content/01-platforms.xml` | Platform comparison (Retell, Vapi, ElevenLabs, LiveKit), connection methods, selection rules |
| `content/02-pipeline.xml` | STT, VAD, LLM, TTS configuration rules; barge-in handling; turn detection; tool call patterns |
| `content/03-production.xml` | Implementation checklist, monitoring metrics, security, compliance, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/retell-webhook.py` | Minimal Retell AI webhook handler (FastAPI, ~45 lines) |
| `templates/system-prompt.txt` | Voice agent system prompt template — short responses, no markdown, tool call pattern |
