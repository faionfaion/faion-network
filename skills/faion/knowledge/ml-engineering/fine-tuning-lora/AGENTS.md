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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/axolotl.yaml`

```yaml
# Axolotl QLoRA config — Llama-3.1-8B-Instruct baseline
# Usage: axolotl train axolotl.yaml

base_model: meta-llama/Meta-Llama-3.1-8B-Instruct
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer
trust_remote_code: false

# Quantization (QLoRA)
load_in_4bit: true
adapter: qlora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

# Dataset
datasets:
  - path: data/train.jsonl
    type: chat_template
    chat_template: llama3
  - path: data/general.jsonl     # 20-30% general data to prevent forgetting
    type: chat_template
    chat_template: llama3
dataset_prepared_path: ./prepared
val_set_size: 0.10

# Training
sequence_len: 2048
micro_batch_size: 1
gradient_accumulation_steps: 8    # effective batch = 8
num_epochs: 3
learning_rate: 0.0002
lr_scheduler: cosine
warmup_ratio: 0.03

# Precision
bf16: true
tf32: true
gradient_checkpointing: true
flash_attention: true

# Evaluation and checkpointing
eval_steps: 100
save_steps: 200
save_total_limit: 3
load_best_model_at_end: true
metric_for_best_model: eval_loss
early_stopping_patience: 3

# Output
output_dir: ./checkpoints
logging_steps: 10
```

### `templates/lora-config.py`

```python
"""

"""LoRA/QLoRA configuration for common model families."""
from peft import LoraConfig, TaskType
from transformers import BitsAndBytesConfig


def qlora_config(
    r: int = 16,
    lora_alpha: int = 32,
    lora_dropout: float = 0.05,
    target_all_linear: bool = False,
) -> tuple[LoraConfig, BitsAndBytesConfig]:
    """Return QLoRA configuration for 4-bit training."""
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="bfloat16",
        bnb_4bit_use_double_quant=True,
    )

    target_modules = (
        "all-linear"
        if target_all_linear
        else ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        target_modules=target_modules,
        bias="none",
        use_rslora=r > 32,  # rsLoRA for high ranks
    )

    return lora_config, bnb_config


def dora_config(r: int = 16, lora_alpha: int = 32) -> LoraConfig:
    """Return DoRA config — use when standard LoRA underperforms baseline."""
    return LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=r,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none",
        use_dora=True,
    )


# Rank selection guide:
# r=4   → style/format tasks (simple, <100 examples)
# r=8   → domain adaptation (300-500 examples)
# r=16  → instruction following (500-2000 examples) — DEFAULT
# r=32  → behavioral alignment (2000+ examples)
# r=64  → major behavioral shift (5000+ examples, use rsLoRA)
```

### `templates/eval-gate.py`

```python
"""

"""Eval gate: block deployment of LoRA-fine-tuned models that fail quality thresholds."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class EvalGateResult:
    passed: bool
    domain_acc: float
    general_score: float
    refusal_rate: float
    failures: list[str]


def run_eval_gate(
    evaluate_domain: Callable,
    evaluate_general: Callable,
    measure_refusal: Callable,
    base_scores: dict[str, float],
    domain_eval_data: list,
    general_eval_data: list,
    domain_threshold_delta: float = 0.10,
    general_threshold_ratio: float = 0.80,
    max_refusal_rate: float = 0.05,
) -> EvalGateResult:
    """
    Run three-gate eval check before permitting model deployment.

    Gates:
    1. Domain accuracy >= base_domain_accuracy + domain_threshold_delta
    2. General score >= base_general_score * general_threshold_ratio
    3. Refusal rate <= max_refusal_rate on domain prompts
    """
    domain_acc = evaluate_domain(domain_eval_data)
    general_score = evaluate_general(general_eval_data)
    refusal_rate = measure_refusal(domain_eval_data)

    failures = []

    domain_threshold = base_scores["domain"] + domain_threshold_delta
    if domain_acc < domain_threshold:
        failures.append(
            f"Domain accuracy {domain_acc:.3f} below threshold {domain_threshold:.3f}"
        )

    general_threshold = base_scores["general"] * general_threshold_ratio
    if general_score < general_threshold:
        failures.append(
            f"General score {general_score:.3f} degraded below "
            f"{general_threshold_ratio*100:.0f}% of base ({general_threshold:.3f})"
        )

    if refusal_rate > max_refusal_rate:
        failures.append(
            f"Refusal rate {refusal_rate:.1%} exceeds {max_refusal_rate:.1%} threshold"
        )

    return EvalGateResult(
        passed=len(failures) == 0,
        domain_acc=domain_acc,
        general_score=general_score,
        refusal_rate=refusal_rate,
        failures=failures,
    )


def assert_gate(result: EvalGateResult) -> None:
    """Raise ValueError if gate failed — use in CI/CD pipeline."""
    if not result.passed:
        raise ValueError(
            "Eval gate FAILED. Model deployment blocked.\n"
            + "\n".join(f"  - {f}" for f in result.failures)
        )
```
