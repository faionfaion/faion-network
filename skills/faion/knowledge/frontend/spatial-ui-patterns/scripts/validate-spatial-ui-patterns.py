#!/usr/bin/env python3
"""validate-spatial-ui-patterns.py

Validate a Spatial UI Patterns artefact against the JSON Schema (draft-07) defined in
`content/02-output-contract.xml`. Stdlib-only; no external pip deps.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable / parse error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "artefact_id",
    "feature_id",
    "anchoring_strategy",
    "window_layout",
    "platform_targets",
    "hig_compliance",
    "motion_sickness_mitigation",
    "evidence",
    "owner",
    "status",
    "last_touched",
    "template_version"
]

FORBIDDEN_OWNERS = {"team", "us", "tbd", "n/a", "everyone", "all", "design", "engineering", "design-team", "design team", ""}

ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append(f"owner is a generic group: {owner!r}")
    last_touched = obj.get("last_touched")
    if isinstance(last_touched, str) and not ISO_DATETIME.match(last_touched):
        errs.append("last_touched is not ISO-8601 datetime")
    tv = obj.get("template_version")
    if isinstance(tv, str) and not SEMVER.match(tv):
        errs.append("template_version is not semver")
    status = obj.get("status")
    if isinstance(status, str) and status not in {"draft", "ready_for_review", "approved", "archived"}:
        errs.append(f"status not in allowed enum: {status!r}")
    evidence = obj.get("evidence")
    if evidence is not None and isinstance(evidence, list) and len(evidence) == 0:
        errs.append("evidence array is empty")
    return errs


OK = {'owner': 'draft', 'last_touched': '2026-05-23T12:00:00Z', 'template_version': '1.1.0', 'artefact_id': 'spatial-ui-patterns-2026-05-23', 'feature_id': 'draft', 'anchoring_strategy': 'draft', 'window_layout': 'draft', 'platform_targets': ['draft-item'], 'hig_compliance': 'draft', 'motion_sickness_mitigation': 'draft', 'evidence': [{'source': 'https://example.com/source-1', 'citation': 'verbatim quote from source'}], 'status': 'ready_for_review'}

BAD = {"foo": "bar"}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"self-test FAIL: valid fixture rejected: {validate(OK)!r}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
        sys.stderr.write(f"JSON parse error: {e}\n")
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
