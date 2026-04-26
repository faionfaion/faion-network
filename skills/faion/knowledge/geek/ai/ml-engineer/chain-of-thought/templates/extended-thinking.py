"""
Claude Extended Thinking API call.
Use for: math, formal logic, code correctness, multi-constraint optimization.
Start with budget_tokens=1024; increase by 1024 until quality plateaus.
"""
import anthropic


def extended_thinking(problem: str, thinking_budget: int = 4096) -> dict:
    """
    Call Claude Opus with Extended Thinking.
    Returns {"thinking": str, "answer": str}
    """
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=thinking_budget + 2048,
        thinking={"type": "enabled", "budget_tokens": thinking_budget},
        messages=[{"role": "user", "content": problem}],
    )
    thinking_text = next(
        (b.thinking for b in response.content if b.type == "thinking"), ""
    )
    answer_text = next(
        (b.text for b in response.content if b.type == "text"), ""
    )
    return {"thinking": thinking_text, "answer": answer_text}


# Cost estimate helper
def estimate_thinking_cost(
    thinking_budget: int, queries_per_day: int, price_per_m_tokens: float = 15.0
) -> float:
    """Estimate daily Extended Thinking cost in USD."""
    tokens_per_day = thinking_budget * queries_per_day
    return (tokens_per_day / 1_000_000) * price_per_m_tokens
