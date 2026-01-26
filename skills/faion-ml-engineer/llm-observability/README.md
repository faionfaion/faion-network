---
id: llm-observability
name: "LLM Observability and Monitoring"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability and Monitoring

## Overview

LLM observability is the practice of tracing, monitoring, evaluating, and debugging LLM applications in production. Unlike traditional APM, LLM observability focuses on output quality, cost tracking, and prompt effectiveness.

**Key Challenge:** LLM applications are non-deterministic - they don't always behave the same way, making them difficult to debug and optimize without proper observability.

## Why LLM Observability Matters

| Traditional Monitoring | LLM Observability |
|------------------------|-------------------|
| System health (CPU, memory) | Output quality (relevance, accuracy) |
| Uptime metrics | Token usage and costs |
| Error rates | Hallucination detection |
| Latency only | TTFT + full latency |

## Core Concepts

### Tracing Data Model

```
Session (conversation)
  └── Trace (single request journey)
        ├── Span (unit of work)
        │     └── Span (nested operation)
        ├── Generation (LLM call: input → output)
        ├── Embedding (vector generation)
        └── Retrieval (RAG context fetch)
```

| Concept | Description |
|---------|-------------|
| **Trace** | Complete execution path of a request through the application |
| **Span** | Unit of work within a trace (function call, API request) |
| **Generation** | LLM call with input prompt, output response, token usage |
| **Embedding** | Vector embedding generation operation |
| **Session** | Group of traces belonging to same conversation/user |

### Key Metrics

| Category | Metrics |
|----------|---------|
| **Cost** | Tokens/request, $/conversation, budget tracking, cost by user/team |
| **Quality** | Response relevance, hallucination rate, user satisfaction, coherence |
| **Performance** | Latency (P50, P95, P99), TTFT (Time to First Token), throughput |
| **Reliability** | Error rate, retry rate, fallback frequency, timeout rate |

## Platform Comparison (2025-2026)

| Platform | Type | Best For | Key Strength |
|----------|------|----------|--------------|
| **Langfuse** | Open Source | Self-hosted, full control | MIT license, 19k+ GitHub stars |
| **LangSmith** | SaaS/Self-hosted | LangChain/LangGraph users | Deep LangChain integration |
| **Helicone** | Proxy-based | Cost optimization | 1-line integration, caching |
| **Portkey** | AI Gateway | Multi-provider routing | 250+ models, failover |
| **Arize Phoenix** | Open Source | Embeddings, evaluation | Drift detection |
| **LangWatch** | Open Source | Quick integration | Single env var setup |
| **Braintrust** | SaaS | CI/CD integration | Unified PM/eng workflow |

### Platform Selection Guide

```
Need self-hosting?
├── YES → Langfuse (MIT, no restrictions)
└── NO
    ├── Using LangChain/LangGraph? → LangSmith
    ├── Cost optimization priority? → Helicone
    ├── Multi-provider routing? → Portkey
    └── General purpose → Langfuse Cloud or Helicone
```

## Observability Stack Architecture

```
Application Layer
       │
       ▼
┌─────────────────────────────────────────┐
│           Observability Layer           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ Tracing │  │  Evals  │  │  Costs  │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
│       └───────────┬┴───────────┘        │
│                   ▼                      │
│  ┌─────────────────────────────────┐    │
│  │         Prompt Registry         │    │
│  │    (Version Control + A/B)      │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│           Dashboard + Alerts            │
└─────────────────────────────────────────┘
```

## 2025-2026 Trends

| Trend | Description |
|-------|-------------|
| **Agent Tracing** | Multi-step agent workflows (LangGraph, AutoGen) with nested spans |
| **Tool Use Observability** | Tracking structured outputs, function calls, tool invocations |
| **OpenTelemetry Native** | OTEL-based SDKs for seamless integration with existing stacks |
| **LLM-as-Judge Tracing** | Debug evaluation prompts, trace evaluator LLM calls |
| **Multimodal Tracking** | Vision, audio, and video modality observability |
| **Real-time Guardrails** | Online evaluation for safety, PII, format validation |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts (this file) |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (Langfuse, LangSmith, Helicone) |
| [templates.md](templates.md) | Config templates and dashboards |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-as-judge evaluation |

## Quick Start

1. **Choose platform** based on requirements (see Platform Selection Guide)
2. **Integrate SDK** (usually 1-5 lines of code)
3. **Configure tracing** for all LLM calls
4. **Set up cost alerts** to avoid budget overruns
5. **Add quality evaluations** (LLM-as-judge or custom)
6. **Create dashboards** for key metrics

## Related Methodologies

- [llm-apis.md](../methodologies/llm-apis.md) - LLM API integration patterns
- [prompt-engineering.md](../methodologies/prompt-engineering.md) - Prompt versioning
- [cost-optimization.md](../methodologies/cost-optimization.md) - Cost reduction strategies

## Sources

- [Langfuse Documentation](https://langfuse.com/docs)
- [LangSmith Documentation](https://docs.langchain.com/langsmith)
- [Helicone Blog](https://www.helicone.ai/blog)
- [Portkey Documentation](https://portkey.ai/docs)
- [Best LLM Observability Tools 2025](https://www.firecrawl.dev/blog/best-llm-observability-tools)
