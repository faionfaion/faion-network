---
id: llm-observability-stack-2026
name: "LLM Observability Stack (2026)"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack (2026)

Comprehensive monitoring for production AI applications: tracing, cost analytics, quality metrics, and performance monitoring.

## Platform Comparison

| Platform | Focus | Self-Host | Pricing |
|----------|-------|-----------|---------|
| Langfuse | Tracing, prompts, evals | Yes (MIT) | Free / $29/mo |
| Helicone | Cost analytics, caching | Yes | Free (10K req) / $79/mo |
| Arize Phoenix | Evaluation, embeddings | Yes | Free / $50/mo managed |
| Braintrust | Multi-agent tracing | No | Enterprise |
| Portkey | Gateway, fallbacks | Limited | Usage-based |
| Weights & Biases | Experiment tracking | No | Free tier / $50+/mo |

## Essential Metrics

| Category | Metrics |
|----------|---------|
| Cost | Token usage, cost/conversation, cache hit rate |
| Quality | Relevance scores, hallucination rate, user feedback |
| Performance | Latency (P50/P95/P99), throughput, TTFT |
| Reliability | Error rate, retry rate, fallback triggers |
| Agent-specific | Tool call success, reasoning steps, iteration count |

## Integration Architecture

```
Application
    |
Observability SDK (OpenTelemetry/OpenInference)
    |
    - Tracing → Langfuse/Phoenix
    - Analytics → Helicone Dashboard
    - Evaluation → Automated quality gates
    - Alerting → Cost/quality thresholds
```

## Langfuse Setup (SDK-based)

```python
from langfuse import Langfuse
from langfuse.decorators import observe

# Initialize
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"
)

# Trace LLM calls
@observe()
def generate_response(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

# Track custom metrics
langfuse.score(
    trace_id="trace-123",
    name="quality",
    value=0.95
)
```

## Helicone Setup (Proxy-based)

```python
from openai import OpenAI

# Change base URL to Helicone proxy
client = OpenAI(
    api_key="your-openai-key",
    base_url="https://oai.hconeai.com/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {helicone_api_key}",
        "Helicone-Cache-Enabled": "true",
        "Helicone-User-Id": "user-123"
    }
)

# All calls automatically tracked
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Arize Phoenix (Evaluation & Embeddings)

```python
import phoenix as px

# Launch Phoenix
session = px.launch_app()

# Track embeddings for RAG
px.log_embeddings(
    embeddings=embeddings,
    metadata={"source": "documents"}
)

# Evaluate responses
from phoenix.evals import OpenAIModel, llm_classify

model = OpenAIModel(model="gpt-4o")

eval_df = llm_classify(
    dataframe=responses_df,
    template="Is this response helpful? Yes or No",
    model=model
)
```

## Key Features by Tool

| Feature | Langfuse | Helicone | Phoenix | Braintrust |
|---------|----------|----------|---------|------------|
| LLM tracing | ✅ | ✅ | ✅ | ✅ |
| Cost analytics | ✅ | ✅ | ❌ | ✅ |
| Prompt versioning | ✅ | ❌ | ❌ | ✅ |
| Caching | ❌ | ✅ | ❌ | ❌ |
| Self-hostable | ✅ | ✅ | ✅ | ❌ |
| Evaluation | ✅ | ❌ | ✅ | ✅ |
| Agent tracing | ✅ | ❌ | ❌ | ✅ |

## Setup Times & ROI

| Tool | Setup Time | Primary Benefit | Cost Savings |
|------|------------|-----------------|--------------|
| Helicone | 15 min | Instant caching, cost tracking | 20-30% (caching) |
| Langfuse | 2-4 hours | Trace analysis, prompt versions | 10-15% (optimization) |
| Phoenix | 1-2 hours | Embedding analysis, quality eval | Quality improvement |

## Best Practices

1. **Start with Helicone** - Quickest setup, immediate cost savings via caching
2. **Add Langfuse** - Deep tracing, prompt management for complex workflows
3. **Use Phoenix** - Evaluation and embedding analysis for RAG apps
4. **Set Alerts** - Cost thresholds, error rates, quality degradation
5. **Version Prompts** - Track changes, A/B test variations
6. **Monitor Continuously** - Dashboard review, anomaly detection

## Common Pitfalls

1. **No Baseline Metrics** - Can't measure improvement without baseline
2. **Ignoring Latency** - P95/P99 matter more than average
3. **Over-reliance on Cost** - Quality metrics are equally important
4. **No User Feedback Loop** - Automated metrics miss user satisfaction
5. **Alert Fatigue** - Too many alerts = ignored alerts

## Sources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Helicone Documentation](https://docs.helicone.ai)
- [Arize Phoenix](https://docs.arize.com/phoenix)
- [Braintrust AI](https://www.braintrust.dev/docs)
- [OpenTelemetry for LLMs](https://opentelemetry.io/docs/languages/python/)
