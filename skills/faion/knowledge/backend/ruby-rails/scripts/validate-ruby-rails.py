#!/usr/bin/env python3
"""validate-ruby-rails.py

Validate the Rails-app manifest for the ruby-rails methodology against the
JSON Schema declared in 02-output-contract.xml.

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

REQUIRED = ["rails_version", "ruby_version", "service_result_class_count", "services", "sidekiq_jobs"]
RAILS_RE = re.compile(r"^(7|8)\.")
RUBY_RE = re.compile(r"^3\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not RAILS_RE.match(str(obj.get("rails_version", ""))):
        errs.append("rails_version must be 7.x or 8.x")
    if not RUBY_RE.match(str(obj.get("ruby_version", ""))):
        errs.append("ruby_version must start with 3.")
    if obj.get("service_result_class_count") != 1:
        errs.append("service_result_class_count must be exactly 1")
    services = obj.get("services") or []
    if not isinstance(services, list) or len(services) < 1:
        errs.append("services must be non-empty list")
    for i, s in enumerate(services):
        if not str(s.get("class", "")).endswith("Service"):
            errs.append(f"services[{i}].class must end with 'Service'")
        if s.get("returns_service_result") is not True:
            errs.append(f"services[{i}].returns_service_result must be true")
        if s.get("accepts_params_kwarg") is not True:
            errs.append(f"services[{i}].accepts_params_kwarg must be true")
    for i, j in enumerate(obj.get("sidekiq_jobs") or []):
        if not str(j.get("class", "")).endswith("Job"):
            errs.append(f"sidekiq_jobs[{i}].class must end with 'Job'")
        if j.get("args_are_primitives") is not True:
            errs.append(f"sidekiq_jobs[{i}].args_are_primitives must be true")
        if not isinstance(j.get("retry"), int) or j.get("retry", 0) < 1:
            errs.append(f"sidekiq_jobs[{i}].retry must be >= 1")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "rails_version": "7.1",
    "ruby_version": "3.3",
    "service_result_class_count": 1,
    "services": [{"class": "Users::CreateService", "returns_service_result": True, "accepts_params_kwarg": True}],
    "sidekiq_jobs": [{"class": "Users::SendWelcomeJob", "args_are_primitives": True, "retry": 5}],
    "forbidden_patterns_found": [],
}
BAD = {
    "rails_version": "5.2",
    "ruby_version": "2.7",
    "service_result_class_count": 4,
    "services": [{"class": "UserManager", "returns_service_result": False, "accepts_params_kwarg": False}],
    "sidekiq_jobs": [{"class": "SendWelcome", "args_are_primitives": False, "retry": 0}],
    "forbidden_patterns_found": ["deliver_later inside transaction"],
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
