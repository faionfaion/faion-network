# Claude API Integration

## Summary

Full Claude API integration patterns: client initialization, sync/async completions, streaming, tool use, vision (URL and base64), Extended Thinking for complex reasoning, Prompt Caching for cost reduction, and the Batch API for offline jobs. The core rule: always check `stop_reason` — `"max_tokens"` is silent truncation; `"tool_use"` means the agent loop must continue; only `"end_turn"` is normal completion.

## Why

Claude's 200K context, first-class system prompt support, and Extended Thinking make it the primary reasoning engine for complex multi-step agents. Without `stop_reason` handling, agents silently return truncated text or hang waiting for tool results. Prompt Caching requires a byte-identical system prompt prefix — a single extra space invalidates the cache and doubles costs for repetitive pipelines.

## When To Use

- Tasks requiring deep instruction-following across long contexts (up to 200K tokens)
- Code generation, review, or refactoring where nuance and safety matter
- Multi-turn conversation pipelines where system prompt stability is critical
- Long document processing (legal, technical, medical) in a single shot
- Extended Thinking tasks: multi-step math, architecture decisions, strategic planning
- When Anthropic's safety defaults are a feature, not a bug

## When NOT To Use

- High-volume, low-cost inner loops where gpt-4o-mini is sufficient (Claude Haiku excepted)
- When OpenAI Structured Outputs (`beta.parse`) schema enforcement is required — Claude lacks this
- Tasks needing OpenAI Assistants' persistent thread and file storage model
- When Google Search grounding is required — use Gemini instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-client-setup.xml` | Client initialization, model hierarchy table, sync and async patterns, streaming |
| `content/02-tool-use.xml` | Tool definition, single-turn tool dispatch, vision (URL and base64), Extended Thinking |
| `content/03-production.xml` | ClaudeService wrapper, ClaudeConfig dataclass, tenacity retry, error type handling |
| `content/04-advanced.xml` | Prompt Caching (1024-token minimum, prefix matching), Batch API helper, cost tracking |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-service.py` | ClaudeService class with ClaudeConfig, retry decorator, and token counting |
| `templates/batch-api.py` | create_batch() and poll_batch() helpers for the Anthropic Batch API |
