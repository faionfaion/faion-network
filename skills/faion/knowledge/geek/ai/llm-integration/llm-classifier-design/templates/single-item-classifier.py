"""
purpose: Single-item Anthropic SDK classifier — forced tool_use, one boolean answer.
consumes: item_text + system_prompt + tool schema
produces: boolean verdict
depends-on: content/01-core-rules.xml r2, r3
token-budget-impact: per-call; output reduced to JSON of answer
"""
from __future__ import annotations

from anthropic import Anthropic

SYSTEM_PROMPT = "You are an auditor. Reply only via the verdict tool."

VERDICT_TOOL = {
    "name": "verdict",
    "description": "Report whether the input meets the criterion.",
    "input_schema": {
        "type": "object",
        "properties": {"sufficient": {"type": "boolean"}},
        "required": ["sufficient"],
        "additionalProperties": False,
    },
}


def classify(item_text: str, model: str = "claude-sonnet-4-6") -> bool:
    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=64,
        system=SYSTEM_PROMPT,
        tools=[VERDICT_TOOL],
        tool_choice={"type": "tool", "name": "verdict"},
        messages=[{"role": "user", "content": item_text}],
    )
    return next(b.input["sufficient"] for b in resp.content if b.type == "tool_use")
