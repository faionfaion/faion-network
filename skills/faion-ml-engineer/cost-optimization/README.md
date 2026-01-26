---
id: cost-optimization
name: "Cost Optimization"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
version: "2.0.0"
updated: "2025-01"
---

# LLM Cost Optimization

> **Entry point:** `/faion-net` - invoke for automatic routing.

Comprehensive guide to reducing LLM API costs by 60-90% while maintaining quality.

## Overview

LLM costs can escalate rapidly in production. Strategic optimization through model selection, caching, token reduction, and batching achieves 60-80% cost reduction without quality compromise. Research shows potential savings up to 98%.

## Cost Reduction Potential

| Strategy | Typical Savings | Complexity |
|----------|-----------------|------------|
| Model routing | 50-75% | Low |
| Prompt caching | 80-90% | Medium |
| Token optimization | 20-40% | Low |
| Batch processing | 40-50% | Medium |
| Response caching | 70-95% | Medium |
| Combined approach | 60-90% | High |

## Cost Components

| Component | Impact | Optimization Lever |
|-----------|--------|-------------------|
| Model selection | 10-100x | Route to cheaper models |
| Input tokens | Linear | Compress prompts, cache prefixes |
| Output tokens | 3-5x input | Limit response length |
| API calls | Fixed overhead | Cache responses, batch |
| Latency | Indirect | Async, parallel processing |

## Model Pricing (2025)

| Model | Input/1M | Output/1M | Context | Best For |
|-------|----------|-----------|---------|----------|
| GPT-4.1 | $2.00 | $8.00 | 1M | Complex reasoning |
| GPT-4.1-mini | $0.40 | $1.60 | 1M | General tasks |
| GPT-4.1-nano | $0.10 | $0.40 | 1M | Simple tasks |
| Claude 4 Opus | $15.00 | $75.00 | 200K | Research, analysis |
| Claude 4 Sonnet | $3.00 | $15.00 | 200K | Balanced quality/cost |
| Claude 3.5 Haiku | $0.80 | $4.00 | 200K | Fast, efficient |
| Gemini 2.0 Pro | $1.25 | $5.00 | 2M | Long context |
| Gemini 2.0 Flash | $0.10 | $0.40 | 1M | Speed, cost |
| o3-mini | $1.10 | $4.40 | 200K | Reasoning |

**Batch API Discounts:**
- OpenAI Batch: 50% off
- Google Batch: 50% off
- Mistral Batch: 50% off

## Quick Start

### 1. Implement Model Routing

```python
# Route 80% to cheap model, 20% to premium
# Results: 75% cost reduction vs all-premium
router = ModelRouter()
model = router.get_model(prompt)  # Auto-selects by complexity
```

### 2. Enable Prompt Caching

```python
# Cache static system prompts
# Results: 80-90% input cost reduction
cache = PromptCache(ttl_hours=24)
response = cached_client.complete(prompt, use_cache=True)
```

### 3. Optimize Tokens

```python
# Compress prompts, limit outputs
# Results: 20-40% token reduction
optimized = optimizer.compress_prompt(prompt)
```

### 4. Batch Requests

```python
# Use async batch processing
# Results: 40-50% cost reduction
results = await batch_processor.process(prompts, model="gpt-4.1-mini")
```

## Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Production code examples |
| [templates.md](templates.md) | Ready-to-use components |
| [llm-prompts.md](llm-prompts.md) | Analysis & optimization prompts |

## Key Strategies

### Tiered Model Routing

Use small models for classification/extraction, mid-tier for general queries, frontier models only for complex tasks:

| Tier | Model | Use Case |
|------|-------|----------|
| Classifier | gpt-4.1-nano | Intent detection, routing |
| Standard | gpt-4.1-mini | Most queries |
| Premium | gpt-4.1 / claude-4-sonnet | Complex reasoning |

### Caching Hierarchy

1. **Response cache** - Exact match for deterministic queries (temperature=0)
2. **Semantic cache** - Similar queries via embeddings
3. **Prompt cache** - Reuse system prompts, static context
4. **KV cache** - Provider-level attention caching

### Token Reduction

1. Remove verbose phrases ("please", "kindly", "I would like")
2. Use structured outputs (JSON) over free-form
3. Limit max_tokens parameter
4. Summarize long context with cheap model first
5. Use sliding window for conversation history

### Batching Best Practices

1. Group similar requests for better GPU utilization
2. Use continuous batching to avoid padding overhead
3. Optimal batch size: 32-64 (test for your workload)
4. Use async APIs for parallel processing
5. Consider Batch APIs for 50% discount on latency-tolerant jobs

## Budget Controls

| Control | Implementation |
|---------|----------------|
| Daily limits | Hard cap per day |
| Per-request limits | Max tokens, timeout |
| Alerts | Threshold notifications |
| Kill switch | Disable non-critical calls |
| Rate limiting | Requests per minute |

## Monitoring Metrics

| Metric | Purpose |
|--------|---------|
| Cost per request | Track average spend |
| Cost per feature | Allocate by product area |
| Cache hit rate | Measure caching effectiveness |
| Token efficiency | Input/output ratio |
| Model distribution | Routing effectiveness |

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Over-caching | Set appropriate TTLs, invalidate on data changes |
| Wrong model tier | Use complexity-based routing |
| No monitoring | Track cost per endpoint from day 1 |
| Ignoring output costs | Output tokens cost 3-5x more |
| No budget limits | Set hard caps before production |
| Premature optimization | Start simple, optimize with data |

## References

- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Google AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [tiktoken Library](https://github.com/openai/tiktoken)

## Research Sources

- [LLM Cost Optimization: Complete Guide](https://ai.koombea.com/blog/llm-cost-optimization)
- [Reduce LLM Costs: Token Optimization](https://www.glukhov.org/post/2025/11/cost-effective-llm-applications/)
- [LLM Inference Optimization](https://deepsense.ai/blog/llm-inference-optimization-how-to-speed-up-cut-costs-and-scale-ai-models/)
- [Scaling LLMs with Batch Processing](https://latitude-blog.ghost.io/blog/scaling-llms-with-batch-processing-ultimate-guide/)
- [Reducing Latency and Costs in Agentic AI](https://georgian.io/reduce-llm-costs-and-latency-guide/)
