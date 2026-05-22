#!/usr/bin/env python3
"""validate-bug-report-quality-rubric.py

Validate a bug-report-quality-rubric output JSON against the schema.

Inputs:
    --file PATH      path to JSON to validate
    --self-test      run built-in fixture (pass + fail)
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_VERDICTS = {
    "accept",
    "block-need-repro",
    "block-need-evidence",
    "block-need-ai-context",
    "block-need-env",
}
ID_RE = re.compile(r"^brq-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DIM_KEYS_REQUIRED = {"title", "repro", "expected_vs_actual", "environment", "severity", "priority", "evidence"}
DIM_MAX = {"title": 10, "repro": 20, "expected_vs_actual": 15, "environment": 15, "severity": 10, "priority": 10, "evidence": 10, "ai_context": 10}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "ticket_ref", "verdict", "score", "dimensions", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^brq-[a-z0-9-]{6,}$")
    if "verdict" in obj and obj["verdict"] not in ALLOWED_VERDICTS:
        errs.append(f"verdict must be one of {sorted(ALLOWED_VERDICTS)}")
    if "score" in obj:
        s = obj["score"]
        if not isinstance(s, int) or not (0 <= s <= 100):
            errs.append("score must be int in [0,100]")
        if obj.get("verdict") == "accept" and isinstance(s, int) and s < 70:
            errs.append("verdict=accept requires score >= 70")
    dims = obj.get("dimensions") or {}
    if not isinstance(dims, dict):
        errs.append("dimensions must be an object")
    else:
        missing = DIM_KEYS_REQUIRED - dims.keys()
        if missing:
            errs.append(f"dimensions missing keys: {sorted(missing)}")
        for k, v in dims.items():
            if k not in DIM_MAX:
                errs.append(f"unknown dimension key: {k}")
                continue
            if not isinstance(v, int) or not (0 <= v <= DIM_MAX[k]):
                errs.append(f"dimensions.{k} must be int in [0,{DIM_MAX[k]}]")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    if obj.get("is_ai_feature") and "ai_context" not in dims:
        errs.append("is_ai_feature=true requires dimensions.ai_context")
    fixes = obj.get("field_fixes") or []
    if not isinstance(fixes, list):
        errs.append("field_fixes must be a list")
    else:
        for i, fx in enumerate(fixes):
            for k in ("field", "issue", "suggested_fix"):
                if k not in fx:
                    errs.append(f"field_fixes[{i}] missing {k}")
    return errs


VALID_FIXTURE = {
    "artefact_id": "brq-issue-4421",
    "ticket_ref": "https://github.com/org/repo/issues/4421",
    "verdict": "accept",
    "score": 88,
    "dimensions": {"title": 9, "repro": 18, "expected_vs_actual": 14, "environment": 14, "severity": 9, "priority": 9, "evidence": 8, "ai_context": 7},
    "field_fixes": [],
    "is_ai_feature": True,
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}

INVALID_FIXTURE = {
    "artefact_id": "bad",
    "ticket_ref": "x",
    "verdict": "accept",
    "score": 35,
    "dimensions": {"title": 5},
    "version": "1.0",
    "last_reviewed": "yesterday",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to rubric JSON")
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
