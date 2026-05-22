---
slug: finetuning-datasets
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Dataset lifecycle methodology for open-model fine-tuning: cleaning and deduplication, format conversion (Alpaca/ShareGPT/OpenAI JSONL), training hyperparameter selection, evaluation with LM Evaluation Harness benchmarks, and deployment to Ollama (GGUF), vLLM, or TGI.
content_id: "d42461a989202f84"
tags: [datasets, fine-tuning, data-preparation, evaluation, deployment]
---
# Fine-tuning Datasets — Preparation, Training, and Deployment

## Summary

**One-sentence:** Dataset lifecycle methodology for open-model fine-tuning: cleaning and deduplication, format conversion (Alpaca/ShareGPT/OpenAI JSONL), training hyperparameter selection, evaluation with LM Evaluation Harness benchmarks, and deployment to Ollama (GGUF), vLLM, or TGI.

**One-paragraph:** Dataset lifecycle methodology for open-model fine-tuning: cleaning and deduplication, format conversion (Alpaca/ShareGPT/OpenAI JSONL), training hyperparameter selection, evaluation with LM Evaluation Harness benchmarks, and deployment to Ollama (GGUF), vLLM, or TGI. Includes GPU selection and cost estimation for training runs.

## Applies If (ALL must hold)

- Preparing a domain-specific dataset for LoRA/QLoRA or OpenAI fine-tuning from raw source data
- Evaluating a fine-tuned model against baselines using standard benchmarks (MMLU, HellaSwag, HumanEval)
- Deploying a fine-tuned model to a local (Ollama) or production (vLLM/TGI) inference server
- Estimating GPU cost and training duration before committing cloud spend

## Skip If (ANY kills it)

- Fewer than 100 cleaned, verified examples — dataset preparation overhead is not justified; use few-shot instead
- Benchmark accuracy on MMLU/HellaSwag is the primary goal — task-specific fine-tuning often hurts general benchmarks
- Deployment target does not support GGUF or HF-format models
- vLLM deployment without first merging the LoRA adapter — vLLM requires a merged model

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
