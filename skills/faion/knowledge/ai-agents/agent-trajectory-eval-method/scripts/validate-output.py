#!/usr/bin/env python3
"""validate-output.py — validate an agent-trajectory-eval report.

Inputs: path to JSON report. Exit 0 valid; 1 violations.
Exit codes: 0,1,2,3.
"""
from __future__ import annotations
import json, re, sys
from datetime import date, datetime
from pathlib import Path

def metric_ok(m):
    return isinstance(m, dict) and all(isinstance(m.get(k), (int, float)) for k in ("mean","ci_low","ci_high"))

def validate(p):
    v = []
    for k in ["report_id","golden_set_version","n_examples","agent_version",
              "system_efficiency","session_quality","node_precision",
              "judge_calibration_date","cost_usd","owner","version","produced_at"]:
        if k not in p: v.append(f"missing {k}")
    if v: return v

    if p["n_examples"] < 30:
        v.append("f3: n_examples < 30")
    for layer, fields in [
        ("system_efficiency", ["latency_ms","tokens","tool_calls"]),
        ("session_quality", ["trajectory_exact_match","trajectory_precision","trajectory_recall"]),
        ("node_precision", ["tool_selection_accuracy","param_accuracy"]),
    ]:
        for f in fields:
            m = p[layer].get(f)
            if not metric_ok(m):
                v.append(f"f1/f2: {layer}.{f} must be {{mean,ci_low,ci_high}}")
    try:
        cal = date.fromisoformat(p["judge_calibration_date"])
        if (date.today() - cal).days > 90:
            v.append("f4: judge_calibration_date > 90 days old")
    except Exception:
        v.append("judge_calibration_date must be ISO date")
    if not isinstance(p["cost_usd"], (int,float)) or p["cost_usd"] < 0:
        v.append("f5: cost_usd missing/negative")
    if str(p["owner"]).strip().lower() in {"team","we","us","tbd",""}:
        v.append("owner must be named")
    if not re.fullmatch(r"\d+\.\d+\.\d+", p["version"]):
        v.append("version must be semver")
    return v

def main(argv):
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__); return 0
    if "--self-test" in argv:
        good = {"report_id":"r1","golden_set_version":"g1","n_examples":30,
                "agent_version":"a@1","system_efficiency":{k:{"mean":1,"ci_low":0,"ci_high":2} for k in ["latency_ms","tokens","tool_calls"]},
                "session_quality":{k:{"mean":1,"ci_low":0,"ci_high":1} for k in ["trajectory_exact_match","trajectory_precision","trajectory_recall"]},
                "node_precision":{k:{"mean":1,"ci_low":0,"ci_high":1} for k in ["tool_selection_accuracy","param_accuracy"]},
                "judge_calibration_date": date.today().isoformat(),
                "cost_usd":1.0,"owner":"qa@faion.net","version":"1.0.0","produced_at":"2026-05-22T10:00:00Z"}
        vs = validate(good)
        if vs: sys.stderr.write(f"FAIL: {vs}\n"); return 1
        sys.stdout.write("self-test passed\n"); return 0
    if len(argv) < 2:
        sys.stderr.write("usage: validate-output.py <report.json>\n"); return 2
    try: payload = json.loads(Path(argv[1]).read_text())
    except Exception as e: sys.stderr.write(f"load: {e}\n"); return 3
    vs = validate(payload)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
