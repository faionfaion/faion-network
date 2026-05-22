"""
purpose: peft LoraConfig + QLoraConfig factory.
consumes: see AGENTS.md ## Prerequisites
produces: config
depends-on: content/02-output-contract.xml schema for fine-tuning-lora
token-budget-impact: ≤500 tokens to fill
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
