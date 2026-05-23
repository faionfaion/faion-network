#!/usr/bin/env python3
"""validate-billing-rollout-coordination-checklist.py

Validate a Billing Rollout Coordination Checklist `checklist` artefact against the JSON Schema in
content/02-output-contract.xml + the forbidden-pattern rules.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

REQUIRED = ['artefact_id', 'owner', 'decision', 'rationale', 'inputs_used', 'version', 'last_reviewed', 'items']
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]+$")


def _is_iso_date(value: str) -> bool:
    try:
        _dt.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for key in REQUIRED:
        if key not in obj:
            errs.append(f"missing required field: {key}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append(f"forbidden owner value: {owner!r} (must be a named handle / email / role)")
    artefact_id = obj.get("artefact_id")
    if isinstance(artefact_id, str) and not SLUG_RE.match(artefact_id):
        errs.append(f"artefact_id must be kebab-case: {artefact_id!r}")
    version = obj.get("version")
    if isinstance(version, str) and not SEMVER_RE.match(version):
        errs.append(f"version must be semver: {version!r}")
    last_reviewed = obj.get("last_reviewed")
    if isinstance(last_reviewed, str):
        if not _is_iso_date(last_reviewed):
            errs.append(f"last_reviewed must be ISO date: {last_reviewed!r}")
        else:
            today = _dt.date.today()
            if _dt.date.fromisoformat(last_reviewed) > today:
                errs.append("last_reviewed cannot be in the future")
    inputs_used = obj.get("inputs_used")
    decision = obj.get("decision")
    if isinstance(inputs_used, list):
        if not inputs_used and decision != "no-op":
            errs.append("inputs_used is empty AND decision is not 'no-op'")
        for idx, entry in enumerate(inputs_used):
            if not isinstance(entry, dict) or "name" not in entry or "source" not in entry:
                errs.append(f"inputs_used[{idx}] must be an object with name + source")
    rationale = obj.get("rationale")
    if isinstance(rationale, str) and isinstance(inputs_used, list) and inputs_used:
        if not any(isinstance(e, dict) and e.get("name") and e["name"] in rationale for e in inputs_used):
            errs.append("rationale must cite at least one entry from inputs_used by name")
    if isinstance(decision, str) and not decision.strip():
        errs.append("decision must be non-empty")
    return errs


OK_FIXTURE = json.loads("{\"artefact_id\": \"billing-rollout-coordination-checklist-2026-05-23-acme\", \"owner\": \"ruslan@faion.net\", \"decision\": \"Proceed with the agreed plan per inputs.\", \"rationale\": \"Decision rests on engagement-notes-2026-05-22 and baseline-2026-05-15; both inputs corroborate the same direction.\", \"inputs_used\": [{\"name\": \"engagement-notes-2026-05-22\", \"source\": \"wiki://pm/acme/notes.md\"}], \"version\": \"1.0.0\", \"last_reviewed\": \"2026-05-23\", \"items\": [{\"text\": \"Comms reviewed\", \"done\": true, \"owner\": \"ruslan@faion.net\", \"due_by\": \"2026-05-22\"}]}")
BAD_FIXTURE = json.loads("{\"artefact_id\": \"BAD\", \"owner\": \"team\"}")


def self_test() -> int:
    ok_errs = validate(OK_FIXTURE)
    if ok_errs:
        sys.stderr.write("self-test FAIL: OK fixture rejected\n")
        for e in ok_errs:
            sys.stderr.write(f"  - {e}\n")
        return 1
    bad_errs = validate(BAD_FIXTURE)
    if not bad_errs:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"json parse error: {exc}\n")
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
