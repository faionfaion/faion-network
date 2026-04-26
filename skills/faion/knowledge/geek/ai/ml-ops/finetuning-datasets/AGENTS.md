# Fine-tuning Datasets — Preparation, Training, and Deployment

## Summary

Dataset lifecycle methodology for open-model fine-tuning: cleaning and deduplication, format conversion (Alpaca/ShareGPT/OpenAI JSONL), training hyperparameter selection, evaluation with LM Evaluation Harness benchmarks, and deployment to Ollama (GGUF), vLLM, or TGI. Includes GPU selection and cost estimation for training runs.

## Why

Dataset format consistency is the single highest-impact factor in fine-tuning quality. Semantic duplicates, inconsistent system prompts, and unsanitized PII silently degrade model behavior. Getting the cleaning pipeline right before training saves GPU spend and avoids retraining cycles. Export format must match the inference server (GGUF for Ollama, merged HF for vLLM/TGI).

## When To Use

- Preparing a domain-specific dataset for LoRA/QLoRA or OpenAI fine-tuning from raw source data
- Evaluating a fine-tuned model against baselines using standard benchmarks (MMLU, HellaSwag, HumanEval)
- Deploying a fine-tuned model to a local (Ollama) or production (vLLM/TGI) inference server
- Estimating GPU cost and training duration before committing cloud spend

## When NOT To Use

- Fewer than 100 cleaned, verified examples — dataset preparation overhead is not justified; use few-shot instead
- Benchmark accuracy on MMLU/HellaSwag is the primary goal — task-specific fine-tuning often hurts general benchmarks
- Deployment target does not support GGUF or HF-format models
- vLLM deployment without first merging the LoRA adapter — vLLM requires a merged model

## Content

| File | What's inside |
|------|---------------|
| `content/01-dataset-cleaning.xml` | Deduplication, filtering, PII removal, format conversion (Alpaca/ShareGPT/OpenAI), train/val split |
| `content/02-training-config.xml` | Hyperparameter table, learning rate schedules, gradient accumulation, GPU selection and cost table |
| `content/03-evaluation-deployment.xml` | Perplexity, lm-eval benchmarks, GGUF export, Ollama Modelfile, vLLM server launch, TGI Docker |

## Templates

| File | Purpose |
|------|---------|
| `templates/clean-dataset.py` | Deduplication + filter + train/val split pipeline (~35 lines) |
| `templates/ollama-modelfile` | Ollama Modelfile for LLaMA-3 chat template with stop tokens |
