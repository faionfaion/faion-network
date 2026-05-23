#!/usr/bin/env python3
"""validate-framework-decomposition-patterns.py

Validate a per-file decomposition report JSON against schema + pattern-framework rule.

Inputs:
    --file PATH      path to report JSON
    --self-test      run built-in valid + invalid fixtures
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

ID_RE = re.compile(r"^fdp-[a-z0-9-]{6,}$")
FRAMEWORKS = {"django", "rails", "laravel", "react", "nextjs", "generic"}
FILE_TYPES = {"view", "controller", "model", "component", "route", "service", "form"}
PATTERNS = {"service-layer", "selector", "dto", "query-object", "action", "custom-hook", "extract-helper", "split-by-domain"}
VERDICTS = {"propose-extraction", "block-no-coverage", "block-pattern-not-applicable", "skip-already-small"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

PATTERN_BY_FRAMEWORK = {
    "django":  {"service-layer", "query-object", "dto", "selector", "extract-helper", "split-by-domain"},
    "rails":   {"service-layer", "query-object", "dto", "selector", "extract-helper", "split-by-domain"},
    "laravel": {"service-layer", "query-object", "dto", "selector", "extract-helper", "split-by-domain"},
    "react":   {"custom-hook", "selector", "action", "extract-helper", "split-by-domain"},
    "nextjs":  {"custom-hook", "selector", "action", "extract-helper", "split-by-domain"},
    "generic": PATTERNS,
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "file_path", "framework", "file_type", "current_loc", "proposed_pattern", "target_loc", "coverage_or_plan", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^fdp-[a-z0-9-]{6,}$")

    fw = obj.get("framework")
    if fw not in FRAMEWORKS:
        errs.append(f"framework must be one of {sorted(FRAMEWORKS)}")
    if obj.get("file_type") not in FILE_TYPES:
        errs.append(f"file_type must be one of {sorted(FILE_TYPES)}")
    pat = obj.get("proposed_pattern")
    if pat not in PATTERNS:
        errs.append(f"proposed_pattern must be one of {sorted(PATTERNS)}")

    if fw in PATTERN_BY_FRAMEWORK and pat not in PATTERN_BY_FRAMEWORK[fw]:
        errs.append(f"proposed_pattern '{pat}' does not apply to framework '{fw}'")

    cl = obj.get("current_loc")
    tl = obj.get("target_loc")
    if not isinstance(cl, int) or cl < 100:
        errs.append("current_loc must be int >= 100")
    if not isinstance(tl, int) or not (1 <= tl <= 200):
        errs.append("target_loc must be int in [1,200]")
    if isinstance(cl, int) and isinstance(tl, int) and tl > cl:
        errs.append("target_loc must be <= current_loc (decomposition cannot grow the file)")

    if not isinstance(obj.get("coverage_or_plan"), str) or len(obj.get("coverage_or_plan", "")) < 5:
        errs.append("coverage_or_plan must be non-empty string (min 5 chars)")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "propose-extraction":
        if not str(obj.get("coverage_or_plan", "")).strip():
            errs.append("verdict=propose-extraction requires coverage_or_plan")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "fdp-order-views-py",
    "file_path": "src/orders/views.py",
    "framework": "django",
    "file_type": "view",
    "current_loc": 487,
    "proposed_pattern": "service-layer",
    "target_loc": 150,
    "coverage_or_plan": "tests/test_views.py (89% branch)",
    "ai_context_savings_tokens": 8500,
    "verdict": "propose-extraction",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "decomp",
    "file_path": "src/orders/views.py",
    "framework": "phoenix",
    "file_type": "thing",
    "current_loc": 60,
    "proposed_pattern": "service-layer",
    "target_loc": 800,
    "coverage_or_plan": "",
    "verdict": "propose-extraction",
    "version": "1.0",
    "last_reviewed": "today",
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
    ap.add_argument("--file", type=str, help="path to report JSON")
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
