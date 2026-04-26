"""Sequential five-mode MLP pipeline coordinator.

Runs faion-mlp-agent across all 5 modes in order.
Returns per-mode results; human review required between propose and update.
"""


def run_mlp_pipeline(project_path: str, product_type: str) -> list[dict]:
    """Run all 5 MLP modes sequentially; return results per mode.

    IMPORTANT: pause after mode:propose for human feature selection
    before allowing mode:update to proceed.
    """
    modes = ["analyze", "find-gaps", "propose", "update", "plan"]
    results = []
    for mode in modes:
        prompt = f"mode: {mode}\nproject_path: {project_path}"
        if mode == "propose":
            prompt += f"\nproduct_type: {product_type}"
        # Invoke faion-mlp-agent with prompt, store result.
        # Pass prior result as context for the next mode.
        results.append({"mode": mode, "prompt": prompt, "status": "pending"})
    return results
