#!/usr/bin/env python3
"""validate-php-laravel-patterns.py

Validate the layered-Laravel manifest for the php-laravel-patterns methodology
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
import sys
from pathlib import Path

REQUIRED = [
    "controllers",
    "services",
    "uses_form_requests",
    "uses_json_resources",
    "uses_db_transaction_closure",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    controllers = obj.get("controllers") or []
    if not isinstance(controllers, list) or len(controllers) < 1:
        errs.append("controllers must be non-empty list")
    for i, c in enumerate(controllers):
        if not str(c.get("class", "")).endswith("Controller"):
            errs.append(f"controllers[{i}].class must end with 'Controller'")
        if c.get("contains_eloquent") is not False:
            errs.append(f"controllers[{i}].contains_eloquent must be false")
        if not isinstance(c.get("loc"), int) or c.get("loc", 0) > 150:
            errs.append(f"controllers[{i}].loc must be <= 150")
    services = obj.get("services") or []
    if not isinstance(services, list) or len(services) < 1:
        errs.append("services must be non-empty list")
    for i, s in enumerate(services):
        if not str(s.get("class", "")).endswith("Service"):
            errs.append(f"services[{i}].class must end with 'Service'")
        if s.get("uses_request_globals") is not False:
            errs.append(f"services[{i}].uses_request_globals must be false")
        if s.get("returns_jsonresponse") is not False:
            errs.append(f"services[{i}].returns_jsonresponse must be false")
    if obj.get("uses_form_requests") is not True:
        errs.append("uses_form_requests must be true")
    if obj.get("uses_json_resources") is not True:
        errs.append("uses_json_resources must be true")
    if obj.get("uses_db_transaction_closure") is not True:
        errs.append("uses_db_transaction_closure must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "controllers": [{"class": "App\\Http\\Controllers\\UserController", "contains_eloquent": False, "loc": 84}],
    "services": [{"class": "App\\Services\\UserService", "uses_request_globals": False, "returns_jsonresponse": False}],
    "uses_form_requests": True,
    "uses_json_resources": True,
    "uses_db_transaction_closure": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "controllers": [{"class": "UserController", "contains_eloquent": True, "loc": 410}],
    "services": [{"class": "UserManager", "uses_request_globals": True, "returns_jsonresponse": True}],
    "uses_form_requests": False,
    "uses_json_resources": False,
    "uses_db_transaction_closure": False,
    "forbidden_patterns_found": ["User::query() in controller"],
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
