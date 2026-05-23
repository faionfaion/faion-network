# purpose: Minimal viable invocation showing thinking + cached + batch wrappers wired in.
# consumes: nothing (uses in-process stubs); for live use replace stubs with anthropic.Anthropic().
# produces: a printable dict the validator script can ingest as output.
# depends-on: think-deeply.py + call-with-cache.py + batch-submit-poll.py.
# token-budget-impact: zero (no live API calls; stubs only).
"""Smoke test — minimum viable filled-in version of the wrappers."""
from __future__ import annotations


def fake_output() -> dict:
    return {
        "features_enabled": ["extended_thinking", "prompt_caching"],
        "model_id": "claude-opus-4-5-20251101",
        "extended_thinking": {"budget_tokens": 5000, "max_tokens": 9096},
        "prompt_caching": {"cached_prefix_tokens": 4200, "hit_ratio_target": 0.75},
        "cache_hit_ratio": 0.82,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
