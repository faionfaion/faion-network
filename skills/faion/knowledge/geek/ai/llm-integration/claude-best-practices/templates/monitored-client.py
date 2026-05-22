# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""Minimal Claude client with token usage and latency logging.

Usage:
    r = call("generator", system, messages)
    text = r.content[0].text
"""
import anthropic
import logging
import time

log = logging.getLogger(__name__)
client = anthropic.Anthropic()

MODELS = {
    "router": "claude-3-5-haiku-20241022",
    "generator": "claude-sonnet-4-20250514",
    "reasoner": "claude-opus-4-5-20251101",
}


def call(
    role: str,
    system: list,
    messages: list,
    max_tokens: int = 2048,
) -> anthropic.types.Message:
    """Call Claude with logging of model, tokens, latency, and cache metrics.

    Args:
        role: One of "router", "generator", "reasoner" — selects model tier.
        system: System prompt as list of content blocks.
        messages: Conversation history.
        max_tokens: Explicit max tokens (required — never rely on default).

    Raises:
        ValueError: If response is truncated (stop_reason == "max_tokens").
    """
    model = MODELS[role]
    t0 = time.monotonic()
    r = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    elapsed = time.monotonic() - t0
    u = r.usage
    total = u.input_tokens + u.output_tokens
    cache_hit = getattr(u, "cache_read_input_tokens", 0)
    log.info(
        "role=%s model=%s tokens=%d cache_read=%d elapsed=%.2fs",
        role, model, total, cache_hit, elapsed,
    )
    if r.stop_reason == "max_tokens":
        raise ValueError(f"Response truncated for role={role}. Retry with higher max_tokens.")
    return r
