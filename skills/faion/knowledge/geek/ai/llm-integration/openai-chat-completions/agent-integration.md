# Agent Integration — OpenAI Chat Completions

## When to use
- Building agent pipelines that call OpenAI models (gpt-4o, gpt-4o-mini, o1, o3-mini)
- Streaming partial outputs to users or downstream steps in real time
- Generating structured JSON via `response_format` or function-forcing pattern
- Multi-image or screenshot analysis inside an automated workflow
- Cost-sensitive pipelines where gpt-4o-mini is an acceptable quality trade-off

## When NOT to use
- When you need persistent conversation state across requests (use Assistants API instead)
- When you need guaranteed schema compliance (use Structured Outputs / `beta.parse` instead of JSON Mode)
- Tasks requiring >128K context (use Claude 200K or Gemini 1M)
- When Anthropic Claude is already available and task quality matters more than vendor diversity

## Where it fails / limitations
- JSON Mode only guarantees valid JSON, not schema conformance — production pipelines must validate externally
- Rate limits at lower tiers (3 RPM free, 500 RPM Tier 1) block burst pipelines without a queue layer
- `seed` parameter reduces but does not eliminate non-determinism
- Vision struggles with rotated or small text, spatial reasoning, and animated GIFs
- No native conversation memory — every call is stateless; history must be maintained by caller
- Token cost for long context grows linearly; 128K contexts at gpt-4o pricing are expensive

## Agentic workflow
A Claude subagent can drive Chat Completions by constructing message arrays, calling the OpenAI SDK, parsing the response, and routing the output to the next pipeline stage. For batch parallelism, use `AsyncOpenAI` with `asyncio.gather`. Always extract `usage` tokens and log them per call to detect cost anomalies. Stop sequences and `n=1` keep outputs predictable in automated pipelines.

### Recommended subagents
- `faion-sdd-executor-agent` — executes code-generation or review tasks using Chat Completions as the inference backend
- `nero-sdd-executor-agent` — same pattern for NERO platform pipelines

### Prompt pattern
```python
# Minimal agentic call with structured-ish output
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Return only valid JSON."},
        {"role": "user", "content": task_prompt}
    ],
    response_format={"type": "json_object"},
    temperature=0.2
)
result = json.loads(response.choices[0].message.content)
```

```python
# Async parallel — N prompts in one pass
import asyncio
from openai import AsyncOpenAI
client = AsyncOpenAI()

async def batch(prompts):
    tasks = [client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": p}]
    ) for p in prompts]
    return await asyncio.gather(*tasks)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` CLI | Quick completions, fine-tune, files | `pip install openai` → `openai api chat_completions.create` |
| `tiktoken` | Token counting before calls | `pip install tiktoken` |
| `httpie` | Raw API debugging | `pip install httpie` → `http POST api.openai.com/v1/chat/completions` |
| `tenacity` | Retry with backoff | `pip install tenacity` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Platform | SaaS | Yes | Main endpoint; usage dashboard for cost tracking |
| LiteLLM | OSS proxy | Yes | Unified interface across providers; rate-limit handling built in |
| Helicone | SaaS | Yes | Request logging, cost tracking, replay — drop-in proxy |
| Portkey | SaaS | Yes | Fallback routing, caching, observability |
| OpenRouter | SaaS | Yes | Multi-provider routing; useful for fallback when OpenAI is down |

## Templates & scripts
See `templates.md` for PromptTemplate and few-shot patterns. Inline retry helper:

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(min=1, max=60),
    stop=stop_after_attempt(5)
)
def call_chat(messages, model="gpt-4o-mini", temperature=0.2):
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )
    return response.choices[0].message.content, response.usage
```

## Best practices
- Use `gpt-4o-mini` for agent inner loops (cheap, fast); escalate to `gpt-4o` only for quality gates
- Always read `response.usage` and accumulate token counts per pipeline run
- Set `temperature=0.0-0.2` for deterministic extraction tasks; `0.7+` only for creative generation
- Use `stop=["```"]` or similar when extracting code blocks to prevent runaway outputs
- Prefer `AsyncOpenAI` for any pipeline that spawns > 2 parallel LLM calls
- Check `x-ratelimit-remaining-requests` header before dispatching large batches
- Do not mix JSON Mode with ambiguous system prompts — be explicit: "Return only valid JSON"
- Log `model`, `usage`, and `stop_reason` for every call; `max_tokens` stop reason silently truncates output

## AI-agent gotchas
- `stop_reason == "max_tokens"` means output is truncated — never parse truncated JSON blindly; detect and retry with larger `max_tokens`
- Token counting with `tiktoken` is approximate for multimodal (images add 85–1105 tokens depending on detail level)
- `seed` does not guarantee identical outputs across API versions or after model updates
- JSON Mode can return `{}` or minimal JSON when model is confused — always validate schema before passing to next step
- Rate limit headers are per-model, not global — a Tier 1 account can hit limits on gpt-4o while gpt-4o-mini is free
- Parallel async calls all count toward the same TPM budget — throttle with a semaphore for large batches
- Vision + long text in one message inflates context significantly; profile token cost before shipping

## References
- https://platform.openai.com/docs/guides/chat-completions
- https://platform.openai.com/docs/guides/vision
- https://platform.openai.com/docs/guides/rate-limits
- https://platform.openai.com/docs/guides/prompt-engineering
- https://github.com/openai/openai-python
