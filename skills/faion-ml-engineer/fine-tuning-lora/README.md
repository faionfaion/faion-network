---
id: fine-tuning-lora
name: "Fine-tuning (LoRA)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
version: "2.0.0"
updated: "2026-01"
---

# Fine-tuning (LoRA)

Parameter-efficient fine-tuning techniques: LoRA, QLoRA, DoRA, rsLoRA for LLM adaptation.

## Overview

LoRA (Low-Rank Adaptation) trains small adapter layers instead of updating all model weights, reducing memory 10-20x while retaining 90-95% of full fine-tuning quality. Combined with quantization (QLoRA) or weight decomposition (DoRA), enables fine-tuning 70B+ models on consumer hardware.

## Techniques Comparison

| Technique | Memory | Performance | Best For |
|-----------|--------|-------------|----------|
| **LoRA** | ~10-15% of full | 95-98% | Standard fine-tuning, multi-adapter serving |
| **QLoRA** | ~3-5% of full | 90-95% | Limited VRAM, consumer GPUs |
| **DoRA** | ~12-18% of full | 98-100%+ | Maximum quality, complex tasks |
| **rsLoRA** | Same as LoRA | Better at high ranks | High-rank adapters (r>64) |
| **QDoRA** | ~4-6% of full | 95-100% | Best of QLoRA + DoRA |

## Hardware Requirements (2025-2026)

| Model Size | LoRA | QLoRA | Recommended GPU |
|------------|------|-------|-----------------|
| 7B | 24GB+ | 8-12GB | RTX 4090, A10 |
| 13B | 40GB+ | 16GB | A100 40GB, L40S |
| 70B | 160GB+ | 48-80GB | A100 80GB, H100 |

## Key Concepts

### How LoRA Works

```
Original weight: W (d x k matrix)
LoRA adds: W' = W + BA
  Where: B (d x r), A (r x k), r << min(d, k)

Example: d=4096, k=4096, r=8
  Original: 16.7M parameters
  LoRA: 65K parameters (250x reduction)
```

### Scaling Factor

| Method | Scaling | Formula |
|--------|---------|---------|
| LoRA | alpha/r | Linear scaling |
| rsLoRA | alpha/sqrt(r) | Rank-stabilized |

rsLoRA enables effective use of higher ranks (r>64) without gradient collapse.

### Weight Decomposition (DoRA)

DoRA decomposes pretrained weights into:
1. **Magnitude** (m): scalar per output dimension, trained directly
2. **Direction** (V): normalized weight matrix, updated via LoRA

This mimics full fine-tuning learning patterns more closely.

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Pre-flight checklist for fine-tuning |
| [examples.md](examples.md) | Code examples (LoRA, QLoRA, DoRA) |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for fine-tuning assistance |

## Quick Decision Tree

```
Need to fine-tune LLM?
│
├─ Limited VRAM (<24GB)?
│  └─ QLoRA (4-bit) or QDoRA
│
├─ Maximum quality needed?
│  └─ DoRA or QDoRA
│
├─ High rank adapters (r>64)?
│  └─ rsLoRA (use_rslora=True)
│
├─ Standard fine-tuning?
│  └─ LoRA with all linear layers
│
└─ Multiple task adapters?
   └─ LoRA with adapter switching
```

## Best Practices Summary

1. **Target all linear layers** (attention + MLP) for best results
2. **Start with r=8-16**, increase if underfitting
3. **Set alpha = 2 x rank** (or use rsLoRA for high ranks)
4. **Learning rate 10x higher** than full fine-tuning (1e-4 to 5e-4)
5. **Quality over quantity**: 1,000 good examples beat 100,000 mediocre ones
6. **Mix general data (20-30%)** with task-specific to prevent forgetting

## References

### Papers

- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685) (Hu et al., 2021)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (Dettmers et al., 2023)
- [DoRA: Weight-Decomposed Low-Rank Adaptation](https://arxiv.org/abs/2402.09353) (NVIDIA, ICML 2024)
- [rsLoRA: Rank Stabilization Scaling Factor](https://arxiv.org/abs/2312.03732) (Kalajdzievski, 2023)

### Libraries

- [PEFT (HuggingFace)](https://huggingface.co/docs/peft)
- [TRL (HuggingFace)](https://huggingface.co/docs/trl)
- [Unsloth](https://github.com/unslothai/unsloth) - 2x faster fine-tuning
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) - Config-driven
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) - Easy WebUI

### Guides

- [Unsloth LoRA Hyperparameters Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- [Databricks: Efficient Fine-Tuning with LoRA](https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms)
- [Sebastian Raschka: Practical Tips for LoRA](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)
- [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| LoRA configuration | sonnet | Parameter tuning |
| Training optimization | opus | Advanced optimization |
| Model merging | sonnet | Model composition |
