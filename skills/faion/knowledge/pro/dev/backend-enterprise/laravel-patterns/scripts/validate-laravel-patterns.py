#!/usr/bin/env python3
"""validate-laravel-patterns.py

Validate the Laravel-patterns manifest for the laravel-patterns methodology
against the JSON Schema declared in 02-output-contract.xml.

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
    "laravel_version",
    "php_version",
    "uses_form_requests",
    "prevent_lazy_loading_enabled",
    "queue_jobs",
    "api_resources",
]
LARAVEL_RE = re.compile(r"^(10|11)\.")
PHP_RE = re.compile(r"^8\.(2|3|4)")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not LARAVEL_RE.match(str(obj.get("laravel_version", ""))):
        errs.append("laravel_version must be 10.x or 11.x")
    if not PHP_RE.match(str(obj.get("php_version", ""))):
        errs.append("php_version must be 8.2, 8.3, or 8.4")
    if obj.get("uses_form_requests") is not True:
        errs.append("uses_form_requests must be true")
    if obj.get("prevent_lazy_loading_enabled") is not True:
        errs.append("prevent_lazy_loading_enabled must be true")
    for i, j in enumerate(obj.get("queue_jobs") or []):
        if j.get("implements_should_be_unique") is not True:
            errs.append(f"queue_jobs[{i}].implements_should_be_unique must be true")
    for i, r in enumerate(obj.get("api_resources") or []):
        if not str(r.get("class", "")).endswith("Resource"):
            errs.append(f"api_resources[{i}].class must end with 'Resource'")
        if r.get("uses_explicit_fields") is not True:
            errs.append(f"api_resources[{i}].uses_explicit_fields must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "laravel_version": "11.0",
    "php_version": "8.3",
    "uses_form_requests": True,
    "prevent_lazy_loading_enabled": True,
    "queue_jobs": [{"class": "App\\Jobs\\ChargeInvoice", "implements_should_be_unique": True}],
    "api_resources": [{"class": "App\\Http\\Resources\\InvoiceResource", "uses_explicit_fields": True}],
    "forbidden_patterns_found": [],
}
BAD = {
    "laravel_version": "8.0",
    "php_version": "7.4",
    "uses_form_requests": False,
    "prevent_lazy_loading_enabled": False,
    "queue_jobs": [{"class": "ChargeInvoice", "implements_should_be_unique": False}],
    "api_resources": [{"class": "InvoiceResource", "uses_explicit_fields": False}],
    "forbidden_patterns_found": ["$request->all()"],
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
