# purpose: Minimal viable invocation showing claude-messages-api output produced.
# consumes: nothing (in-process stub).
# produces: dict matching the output contract.
# depends-on: rules in content/01-core-rules.xml.
# token-budget-impact: zero (no live API calls).
"""Smoke test — minimum viable filled-in version for claude-messages-api."""
from __future__ import annotations


def fake_output() -> dict:
    return {
    "stop_reason_centralised": true,
    "max_tokens_explicit": true,
    "multimodal_image_first": true,
    "pdf_preflight_check": true,
    "metadata_user_id": true,
    "streaming_delta_aware": true,
    "model_id": "claude-sonnet-4-20250514",
    "forbidden_seen": []
}


if __name__ == "__main__":
    import json as _j
    print(_j.dumps(fake_output(), indent=2))
