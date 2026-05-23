#!/usr/bin/env python3
"""validate-frontend-design.py

Validate the artefact for the frontend-design methodology against the JSON Schema
in content/02-output-contract.xml.

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
import sys
from pathlib import Path

REQUIRED = ["spec_id", "variant_count", "chosen_variant", "tokens_defined", "storybook_version_pinned", "components_planned"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'variant_count' in obj and (not isinstance(obj['variant_count'], int) or obj['variant_count'] < 3 or obj['variant_count'] > 5):
        errs.append('variant_count must be int in [3,5]')
    if 'chosen_variant' in obj and (not isinstance(obj['chosen_variant'], int) or obj['chosen_variant'] < 1 or obj['chosen_variant'] > 5):
        errs.append('chosen_variant must be int in [1,5]')
    if 'spec_id' in obj and (not isinstance(obj['spec_id'], str) or len(obj['spec_id']) < 3):
        errs.append('spec_id must be >= 3 chars')
    if 'components_planned' in obj and (not isinstance(obj['components_planned'], int) or obj['components_planned'] < 1):
        errs.append('components_planned must be int >= 1')
    return errs


OK = {'spec_id': 'acme-dashboard-2026', 'variant_count': 4, 'chosen_variant': 2, 'tokens_defined': True, 'storybook_version_pinned': True, 'components_planned': 32, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'spec_id': 'x', 'variant_count': 2, 'tokens_defined': False}


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
