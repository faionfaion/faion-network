---
slug: finetuning
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a fine-tuning decision record naming technique (Full FT / LoRA / QLoRA / DoRA / API-SFT), framework, data plan, and budget — gated by prompt+RAG-first scoring.
content_id: "381c1f92ad7e8880"
complexity: deep
produces: decision-record
est_tokens: 4500
tags: [fine-tuning, decision-tree, frameworks, llm, data-pipeline]
---
# LLM Fine-tuning (General Guide)

## Summary

**One-sentence:** Produces a fine-tuning decision record naming technique (Full FT / LoRA / QLoRA / DoRA / API-SFT), framework, data plan, and budget — gated by prompt+RAG-first scoring.

**One-paragraph:** Produces a fine-tuning decision record. Covers chosen technique (Full FT, LoRA, QLoRA, DoRA, OpenAI API SFT/DPO), framework (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune), training data plan, expected cost, and rollback owner. Fine-tuning is the most expensive and least reversible enhancement strategy — practitioners MUST score prompt engineering and RAG first and only commit when prompting plateaus.

**Ефективно для:** ML інженер під час архітектурного вибору — фіксує decision record до того, як спалить GPU-години на FT.

## Applies If (ALL must hold)

- Prompt + RAG plateau verified: ≥30 representative examples show prompting cannot close the gap.
- Training data ≥100 labelled examples (≥1000 for full FT) is available.
- Target behaviour is stable — fine-tuning a moving target wastes compute.
- Latency or cost constraints justify a smaller fine-tuned model over a larger zero-shot one.
- Team has GPU access (own / Modal / RunPod / OpenAI API) and an eval harness in place.

## Skip If (ANY kills it)

- Prompt engineering not exhausted — try few-shot, CoT, structured output first.
- Training data <100 examples — fine-tune overfits and degrades.
- Target behaviour changes within a quarter — RAG is more reversible.
- No eval harness — without offline metrics, fine-tune output cannot be measured.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Training corpus | jsonl | data team / validate-jsonl.py |
| Held-out eval set | jsonl | separate split, never used for training |
| Baseline metrics (prompt+RAG) | csv | eval harness |
| Budget envelope | yaml | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Decides whether prompt / RAG / fine-tune at all — this is the downstream node. |
| `geek/ai/ml-engineer/fine-tuning-openai-eval` | Eval gate the resulting model must pass before deployment. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: prompt-baseline → RAG-baseline → technique-select → framework-select → train → eval-gate. | ~800 |
| `content/05-examples.xml` | medium | Worked example: tone classification → QLoRA on Mistral-7B via Axolotl. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by data volume / hardware / target. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-prompt-baseline` | sonnet | Run prompt baseline; structured output. |
| `technique-and-framework-select` | opus | Budget + hardware + reversibility — weighs trade-offs. |
| `training-config-fill` | haiku | Template-fill: scaffold yaml/python config from decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-formats.json` | JSONL format reference (sft_chat / dpo / completion) cross-framework. |
| `templates/framework-selector.py` | CLI choosing framework given (model, hardware, data shape). |
| `templates/validate-jsonl.py` | Pre-flight validator for training JSONL (schema + token counts). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetuning.py` | Validate that the decision record matches the schema. | Pre-merge of every fine-tune ADR. |

## Related

- [[llm-decision-framework]] — parent decision; emits the 'fine-tune' branch this methodology elaborates.
- [[fine-tuning-lora]] — concrete LoRA recipe when this guide lands on LoRA/QLoRA.
- [[fine-tuning-openai-sft]] — concrete OpenAI SFT recipe when the decision lands on API-side SFT.

## Decision tree

Decision tree at `content/06-decision-tree.xml` partitions by (prompt+RAG plateaued?), data volume, hardware, target domain. Use BEFORE provisioning GPUs.
