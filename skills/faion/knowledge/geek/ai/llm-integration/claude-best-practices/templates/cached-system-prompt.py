"""Cached system prompt structure: stable prefix cached, dynamic tail not cached.

Usage:
    response = call_with_cached_system(STATIC_DOCS, dynamic_instructions, user_task)
"""
import anthropic

client = anthropic.Anthropic()

# This large block never changes across calls — will be cached after first call
STATIC_DOCS = """
... large stable documentation (10k+ tokens) ...
... product specs, API references, style guides ...
"""


def call_with_cached_system(
    static_content: str,
    dynamic_instructions: str,
    user_task: str,
    max_tokens: int = 4096,
) -> anthropic.types.Message:
    """Call Claude with a two-part system prompt: cached static + uncached dynamic.

    Args:
        static_content: Large stable context (> 1024 tokens). Will be cached.
        dynamic_instructions: Per-run instructions. Not cached.
        user_task: User's message for this turn.
        max_tokens: Maximum tokens for the response.

    Returns:
        Anthropic Message object. Check usage.cache_read_input_tokens for hit rate.
    """
    system = [
        {
            "type": "text",
            "text": static_content,
            "cache_control": {"type": "ephemeral"},  # cached prefix
        },
        {
            "type": "text",
            "text": dynamic_instructions,  # not cached; changes per-run
        },
    ]
    return client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_task}],
    )
