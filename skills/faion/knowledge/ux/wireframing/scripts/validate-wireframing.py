#!/usr/bin/env python3
"""validate-wireframing.py - stdlib-only validator for the wireframing output artefact.

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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "screens", "open_questions"]
SCREEN_REQ = ["name", "variants", "annotations", "states", "mobile_notes"]
STATES_REQ = ("default", "empty", "loading", "error", "success")
ANNOTATION_REQ = ("element", "behaviour", "conditional_states", "tech_requirement")
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
    screens = obj.get("screens", [])
    if isinstance(screens, list):
        for i, s in enumerate(screens):
            if not isinstance(s, dict):
                errs.append(f"screens[{i}] not object")
                continue
            for k in SCREEN_REQ:
                if k not in s:
                    errs.append(f"screens[{i}] missing {k}")
            variants = s.get("variants") or []
            if isinstance(variants, list) and len(variants) < 3:
                errs.append(f"screens[{i}].variants count {len(variants)} < 3")
            annotations = s.get("annotations") or []
            if isinstance(annotations, list):
                if not annotations:
                    errs.append(f"screens[{i}].annotations empty")
                for j, a in enumerate(annotations):
                    if not isinstance(a, dict):
                        errs.append(f"screens[{i}].annotations[{j}] not object")
                        continue
                    for k in ANNOTATION_REQ:
                        if k not in a:
                            errs.append(f"screens[{i}].annotations[{j}] missing {k}")
            states = s.get("states") or {}
            if isinstance(states, dict):
                for st in STATES_REQ:
                    if not states.get(st):
                        errs.append(f"screens[{i}].states missing or empty {st}")
            if not s.get("mobile_notes"):
                errs.append(f"screens[{i}].mobile_notes empty")
    oq = obj.get("open_questions") or []
    if isinstance(oq, list) and not oq:
        errs.append("open_questions must be non-empty")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "wireframe-checkout-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "screens": [{
        "name": "checkout-review",
        "variants": ["single-column stack", "two-column with sticky summary", "accordion sections"],
        "annotations": [{"element": "pay-now button", "behaviour": "submit order; disable on click", "conditional_states": ["loading", "disabled-if-invalid"], "tech_requirement": "POST /orders; 3-state idempotent"}],
        "states": {"default": "items + summary visible", "empty": "redirect to /cart", "loading": "skeleton review block", "error": "inline error above CTA", "success": "navigate to /confirmation"},
        "mobile_notes": "Stack variants only at <600px; sticky bottom bar holds primary CTA.",
    }],
    "open_questions": ["Tax position relative to shipping?"],
})
BAD_JSON = json.dumps({
    "owner": "team",
    "screens": [{"name": "x", "variants": ["one"], "annotations": [], "states": {"default": "a"}, "mobile_notes": ""}],
    "open_questions": [],
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
