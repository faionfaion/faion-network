# purpose: Minimal Claude client logging response.model + usage + elapsed + x-request-id.
# consumes: (role, system, messages, max_tokens).
# produces: anthropic.types.Message; logs every call (rule r2).
# depends-on: rules r1+r2+r3 in content/01-core-rules.xml.
# token-budget-impact: zero (pure logging on top of one API call).
"""Minimal Claude client with model + usage + latency + cache + request-id logging."""
from __future__ import annotations

import logging
import time

import anthropic

log = logging.getLogger(__name__)
client = anthropic.Anthropic()

MODELS = {
    "router": "claude-3-5-haiku-20241022",
    "generator": "claude-sonnet-4-20250514",
    "reasoner": "claude-opus-4-5-20251101",
}


def call(role: str, system, messages: list, max_tokens: int = 2048):
    """Call Claude with logging of model, tokens, latency, and cache metrics."""
    model = MODELS[role]
    t0 = time.monotonic()
    r = client.messages.with_raw_response.create(  # captures headers for x-request-id.
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    msg = r.parse()
    elapsed = time.monotonic() - t0
    u = msg.usage
    total = u.input_tokens + u.output_tokens
    cache_hit = getattr(u, "cache_read_input_tokens", 0)
    request_id = r.headers.get("x-request-id", "")
    log.info(
        "role=%s requested=%s response=%s tokens=%d cache_read=%d elapsed=%.2fs request_id=%s",
        role, model, msg.model, total, cache_hit, elapsed, request_id,
    )
    if msg.stop_reason == "max_tokens":  # rule r3.
        raise ValueError(f"Response truncated for role={role}. Retry with higher max_tokens.")
    return msg
