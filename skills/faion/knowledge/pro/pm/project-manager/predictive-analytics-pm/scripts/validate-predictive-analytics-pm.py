#!/usr/bin/env python3
"""validate-predictive-analytics-pm.py

Validate a spec artefact for Predictive Analytics for PM against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['model_id', 'model_version', 'feature_spec_version', 'training_corpus_size', 'calibration', 'forecasts']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", str(obj.get("model_version", ""))):
        errs.append(f"model_version pattern invalid: {obj.get('model_version')!r}")
    if not isinstance(obj.get("training_corpus_size"), int) or obj["training_corpus_size"] < 30:
        errs.append(f"training_corpus_size {obj.get('training_corpus_size')} < 30")
    cal = obj.get("calibration") or {}
    for k in ("last_checked", "brier_score", "pi80_coverage", "pi95_coverage"):
        if k not in cal:
            errs.append(f"calibration.{k} missing")
    cov80 = cal.get("pi80_coverage")
    if isinstance(cov80, (int, float)) and not (0.7 <= cov80 <= 0.9):
        errs.append(f"calibration.pi80_coverage {cov80} outside [0.7, 0.9]")
    fc = obj.get("forecasts") or []
    if not isinstance(fc, list) or not fc:
        errs.append("forecasts must be non-empty")
    else:
        for i, f in enumerate(fc):
            for k in ("project_id", "risk_dimension", "point_estimate",
                      "pi_80", "pi_95", "top_features"):
                if k not in f:
                    errs.append(f"forecasts[{i}].{k} missing")
            if isinstance(f.get("top_features"), list) and len(f["top_features"]) < 3:
                errs.append(f"forecasts[{i}].top_features must have >=3 entries")

    return errs


GOOD = {'model_id': 'm1', 'model_version': '1.2.0', 'feature_spec_version': 'v3', 'training_corpus_size': 142, 'calibration': {'last_checked': '2026-05-01', 'brier_score': 0.18, 'pi80_coverage': 0.79, 'pi95_coverage': 0.94}, 'forecasts': [{'project_id': 'p1', 'risk_dimension': 'schedule_slip_weeks', 'point_estimate': 2.4, 'pi_80': [1.0, 4.0], 'pi_95': [0.5, 6.0], 'top_features': [{'feature': 'f1', 'contribution': 0.3}, {'feature': 'f2', 'contribution': 0.2}, {'feature': 'f3', 'contribution': 0.1}]}]}
BAD = {'model_id': 'x', 'model_version': '1.0', 'feature_spec_version': '', 'training_corpus_size': 12, 'calibration': {}, 'forecasts': [{'project_id': 'x'}]}


def self_test():
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
