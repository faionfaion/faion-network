# LLM Decision Framework

Decision framework for LLM architecture: prompting vs RAG vs fine-tuning.

## Overview

This framework provides systematic guidance for selecting the optimal LLM enhancement strategy based on requirements, constraints, and ROI.

## Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Framework overview |
| [checklist.md](checklist.md) | Decision checklist |
| [examples.md](examples.md) | Real-world examples |
| [templates.md](templates.md) | Architecture templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for decisions |

## Decision Hierarchy

```
Prompt Engineering (baseline)
    |
    v
Structured Output (format control)
    |
    v
RAG (external knowledge)
    |
    v
Fine-tuning (specialized behavior)
    |
    v
RAFT (hybrid: fine-tuning + RAG)
```

## Quick Decision Matrix

| Need | Solution | Complexity | Cost |
|------|----------|------------|------|
| Better instructions | Prompt engineering | Low | Per-token |
| Consistent JSON output | Structured output | Low | Per-token |
| Real-time/private data | RAG | Medium | Infrastructure + tokens |
| Domain expertise | Fine-tuning | High | Training + higher inference |
| Both knowledge + expertise | RAFT (hybrid) | Very High | Full stack |

## Cost Comparison (2026)

| Approach | Setup | Ongoing | Deploy Time |
|----------|-------|---------|-------------|
| Prompting | $0 | $0.01-0.10/1K tokens | Hours |
| Structured Output | $0 | +10-20% tokens | Hours |
| RAG | $500-5K | $100-2K/month | Days-Weeks |
| Fine-tuning | $1K-50K | 2-6x inference cost | Weeks-Months |
| RAFT (hybrid) | $5K-100K | Full infrastructure | Months |

## When to Use What

### Prompt Engineering

- **Use when:** Improving instruction clarity, few-shot examples suffice
- **Avoid when:** Need real-time data, specialized domain knowledge
- **ROI:** Highest (nearly free, immediate results)

### RAG (Retrieval-Augmented Generation)

- **Use when:** Dynamic data, organizational knowledge, citations needed
- **Avoid when:** Static knowledge sufficient, latency-critical, offline required
- **ROI:** High for knowledge-intensive applications

### Fine-tuning

- **Use when:** Consistent style/format, domain-specific language, cost reduction at scale
- **Avoid when:** Data changes frequently, small scale, general-purpose use
- **ROI:** High at scale, low for small deployments

### RAFT (Retrieval-Augmented Fine-Tuning)

- **Use when:** Need both domain expertise AND dynamic knowledge
- **Avoid when:** Simpler approaches work, limited budget/expertise
- **ROI:** Highest accuracy, highest investment

## Key Metrics for Decision

| Metric | Description | Target |
|--------|-------------|--------|
| Accuracy | Factual correctness | >95% for production |
| Latency | Response time | <2s for user-facing |
| Cost per query | Total inference cost | <$0.01 for high-volume |
| Freshness | Data currency | Real-time for RAG, static for fine-tuning |
| Hallucination rate | False information | <1% for critical apps |

## Related

- [decision-framework/](../decision-framework/README.md) - General ML decision framework
- [cost-optimization/](../cost-optimization/README.md) - Cost optimization strategies
- [finetuning/](../finetuning/README.md) - Fine-tuning implementation
- [vector-databases/](../vector-databases/README.md) - RAG infrastructure


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Model selection framework | sonnet | Decision criteria |
| Cost-quality trade-off | sonnet | Analysis |
| Provider comparison | sonnet | Evaluation |

## Sources

- [RAG vs Fine-Tuning - Monte Carlo](https://www.montecarlodata.com/blog-rag-vs-fine-tuning/)
- [RAG vs Fine-Tuning - Oracle](https://www.oracle.com/artificial-intelligence/generative-ai/retrieval-augmented-generation-rag/rag-fine-tuning/)
- [Fine-Tuning vs RAG 2025 - orq.ai](https://orq.ai/blog/finetuning-vs-rag)
- [RAG vs Fine-Tuning 2026 - Kanerika](https://kanerika.com/blogs/rag-vs-fine-tuning/)
- [RAG vs LLM Fine-Tuning - Elephas](https://elephas.app/blog/rag-vs-llm-fine-tuning)

---

*LLM Decision Framework v2.0 - Updated January 2026*
