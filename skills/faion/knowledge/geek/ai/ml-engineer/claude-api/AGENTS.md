# Claude API

## Summary

Production guide for calling Anthropic's Claude API directly via the Python and TypeScript SDKs. Covers the Messages API, Tool Use (agentic loops with MAX_TURNS guard), Prompt Caching (90% input-cost reduction on repeated system prompts), Extended Thinking (Opus 4.5 only, minimum 1,024 budget tokens), Streaming (SSE), and the Batch API (50% cost savings, 24-hour window). Always cache system prompts; always enforce MAX_TURNS; always use forced tool use for structured output.

## Why

The Claude API is the lowest-latency path to Claude without proxy overhead. Direct SDK use exposes all billing-reducing features (caching, batching) and all beta capabilities (extended thinking, interleaved thinking with tools) that higher-level frameworks may not surface. For agentic loops where Claude selects tools, direct SDK control over the conversation array is clearer and more debuggable than framework abstractions.

## When To Use

- Building an agentic loop that calls tools and needs full control over the message array
- System prompts or large context blocks repeat across requests — Prompt Caching applies immediately
- Processing hundreds of documents in batch where 50% cost savings outweigh 24-hour latency
- Complex reasoning tasks where Extended Thinking (Opus 4.5) meaningfully improves accuracy
- Existing codebase has no multi-provider requirement — LiteLLM abstraction adds unnecessary overhead

## When NOT To Use

- The codebase already uses LiteLLM, LangChain, or another multi-provider abstraction — keep that layer
- Latency budget is under 200ms — streaming still has SSE overhead; Batch API is unsuitable
- Task complexity does not justify Sonnet or above — route to Haiku or a cheaper provider first (see decision-framework)
- System is already in production with a working multi-provider setup — don't break it for caching savings

## Content

| File | What's inside |
|------|---------------|
| `content/01-api-features.xml` | Messages API, Tool Use, Prompt Caching, Extended Thinking, Streaming, Batch API — rules and usage notes |
| `content/02-gotchas.xml` | Infinite tool loops, cache TTL failure, tool schema drift, thinking token billing, side-effect guards, key rotation |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-caching-agent.py` | Cached system prompt + tool-use loop with MAX_TURNS guard |
| `templates/tool-use-loop.py` | Complete tool-use skeleton with ToolExecutor, retry decorator, forced structured output |
