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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/data-formats.json`

```json
{
  "formats": {
    "sft_chat": {
      "description": "Supervised fine-tuning with chat template (messages array)",
      "supported_by": [
        "TRL",
        "Axolotl",
        "LLaMA-Factory",
        "Unsloth",
        "OpenAI"
      ],
      "example": {
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "What is the capital of France?"
          },
          {
            "role": "assistant",
            "content": "Paris."
          }
        ]
      }
    },
    "sft_alpaca": {
      "description": "Alpaca instruction format (instruction/input/output)",
      "supported_by": [
        "Axolotl",
        "LLaMA-Factory"
      ],
      "example": {
        "instruction": "Summarize the following text.",
        "input": "Text to summarize...",
        "output": "Summary of the text."
      }
    },
    "dpo": {
      "description": "Direct Preference Optimization (prompt/chosen/rejected)",
      "supported_by": [
        "TRL",
        "Axolotl",
        "LLaMA-Factory"
      ],
      "example": {
        "prompt": "Explain quantum entanglement.",
        "chosen": "Quantum entanglement is a phenomenon where two particles become correlated...",
        "rejected": "Quantum stuff is when particles are connected or something."
      }
    },
    "grpo": {
      "description": "Group Relative Policy Optimization (prompt + verifiable reward)",
      "supported_by": [
        "TRL"
      ],
      "note": "Reward is computed externally (code executor, math verifier) \u2014 not stored in file",
      "example": {
        "prompt": "Solve: what is 127 * 43?",
        "answer": "5461"
      }
    }
  },
  "validation_rules": {
    "common": [
      "One JSON object per line (JSONL format)",
      "No trailing commas",
      "UTF-8 encoding",
      "No empty content fields",
      "No duplicate examples (hash check)"
    ],
    "sft_chat": [
      "Must have at least 'user' and 'assistant' roles",
      "System message optional but must be first if present",
      "Alternating user/assistant turns recommended"
    ],
    "dpo": [
      "chosen and rejected must differ meaningfully",
      "chosen must be clearly better, not just longer",
      "Avoid trivially wrong rejected examples"
    ]
  }
}
```

### `templates/framework-selector.py`

```python
"""

"""Fine-tuning framework selector based on constraints."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingConstraints:
    gpu_count: int               # Number of available GPUs
    gpu_vram_gb: int             # VRAM per GPU in GB
    model_size_b: float          # Model size in billions of parameters
    dataset_size: int            # Number of training examples
    needs_web_ui: bool           # Non-engineer users need a UI
    needs_distributed: bool      # Multi-node training required
    training_method: str         # "sft", "dpo", "ppo", "grpo"
    prefer_speed: bool           # Optimize for training speed over flexibility


def select_framework(c: TrainingConstraints) -> dict[str, str]:
    """
    Select the best fine-tuning framework for the given constraints.
    Returns {"framework": name, "rationale": explanation}
    """
    # Unsloth: best single-GPU speed with QLoRA
    if (c.gpu_count == 1
            and c.gpu_vram_gb <= 80
            and c.training_method == "sft"
            and c.prefer_speed):
        return {
            "framework": "Unsloth",
            "rationale": (
                "Single GPU, SFT with QLoRA. "
                "Unsloth's patched kernels give 2-5x speedup and 60% VRAM reduction."
            ),
            "install": "pip install unsloth",
            "config": "FastLanguageModel.from_pretrained(..., load_in_4bit=True)",
        }

    # LLaMA-Factory: needs web UI
    if c.needs_web_ui:
        return {
            "framework": "LLaMA-Factory",
            "rationale": "WebUI required. LLaMA-Factory provides a no-code training interface.",
            "install": "pip install llamafactory",
            "config": "llamafactory-cli webui",
        }

    # Axolotl: multi-GPU or complex configs
    if c.needs_distributed or c.gpu_count > 1:
        return {
            "framework": "Axolotl",
            "rationale": (
                f"Multi-GPU ({c.gpu_count}x) or distributed training. "
                "Axolotl has battle-tested FSDP/DeepSpeed YAML configs."
            ),
            "install": "pip install axolotl",
            "config": "axolotl train config.yaml",
        }

    # TRL: DPO/PPO/GRPO or programmatic control
    if c.training_method in ("dpo", "ppo", "grpo"):
        return {
            "framework": "TRL",
            "rationale": (
                f"Training method '{c.training_method}' requires TRL's "
                "DPOTrainer/PPOTrainer/GRPOTrainer."
            ),
            "install": "pip install trl",
            "config": f"from trl import {c.training_method.upper()}Trainer",
        }

    # Default: TRL SFTTrainer for programmatic pipelines
    return {
        "framework": "TRL (SFTTrainer)",
        "rationale": "General-purpose SFT with HuggingFace integration and full Python control.",
        "install": "pip install trl peft transformers",
        "config": "from trl import SFTTrainer",
    }
```

### `templates/validate-jsonl.py`

```python
"""

"""JSONL fine-tuning dataset validator with deduplication check."""
import hashlib
import json
import sys
from pathlib import Path


def validate_jsonl(
    path: str,
    required_roles: tuple[str, ...] = ("user", "assistant"),
    min_examples: int = 100,
    check_duplicates: bool = True,
) -> dict:
    """
    Validate fine-tuning JSONL dataset.
    Returns stats dict or raises ValueError on critical errors.
    """
    errors: list[str] = []
    warnings: list[str] = []
    seen_hashes: set[str] = set()
    stats = {"total": 0, "valid": 0, "duplicates": 0, "errors": 0}

    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            stats["total"] += 1

            # Parse JSON
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: invalid JSON: {e}")
                stats["errors"] += 1
                continue

            # Check required structure
            if "messages" not in obj:
                errors.append(f"Line {line_num}: missing 'messages' key")
                stats["errors"] += 1
                continue

            messages = obj["messages"]
            if not isinstance(messages, list) or len(messages) < 2:
                errors.append(f"Line {line_num}: 'messages' must be a list with 2+ items")
                stats["errors"] += 1
                continue

            # Check required roles
            roles = {m.get("role") for m in messages}
            for role in required_roles:
                if role not in roles:
                    errors.append(f"Line {line_num}: missing required role '{role}'")

            # Check for empty content
            for j, msg in enumerate(messages):
                if not str(msg.get("content", "")).strip():
                    errors.append(f"Line {line_num}, message {j}: empty content")

            # Deduplication
            if check_duplicates:
                content_hash = hashlib.md5(line.encode()).hexdigest()
                if content_hash in seen_hashes:
                    warnings.append(f"Line {line_num}: duplicate example")
                    stats["duplicates"] += 1
                else:
                    seen_hashes.add(content_hash)
                    stats["valid"] += 1
            else:
                stats["valid"] += 1

    # Aggregate errors
    if len(errors) > 0:
        raise ValueError(
            f"Dataset validation failed ({len(errors)} errors):\n"
            + "\n".join(f"  {e}" for e in errors[:20])
            + (f"\n  ... and {len(errors)-20} more" if len(errors) > 20 else "")
        )

    if stats["valid"] < min_examples:
        raise ValueError(
            f"Insufficient valid examples: {stats['valid']} < minimum {min_examples}"
        )

    if warnings:
        print(f"Warnings ({len(warnings)}):", file=sys.stderr)
        for w in warnings[:10]:
            print(f"  {w}", file=sys.stderr)

    return stats


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate fine-tuning JSONL dataset")
    parser.add_argument("path", help="Path to JSONL file")
    parser.add_argument("--min-examples", type=int, default=100)
    args = parser.parse_args()

    stats = validate_jsonl(args.path, min_examples=args.min_examples)
    print(f"Validation passed: {stats}")
```
