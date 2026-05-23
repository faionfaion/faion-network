#!/usr/bin/env python3
"""validate-api-error-handling.py

Validate the api-error-handling artefact against the schema declared in
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

REQUIRED = ('catalogue_id', 'envelope_shape', 'errors', 'traceid_field')


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("envelope_shape") != "rfc-7807":
        errs.append("envelope_shape must be rfc-7807 (rfc-7807-envelope)")
    errs_arr = obj.get("errors") or []
    for i, e in enumerate(errs_arr):
        if not isinstance(e, dict):
            continue
        status = e.get("status", 0)
        cls = e.get("class")
        if isinstance(status, int):
            if 400 <= status < 500 and cls != "client":
                errs.append(f"errors[{i}] 4xx must have class=client (4xx-vs-5xx-split)")
            if 500 <= status < 600 and cls != "server":
                errs.append(f"errors[{i}] 5xx must have class=server (4xx-vs-5xx-split)")
        t = e.get("type", "")
        if not (isinstance(t, str) and t.startswith("http")):
            errs.append(f"errors[{i}].type must be a URI (stable-type-uri)")
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
