#!/usr/bin/env python3
"""validate-characterization-test-recipes.py

Validate a characterization suite-manifest JSON against the schema + rule consistency.

Inputs:
    --file PATH      path to manifest JSON
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

ID_RE = re.compile(r"^ctr-[a-z0-9-]{6,}$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ORIGINS = {"production-sample", "spec-edge", "regression-test", "synthetic"}
VERDICTS = {"wrap-refactor", "block-insufficient-coverage", "block-no-signoff", "block-bug-on-purpose", "skip-deleting-code"}
COVERAGE_GATE = 70.0


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "module_under_test", "capture_branch_sha", "fixtures", "normalizer_path", "branch_coverage_pct", "baseline_signoff", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^ctr-[a-z0-9-]{6,}$")
    if "capture_branch_sha" in obj and not SHA_RE.match(str(obj["capture_branch_sha"])):
        errs.append("capture_branch_sha must be a git sha (7-40 hex chars)")

    fixtures = obj.get("fixtures")
    if not isinstance(fixtures, list) or len(fixtures) < 1:
        errs.append("fixtures must be a non-empty list")
    else:
        for i, f in enumerate(fixtures):
            for sub in ("id", "origin", "capture_date", "redacted"):
                if sub not in f:
                    errs.append(f"fixtures[{i}] missing {sub}")
            if f.get("origin") not in ORIGINS:
                errs.append(f"fixtures[{i}].origin must be one of {sorted(ORIGINS)}")
            if f.get("redacted") is False:
                errs.append(f"fixtures[{i}].redacted=false — redact before commit")

    if not isinstance(obj.get("normalizer_path"), str) or not obj.get("normalizer_path").strip():
        errs.append("normalizer_path must be non-empty string")

    cov = obj.get("branch_coverage_pct")
    if not isinstance(cov, (int, float)) or not (0 <= cov <= 100):
        errs.append("branch_coverage_pct must be number in [0,100]")

    signoff = obj.get("baseline_signoff") or {}
    if not isinstance(signoff, dict):
        errs.append("baseline_signoff must be an object")
    else:
        for sub in ("reviewer", "signed_off_at", "snapshot_commit_sha"):
            if sub not in signoff:
                errs.append(f"baseline_signoff.{sub} missing")
        if "signed_off_at" in signoff and not DATE_RE.match(str(signoff["signed_off_at"])):
            errs.append("baseline_signoff.signed_off_at must be ISO date")
        if "snapshot_commit_sha" in signoff and not SHA_RE.match(str(signoff["snapshot_commit_sha"])):
            errs.append("baseline_signoff.snapshot_commit_sha must be a git sha")

    if obj.get("ci_auto_update_disabled") is False:
        errs.append("ci_auto_update_disabled=false (r5 violation)")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "wrap-refactor":
        if isinstance(cov, (int, float)) and cov < COVERAGE_GATE:
            errs.append(f"verdict=wrap-refactor requires branch_coverage_pct >= {COVERAGE_GATE}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "ctr-billing-engine",
    "module_under_test": "src/billing/engine.py",
    "capture_branch_sha": "a1b2c3d",
    "fixtures": [{"id": "prod-001", "origin": "production-sample", "capture_date": "2026-05-20", "redacted": True}],
    "normalizer_path": "tests/characterization/normalize.py",
    "branch_coverage_pct": 87.4,
    "baseline_signoff": {"reviewer": "ruslan@faion.net", "signed_off_at": "2026-05-22", "snapshot_commit_sha": "c3d4e5f"},
    "ci_auto_update_disabled": True,
    "verdict": "wrap-refactor",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "ctr",
    "module_under_test": "billing",
    "capture_branch_sha": "main",
    "fixtures": [],
    "normalizer_path": "",
    "branch_coverage_pct": 42,
    "baseline_signoff": {"reviewer": "team", "signed_off_at": "today", "snapshot_commit_sha": "xx"},
    "ci_auto_update_disabled": False,
    "verdict": "wrap-refactor",
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
    ap.add_argument("--file", type=str, help="path to manifest JSON")
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
