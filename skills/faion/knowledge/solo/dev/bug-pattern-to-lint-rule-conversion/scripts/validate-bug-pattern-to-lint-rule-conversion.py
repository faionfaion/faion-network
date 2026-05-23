#!/usr/bin/env python3
"""validate-bug-pattern-to-lint-rule-conversion.py

Validate a decision-record JSON against the schema and rule consistency.

Inputs:
    --file PATH      path to decision-record JSON
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

ID_RE = re.compile(r"^bplrc-[a-z0-9-]{6,}$")
PATTERN_ID_RE = re.compile(r"^[a-z][a-z0-9-]{3,63}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
DETECTOR_KINDS = {"ruff", "eslint", "regex", "ast-visitor", "test-name", "shellcheck", "custom"}
VERDICTS = {"record-and-wire", "block-low-recurrence", "block-no-detector", "block-fp-too-high"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FP_GATE = 5.0


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "pattern_id", "ticket_refs", "detector", "fix", "owner_email", "fp_rate_pct", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^bplrc-[a-z0-9-]{6,}$")
    if "pattern_id" in obj and not PATTERN_ID_RE.match(str(obj["pattern_id"])):
        errs.append("pattern_id must match ^[a-z][a-z0-9-]{3,63}$")

    tr = obj.get("ticket_refs")
    if not isinstance(tr, list) or len(tr) < 3:
        errs.append("ticket_refs must be a list of at least 3 entries")

    det = obj.get("detector") or {}
    if not isinstance(det, dict):
        errs.append("detector must be an object")
    else:
        if det.get("kind") not in DETECTOR_KINDS:
            errs.append(f"detector.kind must be one of {sorted(DETECTOR_KINDS)}")
        if not isinstance(det.get("definition"), str) or not det.get("definition").strip():
            errs.append("detector.definition must be non-empty string")

    if not isinstance(obj.get("fix"), str) or not obj.get("fix").strip():
        errs.append("fix must be non-empty string")

    em = str(obj.get("owner_email", ""))
    if em and not EMAIL_RE.match(em):
        errs.append("owner_email must be a valid email")
    local = em.split("@", 1)[0].lower() if "@" in em else em.lower()
    if local in TEAM_ALIASES:
        errs.append(f"owner_email is a team alias ({local}); use a named human")

    fp = obj.get("fp_rate_pct")
    if not isinstance(fp, (int, float)) or not (0 <= fp <= 100):
        errs.append("fp_rate_pct must be number in [0,100]")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "record-and-wire":
        if isinstance(fp, (int, float)) and fp > FP_GATE:
            errs.append(f"verdict=record-and-wire requires fp_rate_pct <= {FP_GATE}")
        if isinstance(tr, list) and len(tr) < 3:
            errs.append("verdict=record-and-wire requires ticket_refs >= 3")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "bplrc-print-in-prod",
    "pattern_id": "no-print-statements",
    "ticket_refs": ["BUG-101", "BUG-114", "BUG-129", "BUG-141"],
    "detector": {"kind": "ruff", "definition": "select=T201", "rule_id": "T201"},
    "fix": "Replace print() with logger.info()",
    "owner_email": "ruslan@faion.net",
    "fp_rate_pct": 1.3,
    "wired_into_pre_commit": True,
    "verdict": "record-and-wire",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "lint",
    "pattern_id": "X",
    "ticket_refs": ["BUG-101"],
    "detector": {"kind": "checklist", "definition": "look for print"},
    "fix": "be careful",
    "owner_email": "team@faion.net",
    "fp_rate_pct": 18,
    "verdict": "record-and-wire",
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
    ap.add_argument("--file", type=str, help="path to decision-record JSON")
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
