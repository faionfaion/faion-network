#!/usr/bin/env python3
"""validate-stakeholder-register.py

Validate the config artefact for the stakeholder-register methodology against the schema
defined in content/02-output-contract.xml.

Usage:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            show this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

METHODOLOGY = "stakeholder-register"
VERSION = "1.1.0"
PRODUCES = "config"
RULES = ['groups-as-groups', 'evidence-not-gut-feel', 'verify-attitude-in-conversation', 'attitude-unknown-without-evidence', 'pii-separated', 'refresh-after-stage-gate']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ block")
        return errs
    if hdr.get("methodology") != METHODOLOGY:
        errs.append(f"header.methodology != {METHODOLOGY}")
    if hdr.get("version") != VERSION:
        errs.append(f"header.version != {VERSION}")
    if hdr.get("produces") != PRODUCES:
        errs.append(f"header.produces != {PRODUCES}")
    rs = hdr.get("rules_satisfied")
    if not isinstance(rs, list) or not rs:
        errs.append("header.rules_satisfied must be a non-empty list")
    else:
        for r in rs:
            if r not in RULES:
                errs.append(f"rules_satisfied contains unknown rule id: {r}")
    # produces-specific body field
    if PRODUCES == "spec":
        if "artefact_path" not in obj:
            errs.append("missing artefact_path")
        if not isinstance(obj.get("sections"), list) or not obj.get("sections"):
            errs.append("sections must be a non-empty list")
    elif PRODUCES == "report":
        if "report_id" not in obj:
            errs.append("missing report_id")
        if not isinstance(obj.get("data"), dict):
            errs.append("data must be an object")
    elif PRODUCES == "config":
        if "config_path" not in obj:
            errs.append("missing config_path")
        if not isinstance(obj.get("entries"), list) or not obj.get("entries"):
            errs.append("entries must be a non-empty list")
    elif PRODUCES == "checklist":
        items = obj.get("items")
        if not isinstance(items, list) or not items:
            errs.append("items must be a non-empty list")
        else:
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    errs.append(f"items[{i}] not an object")
                    continue
                if "status" not in it or it["status"] not in ("pass", "fail", "na"):
                    errs.append(f"items[{i}].status invalid")
                if not it.get("evidence"):
                    errs.append(f"items[{i}].evidence empty")
    elif PRODUCES == "rubric":
        if "rubric_id" not in obj:
            errs.append("missing rubric_id")
        if not isinstance(obj.get("criteria"), list) or not obj.get("criteria"):
            errs.append("criteria must be a non-empty list")
    return errs


OK = {"__faion_header__": {"methodology": "stakeholder-register", "version": "1.1.0", "produces": "config", "rules_satisfied": ["groups-as-groups", "evidence-not-gut-feel", "verify-attitude-in-conversation"]}, "config_path": "config/stakeholder-register.yaml", "entries": [{"key": "k1", "value": "v1"}]}
BAD = {"artefact_path": "docs/stakeholder-register.md"}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: valid example rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: invalid example accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
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
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
