"""Prompt Caching wrapper — returns (response_text, cache_hit_rate).

Usage:
    text, hit_rate = call_with_cache(SYSTEM_DOCS, "What is X?")
    # hit_rate: 0.0 on first call (cache miss), ~0.9 on subsequent calls
"""
import anthropic

client = anthropic.Anthropic()


def call_with_cache(system_text: str, user_msg: str) -> tuple[str, float]:
    """Call Claude with a cached system prompt.

    Args:
        system_text: Large stable system prompt (must be > 1024 tokens to cache).
        user_msg: Per-turn user message (not cached).

    Returns:
        (response_text, cache_hit_rate) where cache_hit_rate is 0.0 on miss.
    """
    resp = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        betas=["prompt-caching-2024-07-31"],
        system=[{
            "type": "text",
            "text": system_text,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_msg}],
    )
    u = resp.usage
    hit_rate = u.cache_read_input_tokens / max(u.input_tokens, 1)
    return resp.content[0].text, hit_rate
