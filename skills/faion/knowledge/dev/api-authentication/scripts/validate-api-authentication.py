#!/usr/bin/env python3
"""validate-api-authentication.py

Validate the api-authentication artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (OK + BAD)
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

REQUIRED = ('spec_id', 'scheme', 'audience', 'access_token_ttl_seconds', 'revocation_path')


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sch = obj.get("scheme")
    aud = obj.get("audience")
    ttl = obj.get("access_token_ttl_seconds", 0)
    rev = obj.get("revocation_path", "")
    if sch == "jwt" and aud == "b2c-browser":
        if ttl > 900:
            errs.append("scheme=jwt + audience=b2c-browser requires ttl <= 900 (jwt-not-for-b2c-session)")
    if not isinstance(rev, str) or len(rev) < 8:
        errs.append("revocation_path empty or too short (revocation-path-required)")
    if sch == "api-key":
        cad = obj.get("key_rotation_cadence_days", 9999)
        if not isinstance(cad, int) or cad > 90:
            errs.append("api-key rotation cadence must be <= 90 days (api-key-rotation-cadence)")
    return errs


def _load_smoke():
    p = Path(__file__).resolve().parent.parent / "templates" / "_smoke-test.json"
    obj = json.loads(p.read_text())
    obj.pop("__faion_header__", None)
    return obj


def self_test() -> int:
    ok = _load_smoke()
    errs_ok = validate(ok)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    bad = {}
    if not validate(bad):
        sys.stderr.write("empty BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
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
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
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
