"""
Verify trainable parameter count after applying LoRA.
Raises ValueError if 0 trainable params (wrong target_modules).
"""


def check_lora_params(model) -> dict:
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    if trainable == 0:
        raise ValueError(
            "No trainable parameters — target_modules names do not match "
            "this model's architecture. Check model.named_modules() for valid names."
        )
    return {
        "trainable": trainable,
        "total": total,
        "pct": f"{100 * trainable / total:.4f}%",
    }
