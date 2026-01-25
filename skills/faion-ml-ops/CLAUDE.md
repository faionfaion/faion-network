# ML Ops Skill

> **Entry Point:** Invoked via [/faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)

## When to Use

- Fine-tuning LLMs (OpenAI, LoRA, QLoRA)
- Model evaluation and benchmarking
- LLM cost optimization
- Observability and monitoring
- Dataset preparation for fine-tuning

## Overview

Handles ML model operations and optimization.

**Methodologies:** 15 | **Focus:** Fine-tuning, evaluation, cost, observability

## Quick Reference

| Area | Files |
|------|-------|
| Fine-tuning | finetuning-basics.md, lora-qlora.md, fine-tuning-openai-basics.md |
| Evaluation | evaluation-metrics.md, evaluation-framework.md, evaluation-benchmarks.md |
| Cost | llm-cost-basics.md, cost-reduction-strategies.md |
| Observability | llm-observability-stack-2026.md, llm-management-observability.md |

## Methodology Count

- Fine-tuning: 5 methodologies
- Evaluation: 3 methodologies
- Cost Optimization: 2 methodologies
- Observability: 5 methodologies

**Total: 15**

## Fine-tuning Decision

| Scenario | Approach |
|----------|----------|
| <100 examples | Few-shot prompting |
| 100-1000 examples | OpenAI fine-tuning |
| >1000 examples | LoRA/QLoRA |
| Custom behavior | Fine-tuning |
| New knowledge | RAG (not fine-tuning) |

## Related

- Parent: [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)
- Uses: faion-llm-integration (APIs)
- Peers: faion-rag-engineer

---

*ML Ops v1.0*
