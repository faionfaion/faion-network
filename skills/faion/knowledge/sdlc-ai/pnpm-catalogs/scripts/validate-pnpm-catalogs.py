#!/usr/bin/env python3
"""validate-pnpm-catalogs.py — validate the pnpm catalog artefact.

Inputs:
    --file PATH       path to artefact (JSON; pnpm-workspace.yaml can be parsed via yq first)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["packages", "catalog", "ci_filter"]

VALID_FIXTURE = {
    "packages": ["packages/*", "apps/*"],
    "catalog": {"react": "^19.0.0", "typescript": "^5.7.0", "vitest": "^3.0.0"},
    "catalogs": {"next": {"react": "19.1.0-canary"}},
    "ci_filter": "pnpm --filter '...[origin/main]' test",
    "publish_step_replaces_protocol": True,
}

INVALID_FIXTURE = {
    "packages": [],
    "catalog": {},
    "ci_filter": "pnpm test",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    pkgs = obj.get("packages", [])
    if not isinstance(pkgs, list) or len(pkgs) < 2:
        errs.append("packages: must be array with minItems 2")
    cat = obj.get("catalog", {})
    if not isinstance(cat, dict) or len(cat) < 1:
        errs.append("catalog: must be object with minProperties 1")
    cf = obj.get("ci_filter", "")
    if not isinstance(cf, str) or "origin/main" not in cf:
        errs.append("ci_filter: must contain 'origin/main'")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
