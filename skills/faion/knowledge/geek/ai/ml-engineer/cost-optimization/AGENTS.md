# LLM Cost Optimization

## Summary

LLM costs can be reduced 60-90% through model routing (50-75% savings), prompt caching (80-90% on repeated system prompts), response caching (70-95% for deterministic queries), token reduction (20-40%), and Batch API (50% discount on async workloads). Track cost per pipeline stage from day 1 — you cannot optimize what you cannot attribute. Optimize only after measuring; premature optimization wastes time.

## Why

LLM costs scale super-linearly in production: each agent turn, each pipeline stage, each user query multiplies. Output tokens cost 3-5x more than input tokens. Without model routing, every request goes to the most expensive model by default. Without prompt caching, the same 2K-token system prompt is billed repeatedly. Budget runaway is possible within hours on high-traffic agentic pipelines.

## When To Use

- Monthly LLM spend exceeds $500 and is growing faster than revenue
- Agentic pipelines with &gt;10K requests/day where model selection matters
- Batch workloads with &gt;1h latency tolerance (Batch API = 50% off)
- System prompts &gt;1K tokens (OpenAI) or &gt;2K tokens (Claude) that repeat across many calls
- Multi-step pipelines where early stages can use cheap models for routing

## When NOT To Use

- Early prototype phase — optimize only after measuring
- Tasks where quality degradation from cheaper models is unacceptable (medical, legal, safety-critical)
- Very low volume (&lt;100 calls/day) — savings are negligible, complexity is not worth it
- When the cost driver is output tokens on complex reasoning tasks — only better prompts help, not routing

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Five cost reduction strategies with savings estimates, mechanisms, and trade-offs |
| `content/02-rules.xml` | Concrete rules, budget controls, caching pitfalls, monitoring requirements |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-router.py` | Complexity-based model router (Haiku → Sonnet → Opus) |
| `templates/token-budget.py` | Per-call token cost tracking with daily budget enforcement |
| `templates/prompt-cache-claude.py` | Claude prompt caching with cache_control header |
