# OpenAI Fine-Tuning Guide

Production guide for fine-tuning OpenAI models (GPT-4.1, GPT-4o, GPT-4o-mini).

## Overview

Fine-tuning customizes OpenAI models for specific tasks by training on your examples. Benefits:

- **Improved quality** - Better performance on domain-specific tasks
- **Reduced costs** - Shorter prompts, fewer tokens per request
- **Lower latency** - Less context processing
- **Consistent format** - Reliable structured outputs

## Supported Models (2025)

| Model | Training Cost | Inference (Input/Output) | Context | Best For |
|-------|--------------|--------------------------|---------|----------|
| gpt-4.1 | $25/M tokens | $2/$8 per M | 1M | Complex reasoning, long context |
| gpt-4.1-mini | $3/M tokens | $0.40/$1.60 per M | 128K | Cost-effective production |
| gpt-4.1-nano | $1/M tokens | $0.10/$0.40 per M | 128K | High-volume, simple tasks |
| gpt-4o | $25/M tokens | $3.75/$15 per M | 128K | Vision, multimodal |
| gpt-4o-mini | $3/M tokens | $0.30/$1.20 per M | 128K | Budget production |

**Note:** Fine-tuned model inference costs are higher than base model costs.

## Fine-Tuning Methods

### Supervised Fine-Tuning (SFT)

Default method. Train on input-output pairs.

```
Input: User query
Output: Ideal assistant response
```

**Use when:** Clear correct answers exist, training on examples.

### Direct Preference Optimization (DPO)

Train on preference pairs (preferred vs non-preferred responses).

```
Input: User query
Preferred: Better response
Non-preferred: Worse response
```

**Use when:** Subjective preferences, tone/style optimization, alignment.

**Supported models for DPO:** gpt-4.1, gpt-4.1-mini, gpt-4.1-nano

### Reinforcement Fine-Tuning (RFT)

Train using reward signals and custom graders.

**Use when:** Complex optimization criteria, multi-step reasoning.

## Cost Calculation

```
Training Cost = Tokens in training file x Epochs x Training price per token
```

**Example:** 1M tokens, 3 epochs, gpt-4o-mini ($3/M):
```
1M x 3 x $3/M = $9 total training cost
```

**Inference discount:** Enable data sharing for lower inference rates.

## Data Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Examples | 10 | 50-100+ |
| Validation split | 10% | 10-20% |
| Example length | - | <4K tokens each |
| Total tokens | - | 10K-100K+ |

## Folder Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step workflow checklist |
| [examples.md](examples.md) | Complete code examples |
| [templates.md](templates.md) | Reusable code templates |
| [llm-prompts.md](llm-prompts.md) | Evaluation and data generation prompts |

## Quick Start

1. **Prepare data** - Format as JSONL with messages array
2. **Validate data** - Check format, balance, quality
3. **Upload files** - Training and validation files
4. **Create job** - Start fine-tuning with hyperparameters
5. **Monitor** - Track progress and metrics
6. **Evaluate** - Compare to base model
7. **Deploy** - Use fine-tuned model in production

## Decision Framework

```
Need fine-tuning?
    |
    v
Can prompt engineering solve it? --> YES --> Use prompts
    |
    NO
    v
Do you have 50+ quality examples? --> NO --> Collect more data
    |
    YES
    v
Is task domain-specific? --> NO --> Consider RAG
    |
    YES
    v
Need preference alignment? --> YES --> Use DPO (after SFT)
    |
    NO
    v
Use Supervised Fine-Tuning (SFT)
```

## Related

- [Fine-tuning Best Practices](https://platform.openai.com/docs/guides/fine-tuning-best-practices)
- [OpenAI Cookbook Fine-tuning](https://cookbook.openai.com/examples/how_to_finetune_chat_models)
- [DPO Guide](https://cookbook.openai.com/examples/fine_tuning_direct_preference_optimization_guide)
- [OpenAI Evals](https://github.com/openai/evals)

## Sources

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning/)
- [OpenAI Fine-tuning API Reference](https://platform.openai.com/docs/api-reference/fine-tuning)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Supervised Fine-tuning](https://platform.openai.com/docs/guides/supervised-fine-tuning)
- [Direct Preference Optimization](https://platform.openai.com/docs/guides/direct-preference-optimization)
- [Evaluation Best Practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
