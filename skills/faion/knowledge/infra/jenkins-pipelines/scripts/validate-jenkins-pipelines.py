#!/usr/bin/env python3
"""validate-jenkins-pipelines.py

Validate a `code` artefact for the jenkins-pipelines methodology against the
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

REQUIRED = ['slug', 'language', 'entrypoint', 'files']
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
    files = obj.get("files")
    if not isinstance(files, list) or len(files) < 1:
        errs.append("files must be a non-empty list")
    return errs

OK = {'slug': 'jenkins-pipelines', 'language': 'yaml', 'entrypoint': 'Chart.yaml', 'files': ['Chart.yaml', 'values.yaml', 'templates/deployment.yaml'], 'build_command': 'helm lint .', 'test_command': 'helm template . | kubeconform -'}
BAD = {'slug': 'jenkins-pipelines'}

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
