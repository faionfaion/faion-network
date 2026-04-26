# OpenAI API Integration

## Summary

OpenAI Platform provides Chat Completions, the Responses API (2025+, stateful), Structured Outputs, Batch API (50% discount), embeddings, Whisper, TTS, DALL-E, and fine-tuning. Pin exact model versions (`gpt-4o-2024-08-06`). Use Structured Outputs (`beta.chat.completions.parse`) not JSON mode. Set `max_tokens` on every call. For new projects, prefer the Responses API over Chat Completions — it manages conversation state server-side.

## Why

The OpenAI API is the most widely supported LLM integration target, with the strongest ecosystem for structured output (native schema enforcement), function calling, and the Batch API for 50% cost reduction on non-time-sensitive workloads. Pinning model versions prevents silent behavior changes; exponential backoff handles rate limits gracefully.

## When To Use

- Native structured output with schema enforcement is required (no other provider matches)
- Vision tasks requiring GPT-4o image understanding
- Batch processing of non-time-sensitive data (50% cost discount via Batch API)
- Function calling / tool use as the primary agentic mechanism
- Audio transcription (Whisper) or TTS in agent pipelines
- Responses API's built-in conversation state management is needed

## When NOT To Use

- Privacy-sensitive data that must not leave your infrastructure — use local Ollama
- Context &gt;128K tokens — use Claude (200K) or Gemini (2M)
- Tight budget on high-volume simple tasks — Gemini Flash is cheaper than gpt-4o-mini
- When Claude's instruction-following is more reliable for your specific task

## Content

| File | What's inside |
|------|---------------|
| `content/01-api-overview.xml` | Endpoint overview, model selection, Responses API vs Chat Completions, rate limits |
| `content/02-rules.xml` | Production rules, error handling, cost optimization, agentic loop gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/backoff.py` | Exponential backoff wrapper for rate limit and server errors |
| `templates/agent-loop.py` | Function-calling agent loop with tool execution |
| `templates/batch-submit.py` | Batch API JSONL builder and job submission |
