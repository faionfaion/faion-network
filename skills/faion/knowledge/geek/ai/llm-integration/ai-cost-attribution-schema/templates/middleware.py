"""
purpose: Python middleware that stamps attribution metadata on every LLM call.
consumes: request context (tenant_id, feature, route) + LLM client response
produces: one attribution record per call, emitted to telemetry sink
depends-on: content/02-output-contract.xml; templates/attribution.schema.json
token-budget-impact: runtime overhead ~1ms per call; not in agent prompt budget
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Callable, Any

# In production import the real pricing table + sink.
PRICING: dict[str, dict[str, float]] = {
    "claude-haiku-4": {"in_per_1k": 0.00025, "out_per_1k": 0.00125, "snapshot": "anthropic-2026-05-22"},
    "claude-sonnet-4-5": {"in_per_1k": 0.003, "out_per_1k": 0.015, "snapshot": "anthropic-2026-05-22"},
    "claude-opus-4-5": {"in_per_1k": 0.015, "out_per_1k": 0.075, "snapshot": "anthropic-2026-05-22"},
}


@dataclass
class CallContext:
    tenant_id: str
    feature: str
    route: str


def compute_cost(model: str, input_tokens: int, output_tokens: int) -> tuple[float, str]:
    p = PRICING.get(model)
    if not p:
        return (0.0, "unknown")
    cost = (input_tokens / 1000) * p["in_per_1k"] + (output_tokens / 1000) * p["out_per_1k"]
    return (round(cost, 6), p["snapshot"])


def with_attribution(client_call: Callable[..., Any], ctx: CallContext, sink: Callable[[dict], None]):
    def wrapper(*args, **kwargs):
        rid = str(uuid.uuid4())
        t0 = time.perf_counter()
        resp = client_call(*args, **kwargs)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        # Adapt the next two lines to the real SDK shape (anthropic / openai / gemini).
        usage = getattr(resp, "usage", None) or {}
        model = getattr(resp, "model", kwargs.get("model", "unknown"))
        in_tok = usage.get("input_tokens", 0) if isinstance(usage, dict) else getattr(usage, "input_tokens", 0)
        out_tok = usage.get("output_tokens", 0) if isinstance(usage, dict) else getattr(usage, "output_tokens", 0)
        cache_hit = bool(getattr(resp, "prompt_cache_hit", False) or (isinstance(usage, dict) and usage.get("cache_read_input_tokens", 0) > 0))
        cost, snap = compute_cost(model, in_tok, out_tok)
        record = {
            "request_id": rid,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tenant_id": ctx.tenant_id or f"anon_session_{rid[:8]}",
            "feature": ctx.feature,
            "route": ctx.route,
            "model": model,
            "prompt_cache_hit": cache_hit,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "latency_ms": latency_ms,
            "cost_usd": cost,
            "pricing_snapshot_id": snap,
        }
        sink(record)
        return resp
    return wrapper
