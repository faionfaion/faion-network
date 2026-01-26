# LLM Fine-tuning Guide

> **Entry point:** `/faion-net` - invoke for automatic routing.

Comprehensive guide to fine-tuning large language models (2025-2026).

## When to Fine-tune vs. Alternatives

### Decision Framework

```
Start here
    |
    v
Can prompting solve the problem?
    |
    +-- YES --> Use prompt engineering (cheaper, faster)
    |
    +-- NO --> Continue
            |
            v
        Can RAG provide necessary context?
            |
            +-- YES --> Use RAG (real-time data, no training)
            |
            +-- NO --> Continue
                    |
                    v
                Do you have quality labeled data?
                    |
                    +-- NO --> Collect data first
                    |
                    +-- YES --> Fine-tuning is appropriate
```

### When to Fine-tune

| Scenario | Recommendation |
|----------|----------------|
| **Domain-specific terminology** | Fine-tune for consistent jargon |
| **Specific output format** | Fine-tune for structured outputs |
| **Task specialization** | Fine-tune for narrow deep expertise |
| **Style/tone consistency** | Fine-tune for brand voice |
| **Reduce prompt length** | Fine-tune to internalize instructions |
| **Improve reliability** | Fine-tune for consistent behavior |

### When NOT to Fine-tune

| Scenario | Better Alternative |
|----------|-------------------|
| Need current information | RAG |
| Exploratory/changing requirements | Prompt engineering |
| Limited data (<50 examples) | Few-shot prompting |
| Need explainability | RAG with citations |
| Broad general knowledge | Base model + prompting |

## Technique Comparison

| Technique | GPU Memory | Speed | Quality | Use Case |
|-----------|------------|-------|---------|----------|
| **Full FT** | 80GB+ | Slow | Best | Large budgets, critical tasks |
| **LoRA** | 16-24GB | Fast | Good | Most production cases |
| **QLoRA** | 8-12GB | Medium | Good | Consumer GPUs, prototyping |
| **DoRA** | 16-24GB | Fast | Better | LoRA successor (2024+) |
| **OpenAI FT** | N/A | Fast | Good | API-only workflows |

## Framework Comparison (2025-2026)

| Framework | Best For | Key Advantage |
|-----------|----------|---------------|
| **Unsloth** | Limited GPU resources | 2-5x faster, 80% less memory |
| **LLaMA-Factory** | Beginners, WebUI | User-friendly interface |
| **Axolotl** | Complex scenarios | Advanced configuration |
| **Torchtune** | PyTorch native | Clean, extensible design |
| **TRL** | Alignment (DPO/ORPO) | Hugging Face integration |

## Files in This Directory

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and decision framework |
| [checklist.md](checklist.md) | Step-by-step fine-tuning checklist |
| [examples.md](examples.md) | Code examples for all major frameworks |
| [templates.md](templates.md) | Configuration templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for fine-tuning tasks |

## Quick Start Path

1. **Decide** - Use decision framework above
2. **Prepare Data** - Follow [checklist.md](checklist.md) data section
3. **Choose Framework** - Based on GPU and requirements
4. **Configure** - Use [templates.md](templates.md)
5. **Train** - Follow [examples.md](examples.md)
6. **Evaluate** - Use metrics from checklist

## Key Metrics

| Metric | Purpose | Target |
|--------|---------|--------|
| **Training Loss** | Model learning | Decreasing, not zero |
| **Validation Loss** | Generalization | Lower than training |
| **Perplexity** | Output quality | Task-dependent |
| **Task-specific** | Accuracy, F1, BLEU | Domain-dependent |

## Related Documentation

| Resource | Link |
|----------|------|
| ML Ops Overview | [../faion-ml-ops/CLAUDE.md](../faion-ml-ops/CLAUDE.md) |
| LLM Integration | [../faion-llm-integration/CLAUDE.md](../faion-llm-integration/CLAUDE.md) |
| RAG Pipeline | [../faion-rag-engineer/CLAUDE.md](../faion-rag-engineer/CLAUDE.md) |

## External References

- [Hugging Face PEFT](https://huggingface.co/docs/peft)
- [TRL Documentation](https://huggingface.co/docs/trl)
- [LLaMA-Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Axolotl GitHub](https://github.com/OpenAccess-AI-Collective/axolotl)
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)

## Research Sources

- [Fine-tuning LLMs in 2025 - SuperAnnotate](https://www.superannotate.com/blog/llm-fine-tuning)
- [LLM Fine-Tuning Guide 2026 - Keymakr](https://keymakr.com/blog/llm-fine-tuning-complete-guide-to-domain-specific-model-adaptation-2026/)
- [LLM Fine-Tuning for Engineering Teams - Heavybit](https://www.heavybit.com/library/article/llm-fine-tuning)
- [Ultimate Guide to Fine-Tuning LLMs - arXiv](https://arxiv.org/html/2408.13296v1)
- [Best Frameworks for Fine-tuning - Modal](https://modal.com/blog/fine-tuning-llms)
- [LLM Fine-Tuning Guide - Lakera](https://www.lakera.ai/blog/llm-fine-tuning-guide)
- [LLM Fine-Tuning for Enterprises 2026 - AIMultiple](https://research.aimultiple.com/llm-fine-tuning/)

---

*Last updated: 2026-01-25*
