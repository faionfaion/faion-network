#!/usr/bin/env python3
"""validate-grafana-dashboards.py

Validate a `spec` artefact for the grafana-dashboards methodology against the
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

REQUIRED = ['slug', 'title', 'scope', 'components', 'decisions']
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
    for k in ("components", "decisions"):
        v = obj.get(k)
        if not isinstance(v, list) or len(v) < (3 if k == "decisions" else 1):
            errs.append(k + " must be a list with the required minimum length")
    return errs

OK = {'slug': 'grafana-dashboards', 'title': 'Grafana Dashboards', 'scope': 'Production deployment for service X across two environments.', 'components': [{'name': 'frontend'}, {'name': 'api'}], 'decisions': [{'id': 'd1', 'topic': 'topology', 'choice': 'regional'}, {'id': 'd2', 'topic': 'pool', 'choice': 'spot'}, {'id': 'd3', 'topic': 'identity', 'choice': 'WIF'}]}
BAD = {'slug': 'grafana-dashboards'}

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
