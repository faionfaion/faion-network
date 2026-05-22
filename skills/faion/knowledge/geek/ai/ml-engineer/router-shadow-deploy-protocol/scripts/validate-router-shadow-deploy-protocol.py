#!/usr/bin/env python3
"""validate-router-shadow-deploy-protocol.py — validate shadow-report.yaml.

Inputs:
    --file PATH    YAML or JSON file
    --self-test    Run built-in fixtures
    --help         Show this message

Exit codes:
    0  valid
    1  invalid
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["candidate_id", "baseline_router_id", "window_start", "window_end",
            "judge", "metrics", "gate_evaluation", "decision"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    judge = obj.get("judge", {})
    if isinstance(judge, dict):
        if judge.get("sme_agreement", 0) < 0.85:
            errs.append("judge.sme_agreement must be >= 0.85 (calibration gate)")
    metrics = obj.get("metrics", {})
    if isinstance(metrics, dict):
        if metrics.get("cost_delta_mean", float("inf")) > 1.10:
            # not a failure of schema, but flag
            pass
        if metrics.get("schema_parity_min_daily", 0) < 1.0:
            errs.append("schema_parity_min_daily must be 1.0 (r4-schema-parity-100)")
    gate = obj.get("gate_evaluation", {})
    if isinstance(gate, dict):
        for k in ("scoring_gate", "cost_gate", "schema_gate"):
            if gate.get(k) not in ("PASS", "FAIL"):
                errs.append(f"gate_evaluation.{k} must be PASS or FAIL")
    if obj.get("decision") not in ("GO", "NO-GO"):
        errs.append("decision must be GO or NO-GO")
    # consistency: if any gate FAIL, decision MUST be NO-GO
    if isinstance(gate, dict) and any(gate.get(k) == "FAIL" for k in ("scoring_gate", "cost_gate", "schema_gate")):
        if obj.get("decision") == "GO":
            errs.append("decision=GO inconsistent with FAIL gate (r1-zero-user-impact)")
    return errs


FIXTURE_VALID = """
candidate_id: router-v2-rc2
baseline_router_id: router-v1
window_start: "2026-04-25"
window_end: "2026-05-02"
judge: {model: claude-sonnet-4-5, prompt_version: judge-v3, sme_agreement: 0.89}
metrics:
  scoring_delta_median: -0.008
  cost_delta_mean: 0.97
  schema_parity_min_daily: 1.00
gate_evaluation: {scoring_gate: PASS, cost_gate: PASS, schema_gate: PASS}
decision: GO
"""

FIXTURE_INVALID = """
candidate_id: x
baseline_router_id: y
window_start: "2026-04-25"
window_end: "2026-05-02"
judge: {model: m, prompt_version: v, sme_agreement: 0.5}
metrics:
  scoring_delta_median: 0.01
  cost_delta_mean: 1.34
  schema_parity_min_daily: 0.91
gate_evaluation: {scoring_gate: PASS, cost_gate: FAIL, schema_gate: FAIL}
decision: GO
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n")
        return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n")
        return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required for YAML input")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-router-shadow-deploy-protocol",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
