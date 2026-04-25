# Agent Integration — Cost Reduction Strategies

## When to use
- Production LLM apps with high request volume (>1000 calls/day) where API costs are significant
- Budget-constrained projects that need to scale without proportional cost increase
- Multi-tenant SaaS where per-request costs must be predictable
- Pipelines running batch classification, extraction, or summarization at scale

## When NOT to use
- Low-volume prototypes — premature optimization adds complexity with no payoff
- Tasks requiring temperature > 0 (non-deterministic outputs) — caching is ineffective
- Latency-critical real-time systems where cache lookup adds unacceptable overhead
- Workflows where output freshness is mandatory (live data, personalized responses)

## Where it fails / limitations
- Semantic caching (embedding-based similarity) introduces false hits when prompts are superficially similar but contextually different
- Prompt compression that strips whitespace/filler can break structured prompts (e.g., few-shot examples with precise spacing)
- Model routing to cheaper models degrades quality silently — without A/B evaluation, you won't notice regression
- Budget limits block legitimate requests if the daily cap is too aggressive; requires fine-grained tracking per user/tenant
- Redis TTL-based caching does not invalidate on model version changes — stale responses after model updates

## Agentic workflow
A cost-reduction agent runs as a pre-processing layer before any LLM call: check cache → route to cheapest capable model → compress prompt → call API → write cache. Claude subagents can own the routing decision by receiving task metadata (complexity score, required capabilities) and returning a model name. The caching layer and budget guard are best implemented as Python middleware, not inside the agent itself.

### Recommended subagents
- `faion-sdd-execution` — audit existing LLM call sites and score each for caching eligibility and model downgrade potential
- Custom cost-analysis agent — given a list of API call logs, compute per-endpoint cost breakdown and recommend optimizations

### Prompt pattern
```
Given this list of LLM call sites with their average prompt tokens, response tokens,
and call frequency, classify each as: cacheable | model-downgradeable | batch-eligible | none.
Output JSON array: [{endpoint, strategy, estimated_monthly_saving_usd}]
```

```
Compress the following system prompt to under 200 tokens while preserving all behavioral
constraints. Do not remove examples. Mark removed text with [REMOVED].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tiktoken` | Count tokens for OpenAI models before sending | `pip install tiktoken` · github.com/openai/tiktoken |
| `litellm` | Unified API + cost tracking across 100+ providers | `pip install litellm` · litellm.ai |
| `openai` CLI | Batch API, usage stats, file management | `pip install openai` · platform.openai.com/docs/guides/batch |
| `redis-cli` | Inspect/flush response cache in production | Ships with Redis · redis.io |
| `anthropic` | Prompt caching (cache_control) for Claude | `pip install anthropic` · docs.anthropic.com/en/docs/build-with-claude/prompt-caching |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Batch API | SaaS | Yes — async job ID | 50% cost discount; 24h turnaround; ideal for offline pipelines |
| Anthropic Prompt Caching | SaaS | Yes — `cache_control` header | Caches up to 4 system prompt breakpoints; 90% read discount |
| LiteLLM Proxy | OSS | Yes — OpenAI-compatible | Centralizes routing, cost tracking, fallbacks across providers |
| Helicone | SaaS | Yes — proxy layer | Request logging, cost dashboard, caching layer |
| Portkey | SaaS | Yes — gateway | Multi-provider routing, semantic cache, budget alerts |
| Redis | OSS | Yes — Python client | Response cache backend; supports TTL, cluster mode |

## Templates & scripts
See `templates.md` for the `ResponseCache` + `CachedLLMClient` pattern.

Inline: token-count guard before any expensive call:
```python
import tiktoken

def is_within_budget(text: str, model: str = "gpt-4o", max_tokens: int = 4000) -> bool:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text)) <= max_tokens

# Usage: skip expensive model if prompt is too large
if not is_within_budget(prompt, max_tokens=2000):
    model = "gpt-4o-mini"  # fall back to cheaper model
```

## Best practices
- Cache only at temperature=0; use content hash (SHA-256 of model + messages + kwargs) as key
- Set TTL relative to content volatility: static docs → 7 days; user queries → 1-4 hours
- Use Anthropic prompt caching for system prompts >1024 tokens — the 90% read discount is immediate
- Apply OpenAI Batch API for any pipeline that tolerates 24h latency (nightly reports, bulk classification)
- Route by task complexity: pattern-match keywords to select cheap/expensive model, then evaluate quality on a held-out set
- Track cache hit rate per endpoint; below 20% hit rate means the cache key is too specific or TTL too short
- Never compress few-shot examples — the quality loss is disproportionate to the token saving

## AI-agent gotchas
- Caching inside an agentic loop can cause the agent to miss state changes between turns — use turn-scoped (not session-scoped) cache keys or disable cache for tool-call results
- Model routing decisions made by an LLM are circular — use rule-based routing (token count thresholds, task type) not another LLM call
- Budget guards must be checked synchronously before the LLM call, not after; async checks lead to overruns
- Prompt compression applied to agent scratchpad or chain-of-thought steps breaks reasoning — only compress user-facing inputs
- Semantic similarity caches (embedding-based) require a human-in-loop validation step when first deployed; false hit rate is non-obvious

## References
- https://platform.openai.com/docs/guides/batch
- https://platform.openai.com/docs/guides/prompt-caching
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://docs.litellm.ai/docs/proxy/cost_tracking
- https://helicone.ai/docs
- https://github.com/openai/tiktoken
