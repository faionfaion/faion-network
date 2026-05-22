# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Per-call token cost tracking with daily budget enforcement.
Record every API call; raise RuntimeError when daily limit is exceeded.
"""


class TokenBudget:
    """Track LLM spend and enforce a daily USD budget."""

    PRICES = {  # USD per 1M tokens (input, output)
        "claude-haiku-4-5": {"in": 0.80, "out": 4.00},
        "claude-sonnet-4-5": {"in": 3.00, "out": 15.00},
        "claude-opus-4-5": {"in": 15.00, "out": 75.00},
        "gpt-4o-mini": {"in": 0.15, "out": 0.60},
        "gpt-4o-2024-08-06": {"in": 2.50, "out": 10.00},
    }

    def __init__(self, daily_limit_usd: float):
        self.limit = daily_limit_usd
        self.spent = 0.0
        self.calls = 0

    def record(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Record token usage and return cost for this call. Raises on budget exceeded."""
        prices = self.PRICES.get(model, {"in": 3.00, "out": 15.00})
        cost = (input_tokens * prices["in"] + output_tokens * prices["out"]) / 1_000_000
        self.spent += cost
        self.calls += 1
        if self.spent >= self.limit:
            raise RuntimeError(
                f"Daily budget ${self.limit:.2f} exceeded "
                f"(${self.spent:.4f} spent across {self.calls} calls)"
            )
        return cost

    def warn_at(self, threshold: float = 0.80) -> bool:
        """Return True if spend has reached the threshold fraction of limit."""
        return self.spent >= self.limit * threshold

    @property
    def remaining(self) -> float:
        return max(0.0, self.limit - self.spent)
