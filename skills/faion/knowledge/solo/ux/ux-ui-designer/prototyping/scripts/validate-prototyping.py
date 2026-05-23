#!/usr/bin/env python3
"""validate-prototyping.py - stdlib-only validator for the prototyping output artefact.

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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "learning_objectives", "fidelity", "in_scope", "out_of_scope", "tasks", "decision_rule"]
FIDELITY = {"paper", "clickable", "high-fi", "code"}
REVIEW = {"agent-draft", "human-reviewed"}
TASK_REQUIRED = ["scenario", "goal", "success_criterion", "review_status"]
INSTRUCTION_WORDS = ("click ", "tap ", "navigate to ", "press ", "select the ")
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
    fid = obj.get("fidelity")
    if fid and fid not in FIDELITY:
        errs.append(f"fidelity not in enum: {fid!r}")
    oos = obj.get("out_of_scope", [])
    if isinstance(oos, list):
        for i, it in enumerate(oos):
            if not isinstance(it, dict) or "item" not in it or "reason" not in it:
                errs.append(f"out_of_scope[{i}] missing item/reason")
    tasks = obj.get("tasks", [])
    if isinstance(tasks, list):
        if not 3 <= len(tasks) <= 5:
            errs.append(f"tasks count {len(tasks)} not in [3,5]")
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                errs.append(f"tasks[{i}] not object")
                continue
            for k in TASK_REQUIRED:
                if k not in t or t[k] in (None, ""):
                    errs.append(f"tasks[{i}] missing or empty {k}")
            rs = t.get("review_status")
            if rs and rs not in REVIEW:
                errs.append(f"tasks[{i}].review_status not in enum: {rs!r}")
            scen = t.get("scenario", "")
            if isinstance(scen, str) and any(w in scen.lower() for w in INSTRUCTION_WORDS):
                errs.append(f"tasks[{i}].scenario uses instruction phrasing")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "proto-onboarding-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "learning_objectives": ["Can users complete onboarding without help?", "Which step has highest drop-off?"],
    "fidelity": "clickable",
    "in_scope": ["welcome", "account creation", "payment"],
    "out_of_scope": [{"item": "settings", "reason": "not on critical path"}],
    "tasks": [
        {"scenario": "You just downloaded the app and want to start using it.", "goal": "complete onboarding", "success_criterion": "reaches Home", "review_status": "human-reviewed"},
        {"scenario": "You decide to upgrade to paid.", "goal": "upgrade", "success_criterion": "confirmation", "review_status": "human-reviewed"},
        {"scenario": "You forgot your password mid-flow.", "goal": "recover password", "success_criterion": "reset link", "review_status": "human-reviewed"},
    ],
    "decision_rule": "Move to dev if >=4/5 complete unassisted AND no severity-1.",
})
BAD_JSON = json.dumps({
    "owner": "the team",
    "fidelity": "shiny",
    "learning_objectives": [],
    "tasks": [{"scenario": "click the blue button", "review_status": "agent-draft"}],
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
