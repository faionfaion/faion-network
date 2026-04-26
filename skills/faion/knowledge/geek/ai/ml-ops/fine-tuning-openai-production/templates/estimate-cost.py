"""
Estimate OpenAI fine-tuning cost before upload.
Input:  jsonl_path, model, n_epochs, cost_per_1m (USD)
Output: {"total_tokens": int, "training_tokens": int, "estimated_cost_usd": float}
"""
import json
import sys
import tiktoken


def estimate_ft_cost(
    jsonl_path: str,
    model: str = "gpt-4o-mini-2024-07-18",
    n_epochs: int = 3,
    cost_per_1m: float = 3.00,
) -> dict:
    # gpt-4o and gpt-4o-mini share the same tokenizer family
    enc = tiktoken.encoding_for_model("gpt-4o")
    total_tokens = 0
    example_count = 0
    with open(jsonl_path) as f:
        for line in f:
            obj = json.loads(line)
            for msg in obj.get("messages", []):
                total_tokens += len(enc.encode(msg.get("content", "")))
            example_count += 1

    training_tokens = total_tokens * n_epochs
    cost = round((training_tokens / 1_000_000) * cost_per_1m, 4)
    return {
        "examples": example_count,
        "total_tokens": total_tokens,
        "training_tokens": training_tokens,
        "n_epochs": n_epochs,
        "estimated_cost_usd": cost,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "training_data.jsonl"
    result = estimate_ft_cost(path)
    for k, v in result.items():
        print(f"{k}: {v}")
