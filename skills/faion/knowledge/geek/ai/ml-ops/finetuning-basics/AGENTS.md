---
slug: finetuning-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive reference for open-model fine-tuning techniques (LoRA, QLoRA, DoRA, full fine-tuning) and training frameworks (LLaMA-Factory, Unsloth, Axolotl, TRL).
content_id: "68ae3ae806d77de1"
tags: [fine-tuning, llm, lora, qlora, frameworks]
---
# Fine-tuning Basics — Techniques and Frameworks

## Summary

**One-sentence:** Comprehensive reference for open-model fine-tuning techniques (LoRA, QLoRA, DoRA, full fine-tuning) and training frameworks (LLaMA-Factory, Unsloth, Axolotl, TRL).

**One-paragraph:** Comprehensive reference for open-model fine-tuning techniques (LoRA, QLoRA, DoRA, full fine-tuning) and training frameworks (LLaMA-Factory, Unsloth, Axolotl, TRL). Covers technique selection by GPU memory budget, alignment methods (SFT, DPO, ORPO), model merging strategies, and the agent-appropriate division of labor between data preparation (automatable) and GPU training (dispatched externally).

## Applies If (ALL must hold)

- Need a model to consistently follow a domain-specific format or writing style that prompting cannot enforce
- Building a product where inference latency matters and a smaller fine-tuned model can replace a larger prompted one
- Alignment work: converting DPO/ORPO preference data into a tuned model for controlled output behavior
- Repeated task patterns (extraction, classification, rewriting) where a small fine-tuned model beats few-shot on cost

## Skip If (ANY kills it)

- Adding new factual knowledge — fine-tuning memorizes patterns, not facts; use RAG instead
- Fewer than 100 high-quality examples — insufficient signal; use few-shot prompting
- One-off tasks — fine-tuning overhead (data prep, training, eval, hosting) is not justified
- Rapidly changing requirements — every dataset update requires a full retrain cycle
- ORPO/DPO without collected chosen/rejected pairs — obtaining rejection data from production is non-trivial

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
