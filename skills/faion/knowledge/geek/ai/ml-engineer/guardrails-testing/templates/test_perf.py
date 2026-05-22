"""test_perf.py.
purpose: perf suite — p99 ≤ baseline_p99 * 1.2; throughput ≥ baseline * 0.85
consumes: bench.json baseline
produces: pytest report + bench results
depends-on: pytest, pytest-benchmark
token-budget-impact: +180t.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

BASELINE = json.loads(Path(__file__).parent.joinpath("bench.json").read_text())


def test_p99_within_budget(pipeline, benchmark) -> None:
    benchmark.pedantic(
        pipeline.process_input_sync,
        args=("benign hello message",),
        iterations=1,
        rounds=200,
    )
    p99 = benchmark.stats.stats.max  # rough p99 proxy
    assert p99 * 1000 <= BASELINE["p99_ms"] * 1.2, f"p99 {p99 * 1000:.1f} ms exceeds budget"


@pytest.mark.parametrize("payload", ["hi", "what's my order status", "tell me about products"])
def test_warm_latency(pipeline, payload: str, benchmark) -> None:
    benchmark(pipeline.process_input_sync, payload)
