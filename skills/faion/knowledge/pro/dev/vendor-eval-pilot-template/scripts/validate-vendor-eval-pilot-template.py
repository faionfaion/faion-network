#!/usr/bin/env python3
"""validate-vendor-eval-pilot-template.py

Validate the artefact produced by the `vendor-eval-pilot-template` methodology against the
JSON Schema defined in `content/02-output-contract.xml`.

This validator uses stdlib only (no pyyaml/pydantic) for portability.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "owner", "title", "sections", "rationale", "inputs_used", "version", "last_reviewed"]
FORBIDDEN_PLACEHOLDERS = {"TBD", "TODO", "FIXME"}
FORBIDDEN_OWNERS = {"team", "we", "us", "tbd", ""}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.\-]+)?$")


def _scan(value, errors, path):
    if isinstance(value, str):
        if value.strip() in FORBIDDEN_PLACEHOLDERS:
            errors.append(f"placeholder value at {path}: {value!r}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan(item, errors, f"{path}[{i}]")
    elif isinstance(value, dict):
        for k, v in value.items():
            _scan(v, errors, f"{path}.{k}")


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append("owner must be a single named person/role, not 'team' / 'we' / 'us' / 'TBD'")
    version = obj.get("version")
    if isinstance(version, str) and not SEMVER_RE.match(version):
        errs.append(f"version not semver: {version!r}")
    _scan(obj, errs, "$")
    return errs


OK = json.loads(r"""{
  "artefact_id": "vendor-eval-pilot-template-2026Q2-001",
  "owner": "ruslan@faion.net",
  "title": "Example spec for vendor-eval-pilot-template",
  "sections": [
    {
      "name": "Constraints",
      "body": "Quoted client mandate."
    },
    {
      "name": "Options",
      "body": "≥2 options within mandate."
    }
  ],
  "rationale": "Closes the gap surfaced by the parent skill — input artefact 'task-brief.md' explicitly names the constraint set; output ties decisions to rule r1.",
  "inputs_used": [
    "task-brief.md",
    "constitution.md"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23"
}""")
BAD = json.loads(r"""{
  "artefact_id": "",
  "owner": "team",
  "version": "latest"
}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
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
