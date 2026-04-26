# OpenAI Function Calling and Structured Outputs

## Summary

OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.beta.chat.completions.parse`, parallel tool calls, and multimodal extensions (DALL-E 3, Whisper, TTS). The primary distinction from generic tool use: structured outputs enforce schema compliance at the API level, not just via prompt instruction.

## Why

`client.beta.chat.completions.parse` with a Pydantic model enforces field presence at the API level — the model cannot produce a response missing required fields. This eliminates the most common class of extraction failures (missing or mistyped fields) that `json_object` mode cannot prevent.

## When To Use

- Reliable, schema-validated JSON extraction from unstructured text
- Pipeline driving external actions (API calls, DB writes) triggered by model decisions
- Multiple tools needed in a single model response (parallel tool calls) to reduce round-trips
- Image generation (DALL-E 3), speech-to-text (Whisper), or TTS alongside text LLM calls
- Strict output format enforcement where `json_object` mode alone is insufficient

## When NOT To Use

- Only need a JSON blob without schema strictness — `response_format={"type": "json_object"}` is simpler
- Simple prompting + regex post-processing is sufficient
- Schema is deeply nested (>10 params) causing frequent misselection — simplify the schema first
- Real-time audio generation at sub-200ms latency — TTS streaming is not suitable

## Content

| File | What's inside |
|------|---------------|
| `content/01-function-calling.xml` | Tool loop pattern, parallel tool calls, tool_choice options |
| `content/02-structured-outputs.xml` | Pydantic structured extraction, JSON mode, gotchas (refusal, model support) |
| `content/03-multimodal.xml` | DALL-E 3 URL expiry rule, Whisper chunking, TTS model pinning |

## Templates

| File | Purpose |
|------|---------|
| `templates/pydantic-extraction.py` | Structured output extraction with Pydantic + parse() |
| `templates/whisper-chunked.py` | Large audio transcription via ffmpeg chunking (≤30 lines) |
