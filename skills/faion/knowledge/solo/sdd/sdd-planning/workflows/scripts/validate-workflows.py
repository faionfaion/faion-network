#!/usr/bin/env python3
"""validate-workflows.py — stdlib-only validator for the workflows route-record artefact.

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

REQUIRED = [
    "artefact_id", "owner", "version", "last_reviewed",
    "feature_dir", "active_phase", "next_methodology", "phase_statuses",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PHASES = {"spec", "design", "plan", "execution", "done", "blocked"}
PHASE_STATUS = {"missing", "Draft", "Accepted"}
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}
STUB_PATHS = {"placeholder", "placeholder/path", ""}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", [], {}):
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
    ap = obj.get("active_phase", "")
    if isinstance(ap, str) and ap and ap not in PHASES:
        errs.append(f"active_phase not in {sorted(PHASES)}: {ap!r}")
    nm = obj.get("next_methodology", "")
    if isinstance(nm, str) and nm.strip().lower() in STUB_PATHS:
        errs.append(f"next_methodology is stub: {nm!r} (r5-next-methodology-resolvable)")
    ps = obj.get("phase_statuses", {})
    if isinstance(ps, dict):
        for key in ("spec", "design", "plan"):
            if key not in ps:
                errs.append(f"phase_statuses.{key} missing")
            elif ps[key] not in PHASE_STATUS:
                errs.append(f"phase_statuses.{key} not in {sorted(PHASE_STATUS)}: {ps[key]!r}")
    if ap == "blocked":
        blocker = obj.get("blocker")
        if not (isinstance(blocker, str) and blocker.strip()):
            errs.append("active_phase=blocked requires a non-empty blocker (r4-blocker-naming)")
    return errs


OK_JSON = (
    '{"artefact_id":"route-jwt-refresh","owner":"Ruslan Faion <ruslan@faion.net>",'
    '"version":"1.0.0","last_reviewed":"2026-05-23",'
    '"feature_dir":".aidocs/features/in-progress/jwt-refresh/",'
    '"active_phase":"design",'
    '"next_methodology":"solo/sdd/sdd-planning/workflow-design-phase",'
    '"phase_statuses":{"spec":"Accepted","design":"missing","plan":"missing"},'
    '"blocker":null}'
)
BAD_JSON = (
    '{"owner":"team","active_phase":"unknown","next_methodology":"placeholder/path",'
    '"phase_statuses":{}}'
)


def self_test() -> int:
    ok = json.loads(OK_JSON)
    res = validate(ok)
    if res:
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(res) + "\n")
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
