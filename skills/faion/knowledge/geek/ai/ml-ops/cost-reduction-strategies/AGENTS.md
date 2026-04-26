# Cost Reduction Strategies

## Summary

Production LLM cost optimization through four orthogonal techniques: response caching (SHA-256 content hash key, Redis or in-memory TTL), prompt compression (whitespace normalization, redundant phrase removal), async batching, and model routing (default cheap model with fallback). The `CostOptimizedLLM` class composes all four into a single production-ready service layer.

## Why

LLM API cost scales linearly with request volume. At >1000 calls/day the bill becomes significant, and most workloads have substantial caching potential (deterministic outputs at temperature=0). Combining caching, compression, and routing can cut costs 50-80% without degrading output quality for the right task types.

## When To Use

- Production apps with >1000 LLM API calls/day where API costs are a significant budget line
- Budget-constrained projects that need to scale without proportional cost increase
- Multi-tenant SaaS where per-request costs must be predictable and per-user bounded
- Batch classification, extraction, or summarization pipelines at scale

## When NOT To Use

- Low-volume prototypes — premature optimization adds complexity with no payoff
- Tasks requiring temperature > 0 (non-deterministic outputs) — caching is ineffective and misleading
- Latency-critical real-time systems where Redis cache lookup adds unacceptable overhead
- Workflows where output freshness is mandatory (live data, personalized real-time responses)
- Agentic loops — caching inside a loop can cause the agent to miss state changes between turns

## Content

| File | What's inside |
|------|---------------|
| `content/01-caching.xml` | `ResponseCache` design, key construction, TTL strategy, Redis vs. in-memory tradeoffs |
| `content/02-prompt-optimization.xml` | `PromptOptimizer`: token counting, compression, system prompt tightening, context summarization |
| `content/03-routing-batching.xml` | Model routing rules, `BatchProcessor` async pattern, Anthropic prompt caching, OpenAI Batch API |

## Templates

| File | Purpose |
|------|---------|
| `templates/response-cache.py` | `ResponseCache` + `CachedLLMClient` with Redis + memory-fallback (~60 lines) |
| `templates/cost-analysis-prompt.txt` | Prompt for classifying LLM call sites as cacheable/downgradeable/batch-eligible |
