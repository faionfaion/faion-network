#!/usr/bin/env python3
"""validate-iac-pr-review-checklist.py

Validate a `checklist` artefact for the iac-pr-review-checklist methodology against the
schema defined in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK + BAD fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ['slug', 'items', 'summary']
SLUG_PATTERN = re.compile(r'^[a-z][a-z0-9-]+$')

def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if "slug" in obj and isinstance(obj["slug"], str):
        if not SLUG_PATTERN.match(obj["slug"]):
            errs.append("slug does not match pattern " + SLUG_PATTERN.pattern)
    items = obj.get("items")
    if items is not None:
        if not isinstance(items, list) or len(items) < 5:
            errs.append("items must be a list with >=5 entries")
        else:
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    errs.append("items[%d] not an object" % i); continue
                for ik in ["id", "rule", "must_or_should", "evidence"]:
                    if ik not in it:
                        errs.append("items[%d] missing %s" % (i, ik))
                if it.get("must_or_should") not in ("MUST", "SHOULD"):
                    errs.append("items[%d].must_or_should must be MUST|SHOULD" % i)
    return errs

OK = {'slug': 'iac-pr-review-checklist', 'summary': 'Validated iac-pr-review-checklist checklist applied to a single review.', 'items': [{'id': 'i1', 'rule': 'First rule verified in scope', 'must_or_should': 'MUST', 'evidence': 'PR comment ID 42'}, {'id': 'i2', 'rule': 'Second rule verified in scope', 'must_or_should': 'MUST', 'evidence': 'plan output line 7'}, {'id': 'i3', 'rule': 'Third rule verified in scope', 'must_or_should': 'SHOULD', 'evidence': 'monitoring dashboard'}, {'id': 'i4', 'rule': 'Fourth rule verified in scope', 'must_or_should': 'MUST', 'evidence': 'policy report'}, {'id': 'i5', 'rule': 'Fifth rule verified in scope', 'must_or_should': 'SHOULD', 'evidence': 'design doc section 3'}]}
BAD = {'slug': 'iac-pr-review-checklist'}

def self_test():
    es = validate(OK)
    if es:
        sys.stderr.write("OK fixture rejected: " + repr(es) + "\n"); return 1
    es = validate(BAD)
    if not es:
        sys.stderr.write("BAD fixture accepted\n"); return 1
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
        sys.stderr.write("not a file: " + str(p) + "\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write("could not parse JSON: " + str(e) + "\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
