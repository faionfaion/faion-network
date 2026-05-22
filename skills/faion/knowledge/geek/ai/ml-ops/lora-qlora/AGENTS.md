---
slug: lora-qlora
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LoRA (Low-Rank Adaptation) freezes base model weights and injects small trainable matrices into attention layers, reducing trainable parameters from 100% to 0.
content_id: "fa5478ac8d727c47"
tags: [lora, qlora, fine-tuning, adapters, memory-efficient]
---
# LoRA and QLoRA: Low-Rank Adaptation for Efficient Fine-tuning

## Summary

**One-sentence:** LoRA (Low-Rank Adaptation) freezes base model weights and injects small trainable matrices into attention layers, reducing trainable parameters from 100% to 0.

**One-paragraph:** LoRA (Low-Rank Adaptation) freezes base model weights and injects small trainable matrices into attention layers, reducing trainable parameters from 100% to 0.1-1% with minimal quality loss. QLoRA extends this by loading the base model in 4-bit quantized form and training LoRA adapters in fp16, enabling fine-tuning of 70B models on a single 48GB GPU. Both techniques enable task-specific adapter training that can be swapped at inference time without reloading the base model.

## Applies If (ALL must hold)

- Fine-tuning an open-source model (LLaMA, Mistral, Qwen, Phi) on a custom dataset with limited GPU memory.
- Training domain-specific adapters that can be swapped at inference time without reloading the base model.
- Producing multiple task-specific adapters from one base model (customer support, code, summarization).
- Reducing fine-tuning cost vs. full fine-tuning: QLoRA brings a 70B model into a single 48GB GPU.
- Creating a task-specific model when OpenAI fine-tuning is too expensive or the data must stay on-prem.

## Skip If (ANY kills it)

- Fewer than 500-1000 domain-specific examples — few-shot prompting or RAG will outperform a poorly-trained adapter.
- The goal is injecting new factual knowledge — LoRA improves style/format, not factual recall; use RAG for knowledge.
- The target task is simple enough for a prompt template with a smaller base model.
- The team lacks GPU access (even a single A100 or consumer 3090/4090); CPU-only training is impractical.
- Production requires strict reproducibility; adapter merging and quantization introduce non-determinism.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-ops/`
