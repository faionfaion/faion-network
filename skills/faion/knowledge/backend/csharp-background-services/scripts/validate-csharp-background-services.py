#!/usr/bin/env python3
"""validate-csharp-background-services.py — validate a worker-spec artefact against the 02-output-contract schema.

Flags:
  --file PATH   Path to the artefact JSON to validate (also accepted positionally).
  --self-test   Run an internal fixture-based smoke test and exit.
  --help        Print usage and exit (provided by argparse).

Exit codes:
  0 — input passes the schema and forbidden-pattern checks.
  1 — input fails; violations printed to stderr.
  2 — usage / file error.

Dependencies: stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "worker_class",
    "channel",
    "scope_strategy",
    "stopping_token_propagated",
    "exception_handling",
    "health_check",
    "owner",
    "version",
    "last_reviewed",
]
CLASS_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Service$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FULL_MODES = {"Wait", "DropOldest", "DropNewest"}
SCOPE_STRATS = {"create-scope-per-item", "no-scoped-deps"}
SCHEDULE_KINDS = {"periodic-timer", "queue-driven", "poll-loop"}
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "worker_class" in obj and not CLASS_RE.match(str(obj["worker_class"])):
        errs.append("worker_class must be PascalCase ending in 'Service'")
    if obj.get("base_class") and obj["base_class"] != "BackgroundService":
        errs.append("base_class must be 'BackgroundService' (not IHostedService)")
    ch = obj.get("channel") or {}
    if ch.get("mode") == "bounded":
        if not isinstance(ch.get("capacity"), int) or ch["capacity"] < 1:
            errs.append("channel.capacity must be int >= 1 when mode=bounded")
        if ch.get("full_mode") not in FULL_MODES:
            errs.append(f"channel.full_mode must be one of {sorted(FULL_MODES)}")
    sched = obj.get("schedule") or {}
    if sched:
        if sched.get("kind") not in SCHEDULE_KINDS:
            errs.append(f"schedule.kind must be one of {sorted(SCHEDULE_KINDS)}")
        if sched.get("kind") == "periodic-timer":
            period = sched.get("period_seconds")
            if not isinstance(period, int) or period < 1:
                errs.append("schedule.period_seconds must be int >= 1 for periodic-timer")
    if obj.get("scope_strategy") not in SCOPE_STRATS:
        errs.append(f"scope_strategy must be one of {sorted(SCOPE_STRATS)}")
    if obj.get("stopping_token_propagated") is not True:
        errs.append("stopping_token_propagated must be true")
    if obj.get("exception_handling") != "try-catch-per-item":
        errs.append("exception_handling must be 'try-catch-per-item'")
    hc = obj.get("health_check") or {}
    if "registered" not in hc:
        errs.append("health_check.registered required")
    rules = obj.get("rules_checked")
    if rules is not None and (not isinstance(rules, list) or not rules):
        errs.append("rules_checked must be a non-empty array of rule ids when present")
    owner = str(obj.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        errs.append(f"forbidden owner value: {owner!r} (must be a named human or role-with-rotation)")
    version = obj.get("version", "")
    if version and not SEMVER.match(str(version)):
        errs.append(f"version not semver: {version!r}")
    reviewed = obj.get("last_reviewed", "")
    if reviewed and not DATE_RE.match(str(reviewed)):
        errs.append(f"last_reviewed not an ISO date: {reviewed!r}")
    return errs


OK = {
    "worker_class": "OrderProcessorService",
    "base_class": "BackgroundService",
    "channel": {"mode": "bounded", "capacity": 1000, "full_mode": "Wait"},
    "schedule": {"kind": "queue-driven"},
    "scope_strategy": "create-scope-per-item",
    "stopping_token_propagated": True,
    "exception_handling": "try-catch-per-item",
    "log_scope_per_item": True,
    "health_check": {"registered": True, "stale_after_seconds": 300},
    "rules_checked": ["extend-backgroundservice", "bounded-channel"],
    "owner": "ruslan@faion.net",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}
BAD = {
    "worker_class": "orderWorker",
    "base_class": "IHostedService",
    "channel": {"mode": "bounded", "capacity": 0, "full_mode": "Nope"},
    "scope_strategy": "no-scoped-deps",
    "stopping_token_propagated": False,
    "exception_handling": "try-catch-per-item",
    "health_check": {},
    "owner": "team",
    "version": "draft",
    "last_reviewed": "yesterday",
}


def self_test() -> int:
    errs = validate(OK)
    if errs:
        sys.stderr.write(f"self-test FAIL on valid doc: {errs}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid doc passed\n")
        return 1
    sys.stdout.write("self-test ok\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="validate-csharp-background-services.py",
        description="Validate a csharp-background-services worker spec against 02-output-contract. "
                    "Exit 0 on pass, 1 on fail, 2 on usage error.",
    )
    ap.add_argument("path", nargs="?", help="Path to the JSON file to validate")
    ap.add_argument("--file", dest="file", help="Path to the JSON file to validate")
    ap.add_argument("--self-test", action="store_true",
                    help="Run an internal fixture-based smoke test and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    target = args.file or args.path
    if not target:
        ap.print_help(sys.stderr)
        return 2
    p = Path(target)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"json parse error: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
