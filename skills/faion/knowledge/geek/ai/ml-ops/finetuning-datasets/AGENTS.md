---
slug: finetuning-datasets
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Cleans, dedupes, format-converts (Alpaca/ShareGPT/OpenAI JSONL), trains with hyperparameter sweep, evaluates with LM-Evaluation-Harness, and deploys to Ollama (GGUF) / vLLM / TGI.
content_id: "8104e67f1ee088f4"
complexity: deep
produces: spec
est_tokens: 5200
tags: [datasets, fine-tuning, data-preparation, evaluation, deployment]
---
# Fine-tuning Datasets — Preparation, Training, Deployment

## Summary

**One-sentence:** Cleans, dedupes, format-converts (Alpaca/ShareGPT/OpenAI JSONL), trains with hyperparameter sweep, evaluates with LM-Evaluation-Harness, and deploys to Ollama (GGUF) / vLLM / TGI.

**One-paragraph:** Dataset issues account for most fine-tune failures: leaked test set, near-duplicates inflate apparent accuracy, format mismatch (Alpaca vs ShareGPT) confuses the loss curve. This methodology fixes the lifecycle: clean (PII strip, dedupe with MinHash), convert to the target format, select hyperparameters (rank, lr, epochs) per a baseline grid, run LM-Eval-Harness on the held-out set, and deploy to Ollama / vLLM / TGI with a smoke-test prompt suite.

**Ефективно для:**

- First-time finetune by a solo dev (dataset hygiene is the usual failure point).
- Multi-vendor format conversion (CSV → JSONL ShareGPT).
- Pre-deploy quality gate to avoid shipping a worse model.
- Vendor-switch (move from OpenAI ft → self-hosted ft).

## Applies If (ALL must hold)

- Dataset of ≥1k examples available (target ≥10k for instruction tasks).
- Held-out test set can be carved (≥10% of dataset).
- Deployment target known (Ollama / vLLM / TGI / Hosted).

## Skip If (ANY kills it)

- Dataset is private-label and cannot be deduped (license forbids modification).
- <1k examples — finetune underfits.
- Deployment will use closed API ft — different lifecycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Raw dataset | CSV/JSONL | Internal export |
| Target format | Alpaca/ShareGPT/OpenAI | Framework choice |
| Deploy target | Ollama/vLLM/TGI | Infra choice |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `clean_dedupe` | haiku | MinHash + PII regex; deterministic. |
| `format_convert` | haiku | Format mapping. |
| `hyperparam_sweep` | sonnet | Choose grid + rank order. |
| `deploy_pack` | sonnet | GGUF / vLLM config. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dataset-clean.yaml` | Clean + dedupe config skeleton |
| `templates/hyperparam-grid.yaml` | Baseline LoRA grid |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetuning-datasets.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[finetuning-basics]]
- [[fine-tuning-lora]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the dataset already deduped and split? Branches route to a rule id from `content/01-core-rules.xml` (dedupe-minhash, test-split-frozen, format-single-target, ...) so every leaf is traceable to a testable statement.
