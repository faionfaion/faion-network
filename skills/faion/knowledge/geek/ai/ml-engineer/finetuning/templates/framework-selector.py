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
