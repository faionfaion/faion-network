---
slug: fine-tuning-lora
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LoRA (Low-Rank Adaptation) fine-tuning methodology using PEFT + TRL: freezing base model weights and injecting small trainable matrices (rank 8-64) into attention layers, reducing trainable parameters by 100-250x.
content_id: "4d13fa1c6ea48100"
tags: [lora, qlora, fine-tuning, peft, gpu-optimization]
---
# Fine-tuning (LoRA)

## Summary

**One-sentence:** LoRA (Low-Rank Adaptation) fine-tuning methodology using PEFT + TRL: freezing base model weights and injecting small trainable matrices (rank 8-64) into attention layers, reducing trainable parameters by 100-250x.

**One-paragraph:** LoRA (Low-Rank Adaptation) fine-tuning methodology using PEFT + TRL: freezing base model weights and injecting small trainable matrices (rank 8-64) into attention layers, reducing trainable parameters by 100-250x. Covers QLoRA (4-bit quantization), multiple-adapter management, hyperparameter search, and the LoRATrainingPipeline production class.

## Applies If (ALL must hold)

- Consumer GPU available (8-24GB VRAM) and full fine-tuning is not feasible
- Need to maintain multiple task-specific adapters on one base model without reloading weights
- Quick iteration experiments where training must complete in hours, not days
- Adapting model style/behavior without degrading general capabilities
- Production scenario where a specialized smaller model is cheaper to serve than a large prompted model

## Skip If (ANY kills it)

- Task requires injecting new factual knowledge — LoRA adapters do not reliably encode facts; use RAG
- Dataset is smaller than 50 examples — adapter overfits immediately; use few-shot prompting
- Target inference server does not support on-the-fly adapter loading — merge the adapter first
- Real-time latency requirement below 100ms — adapter overhead adds ~5-10ms; merging eliminates this
- Multiple simultaneous LoRA experiments on the same GPU — they will OOM; serialize jobs

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
