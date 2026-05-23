#!/usr/bin/env python3
"""validate-regression-eval-before-fix-rule.py — validate the decision-record artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["incident_id", "eval_case_path", "fix_pr", "root_cause_class", "ci_required_check_id", "verdict"]
ROOT_CAUSE_ENUM = {"prompt", "tool", "model", "context-assembly", "rag-retrieval", "vendor-outage", "user-input"}
VERDICT_ENUM = {"flipped", "no-flip", "regressed-others", "no-fix-transient", "no-fix-vendor"}

VALID_FIXTURE = {
    "incident_id": "INC-441",
    "eval_case_path": "eval/regressions/INC-441.jsonl",
    "fix_pr": "https://github.com/org/repo/pull/482",
    "root_cause_class": "prompt",
    "ci_required_check_id": "eval-suite",
    "verdict": "flipped",
}

INVALID_FIXTURE = {
    "incident_id": "INC-441",
    "eval_case_path": "TBD",
    "fix_pr": "",
    "verdict": "passed",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ecp = obj.get("eval_case_path", "")
    if not isinstance(ecp, str) or not ecp.endswith(".jsonl"):
        errs.append("eval_case_path: must end with .jsonl")
    pr = obj.get("fix_pr", "")
    if not isinstance(pr, str) or not pr:
        errs.append("fix_pr: must be non-empty string")
    rc = obj.get("root_cause_class")
    if rc not in ROOT_CAUSE_ENUM and "root_cause_class" in obj:
        errs.append(f"root_cause_class: {rc!r} not in {sorted(ROOT_CAUSE_ENUM)}")
    v = obj.get("verdict")
    if v not in VERDICT_ENUM:
        errs.append(f"verdict: {v!r} not in {sorted(VERDICT_ENUM)}")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
