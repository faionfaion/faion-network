#!/usr/bin/env python3
"""validate-usability-testing.py - stdlib-only validator for the usability-testing output artefact.

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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "scope", "segments", "tasks", "findings"]
TASK_REQ = ["scenario", "success_criterion"]
FIND_REQ = ["observation", "inference", "task_ref", "participants_blocked", "participants_observed", "severity", "human_reviewed"]
INSTRUCTION_WORDS = ("click ", "tap ", "navigate to ", "press ")
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
    segments = obj.get("segments", [])
    if isinstance(segments, list):
        if not segments:
            errs.append("segments must be non-empty")
        for i, s in enumerate(segments):
            if not isinstance(s, dict) or "name" not in s or "n" not in s:
                errs.append(f"segments[{i}] missing name/n")
    tasks = obj.get("tasks", [])
    if isinstance(tasks, list):
        if not 3 <= len(tasks) <= 5:
            errs.append(f"tasks count {len(tasks)} not in [3,5]")
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                errs.append(f"tasks[{i}] not object")
                continue
            for k in TASK_REQ:
                if k not in t or t[k] in (None, ""):
                    errs.append(f"tasks[{i}] missing or empty {k}")
            scen = t.get("scenario", "")
            if isinstance(scen, str) and any(w in scen.lower() for w in INSTRUCTION_WORDS):
                errs.append(f"tasks[{i}].scenario uses instruction phrasing")
    findings = obj.get("findings", [])
    if isinstance(findings, list):
        for i, f in enumerate(findings):
            if not isinstance(f, dict):
                errs.append(f"findings[{i}] not object")
                continue
            for k in FIND_REQ:
                if k not in f:
                    errs.append(f"findings[{i}] missing {k}")
            sev = f.get("severity")
            if isinstance(sev, int) and not 1 <= sev <= 4:
                errs.append(f"findings[{i}].severity out of [1,4]: {sev}")
            if sev == 1 and not f.get("human_reviewed"):
                errs.append(f"findings[{i}] severity 1 must be human_reviewed=true")
            blocked = f.get("participants_blocked")
            obs_n = f.get("participants_observed")
            if isinstance(blocked, int) and isinstance(obs_n, int) and obs_n > 0 and blocked > obs_n:
                errs.append(f"findings[{i}] participants_blocked > participants_observed")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "usab-checkout-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "scope": "Mobile checkout v3 pre-launch validation",
    "segments": [{"name": "mid-market buyer", "n": 5}, {"name": "first-time buyer", "n": 5}],
    "tasks": [
        {"scenario": "You decided to buy a gift card.", "success_criterion": "reaches confirmation"},
        {"scenario": "Your card on file is expired.", "success_criterion": "updates payment method"},
        {"scenario": "You want a refund for last week's order.", "success_criterion": "submits refund request"},
    ],
    "findings": [{
        "observation": "Participants tap Pay twice when no loading state appears (t=02:14, 03:01, 04:32, 05:55)",
        "inference": "Missing loading state causes double-submission",
        "task_ref": "task-1",
        "participants_blocked": 4,
        "participants_observed": 5,
        "severity": 1,
        "human_reviewed": True,
    }],
})
BAD_JSON = json.dumps({
    "owner": "we",
    "segments": [{"name": "users", "n": 5}],
    "tasks": [{"scenario": "Click the blue button"}],
    "findings": [{"observation": "stuff", "severity": 9, "human_reviewed": False, "participants_blocked": 9, "participants_observed": 5}],
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
