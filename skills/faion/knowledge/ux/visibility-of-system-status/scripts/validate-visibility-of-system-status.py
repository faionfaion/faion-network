#!/usr/bin/env python3
"""validate-visibility-of-system-status.py - stdlib-only validator for the visibility-of-system-status output artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK / BAD fixtures
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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "actions"]
DURATION = {"instant", "short", "medium", "long"}
LOADING = {"spinner", "skeleton", "progress-indeterminate", "progress-determinate", "none"}
ARIA = {"polite", "assertive", "off", "status", "none"}
ACTION_REQ = ["screen", "action", "duration_class", "loading_state", "success_state", "error_state", "trigger_disabled", "aria_live", "severity", "fix_direction"]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "the team"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    actions = obj.get("actions", [])
    if isinstance(actions, list):
        for i, a in enumerate(actions):
            if not isinstance(a, dict):
                errs.append(f"actions[{i}] not object")
                continue
            for k in ACTION_REQ:
                if k not in a:
                    errs.append(f"actions[{i}] missing {k}")
            dc = a.get("duration_class")
            if dc and dc not in DURATION:
                errs.append(f"actions[{i}].duration_class not in enum: {dc!r}")
            ls = a.get("loading_state")
            if ls and ls not in LOADING:
                errs.append(f"actions[{i}].loading_state not in enum: {ls!r}")
            al = a.get("aria_live")
            if al and al not in ARIA:
                errs.append(f"actions[{i}].aria_live not in enum: {al!r}")
            err_state = a.get("error_state") or {}
            if isinstance(err_state, dict):
                if err_state.get("present") and err_state.get("auto_dismiss"):
                    errs.append(f"actions[{i}] error_state auto-dismiss is forbidden")
            # medium/long without loading_state is forbidden
            if dc in ("medium", "long") and ls == "none":
                errs.append(f"actions[{i}] {dc} duration with loading_state=none")
            # non-instant async with active trigger is forbidden
            if dc and dc != "instant" and a.get("trigger_disabled") is False:
                errs.append(f"actions[{i}] {dc} async with trigger_disabled=false")
            sev = a.get("severity")
            if isinstance(sev, int) and not 0 <= sev <= 3:
                errs.append(f"actions[{i}].severity out of [0,3]: {sev}")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "status-audit-checkout-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "actions": [{
        "screen": "/checkout",
        "action": "pay-now",
        "duration_class": "medium",
        "loading_state": "spinner",
        "success_state": True,
        "error_state": {"present": True, "auto_dismiss": False},
        "trigger_disabled": True,
        "aria_live": "polite",
        "severity": 0,
        "fix_direction": "OK",
    }],
})
BAD_JSON = json.dumps({
    "owner": "team",
    "actions": [{
        "screen": "/x",
        "action": "y",
        "duration_class": "medium",
        "loading_state": "none",
        "success_state": False,
        "error_state": {"present": True, "auto_dismiss": True},
        "trigger_disabled": False,
        "aria_live": "assertive",
        "severity": 0,
        "fix_direction": "fine",
    }],
})


def self_test() -> int:
    ok = json.loads(OK_JSON)
    if validate(ok):
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(validate(ok)) + "\n")
        return 1
    bad = json.loads(BAD_JSON)
    if not validate(bad):
        sys.stderr.write("self-test FAIL: BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in OK / BAD fixtures")
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
        sys.stderr.write(f"not valid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
