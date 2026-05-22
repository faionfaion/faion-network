# purpose: Minimal viable invocation showing the policy pack assembled.
# consumes: nothing (uses in-process stub).
# produces: a printable dict matching the output contract.
# depends-on: cached-system-prompt.py + monitored-client.py.
# token-budget-impact: zero (no live API calls).
"""Smoke test — minimum viable filled-in version of the policy pack."""
from __future__ import annotations


def fake_output() -> dict:
    return {
        "model_tier_table": {
            "routing": "claude-3-5-haiku-20241022",
            "generation": "claude-sonnet-4-20250514",
            "reasoning": "claude-opus-4-5-20251101",
        },
        "fallback_logging": True,
        "shared_rate_bucket": True,
        "cache_layout": {"stable_prefix_first": True, "cached_prefix_tokens": 4200},
        "retry_after_parsing": True,
        "batch_api_enabled": True,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
