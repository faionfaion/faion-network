#!/usr/bin/env python3
"""validate-finops-devops-cost-kubernetes.py

Validate a `report` artefact for the finops-devops-cost-kubernetes methodology against the
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

REQUIRED = ['slug', 'period', 'findings', 'recommendations']
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
    period = obj.get("period")
    if not isinstance(period, dict) or "from" not in period or "to" not in period:
        errs.append("period must be an object with from + to")
    for k in ("findings", "recommendations"):
        v = obj.get(k)
        if not isinstance(v, list) or len(v) < 1:
            errs.append(k + " must be a non-empty list")
    return errs

OK = {'slug': 'finops-devops-cost-kubernetes', 'period': {'from': '2026-04-01', 'to': '2026-04-30'}, 'findings': [{'id': 'f1', 'severity': 'high', 'summary': 'Over-provisioned m5.4xlarge in api-prod'}], 'recommendations': [{'id': 'r1', 'action': 'downsize to m5.2xlarge', 'expected_saving_usd': 1280}], 'estimated_savings_usd': 1280}
BAD = {'slug': 'finops-devops-cost-kubernetes'}

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
