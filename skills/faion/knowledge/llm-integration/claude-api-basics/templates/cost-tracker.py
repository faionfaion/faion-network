# purpose: Alias-proof CostTracker keyed off `response.model` and `response.usage`.
# consumes: per-call (response.model, response.usage) pairs.
# produces: per-call cost in USD + cumulative totals via `report()`.
# depends-on: rule r4 in content/01-core-rules.xml; pricing sheet from Anthropic.
# token-budget-impact: zero runtime tokens; pure post-call accounting.
"""CostTracker — per-call + session cost accumulation for Claude API."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CostTracker:
    """Track Claude API costs including prompt-cache pricing.

    Per rule r4, key the PRICES table off `response.model` — the response
    field — not the requested model string, since aliases can resolve to
    a different snapshot than requested.
    """

    PRICES: dict[str, dict[str, float]] = field(default_factory=lambda: {
        "claude-opus-4-5-20251101":  {"in": 15.00, "out": 75.00, "cw": 18.75, "cr": 1.50},
        "claude-sonnet-4-20250514":  {"in":  3.00, "out": 15.00, "cw":  3.75, "cr": 0.30},
        "claude-3-5-haiku-20241022": {"in":  0.80, "out":  4.00, "cw":  1.00, "cr": 0.08},
    })
    total: float = 0.0
    calls: int = 0
    unknown_models: set[str] = field(default_factory=set)

    def track(self, model: str, usage) -> float:
        """Record one API call's cost and return it (USD)."""
        if model not in self.PRICES:
            self.unknown_models.add(model)
        p = self.PRICES.get(model, {"in": 0.0, "out": 0.0, "cw": 0.0, "cr": 0.0})
        cost = (
            usage.input_tokens * p["in"]
            + usage.output_tokens * p["out"]
            + getattr(usage, "cache_creation_input_tokens", 0) * p["cw"]
            + getattr(usage, "cache_read_input_tokens", 0) * p["cr"]
        ) / 1_000_000
        self.total += cost
        self.calls += 1
        return cost

    def report(self) -> str:
        out = f"Total: ${self.total:.4f} across {self.calls} calls"
        if self.unknown_models:
            out += f" (UNKNOWN MODELS: {sorted(self.unknown_models)})"
        return out
