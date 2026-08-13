# Fine-tuning with LoRA (PEFT + TRL)

## Summary

**One-sentence:** Runs a LoRA fine-tune with PEFT + TRL: freeze base weights, inject rank-8-64 matrices on attention layers, 100-250× fewer trainable params, fits on a single 24GB GPU for 7B/8B models.

**One-paragraph:** LoRA injects low-rank trainable matrices into attention projections while freezing base weights, reducing trainable parameters by two orders of magnitude. The recipe: PEFT for the adapter wiring, TRL for the SFT trainer, target_modules covering q_proj/k_proj/v_proj/o_proj, rank 8-64 (8 for cheap, 64 for quality), alpha = 2×rank, dropout 0.05, lr 1e-4 to 3e-4, 1-3 epochs. Save adapters separately; merge or keep modular at inference.

**Ефективно для:**

- Single-GPU finetune on 7B/8B models with ≥24GB VRAM.
- Multi-tenant SaaS where each tenant gets its own adapter (no full-model duplication).
- Iterative experiments where adapters are quick to swap.
- Mixed-budget orgs swapping between base model versions.

## Applies If (ALL must hold)

- Base model is selected (HF id).
- Dataset is in target format (Alpaca/ShareGPT/OpenAI JSONL).
- GPU has VRAM ≥ base_model_gb + 4GB.

## Skip If (ANY kills it)

- GPU VRAM < base_model_gb + 4 — use QLoRA instead (lora-qlora methodology).
- Dataset < 1k examples — prompt engineering is cheaper.
- Quality gap to full-FT measured > 5pp — escalate to full-FT.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prepared dataset | JSONL | finetuning-datasets methodology |
| Base model | HF id | finetuning-basics methodology |
| GPU | ≥24GB VRAM | Cloud or owned |

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
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `config_author` | sonnet | PEFT config + TRL trainer args. |
| `hyperparam_sweep` | sonnet | rank/lr/epochs grid. |
| `eval_runner` | haiku | LM-eval-harness invoke. |

## Templates

| File | Purpose |
|------|---------|
| `templates/peft-config.yaml` | PEFT LoRA config skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[finetuning-basics]]
- [[lora-qlora]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the target attention layer set defined? Branches route to a rule id from `content/01-core-rules.xml` (target-attention-projections, rank-8-to-64, checkpoint-best-eval, ...) so every leaf is traceable to a testable statement.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/peft-config.yaml`

```yaml
# fine-tuning-lora — config skeleton
version: 1.0.0
slug: fine-tuning-lora
fields:
  - name: example-field
    type: string
    required: true
defaults: {}
```
