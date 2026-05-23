#!/usr/bin/env python3
"""validate-status-report-templates-by-audience.py

Validate the per-week emission record against the JSON Schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to emission record JSON
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

WEEK_RE = re.compile(r"^[0-9]{4}-W[0-9]{2}$")
AUDIENCES = {"CEO", "PMO", "Technical Sponsor", "Internal Leadership"}
TEMPLATES = {"ceo-template", "pmo-template", "sponsor-template", "leadership-template"}
PAIR = {
    "CEO": "ceo-template",
    "PMO": "pmo-template",
    "Technical Sponsor": "sponsor-template",
    "Internal Leadership": "leadership-template",
}
REQUIRED = ["week_iso", "source_spreadsheet_id", "emissions", "single_source_verified"]
EM_REQUIRED = ["audience", "template", "stakeholder", "delivered_at", "char_count"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if isinstance(obj.get("week_iso"), str) and not WEEK_RE.match(obj["week_iso"]):
        errs.append("week_iso must match YYYY-Wnn")
    if obj.get("single_source_verified") is not True:
        errs.append("single_source_verified must be true")
    ems = obj.get("emissions")
    if isinstance(ems, list):
        if len(ems) < 1:
            errs.append("emissions must have ≥1 entry")
        for i, em in enumerate(ems):
            if not isinstance(em, dict):
                errs.append(f"emissions[{i}] not object")
                continue
            for k in EM_REQUIRED:
                if k not in em:
                    errs.append(f"emissions[{i}] missing: " + k)
            aud = em.get("audience")
            tpl = em.get("template")
            if aud not in AUDIENCES:
                errs.append(f"emissions[{i}].audience not in enum")
            if tpl not in TEMPLATES:
                errs.append(f"emissions[{i}].template not in enum")
            if aud in PAIR and PAIR[aud] != tpl:
                errs.append(f"emissions[{i}] audience {aud} mismatched with template {tpl}")
            if aud == "CEO" and em.get("line_count", 0) > 5:
                errs.append(f"emissions[{i}] CEO line_count must be <= 5")
            if aud == "Internal Leadership" and em.get("contains_raw_technical") is True:
                errs.append(f"emissions[{i}] Internal Leadership must not contain raw technical")
    elif "emissions" in obj:
        errs.append("emissions must be array")
    return errs


OK = {
    "week_iso": "2026-W21",
    "source_spreadsheet_id": "sheet-abc",
    "single_source_verified": True,
    "emissions": [
        {"audience": "CEO", "template": "ceo-template", "stakeholder": "alice", "delivered_at": "2026-05-23T16:00:00Z", "char_count": 240, "line_count": 5, "contains_raw_technical": False},
        {"audience": "PMO", "template": "pmo-template", "stakeholder": "bob", "delivered_at": "2026-05-23T16:01:00Z", "char_count": 1200, "line_count": 30, "contains_raw_technical": False},
        {"audience": "Technical Sponsor", "template": "sponsor-template", "stakeholder": "carol", "delivered_at": "2026-05-23T16:02:00Z", "char_count": 1600, "line_count": 35, "contains_raw_technical": True},
        {"audience": "Internal Leadership", "template": "leadership-template", "stakeholder": "dave", "delivered_at": "2026-05-23T16:03:00Z", "char_count": 2100, "line_count": 40, "contains_raw_technical": False},
    ],
}
BAD = {
    "week_iso": "2026-W21",
    "source_spreadsheet_id": "sheet-abc",
    "single_source_verified": False,
    "emissions": [
        {"audience": "CEO", "template": "leadership-template", "stakeholder": "alice", "delivered_at": "2026-05-23T16:00:00Z", "char_count": 5000, "line_count": 80, "contains_raw_technical": True}
    ],
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
