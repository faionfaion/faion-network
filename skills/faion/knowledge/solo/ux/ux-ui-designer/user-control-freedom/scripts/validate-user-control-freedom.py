#!/usr/bin/env python3
"""validate-user-control-freedom.py - stdlib-only validator for the user-control-freedom output artefact.

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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "actions", "focus_trap_verified"]
REVERSIBILITY = {"reversible", "soft-reversible", "irreversible"}
EXIT_MECH = {"x-button", "escape-key", "click-outside", "back-button", "none"}
ACTION_REQ = ["screen", "action", "reversibility", "undo_available", "cancel_available", "exit_mechanism", "recovery_method", "severity", "fix_direction"]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "the team"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
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
        if not actions:
            errs.append("actions must be non-empty")
        for i, a in enumerate(actions):
            if not isinstance(a, dict):
                errs.append(f"actions[{i}] not object")
                continue
            for k in ACTION_REQ:
                if k not in a:
                    errs.append(f"actions[{i}] missing {k}")
            rev = a.get("reversibility")
            if rev and rev not in REVERSIBILITY:
                errs.append(f"actions[{i}].reversibility not in enum: {rev!r}")
            sev = a.get("severity")
            if isinstance(sev, int) and not 0 <= sev <= 3:
                errs.append(f"actions[{i}].severity out of [0,3]: {sev}")
            em = a.get("exit_mechanism") or []
            for x in em:
                if x not in EXIT_MECH:
                    errs.append(f"actions[{i}].exit_mechanism entry not in enum: {x!r}")
            # critical: irreversible + no undo + no cancel → severity must be 1
            if rev == "irreversible" and a.get("undo_available") is False and a.get("cancel_available") is False:
                if sev != 1:
                    errs.append(f"actions[{i}] irreversible+no-undo+no-cancel must be severity 1")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "control-audit-settings-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "focus_trap_verified": True,
    "actions": [{
        "screen": "/settings/account",
        "action": "delete-account",
        "reversibility": "irreversible",
        "undo_available": False,
        "cancel_available": True,
        "exit_mechanism": ["x-button", "escape-key", "click-outside"],
        "recovery_method": "support contact within 30 days",
        "severity": 0,
        "fix_direction": "OK",
    }],
})
BAD_JSON = json.dumps({
    "owner": "we",
    "focus_trap_verified": False,
    "actions": [{
        "screen": "/x",
        "action": "delete-forever",
        "reversibility": "irreversible",
        "undo_available": False,
        "cancel_available": False,
        "exit_mechanism": ["none"],
        "recovery_method": "",
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
