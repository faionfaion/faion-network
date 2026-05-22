"""test_accuracy.py.
purpose: accuracy suite — legit inputs must pass; FP rate ≤ budget
consumes: tests/legitimate.jsonl + FP_BUDGET env
produces: pytest report
depends-on: pytest
token-budget-impact: +150t.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

FP_BUDGET = float(os.environ.get("FP_BUDGET", "0.01"))
LEGIT = [
    json.loads(line)
    for line in Path(__file__).parent.joinpath("legitimate.jsonl").read_text().splitlines()
    if line.strip()
]


def test_false_positive_rate_under_budget(pipeline) -> None:
    blocked = 0
    for item in LEGIT:
        sanitised, violations = pipeline.process_input_sync(item["text"])
        if sanitised is None or any(v["type"] in {"injection", "moderation"} for v in violations):
            blocked += 1
    fp = blocked / len(LEGIT)
    assert fp <= FP_BUDGET, f"FP rate {fp:.3f} exceeds budget {FP_BUDGET}"


@pytest.mark.parametrize("item", LEGIT[:50], ids=lambda x: x.get("id", "x"))
def test_individual_legit_passes(item: dict, pipeline) -> None:
    sanitised, violations = pipeline.process_input_sync(item["text"])
    blocking = [v for v in violations if v["type"] in {"injection", "moderation"}]
    assert sanitised is not None and not blocking, f"legit '{item.get('id')}' wrongly blocked"
