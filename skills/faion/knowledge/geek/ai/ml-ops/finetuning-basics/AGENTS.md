# Fine-tuning Basics — Techniques and Frameworks

## Summary

Comprehensive reference for open-model fine-tuning techniques (LoRA, QLoRA, DoRA, full fine-tuning) and training frameworks (LLaMA-Factory, Unsloth, Axolotl, TRL). Covers technique selection by GPU memory budget, alignment methods (SFT, DPO, ORPO), model merging strategies, and the agent-appropriate division of labor between data preparation (automatable) and GPU training (dispatched externally).

## Why

Choosing the wrong technique wastes GPU budget: full fine-tuning on a 7B model requires 80GB+ VRAM while QLoRA achieves comparable results with 6-8GB. Framework selection determines training speed, configurability, and export options. LoRA rank and target module selection are the two highest-impact decisions and must be made before starting any training run.

## When To Use

- Need a model to consistently follow a domain-specific format or writing style that prompting cannot enforce
- Building a product where inference latency matters and a smaller fine-tuned model can replace a larger prompted one
- Alignment work: converting DPO/ORPO preference data into a tuned model for controlled output behavior
- Repeated task patterns (extraction, classification, rewriting) where a small fine-tuned model beats few-shot on cost

## When NOT To Use

- Adding new factual knowledge — fine-tuning memorizes patterns, not facts; use RAG instead
- Fewer than 100 high-quality examples — insufficient signal; use few-shot prompting
- One-off tasks — fine-tuning overhead (data prep, training, eval, hosting) is not justified
- Rapidly changing requirements — every dataset update requires a full retrain cycle
- ORPO/DPO without collected chosen/rejected pairs — obtaining rejection data from production is non-trivial

## Content

| File | What's inside |
|------|---------------|
| `content/01-technique-selection.xml` | LoRA vs. QLoRA vs. DoRA vs. full FT decision matrix; rank selection guide; target_modules by model family |
| `content/02-frameworks.xml` | LLaMA-Factory, Unsloth, Axolotl, TRL: installation, CLI commands, key config options |
| `content/03-alignment.xml` | SFT vs. DPO vs. ORPO: dataset formats, `DPOConfig`/`ORPOConfig` code, model merging with mergekit |

## Templates

| File | Purpose |
|------|---------|
| `templates/validate-jsonl.py` | Validate JSONL format before upload to any training API (~20 lines) |
| `templates/axolotl-config.yaml` | Axolotl YAML config for LoRA fine-tuning of a 7B LLaMA-family model |
