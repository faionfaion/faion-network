# CostTracker: per-call and session cost accumulation for Claude API
# Usage: tracker = CostTracker(); cost = tracker.track(response.model, response.usage)

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CostTracker:
    """Track Claude API costs including prompt cache pricing."""

    PRICES: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "claude-opus-4-5-20251101":  {"in": 15.00, "out": 75.00, "cw": 18.75, "cr": 1.50},
        "claude-sonnet-4-20250514":  {"in":  3.00, "out": 15.00, "cw":  3.75, "cr": 0.30},
        "claude-3-5-haiku-20241022": {"in":  0.80, "out":  4.00, "cw":  1.00, "cr": 0.08},
    })

    total: float = 0.0
    calls: int = 0

    def track(self, model: str, usage) -> float:
        """Record one API call's cost and return it.

        Args:
            model: response.model (not requested model — aliases may differ)
            usage: response.usage object with input_tokens, output_tokens,
                   optionally cache_creation_input_tokens, cache_read_input_tokens
        Returns:
            Cost of this call in USD.
        """
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
        return f"Total: ${self.total:.4f} across {self.calls} calls"
