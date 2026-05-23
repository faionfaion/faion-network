#!/usr/bin/env python3
"""validate-compliance-control-matrix-soc2-gdpr.py

Validate a compliance-control-matrix-soc2-gdpr output artefact against the JSON Schema in
content/02-output-contract.xml (mirrored in templates/compliance-control-matrix-soc2-gdpr.json).

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (no external file needed)
    --help            this message

Outputs:
    stdout "OK" on success; stderr "VIOLATION: <reason>" on failure.

Exit codes:
    0 = valid
    1 = invalid (one or more violations)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ARTEFACT_ID = re.compile(r"^[a-z][a-z0-9-]+$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and isinstance(obj["artefact_id"], str):
        if not ARTEFACT_ID.match(obj["artefact_id"]):
            errs.append("artefact_id must match ^[a-z][a-z0-9-]+$")
    if "owner" in obj and isinstance(obj["owner"], str):
        if obj["owner"].strip().lower() in FORBIDDEN_OWNERS:
            errs.append("owner must be a named human or role, not a plural pronoun")
        elif len(obj["owner"].strip()) < 3:
            errs.append("owner must be at least 3 chars")
    if "rationale" in obj and isinstance(obj["rationale"], str):
        if len(obj["rationale"].strip()) < 30:
            errs.append("rationale must be at least 30 chars (cite inputs)")
    if "inputs_used" in obj:
        iu = obj["inputs_used"]
        if not isinstance(iu, list) or len(iu) < 1:
            errs.append("inputs_used must be a non-empty list")
        else:
            for i, row in enumerate(iu):
                if not isinstance(row, dict) or "name" not in row or "source" not in row:
                    errs.append(f"inputs_used[{i}] missing name/source")
    if "version" in obj and isinstance(obj["version"], str):
        if not SEMVER.match(obj["version"]):
            errs.append("version must be semver (e.g. 1.0.0)")
    if "last_reviewed" in obj and isinstance(obj["last_reviewed"], str):
        if not DATE.match(obj["last_reviewed"]):
            errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    if "produces" in obj and obj["produces"] != "spec":
        errs.append("produces must equal 'spec' for this methodology")
    return errs


GOOD = {
    "artefact_id": "compliance-control-matrix-soc2-gdpr-2026-05-23-001",
    "owner": "alice@example.com",
    "decision": "Adopt option A per rule r1-bound-scope.",
    "rationale": "Driven by parent-activity-context (last sprint events) and owner-roster (CODEOWNERS).",
    "inputs_used": [
        {"name": "parent-activity-context", "source": "repo://docs/parent.md"},
        {"name": "owner-roster", "source": "repo://CODEOWNERS"}
    ],
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "produces": "spec",
}
BAD = {"artefact_id": "X", "owner": "team", "inputs_used": []}


def self_test() -> int:
    if validate(GOOD):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON — {e}\n")
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
