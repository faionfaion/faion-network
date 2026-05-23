# purpose: Extended Thinking wrapper returning (thinking, answer) with safe max_tokens.
# consumes: a problem string + an integer budget (default 5000).
# produces: tuple (thinking_text, answer_text); answer never truncated.
# depends-on: rule r1 + r2 in content/01-core-rules.xml; pinned model id.
# token-budget-impact: budget + 4096 output tokens per call; non-cacheable.
"""Extended Thinking helper — returns (thinking, answer) tuple."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-opus-4-5-20251101"


def think_deeply(problem: str, budget: int = 5000) -> tuple[str, str]:
    """Run Extended Thinking on `problem`. Returns (thinking, answer)."""
    if budget < 1024:
        raise ValueError("Extended Thinking budget below 1024 is degenerate; use the base API path.")
    resp = client.messages.create(
        model=MODEL_ID,
        max_tokens=budget + 4096,  # rule r1: guarantee answer headroom
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": problem}],
        # rule r2: NO temperature parameter when thinking is enabled.
    )
    thinking = next((b.thinking for b in resp.content if b.type == "thinking"), "")
    answer = next((b.text for b in resp.content if b.type == "text"), "")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("Answer truncated — increase max_tokens or shrink budget.")
    return thinking, answer
