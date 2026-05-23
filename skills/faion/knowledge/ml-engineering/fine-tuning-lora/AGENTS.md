# Fine-tuning (LoRA)

## Summary

**One-sentence:** Produces a LoRA/QLoRA/DoRA/rsLoRA training config (rank, alpha, target modules, data mix) for a chosen base model, fitted to single-GPU or multi-GPU budgets.

**One-paragraph:** Produces a LoRA / QLoRA / DoRA / rsLoRA training configuration. LoRA trains small adapter matrices (rank r) instead of full weights, cutting memory 10-20x while retaining 90-95% of full-FT quality. Default: target ALL linear layers (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj), r=16, alpha=32, lr=2e-4, batch 4-8 with grad-accum, mix 20-30% general data. QLoRA adds 4-bit base-model loading for further memory savings.

**Ефективно для:** ML інженер на single-GPU — за один прохід генерує робочий axolotl.yaml + peft config, не марнує GPU-години на debug.

## Applies If (ALL must hold)

- Fine-tuning decision record (parent `finetuning`) landed on LoRA, QLoRA, DoRA, or rsLoRA.
- Base model 1B-70B params (Llama, Mistral, Qwen, Phi typically).
- Task-specific corpus ≥100 labelled examples, JSONL-validated.
- Single GPU ≥24GB (QLoRA on 7B) or multi-GPU budget.
- Eval harness exists with task metric + general-capability holdout.

## Skip If (ANY kills it)

- Base model is API-only (OpenAI/Anthropic/Gemini) — use API SFT instead.
- Data <100 examples — adapter overfits.
- Full-FT decision recorded — use TRL / Torchtune full path.
- VRAM <16GB even with 4-bit — escalate to cloud.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Training corpus | jsonl (sft_chat schema) | validate-jsonl.py |
| Base-model name / HF path | string | model registry |
| Eval harness path | py module | ml-ops repo |
| Hardware envelope | yaml (gpu_count, vram_gb) | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/finetuning` | Parent decision record; this methodology consumes its 'LoRA' branch. |
| `geek/ai/ml-engineer/fine-tuning-openai-eval` | Eval pattern reused for held-out scoring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: validate-data → choose-config → train → checkpoint → eval-gate → merge-or-keep. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch by VRAM / variant (LoRA / QLoRA / DoRA / rsLoRA). | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Fill axolotl.yaml + lora-config.py from decisions — pure templating. |
| `tune-hyperparams` | sonnet | Choose r / alpha / lr / batch from r4 trade-off table — structured reasoning. |
| `debug-divergence` | opus | Loss-spike / NaN / instability triage — Opus diagnoses cross-cutting symptoms. |

## Templates

| File | Purpose |
|------|---------|
| `templates/axolotl.yaml` | Axolotl config skeleton with LoRA + QLoRA toggles. |
| `templates/lora-config.py` | peft LoraConfig + QLoraConfig factory. |
| `templates/eval-gate.py` | Held-out eval-gate runner, exits non-zero on regression. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-lora.py` | Validate that the LoRA config matches the schema (r, alpha, target_modules, lr). | Pre-merge of every LoRA config PR. |

## Related

- [[finetuning]] — parent decision; this methodology implements its LoRA branch.
- [[fine-tuning-openai-eval]] — eval pattern reused.
- [[llm-decision-framework]] — context: when LoRA fits the broader LLM strategy.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks variant: LoRA (full-precision), QLoRA (4-bit base + LoRA adapter), DoRA (decomposed magnitude+direction), rsLoRA (rank-stabilised). Use BEFORE writing the yaml.
