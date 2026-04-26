# OpenAI Chat Completions

## Summary

Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection, parameters (temperature, max_tokens, response_format), streaming, vision (URL and base64), error handling with exponential backoff, rate limit headers, and cost tracking via tiktoken. The core rule: always read `stop_reason` — `"max_tokens"` means silent truncation; never parse JSON from a truncated response.

## Why

Chat Completions is the primary OpenAI inference endpoint. Without proper parameter discipline (temperature for task type, response_format for JSON extraction) and retry logic, pipelines produce inconsistent outputs and fail silently under rate limiting. Vision token cost varies 85–1105 tokens per image depending on detail level — untracked, this blows budgets on multimodal pipelines.

## When To Use

- Building agent pipelines calling OpenAI models (gpt-4o, gpt-4o-mini, o1, o3-mini)
- Streaming partial outputs to users or downstream pipeline steps in real time
- Generating structured JSON via `response_format={"type": "json_object"}`
- Multi-image or screenshot analysis inside an automated workflow
- Cost-sensitive pipelines where gpt-4o-mini quality is acceptable

## When NOT To Use

- When persistent conversation state is needed across sessions — use Assistants API
- When guaranteed schema compliance is required — use Structured Outputs (`beta.parse`) not JSON Mode
- Tasks requiring more than 128K context — use Claude 200K or Gemini 2M
- When Anthropic Claude is available and task quality matters more than vendor diversity

## Content

| File | What's inside |
|------|---------------|
| `content/01-request-response.xml` | Basic request structure, model table with pricing, parameters reference, response parsing, message roles |
| `content/02-streaming.xml` | Streaming with stream=True, async parallel completions with AsyncOpenAI, streaming response collection |
| `content/03-vision.xml` | Image from URL and base64, multiple images, detail level tokens table, vision limitations |
| `content/04-error-handling.xml` | Common error table, retry with backoff (manual and tenacity), rate limit headers, cost tracking with tiktoken |

## Templates

| File | Purpose |
|------|---------|
| `templates/retry-client.py` | OpenAI client wrapper with tenacity retry on RateLimitError and APIError |
| `templates/encode-image.py` | Base64 image encoding helper for vision requests |
