#!/usr/bin/env python3
"""validate-guardrails-testing.py — validate guardrail-test-report.json.

Inputs: --file PATH | --self-test | --help
Exit codes: 0 valid; 1 invalid; 2 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_TOP = ["artefact_id", "version", "last_reviewed", "system_under_test", "suites", "verdict"]
REQUIRED_SUITES = ["security", "accuracy", "perf"]
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    if obj.get("verdict") not in {"pass", "fail"}:
        errs.append("verdict not in {pass,fail}")
    sut = obj.get("system_under_test", {})
    if not isinstance(sut, dict) or "name" not in sut or "version" not in sut:
        errs.append("system_under_test.name/version missing")
    suites = obj.get("suites", {})
    for k in REQUIRED_SUITES:
        if k not in suites:
            errs.append(f"suites.{k} missing")
    sec = suites.get("security", {})
    if not all(k in sec for k in ("payloads_total", "blocked", "leaked")):
        errs.append("suites.security incomplete")
    acc = suites.get("accuracy", {})
    if not all(k in acc for k in ("legit_total", "passed", "false_positive_rate", "fp_budget")):
        errs.append("suites.accuracy incomplete")
    perf = suites.get("perf", {})
    if not all(k in perf for k in ("p50_ms", "p99_ms", "throughput_rps", "baseline_p99_ms")):
        errs.append("suites.perf incomplete")
    return errs


VALID_FIX = {
    "artefact_id": "x", "version": "1.0.0", "last_reviewed": "2026-05-22",
    "system_under_test": {"name": "s", "version": "1.0"},
    "suites": {
        "security": {"payloads_total": 1, "blocked": 1, "leaked": 0},
        "accuracy": {"legit_total": 1, "passed": 1, "false_positive_rate": 0.0, "fp_budget": 0.01},
        "perf": {"p50_ms": 1.0, "p99_ms": 2.0, "throughput_rps": 100.0, "baseline_p99_ms": 2.0},
    },
    "verdict": "pass",
}
INVALID_FIX: dict = {}


def self_test() -> int:
    if validate(VALID_FIX):
        sys.stderr.write("valid rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
