#!/usr/bin/env python3
"""validate-ruby-rails-patterns.py

Validate the Rails-patterns manifest for the ruby-rails-patterns methodology
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

REQUIRED = ["service_result_class_count", "services", "verify_authorized_enabled", "ci_gates"]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("service_result_class_count") != 1:
        errs.append("service_result_class_count must be exactly 1")
    services = obj.get("services") or []
    if not isinstance(services, list) or len(services) < 1:
        errs.append("services must be non-empty list")
    for i, s in enumerate(services):
        if not str(s.get("class", "")).endswith("Service"):
            errs.append(f"services[{i}].class must end with 'Service'")
        for k in ("params_kwarg", "current_user_kwarg", "returns_service_result"):
            if s.get(k) is not True:
                errs.append(f"services[{i}].{k} must be true")
    if obj.get("verify_authorized_enabled") is not True:
        errs.append("verify_authorized_enabled must be true")
    gates = obj.get("ci_gates") or {}
    for g in ("bullet", "brakeman", "bundler_audit"):
        if gates.get(g) is not True:
            errs.append(f"ci_gates.{g} must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "service_result_class_count": 1,
    "services": [{"class": "Users::CreateService", "params_kwarg": True, "current_user_kwarg": True, "returns_service_result": True}],
    "verify_authorized_enabled": True,
    "ci_gates": {"bullet": True, "brakeman": True, "bundler_audit": True},
    "forbidden_patterns_found": [],
}
BAD = {
    "service_result_class_count": 4,
    "services": [{"class": "UserManager", "params_kwarg": False, "current_user_kwarg": False, "returns_service_result": False}],
    "verify_authorized_enabled": False,
    "ci_gates": {"bullet": False, "brakeman": False, "bundler_audit": False},
    "forbidden_patterns_found": ["duplicate ServiceResult"],
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
