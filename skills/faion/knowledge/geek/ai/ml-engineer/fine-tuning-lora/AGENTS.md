# Fine-tuning (LoRA)

## Summary

Parameter-efficient fine-tuning of LLMs using LoRA (Low-Rank Adaptation) and its variants (QLoRA, DoRA, rsLoRA). LoRA trains small adapter layers (rank r) instead of updating all weights, reducing memory 10-20x while retaining 90-95% of full fine-tuning quality. Target all linear layers (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj), start with r=16, alpha=32, and mix 20-30% general data to prevent catastrophic forgetting.

## Why

Full fine-tuning of 70B+ models requires A100/H100 clusters. LoRA makes fine-tuning accessible: QLoRA can fine-tune a 7B model on 8-12GB VRAM (consumer GPU). The adapter size is tiny (~65K parameters for r=8 on a 4096-dim layer), making multi-adapter serving and rollback practical. DoRA improves over LoRA by decomposing weights into magnitude and direction components, achieving near-full fine-tuning quality on complex tasks.

## When To Use

- Need consistent domain-specific terminology or jargon the base model handles inconsistently
- Output format must be exact and reliable (JSON schema, medical codes, proprietary syntax)
- Inference cost reduction: fine-tuned models need shorter system prompts
- You have 500+ quality labeled examples in the target distribution
- Style/brand voice consistency required at high volume

## When NOT To Use

- Fewer than 100 quality examples — few-shot prompting will outperform
- Requirements are changing — fine-tuned model becomes a liability when task evolves
- Need real-time knowledge — fine-tuning bakes in a snapshot; use RAG for live data
- No GPU access and limited budget — OpenAI fine-tuning API is a better path
- Model must handle wildly different tasks — specialized adapter degrades generality

## Content

| File | What's inside |
|------|---------------|
| `content/01-techniques.xml` | LoRA, QLoRA, DoRA, rsLoRA comparison; hardware requirements; how LoRA works; scaling factor rules |
| `content/02-training.xml` | Hyperparameter selection (rank, alpha, LR), data quality rules, catastrophic forgetting prevention, eval gates |
| `content/03-production.xml` | Agentic pipeline (config → submit → poll → eval → deploy), gotchas, rollback strategy |

## Templates

| File | Purpose |
|------|---------|
| `templates/lora-config.py` | LoRAConfig dataclass and LoRATrainingPipeline production class |
| `templates/eval-gate.py` | Pass/fail eval gate script using lm-eval harness |
| `templates/axolotl.yaml` | Axolotl YAML config for QLoRA fine-tuning |
