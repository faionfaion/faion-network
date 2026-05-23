#!/usr/bin/env python3
"""validate-contract-first-development.py

Validate the spec artefact metadata for the contract-first-development methodology
against the JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "spec_id",
    "openapi_version",
    "info_version",
    "paths_count",
    "schemas_count",
    "lint_passed",
    "diff_check",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
OAS3 = re.compile(r"^3\.[0-9]+\.[0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "spec_id" in obj and (not isinstance(obj["spec_id"], str) or len(obj["spec_id"]) < 3):
        errs.append("spec_id must be string >= 3 chars")
    if "openapi_version" in obj and not OAS3.match(str(obj["openapi_version"])):
        errs.append("openapi_version must match ^3\\.[0-9]+\\.[0-9]+$")
    if "info_version" in obj and not SEMVER.match(str(obj["info_version"])):
        errs.append("info_version must be semver MAJOR.MINOR.PATCH")
    if "paths_count" in obj and (not isinstance(obj["paths_count"], int) or obj["paths_count"] < 1):
        errs.append("paths_count must be int >= 1")
    if "schemas_count" in obj and (not isinstance(obj["schemas_count"], int) or obj["schemas_count"] < 1):
        errs.append("schemas_count must be int >= 1")
    if "lint_passed" in obj and not isinstance(obj["lint_passed"], bool):
        errs.append("lint_passed must be boolean")
    if "diff_check" in obj:
        dc = obj["diff_check"]
        if not isinstance(dc, dict) or "breaking" not in dc or "additive" not in dc:
            errs.append("diff_check must be object with breaking + additive")
        else:
            if not isinstance(dc.get("breaking"), int) or dc["breaking"] < 0:
                errs.append("diff_check.breaking must be int >= 0")
            if not isinstance(dc.get("additive"), int) or dc["additive"] < 0:
                errs.append("diff_check.additive must be int >= 0")
    return errs


OK = {
    "spec_id": "payments-api",
    "openapi_version": "3.1.0",
    "info_version": "1.4.0",
    "paths_count": 12,
    "schemas_count": 18,
    "lint_passed": True,
    "diff_check": {"breaking": 0, "additive": 2},
    "validated_at": "2026-05-23T10:00:00Z",
}
BAD = {
    "spec_id": "x",
    "openapi_version": "2.0.0",
    "info_version": "1.4",
    "paths_count": 0,
    "lint_passed": "no",
}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
