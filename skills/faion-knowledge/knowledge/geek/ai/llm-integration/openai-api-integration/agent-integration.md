# Agent Integration — OpenAI API Integration

## When to use
- Building a production application that needs the OpenAI Chat Completions API as the primary LLM backend
- Concurrent/async batch processing of many prompts is required (AsyncOpenAI + asyncio.gather)
- Structured output via Pydantic / `response_format={"type": "json_object"}` is the primary interface contract
- Cost estimation and token counting before request submission is needed (tiktoken)
- The existing stack is already OpenAI-dependent (Assistants API, DALL-E, Whisper, TTS) and switching providers is not planned

## When NOT to use
- The task fits a smaller model (Claude Haiku, GPT-4o-mini) — always start with the cheapest model that meets quality bar
- You need 1M+ context — Gemini 1.5 Pro is the right tool; OpenAI's max is 128K
- The project policy requires on-premise or self-hosted inference — use Ollama or a local model
- The response format is unknown/flexible — structured output requires knowing the schema up front

## Where it fails / limitations
- `finish_reason == "length"` means the response was truncated; agents that do not check this produce silently incomplete outputs
- `json_object` mode does not guarantee a specific schema — the LLM may omit fields or add extras; always validate with Pydantic
- `AsyncOpenAI` does not work inside Jupyter notebooks without `nest_asyncio` — the event loop is already running
- Rate limits are tier-dependent; newly created API keys start at Tier 1 (low RPM/TPM) and must be upgraded manually
- The `openai` SDK v1 (>=1.0) is incompatible with code written for v0.x; `openai.ChatCompletion.create` vs. `client.chat.completions.create` — check package version in CI

## Agentic workflow
A subagent integrating OpenAI should initialize the `OpenAI` or `AsyncOpenAI` client from the environment, wrap calls with exponential backoff using `tenacity`, count tokens with `tiktoken` before sending to catch context overflow, and always check `finish_reason` in the response. For batch operations, the subagent should use `AsyncOpenAI` with `asyncio.gather` and a concurrency semaphore to stay within rate limits. Structured output should use `client.beta.chat.completions.parse` with Pydantic models for guaranteed schema compliance.

### Recommended subagents
- `faion-sdd-executor-agent` — implement OpenAIService class with retry and logging as an SDD task
- General-purpose subagent — run batch async completions for data extraction or classification pipelines

### Prompt pattern
```
Use AsyncOpenAI to process {count} prompts concurrently (max {concurrency} at a time).
Model: gpt-4o-mini. Return structured JSON per prompt matching schema: {schema}.
Log token usage per request. Handle RateLimitError with exponential backoff (max 3 retries).
```

```
Extract structured data from the text below using response_format=Person (Pydantic model).
Validate the parsed object. If parsing fails, return {"error": "parse_failed", "raw": "<response>"}.
Text: {text}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install openai` | Official Python SDK | [pypi](https://pypi.org/project/openai/) |
| `pip install tiktoken` | Token counting for cost estimation | [pypi](https://pypi.org/project/tiktoken/) |
| `pip install tenacity` | Retry with exponential backoff | [pypi](https://pypi.org/project/tenacity/) |
| `pip install pydantic` | Structured output validation | [pypi](https://pypi.org/project/pydantic/) |
| `openai api` | CLI for quick completions and file uploads | bundled with `openai` package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Platform | SaaS | Yes | Primary API; `OPENAI_API_KEY` env var; usage limits per tier |
| Azure OpenAI | SaaS | Yes | Same API surface; enterprise compliance; requires Azure subscription |
| LiteLLM | OSS | Yes | Drop-in proxy; route `openai` SDK calls to Claude/Gemini without code changes |
| Langfuse | OSS/SaaS | Yes | Trace + log all OpenAI calls; self-hostable |
| Helicone | SaaS | Yes | Proxy with caching, rate limiting, analytics; minimal code change |

## Templates & scripts
See `templates.md` for `OpenAIService` class with `CompletionConfig`, retry decorator, and usage logging.

Inline token guard (≤15 lines):
```python
import tiktoken

def guard_context(messages: list, model: str = "gpt-4o", max_tokens: int = 4000) -> bool:
    """Return False if prompt + max_tokens exceeds context limit."""
    enc = tiktoken.encoding_for_model(model)
    limits = {"gpt-4o": 128000, "gpt-4o-mini": 128000, "gpt-4-turbo": 128000}
    prompt_tokens = sum(len(enc.encode(m["content"])) for m in messages)
    return (prompt_tokens + max_tokens) <= limits.get(model, 128000)
```

## Best practices
- Always pin the `openai` SDK version in `requirements.txt`; major versions (v0 → v1) have breaking API changes
- Use `gpt-4o-mini` as default and escalate to `gpt-4o` only when quality tests fail — the cost difference is ~30x
- Log `usage.prompt_tokens`, `usage.completion_tokens`, and `finish_reason` for every call; this data is essential for cost auditing and detecting truncation
- Set `timeout=30.0` on every `client.chat.completions.create` call; without it, a hanging network request blocks the event loop indefinitely
- Use `client.beta.chat.completions.parse` (Pydantic structured output) instead of `json_object` mode when schema compliance is critical — it guarantees the model fills required fields

## AI-agent gotchas
- `message.tool_calls` is `None` (not `[]`) when no tools are called; always use `if message.tool_calls:` not `if message.tool_calls is not None and len(message.tool_calls) > 0:`
- Parallel tool calls: the model may call multiple tools in one response; agents that only handle the first `tool_call` silently drop the rest
- `response_format={"type": "json_object"}` requires the word "json" to appear somewhere in the prompt or system message — otherwise the model ignores the format instruction
- Human checkpoint before switching from `gpt-4o-mini` to `gpt-4o` in production; the cost jump is significant and should be justified by documented quality test results
- Organization-level rate limits are shared across all API keys; multiple subagents running concurrently can exhaust the org's TPM limit even if each individual agent is well-behaved

## References
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [tiktoken GitHub](https://github.com/openai/tiktoken)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Tenacity retry library](https://tenacity.readthedocs.io/)
