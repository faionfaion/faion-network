# Gemini API

## Summary

Google Gemini API for multimodal AI applications. Models: Gemini 3 Pro/Flash (1M+ context, dynamic thinking), Gemini 2.0 Flash (fast, agentic), Gemini 1.5 Pro (2M context). Key differentiators: native video/audio input, Live API for real-time voice/video, code execution sandbox, Google Search grounding, context caching (75% cost reduction).

## Why

Gemini is the only LLM provider with a 2M-token context window, native video input, and a Live API for sub-200ms real-time voice. For long-document processing, video analysis, or real-time voice agents, Gemini 1.5 Pro or 2.0 Flash have no direct OpenAI/Claude equivalent.

## When To Use

- Processing documents, codebases, or video that exceeds 128K tokens (use Gemini 1.5 Pro at 2M)
- Real-time voice/video applications requiring low latency (use Live API with Gemini 2.0 Flash)
- Applications needing code execution in a sandboxed Python environment
- Grounding responses in live Google Search results (use grounding tools)
- High-volume production with cost sensitivity (Gemini 2.0 Flash at $0.10/$0.40 per 1M tokens)

## When NOT To Use

- Agent tooling accuracy is critical: OpenAI and Claude have more mature tool-use ecosystems
- Need the strongest available reasoning: use Claude Opus or o3 for frontier reasoning tasks
- Enterprise compliance requiring no Google data processing — use Azure OpenAI or Claude on AWS

## Content

| File | What's inside |
|------|---------------|
| `content/01-models-and-features.xml` | Model comparison, Gemini 3 features (dynamic thinking, thought signatures), multimodal inputs, pricing, Live API |
| `content/02-patterns-and-gotchas.xml` | Integration patterns (chat, multimodal, function calling, RAG, caching), Gemini 3 prompting rules, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/gemini-client.py` | Production Gemini client: model setup, retry logic, streaming, function calling, chat session |
| `templates/gemini-multimodal.py` | Image analyzer + video analyzer + document processor classes |
