#!/usr/bin/env python3
"""validate-testing-with-assistive-technology.py

Validate the artefact for the testing-with-assistive-technology methodology against the schema in
content/02-output-contract.xml.

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

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
TOOLS = {'ibm-equal-access', 'pa11y', 'lighthouse', 'axe-core'}
SCREEN_READERS = {'talkback', 'narrator', 'nvda', 'voiceover', 'jaws'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'testing-with-assistive-technology':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'tiers' not in obj:
        errs.append(f"missing required field: " + 'tiers')
    if 'bug_report_format' not in obj:
        errs.append(f"missing required field: " + 'bug_report_format')


    tiers = obj.get("tiers") or {}
    for k in ("automated_ci", "manual_release", "at_user_quarterly"):
        if k not in tiers:
            errs.append("tiers." + k + " missing")
    aci = tiers.get("automated_ci") or {}
    tools = aci.get("tools") or []
    if not isinstance(tools, list) or not tools:
        errs.append("tiers.automated_ci.tools must be non-empty list")
    if aci.get("fail_on_new_violations") is not True:
        errs.append("tiers.automated_ci.fail_on_new_violations must be true")
    mr = tiers.get("manual_release") or {}
    srs = mr.get("screen_readers") or []
    if not isinstance(srs, list) or len(srs) < 2:
        errs.append("tiers.manual_release.screen_readers must have >=2")
    atq = tiers.get("at_user_quarterly") or {}
    upq = atq.get("users_per_quarter")
    if not isinstance(upq, int) or upq < 1:
        errs.append("tiers.at_user_quarterly.users_per_quarter must be >=1")
    brf = obj.get("bug_report_format") or {}
    for k in ("wcag_sc", "repro", "apg_pattern", "scope"):
        if brf.get(k) is not True:
            errs.append("bug_report_format." + k + " must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'testing-with-assistive-technology', 'version': '1.1.0', 'produces': 'config'}, 'tiers': {'automated_ci': {'tools': ['axe-core', 'lighthouse'], 'fail_on_new_violations': True, 'owner': 'fe-team'}, 'manual_release': {'screen_readers': ['voiceover', 'nvda'], 'keyboard_only': True, 'owner': 'qa-lead'}, 'at_user_quarterly': {'partner': 'AbilityTech Research', 'users_per_quarter': 2, 'owner': 'a11y-lead'}}, 'bug_report_format': {'wcag_sc': True, 'repro': True, 'apg_pattern': True, 'scope': True}}
BAD = {'tiers': {'automated_ci': {'tools': []}, 'manual_release': {'screen_readers': ['voiceover']}}, 'bug_report_format': {'wcag_sc': False}}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
