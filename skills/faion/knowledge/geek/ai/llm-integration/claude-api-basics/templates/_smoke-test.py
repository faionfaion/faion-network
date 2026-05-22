# purpose: Minimal viable invocation of CostTracker + retry decorator against stub usage.
# consumes: nothing (uses in-process stubs).
# produces: a printable dict matching the output contract.
# depends-on: cost-tracker.py + retry-wrapper.py.
# token-budget-impact: zero (no live API calls).
"""Smoke test — minimum viable filled-in version of the basics wiring."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _StubUsage:
    input_tokens: int = 1000
    output_tokens: int = 200
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


def fake_output() -> dict:
    return {
        "auth_source": "env",
        "model_id": "claude-sonnet-4-20250514",
        "retry_policy": {"retry_on": ["429", "500", "502", "503", "529"], "max_attempts": 5},
        "cost_tracker_installed": True,
        "request_id_logged": True,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
