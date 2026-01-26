# Claude API Reference

Complete guide to Anthropic Claude API for the faion-network framework.

## Quick Reference

| API | Endpoint | Best Model | Use Case |
|-----|----------|------------|----------|
| **Messages** | `/v1/messages` | claude-sonnet-4 | Text generation, conversation |
| **Tool Use** | `/v1/messages` | claude-sonnet-4 | Function calling, structured output |
| **Vision** | `/v1/messages` | claude-sonnet-4 | Image/PDF understanding |
| **Extended Thinking** | `/v1/messages` | claude-opus-4-5 | Complex reasoning |
| **Computer Use** | `/v1/messages` | claude-sonnet-4 | Browser/desktop automation |
| **Batch** | `/v1/messages/batches` | All models | 50% cost savings |
| **Prompt Caching** | `/v1/messages` | All models | 90% cached input savings |
| **Token Counting** | `/v1/messages/count_tokens` | All models | Pre-flight token estimation |

## Models (2025-2026)

| Model | ID | Context | Input $/M | Output $/M | Best For |
|-------|-----|---------|-----------|------------|----------|
| **Claude Opus 4.5** | `claude-opus-4-5-20251101` | 200K | $15.00 | $75.00 | Complex reasoning, research |
| **Claude Sonnet 4** | `claude-sonnet-4-20250514` | 200K | $3.00 | $15.00 | Balanced (recommended) |
| **Claude Haiku 3.5** | `claude-3-5-haiku-20241022` | 200K | $0.80 | $4.00 | Fast, cost-effective |

## Model Selection

| Task | Recommended Model | Why |
|------|-------------------|-----|
| General chat | claude-sonnet-4 | Best balance |
| Complex reasoning | claude-opus-4-5 | Highest capability |
| Code generation | claude-sonnet-4 | Fast, excellent coding |
| Quick classification | claude-3-5-haiku | Fastest, cheapest |
| Long documents | claude-sonnet-4 | Good 200K context |
| Extended thinking | claude-opus-4-5 | Deep reasoning |

## Authentication

```bash
# Environment variable (recommended)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or load from file
source ~/.secrets/anthropic  # Loads ANTHROPIC_API_KEY
```

### Required Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `x-api-key` | `sk-ant-...` | Authentication |
| `anthropic-version` | `2023-06-01` | API version |
| `content-type` | `application/json` | Request format |

### Optional Headers

| Header | Purpose |
|--------|---------|
| `anthropic-beta` | Enable beta features (e.g., `prompt-caching-2024-07-31`) |

## Key Features

### Messages API

Primary API for all Claude interactions. Supports:
- Single and multi-turn conversations
- System prompts for behavior control
- Temperature and sampling parameters
- Stop sequences for controlled output

### Tool Use / Function Calling

Claude 4 models excel at tool use:
- Parallel tool calls supported
- Structured JSON output via forced tool use
- Interleaved thinking with tool use (beta)
- Error handling via `is_error` flag

### Extended Thinking

Enhanced reasoning for complex problems:
- Minimum budget: 1,024 tokens
- Available on Claude 3.7+ and Claude 4 models
- Streaming supported via `thinking_delta` events
- Interleaved thinking with tools (Claude 4)

### Streaming

Real-time response delivery:
- Server-sent events (SSE) format
- Event types: `message_start`, `content_block_delta`, `message_stop`
- Python/TypeScript SDK support
- Async streaming available

### Prompt Caching

90% cost reduction on repeated content:
- TTL: 5 minutes (extends on each use)
- Minimum: 1,024 tokens to cache
- Prefix matching required
- Organization-scoped

### Batch API

50% cost savings for non-urgent workloads:
- Up to 10,000 requests per batch
- 24-hour processing window
- Results available via polling or webhook

## Cost Optimization

1. **Use caching** for repeated system prompts and context
2. **Choose appropriate model** for task complexity
3. **Use Batch API** for non-time-sensitive work
4. **Set max_tokens** appropriately
5. **Pre-count tokens** for large inputs

## Best Practices (2025-2026)

### Tool Use

- Use Claude Sonnet 4 or Opus 4.5 for complex tools
- Enable interleaved thinking for better reasoning
- Handle parallel tool calls efficiently
- Provide clear tool descriptions

### Extended Thinking

- Start with minimum budget (1,024 tokens)
- Increase incrementally for complex problems
- Use for math, logic, code debugging, research
- Stream thinking for user feedback

### Streaming

- Handle multiple content block types
- Resume from text blocks on disconnection
- Use async streaming for concurrent requests
- Process events incrementally

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (Python, TypeScript, curl) |
| [templates.md](templates.md) | Reusable code templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for Claude integration tasks |

## Related Resources

| Resource | Link |
|----------|------|
| Official Docs | [docs.anthropic.com](https://docs.anthropic.com/) |
| API Reference | [docs.anthropic.com/en/api](https://docs.anthropic.com/en/api) |
| Messages API | [docs.anthropic.com/en/api/messages](https://docs.anthropic.com/en/api/messages) |
| Tool Use Guide | [platform.claude.com/docs/en/agents-and-tools/tool-use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) |
| Extended Thinking | [docs.anthropic.com/en/docs/build-with-claude/extended-thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) |
| Streaming | [platform.claude.com/docs/en/build-with-claude/streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) |
| Prompt Engineering | [docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) |
| Anthropic Academy | [anthropic.com/learn/build-with-claude](https://www.anthropic.com/learn/build-with-claude) |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) | Multi-provider LLM APIs |
| [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) | Agent architectures |
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | RAG with Claude |
| [faion-claude-code](../../faion-claude-code/CLAUDE.md) | Claude Code CLI |
