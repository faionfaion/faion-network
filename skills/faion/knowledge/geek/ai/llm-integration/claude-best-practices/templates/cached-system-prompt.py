# purpose: System-prompt object with stable cached prefix + dynamic tail.
# consumes: static_content (≥1024 tokens), dynamic_instructions, user_task.
# produces: anthropic.types.Message; cache_read_input_tokens > 0 from call #2.
# depends-on: rule r4 in content/01-core-rules.xml.
# token-budget-impact: 25% write surcharge on first call; ~10% input cost on cache reads.
"""Cached system prompt structure: stable prefix cached, dynamic tail not cached."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"


def call_with_cached_system(
    static_content: str,
    dynamic_instructions: str,
    user_task: str,
    max_tokens: int = 4096,
):
    """Call Claude with a two-part system prompt: cached static + uncached dynamic.

    `static_content` MUST be byte-identical on every call (rule r4); place dynamic values
    in `dynamic_instructions` or `user_task`, never in `static_content`.
    """
    system = [
        {"type": "text", "text": static_content, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": dynamic_instructions},
    ]
    return client.messages.create(
        model=MODEL_ID,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_task}],
    )
