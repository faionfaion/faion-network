"""_smoke-test.py.
purpose: emit a minimum-viable guardrail-test-report.json
consumes: fake counts (no actual pipeline run)
produces: stdout JSON
depends-on: stdlib only
token-budget-impact: +60t.
"""
from __future__ import annotations

import json

report = {
    "artefact_id": "gtr-smoke-2026-05",
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
    "system_under_test": {"name": "smoke", "version": "0.0.1", "model": "mock"},
    "suites": {
        "security": {"payloads_total": 10, "blocked": 10, "leaked": 0},
        "accuracy": {"legit_total": 20, "passed": 20, "false_positive_rate": 0.0, "fp_budget": 0.01},
        "perf": {"p50_ms": 5, "p99_ms": 20, "throughput_rps": 200, "baseline_p99_ms": 25},
    },
    "verdict": "pass",
}
print(json.dumps(report, indent=2))
