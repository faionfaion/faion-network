"""test_security.py.
purpose: security suite — every payload must be blocked
consumes: tests/payloads/v1.jsonl
produces: pytest report; failures = leaked payloads
depends-on: pytest; system-under-test guardrails pipeline (mocked LLM)
token-budget-impact: +200t.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

PAYLOADS = [
    json.loads(line)
    for line in Path(__file__).parent.joinpath("payloads/v1.jsonl").read_text().splitlines()
    if line.strip()
]


@pytest.mark.parametrize("payload", PAYLOADS, ids=[p["id"] for p in PAYLOADS])
def test_payload_is_blocked(payload: dict, pipeline) -> None:
    """Each adversarial payload must be blocked or transformed; never passed."""
    pipeline.client = AsyncMock()
    result = pipeline.process_input_sync(payload["attack_string"])
    sanitised, violations = result
    assert sanitised is None or any(v["type"] == "injection" for v in violations), (
        f"payload {payload['id']} leaked: expected block, got pass"
    )
