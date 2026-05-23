#!/usr/bin/env python3
"""validate-csharp-dotnet.py

Validate the project-skeleton manifest for the csharp-dotnet methodology against
the JSON Schema declared in 02-output-contract.xml.

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
import sys
from pathlib import Path

REQUIRED = [
    "project_name",
    "target_framework",
    "feature_folders",
    "di_lifetimes",
    "uses_problem_details",
    "cancellation_token_audit",
]
ALLOWED_TFM = {"net8.0", "net9.0"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    name = obj.get("project_name", "")
    if not (isinstance(name, str) and name[:1].isupper() and name.replace("_", "").isalnum()):
        errs.append("project_name must be PascalCase")
    if obj.get("target_framework") not in ALLOWED_TFM:
        errs.append(f"target_framework must be one of {sorted(ALLOWED_TFM)}")
    ff = obj.get("feature_folders") or []
    if not isinstance(ff, list) or len(ff) < 1:
        errs.append("feature_folders must be non-empty list")
    di = obj.get("di_lifetimes") or {}
    if di.get("DbContext") != "Scoped":
        errs.append("di_lifetimes.DbContext must be 'Scoped'")
    if di.get("BackgroundServices") != "Singleton":
        errs.append("di_lifetimes.BackgroundServices must be 'Singleton'")
    if obj.get("uses_problem_details") is not True:
        errs.append("uses_problem_details must be true")
    cta = obj.get("cancellation_token_audit") or {}
    if cta.get("controllers_pass") is not True:
        errs.append("cancellation_token_audit.controllers_pass must be true")
    if cta.get("services_pass") is not True:
        errs.append("cancellation_token_audit.services_pass must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "project_name": "BillingApi",
    "target_framework": "net8.0",
    "feature_folders": ["Features/Invoices"],
    "di_lifetimes": {"DbContext": "Scoped", "BackgroundServices": "Singleton"},
    "uses_problem_details": True,
    "cancellation_token_audit": {"controllers_pass": True, "services_pass": True},
    "forbidden_patterns_found": [],
}
BAD = {
    "project_name": "billing_api",
    "target_framework": "net6.0",
    "feature_folders": [],
    "di_lifetimes": {"DbContext": "Singleton", "BackgroundServices": "Singleton"},
    "uses_problem_details": False,
    "cancellation_token_audit": {"controllers_pass": False, "services_pass": True},
    "forbidden_patterns_found": [".Result"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
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
