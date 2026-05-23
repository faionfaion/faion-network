# Fine-tuning Basics — Techniques and Frameworks

## Summary

**One-sentence:** Picks the cheapest fine-tuning technique (LoRA, QLoRA, DoRA, full FT) and the simplest framework (LLaMA-Factory, Unsloth, Axolotl, TRL) for the task and GPU budget.

**One-paragraph:** Open-model fine-tuning has four mainstream techniques (LoRA, QLoRA, DoRA, full fine-tune) and four mainstream frameworks (LLaMA-Factory, Unsloth, Axolotl, TRL). Each technique has a different GPU floor and quality ceiling; each framework has a different config surface. This methodology picks the (technique, framework) pair by matching dataset size, target task, GPU VRAM, and team skill, then locks the choice in a decision record.

**Ефективно для:**

- Open-model fine-tune from a CSV / JSONL dataset.
- Cost-driven move from closed API to self-hosted finetune.
- Domain adaptation (legal, medical) where general models miss vocabulary.
- On-prem / air-gapped requirements where API fine-tunes are out.

## Applies If (ALL must hold)

- Dataset of ≥1k examples available.
- GPU access (rented or owned) with ≥24GB VRAM (or planning QLoRA on 16GB).
- Base model selected (7B/8B/13B class typical for solopreneur budgets).

## Skip If (ANY kills it)

- Few-shot prompting solves the task — fine-tune is overkill.
- Dataset < 1k examples — finetune underfits; prompt engineer instead.
- Closed API fine-tune is the only option (data residency) — use fine-tuning-openai-* methodologies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dataset | JSONL/CSV | Internal export |
| Base model | HF model id | Provider choice |
| GPU access | rented / on-prem | Cloud or hardware |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `technique_pick` | sonnet | LoRA vs QLoRA vs full FT. |
| `framework_pick` | sonnet | LLaMA-Factory vs Unsloth vs Axolotl vs TRL. |
| `budget_estimate` | haiku | GPU-hour calc. |

## Templates

| File | Purpose |
|------|---------|
| `templates/finetune-config.yaml` | Framework-agnostic finetune config skeleton |
| `templates/decision-record.md` | Technique + framework choice rationale |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetuning-basics.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[fine-tuning-lora]]
- [[lora-qlora]]
- [[finetuning-datasets]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Does available GPU VRAM cover base model + LoRA adapters? Branches route to a rule id from `content/01-core-rules.xml` (lora-default, qlora-when-low-vram, full-ft-only-when-justified, ...) so every leaf is traceable to a testable statement.
