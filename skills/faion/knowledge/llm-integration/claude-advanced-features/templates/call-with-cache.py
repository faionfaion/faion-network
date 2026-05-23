# purpose: Prompt-cached call wrapper returning (text, cache_hit_ratio).
# consumes: a stable system text (≥1024 tokens) + a per-turn user message.
# produces: tuple (text, hit_ratio); hit_ratio is `cache_read / max(input, 1)`.
# depends-on: rule r3 + r4 in content/01-core-rules.xml.
# token-budget-impact: write surcharge 25% on first call; ~10% input cost on cache reads.
"""Prompt Caching wrapper — returns (response_text, cache_hit_ratio)."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"


def call_with_cache(system_text: str, user_msg: str) -> tuple[str, float]:
    """Call Claude with a stable cached system prompt and a dynamic user turn.

    `system_text` MUST be the byte-identical prefix on every call (rule r3).
    Dynamic values must live in `user_msg`, never in `system_text`.
    """
    resp = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": system_text,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_msg}],
    )
    u = resp.usage
    hit_ratio = u.cache_read_input_tokens / max(u.input_tokens, 1)
    return resp.content[0].text, hit_ratio
