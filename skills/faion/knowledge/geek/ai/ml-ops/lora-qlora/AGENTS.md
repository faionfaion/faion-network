---
slug: lora-qlora
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Configures LoRA or QLoRA (4-bit base + LoRA adapters) for memory-efficient fine-tunes on commodity GPUs (16-24GB VRAM) with rank 8-64 and bf16/nf4 dtype rules.
content_id: "1c5da1e9971cb68c"
complexity: deep
produces: code
est_tokens: 4800
tags: [lora, qlora, fine-tuning, adapters, memory-efficient]
---
# LoRA and QLoRA — Low-Rank Adaptation

## Summary

**One-sentence:** Configures LoRA or QLoRA (4-bit base + LoRA adapters) for memory-efficient fine-tunes on commodity GPUs (16-24GB VRAM) with rank 8-64 and bf16/nf4 dtype rules.

**One-paragraph:** LoRA injects rank-r trainable matrices into attention projections while freezing base weights; QLoRA quantises the base to 4-bit (nf4) so LoRA fits in half the VRAM at ~1-2 pp quality cost. This methodology fixes the dtype rules (bf16 for LoRA-only on Ampere+, nf4 + bf16 compute for QLoRA), rank/alpha ratio, gradient checkpointing toggle, and a smoke-test that detects bf16 vs fp16 instability before a long run.

**Ефективно для:**

- Commodity-GPU finetune (16-24GB VRAM) on 7B/8B/13B models.
- Multi-tenant SaaS adapters (one base, many tenants).
- Iterative experiments where checkpoints must be small (<1GB each).
- Cost-driven move from full-FT to memory-efficient ft.

## Applies If (ALL must hold)

- GPU has 16-48GB VRAM.
- Base model is decoder-only Transformer (Llama / Mistral / Qwen family).
- Dataset is in target chat format.

## Skip If (ANY kills it)

- GPU < 16GB VRAM — too tight even for QLoRA on 7B.
- Base model is non-Transformer (state-space, etc.).
- Quality gap measured > 5pp despite rank sweep — escalate to full-FT.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prepared dataset | JSONL | finetuning-datasets methodology |
| Base model | HF id | finetuning-basics methodology |
| GPU dtype | bf16/fp16 | Hardware capability |

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
| `dtype_pick` | sonnet | bf16 vs fp16; nf4 for QLoRA. |
| `rank_sweep` | sonnet | Rank 8/16/32/64. |
| `smoke_test` | haiku | 5-step bf16/fp16 stability check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qlora-config.yaml` | QLoRA bnb_config + PEFT skeleton |
| `templates/smoke-test.py` | 5-step stability smoke test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lora-qlora.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[fine-tuning-lora]]
- [[finetuning-basics]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the available GPU Ampere or newer? Branches route to a rule id from `content/01-core-rules.xml` (bf16-on-ampere, nf4-for-qlora, grad-checkpointing-on, ...) so every leaf is traceable to a testable statement.
