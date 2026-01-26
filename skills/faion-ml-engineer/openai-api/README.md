# OpenAI API Integration

Complete guide to OpenAI Platform APIs for production applications.

## When to Use

- Chat completions for text generation and conversation
- Structured output for reliable JSON responses
- Streaming for real-time user interfaces
- Function calling for tool use and agents
- Vision for image understanding
- Embeddings for semantic search and RAG
- Audio APIs (Whisper, TTS) for voice applications
- Fine-tuning for custom model behavior
- Batch API for cost-optimized bulk processing

## Key Concepts

### API Endpoints Overview

| API | Endpoint | Best Model | Use Case |
|-----|----------|------------|----------|
| **Chat Completions** | `/v1/chat/completions` | gpt-4o | Text generation, conversation |
| **Responses** | `/v1/responses` | gpt-4o | Simplified stateful API (2025+) |
| **Vision** | `/v1/chat/completions` | gpt-4o | Image understanding |
| **Function Calling** | `/v1/chat/completions` | gpt-4o | Tool use, structured output |
| **Embeddings** | `/v1/embeddings` | text-embedding-3-large | Vector search, RAG |
| **Whisper** | `/v1/audio/transcriptions` | whisper-1 | Speech-to-text |
| **TTS** | `/v1/audio/speech` | tts-1-hd | Text-to-speech |
| **DALL-E** | `/v1/images/generations` | dall-e-3 | Image generation |
| **Batch** | `/v1/batches` | gpt-4o | 50% cost savings |
| **Fine-tuning** | `/v1/fine_tuning/jobs` | gpt-4o-mini | Custom models |

### Model Selection (2025-2026)

| Model | Context | Input $/M | Output $/M | Best For |
|-------|---------|-----------|------------|----------|
| **gpt-4o** | 128K | $2.50 | $10.00 | General purpose, best quality |
| **gpt-4o-mini** | 128K | $0.15 | $0.60 | Cost-effective, fast |
| **o1** | 128K | $15.00 | $60.00 | Complex reasoning |
| **o3-mini** | 200K | $1.10 | $4.40 | Latest reasoning model |
| **gpt-4.1** | 1M | TBD | TBD | Long context (when available) |

### Responses API vs Chat Completions

OpenAI recommends using the **Responses API** for new applications (2025+):

| Feature | Chat Completions | Responses API |
|---------|------------------|---------------|
| State management | Manual | Built-in (`previous_response_id`) |
| Conversation history | Developer manages | Optional persistent storage |
| Tool results | Separate messages | Integrated |
| Reasoning models | Works | Better performance |
| Future development | Maintenance mode | Active development |

**Migration recommended** for:
- New projects
- Reasoning model usage (o1, o3)
- Applications needing conversation state

### Authentication

```bash
# Environment variable (recommended)
export OPENAI_API_KEY="sk-proj-..."

# API Key types
# sk-proj-*   Project key (recommended, single project)
# sk-*        User key (legacy, all projects)
# sk-svcacct-* Service account (automated systems)
```

### Structured Outputs

**Always prefer Structured Outputs over JSON mode** when possible:

| Method | Guarantees | Schema Compliance |
|--------|------------|-------------------|
| **Structured Outputs** | Valid JSON + Schema | Yes |
| **JSON Mode** | Valid JSON only | No |

```python
from pydantic import BaseModel

class Response(BaseModel):
    answer: str
    confidence: float

# Native structured output
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=Response
)
result = response.choices[0].message.parsed  # Typed Response object
```

### Streaming Best Practices

```python
# Basic streaming
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Key considerations:**
- Reduces time-to-first-token (TTFT)
- Same total generation time
- Content moderation more difficult with partial outputs
- Use SDK helpers for streaming with structured outputs

### Error Handling

| Error | HTTP Code | Solution |
|-------|-----------|----------|
| `invalid_api_key` | 401 | Check OPENAI_API_KEY |
| `rate_limit_exceeded` | 429 | Implement exponential backoff |
| `insufficient_quota` | 429 | Add credits or wait for reset |
| `context_length_exceeded` | 400 | Reduce input or use larger context model |
| `server_error` | 500 | Retry with backoff |

### Production Best Practices

1. **Pin model versions** - Use `gpt-4o-2024-08-06` not `gpt-4o`
2. **Build evals** - Monitor prompt performance over time
3. **Use prompt caching** - Reduces latency and cost for repeated prefixes
4. **Set max_tokens** - Prevents runaway token generation
5. **Use stop sequences** - Prevents generating unneeded tokens
6. **Implement backoff** - Handle rate limits gracefully
7. **Never expose keys** - Keep API keys server-side only

### Rate Limiting

| Tier | RPM | TPM | Monthly Spend |
|------|-----|-----|---------------|
| Free | 3 | 200 | Limited |
| Tier 1 | 500 | 30K | $100 |
| Tier 2 | 5,000 | 450K | $500 |
| Tier 3 | 5,000 | 800K | $1,000 |
| Tier 4 | 10,000 | 2M | $5,000 |
| Tier 5 | 10,000 | 10M | $50,000 |

### Cost Optimization

1. **Use gpt-4o-mini** for simple tasks (90% cheaper than gpt-4o)
2. **Batch API** for non-time-sensitive work (50% discount)
3. **Prompt caching** for repeated system prompts
4. **Reduce dimensions** for embeddings when quality permits
5. **Use `max_tokens`** to limit output length
6. **Monitor usage** with `response.usage` tracking

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists for production readiness |
| [examples.md](examples.md) | Code examples for all major APIs |
| [templates.md](templates.md) | Reusable code templates and patterns |
| [llm-prompts.md](llm-prompts.md) | Prompts for API integration assistance |

## External Resources

### Official Documentation

- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [Streaming Responses Guide](https://platform.openai.com/docs/guides/streaming-responses)
- [Production Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [Migrate to Responses API](https://platform.openai.com/docs/guides/migrate-to-responses)

### Libraries

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Node.js SDK](https://github.com/openai/openai-node)
- [tiktoken](https://github.com/openai/tiktoken) - Token counting
- [Instructor](https://github.com/jxnl/instructor) - Structured outputs helper

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-llm-integration](../faion-llm-integration/CLAUDE.md) | LLM API patterns across providers |
| [faion-rag-engineer](../faion-rag-engineer/CLAUDE.md) | Embeddings for RAG pipelines |
| [faion-ai-agents](../faion-ai-agents/CLAUDE.md) | Function calling for agents |
| [faion-ml-ops](../faion-ml-ops/CLAUDE.md) | Fine-tuning and evaluation |
