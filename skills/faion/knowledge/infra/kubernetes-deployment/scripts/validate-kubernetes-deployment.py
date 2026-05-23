#!/usr/bin/env python3
"""validate-kubernetes-deployment.py

Validate a `decision-record` artefact for the kubernetes-deployment methodology against the
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

REQUIRED = ['slug', 'title', 'context', 'options', 'decision', 'consequences']
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
    if not isinstance(obj.get("options"), list) or len(obj.get("options") or []) < 2:
        errs.append("options must be a list of >=2 entries")
    if not isinstance(obj.get("consequences"), list) or len(obj.get("consequences") or []) < 1:
        errs.append("consequences must be a list of >=1 entries")
    return errs

OK = {'slug': 'kubernetes-deployment', 'title': 'Kubernetes Deployment', 'context': 'Selecting commitment strategy for the next 12 months of compute baseline.', 'options': [{'id': 'o1', 'name': 'Standard RI'}, {'id': 'o2', 'name': 'Compute Savings Plan'}], 'decision': 'Choose Compute Savings Plan at 55% of 5th percentile floor.', 'consequences': ['Locks $X/yr discount', 'Re-evaluate quarterly']}
BAD = {'slug': 'kubernetes-deployment'}

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
