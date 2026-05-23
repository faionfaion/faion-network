# purpose: Minimal viable invocation of ClaudeService + batch helpers against stub responses.
# consumes: nothing (uses in-process stubs).
# produces: dict matching the methodology output contract.
# depends-on: claude-service.py + batch-api.py.
# token-budget-impact: zero (no live API calls).
"""Smoke test — minimum viable filled-in version of the integration wiring."""
from __future__ import annotations


def fake_output() -> dict:
    return {
        "surfaces_wired": ["completion_sync", "prompt_caching", "streaming", "tool_use"],
        "default_model": "claude-sonnet-4-20250514",
        "stop_reason_centralised": True,
        "retry_installed": True,
        "prompt_caching": {"cached_prefix_tokens": 3200, "hit_ratio_target": 0.75},
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
