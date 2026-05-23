#!/usr/bin/env python3
"""validate-ai-code-review-checklist.py

Validate the per-PR AI-code-review JSON against schema + verdict-aggregation rule.

Inputs:
    --file PATH      path to review-decision JSON
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

ID_RE = re.compile(r"^aicr-[a-z0-9-]{6,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CHECK_KEYS = (
    "c01-hallucinated-imports", "c02-silent-skip-tests", "c03-convention-drift", "c04-supply-chain",
    "c05-secret-exposure", "c06-deferred-debt", "c07-error-handling-coverage", "c08-overscoped-changes",
    "c09-test-quality", "c10-perf-regression", "c11-deferred-impl", "c12-ai-disclosure",
)
CHECK_VALUES = {"approve", "approve-with-note", "request-changes", "block"}
VERDICTS = {"approve", "request-changes", "block"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "pr_ref", "ai_pct_lines", "checks", "verdict", "reviewer_email", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^aicr-[a-z0-9-]{6,}$")

    ai = obj.get("ai_pct_lines")
    if not isinstance(ai, int) or not (0 <= ai <= 100):
        errs.append("ai_pct_lines must be int in [0,100]")

    checks = obj.get("checks") or {}
    if not isinstance(checks, dict):
        errs.append("checks must be an object")
    else:
        for k in CHECK_KEYS:
            if k not in checks:
                errs.append(f"checks.{k} missing")
            elif checks[k] not in CHECK_VALUES:
                errs.append(f"checks.{k}={checks[k]} not in {sorted(CHECK_VALUES)}")
        if all(k in checks for k in CHECK_KEYS):
            verdict = obj.get("verdict")
            has_block = any(checks[k] == "block" for k in CHECK_KEYS)
            has_rc    = any(checks[k] == "request-changes" for k in CHECK_KEYS)
            if has_block and verdict != "block":
                errs.append("any check=block requires aggregate verdict=block")
            elif (not has_block) and has_rc and verdict != "request-changes":
                errs.append("any request-changes (no block) requires aggregate verdict=request-changes")
            elif (not has_block) and (not has_rc) and verdict != "approve":
                errs.append("all checks approve/approve-with-note requires aggregate verdict=approve")
            if verdict == "block" and not obj.get("block_reason"):
                errs.append("verdict=block requires non-empty block_reason")

    em = str(obj.get("reviewer_email", ""))
    if em and not EMAIL_RE.match(em):
        errs.append("reviewer_email must be valid email")
    if em.split("@", 1)[0].lower() in TEAM_ALIASES:
        errs.append("reviewer_email is a team alias")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "aicr-pr-483",
    "pr_ref": "https://github.com/org/repo/pull/483",
    "ai_pct_lines": 62,
    "checks": {k: "approve" for k in CHECK_KEYS},
    "verdict": "approve",
    "reviewer_email": "ruslan@faion.net",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "pr483",
    "pr_ref": "pr 483",
    "ai_pct_lines": 80,
    "checks": {"c01-hallucinated-imports": "block"},
    "verdict": "approve",
    "reviewer_email": "team@faion.net",
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
    ap.add_argument("--file", type=str, help="path to review-decision JSON")
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
