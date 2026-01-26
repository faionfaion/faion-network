---
id: llm-observability-stack
name: "LLM Observability Stack (2026)"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack (2026)

## Overview

Production AI systems require comprehensive monitoring that goes beyond traditional APM. This methodology covers the complete observability stack: tracing, cost analytics, quality evaluation, and alerting - with emphasis on monitoring stack components and integration patterns.

**Key Insight:** Up to 84% of observability users struggle with costs and complexity. The solution is consolidation and OpenTelemetry-based standards.

## Why LLM Observability Requires a New Stack

| Traditional Monitoring | LLM Observability Stack |
|------------------------|-------------------------|
| CPU, memory, uptime | Token usage, cost per conversation |
| Error rates | Hallucination rate, quality scores |
| Latency only | TTFT, throughput, P50/P95/P99 |
| Static metrics | Non-deterministic output evaluation |
| Single-request scope | Multi-turn conversation tracking |

## Core Stack Components

```
Application Layer
       |
       v
+------------------------------------------+
|        Observability SDK Layer           |
|  (OpenTelemetry / OpenLLMetry / Native)  |
+------------------------------------------+
       |
       +-----> Tracing Platform (Langfuse/Phoenix/LangSmith)
       |
       +-----> Analytics Gateway (Helicone/Portkey)
       |
       +-----> Evaluation System (LLM-as-Judge)
       |
       +-----> Alerting (Prometheus/Grafana/PagerDuty)
       |
       v
+------------------------------------------+
|        Unified Dashboard Layer           |
|     (Cost, Quality, Performance)         |
+------------------------------------------+
```

## Platform Comparison (2026)

| Platform | Type | Focus | Self-Host | Pricing | Best For |
|----------|------|-------|-----------|---------|----------|
| **Langfuse** | Open Source | Tracing, prompts, evals | Yes (MIT) | Free / $29/mo | Full control, privacy |
| **LangSmith** | SaaS | Agent debugging | Limited | Free tier + usage | LangChain users |
| **Helicone** | Proxy | Cost analytics, caching | Yes | Free (10K) / $79/mo | Cost optimization |
| **Arize Phoenix** | Open Source | Evaluation, embeddings | Yes | Free / $50/mo | ML teams |
| **Portkey** | AI Gateway | Multi-provider routing | Limited | Usage-based | Multi-model apps |
| **OpenLLMetry** | Open Source | OTEL integration | Yes | Free | Existing APM users |
| **Datadog LLM** | Enterprise | Full-stack APM | No | Usage-based | Enterprise |
| **Braintrust** | SaaS | Multi-agent tracing | No | Enterprise | Complex agents |
| **Traceloop** | Platform | OTEL-native | Limited | Free tier | Production scale |

## Essential Metrics

| Category | Metrics | Tools |
|----------|---------|-------|
| **Cost** | Token usage, $/conversation, cache hit rate, cost by user/team | Helicone, Portkey, Langfuse |
| **Quality** | Relevance scores, hallucination rate, user feedback, safety scores | Phoenix, Langfuse, Braintrust |
| **Performance** | Latency (P50/P95/P99), TTFT, throughput, queue depth | All platforms |
| **Reliability** | Error rate, retry rate, fallback triggers, timeout rate | Helicone, Portkey |
| **Agent-specific** | Tool call success, reasoning steps, iteration count, loop detection | LangSmith, Phoenix |

## OpenTelemetry Integration

OpenTelemetry is emerging as the standard for LLM observability (2025-2026):

```
OpenTelemetry Collector
       |
       +----> Langfuse (via OTEL exporter)
       +----> Datadog
       +----> Honeycomb
       +----> Grafana/Tempo
       +----> New Relic
       +----> SigNoz
```

**OpenLLMetry:** 6.6k+ stars, supports 23+ backends, Apache 2.0 license.

## 2026 Trends

| Trend | Description | Impact |
|-------|-------------|--------|
| **Agent Tracing** | Multi-step workflows (LangGraph, AutoGen) with nested spans | Required for agentic AI |
| **OTEL-Native** | OpenTelemetry-based SDKs for unified observability | Vendor consolidation |
| **Real-time Guardrails** | Online evaluation for safety, PII, format validation | Production safety |
| **LLM-as-Judge Tracing** | Debug evaluation prompts, trace evaluator calls | Quality debugging |
| **Multimodal Tracking** | Vision, audio, video modality observability | Expanding use cases |
| **Cost Optimization** | Smart caching, semantic routing, model fallbacks | 20-40% savings |

## Stack Selection Decision Tree

```
Start
  |
  v
Need self-hosting (privacy/compliance)?
  |
  +-- YES --> Langfuse (MIT) or Phoenix
  |
  +-- NO
        |
        v
      Using LangChain/LangGraph?
        |
        +-- YES --> LangSmith
        |
        +-- NO
              |
              v
            Primary goal?
              |
              +-- Cost optimization --> Helicone
              |
              +-- Multi-provider routing --> Portkey
              |
              +-- Existing APM integration --> OpenLLMetry
              |
              +-- General purpose --> Langfuse Cloud
```

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and stack architecture (this file) |
| [checklist.md](checklist.md) | Stack setup and integration checklist |
| [examples.md](examples.md) | Integration code examples |
| [templates.md](templates.md) | Config templates, docker-compose, alerts |
| [llm-prompts.md](llm-prompts.md) | Prompts for stack evaluation and debugging |

## Quick Start

1. **Choose primary platform** based on decision tree above
2. **Install SDK** (usually 1-5 lines of code)
3. **Configure OpenTelemetry** for unified tracing
4. **Set up cost tracking** with Helicone or Portkey
5. **Add quality evaluations** (LLM-as-judge)
6. **Create alerting rules** for cost/quality thresholds
7. **Build unified dashboard** (Grafana or platform-native)

## Related Methodologies

- [llm-observability/](../llm-observability/README.md) - General observability concepts
- [cost-optimization/](../cost-optimization/README.md) - Cost reduction strategies
- [model-evaluation/](../model-evaluation/README.md) - Quality evaluation frameworks

## Sources

- [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)
- [OpenLLMetry GitHub](https://github.com/traceloop/openllmetry)
- [LLM Observability Tools 2026](https://lakefs.io/blog/llm-observability-tools/)
- [Best LLM Observability Tools 2025](https://logz.io/blog/top-llm-observability-tools/)
- [OpenTelemetry and Observability 2026](https://thenewstack.io/can-opentelemetry-save-observability-in-2026/)
- [LLM Observability Best Practices 2025](https://www.getmaxim.ai/articles/llm-observability-best-practices-for-2025/)
