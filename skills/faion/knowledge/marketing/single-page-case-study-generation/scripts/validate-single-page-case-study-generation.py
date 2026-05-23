#!/usr/bin/env python3
"""validate-single-page-case-study-generation.py

Validate an artefact produced by the `single-page-case-study-generation` methodology against the
schema declared in `content/02-output-contract.xml`.

Inputs:
    --file PATH       path to artefact JSON file
    --self-test       run built-in fixtures (pass + fail) and report
    --help            print this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def _err(errs: list, msg: str) -> None:
    errs.append(msg)


def validate(obj: dict) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]

    for k in ("artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed"):
        if k not in obj:
            _err(errs, f"missing required field: {k}")

    v = obj.get("version", "")
    if v and not SEMVER.match(v):
        _err(errs, f"version: not semver ({v!r})")

    d = obj.get("last_reviewed", "")
    if d and not ISO_DATE.match(d):
        _err(errs, f"last_reviewed: not ISO date ({d!r})")

    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        _err(errs, f"owner: not a named human ({owner!r})")

    inputs = obj.get("inputs_used", [])
    if not isinstance(inputs, list) or len(inputs) < 1:
        _err(errs, "inputs_used: must be a non-empty list")

    rationale = obj.get("rationale", "")
    if isinstance(rationale, str) and len(rationale) < 30:
        _err(errs, "rationale: must be >=30 chars and cite at least one input")

    return errs


_OK_FIXTURE = {
    "artefact_id": "single-page-case-study-generation-2026-05-23-01",
    "owner": "Anna Schmidt",
    "decision": "ship the canonical artefact for this client cycle",
    "rationale": "Anchored to discovery notes (call 2026-05-21) and current rate card; precondition checklist passed.",
    "inputs_used": ["discovery-notes-2026-05-21.md", "rate-card-2026-Q2.yaml"],
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

_BAD_FIXTURE = {
    "artefact_id": "x",
    "owner": "team",
    "decision": "tbd",
    "rationale": "obviously",
    "inputs_used": [],
    "version": "1",
    "last_reviewed": "yesterday",
}


def self_test() -> int:
    ok_errs = validate(_OK_FIXTURE)
    if ok_errs:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {ok_errs}\n")
        return 1
    bad_errs = validate(_BAD_FIXTURE)
    if not bad_errs:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
        sys.stderr.write(f"invalid JSON: {e}\n")
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
