# Claude Messages API

## Summary

The Claude Messages API is the single completion endpoint for all Claude calls. Covers basic request structure, parameters, response object, multi-turn history management, vision (base64 and URL, images and PDFs), streaming (text_stream and event-based), and SSE event format. The core rule: append the full `resp.content` list (not just text) as the assistant turn in multi-turn history — tool_use blocks must be preserved or the next turn gets a 400 error.

## Why

The Messages API is the integration point for every Claude-based agent. Its `stop_reason` field drives agent branching logic: `"end_turn"` is normal, `"max_tokens"` is silent truncation, `"tool_use"` means the loop must continue. Without explicit `stop_reason` handling and correct multi-turn history construction, agents silently return truncated text, discard tool state, or break with consecutive same-role messages.

## When To Use

- All direct Claude API calls — Messages is the only completion endpoint
- Streaming responses to a user interface or pipeline sink consuming partial text
- Multi-turn agent conversations with explicit message history management
- Vision tasks: screenshot analysis, document OCR, UI inspection, PDF summarization
- When the agent needs to detect `stop_reason` to branch logic

## When NOT To Use

- When persistent thread storage is needed across sessions — build your own; Anthropic has no Threads equivalent
- When guaranteed schema compliance without retry loops is required — use OpenAI `beta.parse` or `instructor`
- High-volume batch jobs — prefer the Batch API (50% cost reduction)
- Computer Use or Extended Thinking inside a stateless lambda — those require multi-turn conversation state

## Content

| File | What's inside |
|------|---------------|
| `content/01-messages-api.xml` | Basic request, parameters table, response structure, content block types, multi-turn pattern |
| `content/02-vision.xml` | Image from base64 and URL, multiple images, PDF document type, supported formats and size limits |
| `content/03-streaming.xml` | text_stream iteration, event-based streaming, stream with tools, async streaming, SSE event format |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-loop.py` | Multi-turn agent loop with explicit stop_reason branching and max-turns guard |
| `templates/vision.py` | analyze_screenshot() helper using base64 encoding for local files |
