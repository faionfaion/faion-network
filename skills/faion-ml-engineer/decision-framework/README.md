# Decision Framework

> ML/AI approach and model selection decision framework.

## Overview

When building AI applications, the key decisions are:
1. **Approach Selection** - Prompting vs RAG vs Fine-tuning
2. **Model Selection** - Which LLM provider and model tier
3. **Cost Optimization** - Balancing performance and budget

## Progressive Enhancement Strategy

```
Start: Prompt Engineering ($0, hours)
         |
         v
Need external/private data? --> RAG ($70-1000/mo)
         |
         v
Need specialized behavior? --> Fine-tuning (6x inference cost)
         |
         v
High volume optimization? --> Smaller model + fine-tuning
```

## Approach Decision Matrix

| Need | Solution | Setup | Ongoing |
|------|----------|-------|---------|
| Better instructions | Prompt engineering | Low | Per-token |
| Real-time/private data | RAG | Medium | Infra + tokens |
| Specific output format | Structured output | Low | Per-token |
| Domain expertise | Fine-tuning | High | Higher per-token |
| Cost reduction at scale | Smaller model + fine-tuning | High | Lower per-token |

## Model Selection (2025-2026)

### Multi-Model Strategy

Modern AI systems use 2-3 models with intelligent routing:

| Use Case | Recommended Model |
|----------|-------------------|
| User-facing interactions | GPT-4o, GPT-5.2 |
| Complex reasoning, code | Claude Opus 4.5, Sonnet 4 |
| Multimodal, long context | Gemini 2 Pro, 3 Pro |
| High-volume processing | DeepSeek, Llama 3.x |
| Privacy-sensitive | Self-hosted open source |

### Cost Comparison (per 1M tokens, Jan 2026)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| GPT-4o | $2.50 | $10.00 | General purpose |
| GPT-5.2 | $5.00 | $20.00 | Complex tasks |
| Claude Opus 4.5 | $15.00 | $75.00 | Deep reasoning |
| Claude Sonnet 4 | $3.00 | $15.00 | Code, analysis |
| Gemini 2 Pro | $3.50 | $10.50 | Multimodal |
| DeepSeek V3 | $0.14 | $0.28 | High volume |

### Latency Comparison

| Model | Tokens/sec | Response Time (500 tokens) |
|-------|------------|---------------------------|
| GPT-5.2 | ~180 tok/s | ~2.8s |
| Claude Sonnet 4 | ~120 tok/s | ~4.2s |
| Claude Opus 4.5 | ~50 tok/s | ~10s |
| DeepSeek V3 | ~100 tok/s | ~5s |

## Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Decision checklist for model/approach selection |
| [examples.md](examples.md) | Real-world selection scenarios |
| [templates.md](templates.md) | Decision document templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for model evaluation |

## Key Insights

### From Industry Research

1. **Match model to task complexity** - Using GPT-5.2 for simple tasks = 2-3x overspending
2. **Calculate total cost** - Include API + developer fix-time + prompt engineering
3. **Model routing saves 40-60%** - Route simple tasks to DeepSeek, critical to Claude
4. **Latency matters for UX** - 3-4x speed difference between models
5. **Price your mistakes** - "How much is an error worth?" drives model choice

### Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Defaulting to GPT | 2-3x overspend on simple tasks | Match model to complexity |
| Comparing only API pricing | 40-60% cost underestimate | Include total ownership cost |
| Single model for all tasks | Suboptimal cost/performance | Implement model routing |
| Ignoring latency | Poor user experience | Factor speed into selection |

## Related

- [llm-decision-framework.md](../llm-decision-framework.md) - Detailed provider comparison
- [cost-optimization/](../cost-optimization/README.md) - Cost optimization strategies
- [model-evaluation/](../model-evaluation/README.md) - Evaluation frameworks

## Sources

- [LLM Model Comparison Guide 2025](https://www.helicone.ai/blog/the-complete-llm-model-comparison-guide)
- [LLM System Design and Model Selection](https://www.oreilly.com/radar/llm-system-design-and-model-selection/)
- [Open vs Closed LLMs 2025](https://medium.com/data-science-collective/open-vs-closed-llms-in-2025-strategic-tradeoffs-for-enterprise-ai-668af30bffa0)
- [How to Choose the Right LLM](https://marutitech.com/how-to-choose-right-llm/)
- [Beyond the Pareto Frontier](https://cognaptus.com/blog/2025-07-08-beyond-the-pareto-frontier-pricing-llm-mistakes-in-the-real-world/)
