"""Extended Thinking helper — returns (thinking, answer) tuple.

Usage:
    thinking, answer = think_deeply("Solve this complex problem...")
    # thinking: model's reasoning chain (do NOT show to end users)
    # answer: final answer text
"""
import anthropic

client = anthropic.Anthropic()


def think_deeply(problem: str, budget: int = 8000) -> tuple[str, str]:
    """Run Extended Thinking on problem. Returns (thinking, answer).

    Args:
        problem: The question or task for the model to reason about.
        budget: Thinking token budget. Max tokens will be set to budget + 4096.
    """
    resp = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=budget + 4096,  # must exceed budget_tokens
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": problem}],
    )
    thinking = next((b.thinking for b in resp.content if b.type == "thinking"), "")
    answer = next((b.text for b in resp.content if b.type == "text"), "")
    return thinking, answer
