---
slug: fine-tuning-openai-sft
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an OpenAI SFT job config + launched fine-tune job, customising GPT-4.1 / GPT-4o on input-output JSONL pairs with eval-gate-gated deployment.
content_id: "e25456c1bee0a12d"
complexity: medium
produces: config
est_tokens: 3500
tags: [fine-tuning, openai, sft, gpt, training]
---
# OpenAI Supervised Fine-Tuning (SFT)

## Summary

**One-sentence:** Produces an OpenAI SFT job config + launched fine-tune job, customising GPT-4.1 / GPT-4o on input-output JSONL pairs with eval-gate-gated deployment.

**One-paragraph:** Produces an OpenAI Supervised Fine-Tuning (SFT) job config + launched job. SFT is the default and primary OpenAI fine-tuning method: upload a JSONL training file, create a fine-tuning job with chosen base model + hyperparameters, poll until completion, then use the returned model ID. This methodology pins the config (base model, epochs, batch, lr_multiplier, n_epochs auto vs fixed) and the launch playbook.

**Ефективно для:** ML інженер для production tuning — fixed SFT job spec з base, hyperparams, polling pattern.

## Applies If (ALL must hold)

- Decision record selected 'api-sft' (per `finetuning` methodology).
- Training JSONL validated (per `fine-tuning-openai-data-prep`).
- Validation JSONL split (≥10 examples) available for OpenAI eval traces.
- Base model chosen: gpt-4o-mini-2024-07-18 (cheap, fast), gpt-4o-2024-08-06 (quality), gpt-4.1-2025-04-14 (latest, multimodal).
- Budget envelope: $/job approved (typically $1-100 for ≤10k examples).

## Skip If (ANY kills it)

- Decision record selected LoRA / Full FT — use HF training path.
- Training data not yet validated — run data-prep methodology first.
- Base model not on OpenAI catalogue — use HF path.
- Budget unapproved — escalate before launch.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| OpenAI training file ID | string (file_...) | fine-tuning-openai-data-prep |
| OpenAI validation file ID | string | fine-tuning-openai-data-prep |
| Base model name | string | model registry |
| Job hyperparams | yaml | ml-ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/fine-tuning-openai-data-prep` | Supplies file IDs. |
| `geek/ai/ml-engineer/fine-tuning-openai-eval` | Downstream eval-gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 4-step procedure: prepare-job → launch → poll → record-model-id. | ~600 |
| `content/06-decision-tree.xml` | essential | Branch by base-model + epoch count + n_epochs auto vs fixed. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-job-config` | haiku | Fill openai-sft-job.py from inputs. |
| `choose-hyperparams` | sonnet | Pick epochs/lr_multiplier from data volume + task type. |
| `debug-job-failure` | opus | Diagnose validation failures / cost spikes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openai-sft-job.py` | Job-launch + polling script. |
| `templates/sft-config.yaml` | Hyperparams: base, epochs, lr_multiplier, batch. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-sft.py` | Validate the SFT config (base, epochs, file IDs, hyperparams). | Pre-merge of every SFT job PR. |

## Related

- [[fine-tuning-openai-data-prep]] — upstream.
- [[fine-tuning-openai-eval]] — downstream eval-gate.
- [[fine-tuning-openai-deployment]] — downstream rollout.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks base model + epoch policy + lr_multiplier from (data volume, task type, budget).
