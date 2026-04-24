# Cost Optimization Checklist

Pre-production and ongoing optimization checklist for LLM applications.

## Pre-Launch Checklist

### Model Selection

- [ ] Benchmark task with multiple models to find cheapest acceptable
- [ ] Implement tiered routing (classifier → standard → premium)
- [ ] Configure fallback chain for failures
- [ ] Test with mini/nano models first before scaling up
- [ ] Document model selection rationale

### Token Optimization

- [ ] Audit prompts for verbosity (remove "please", "kindly", etc.)
- [ ] Implement prompt compression utility
- [ ] Set explicit max_tokens limits
- [ ] Use structured outputs (JSON) where possible
- [ ] Implement sliding window for conversation history
- [ ] Tokenize and measure all prompts pre-deployment

### Caching

- [ ] Implement response cache for deterministic queries (temp=0)
- [ ] Enable provider prompt caching (Claude, OpenAI)
- [ ] Cache system prompts and static context
- [ ] Set appropriate TTLs based on data freshness needs
- [ ] Implement cache invalidation strategy
- [ ] Consider semantic caching for similar queries

### Batching

- [ ] Identify latency-tolerant workloads for batch APIs
- [ ] Implement async batch processor
- [ ] Configure optimal batch size (test 32-64)
- [ ] Enable continuous batching for variable-length inputs
- [ ] Use provider Batch APIs (50% discount)

### Budget Controls

- [ ] Set daily/monthly budget limits
- [ ] Implement per-request cost tracking
- [ ] Configure budget alerts (50%, 80%, 100%)
- [ ] Create emergency kill switch
- [ ] Set rate limits per endpoint/user

### Monitoring

- [ ] Track cost per request
- [ ] Track cost per feature/endpoint
- [ ] Monitor cache hit rates
- [ ] Alert on cost anomalies
- [ ] Dashboard for real-time visibility

## Weekly Optimization Review

- [ ] Review cost breakdown by model
- [ ] Identify high-cost endpoints
- [ ] Check cache hit rates (target: >60%)
- [ ] Analyze token usage patterns
- [ ] Review routing effectiveness
- [ ] Update model selection based on new releases
- [ ] Test cheaper models for stable workloads

## Monthly Cost Audit

- [ ] Full cost analysis by feature
- [ ] Compare actual vs. budgeted spend
- [ ] Evaluate new model pricing
- [ ] Review batch vs. real-time split
- [ ] Assess caching strategy effectiveness
- [ ] Plan optimization improvements
- [ ] Update budget forecasts

## Red Flags

| Issue | Immediate Action |
|-------|------------------|
| Cost spike >50% | Check for loops, missing cache |
| Cache hit <30% | Review cache key strategy |
| Premium model >30% | Adjust routing thresholds |
| Output tokens > input | Review prompt design |
| No fallback triggers | Test error handling |

## Quick Wins

| Optimization | Typical Savings | Effort |
|--------------|-----------------|--------|
| Set max_tokens | 10-20% | 5 min |
| Enable prompt caching | 30-50% | 30 min |
| Route to mini models | 50-75% | 2 hours |
| Batch API for async jobs | 50% | 4 hours |
| Response caching | 70-90% | 4 hours |

## Cost Estimation Formula

```
Monthly Cost =
  (input_tokens / 1M) * input_price +
  (output_tokens / 1M) * output_price *
  (1 - cache_hit_rate) *
  monthly_requests
```

Example for 1M requests/month, 1K tokens avg:
- GPT-4.1: $2 + $8 = $10/M tokens → $10,000/month (no cache)
- GPT-4.1-mini: $0.4 + $1.6 = $2/M → $2,000/month
- With 70% cache: $2,000 * 0.3 = $600/month
