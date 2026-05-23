#!/usr/bin/env python3
"""validate-graphql-api-design.py

Validate the artefact for the graphql-api-design methodology against the JSON Schema
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

REQUIRED = ["schema_id", "types_count", "mutations_count", "payload_types_present", "auth_directives_present", "non_payload_mutations", "scalar_id_relations"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'schema_id' in obj and (not isinstance(obj['schema_id'], str) or len(obj['schema_id']) < 3):
        errs.append('schema_id must be >= 3 chars')
    if 'types_count' in obj and (not isinstance(obj['types_count'], int) or obj['types_count'] < 5):
        errs.append('types_count must be int >= 5')
    if 'mutations_count' in obj and (not isinstance(obj['mutations_count'], int) or obj['mutations_count'] < 1):
        errs.append('mutations_count must be int >= 1')
    if 'non_payload_mutations' in obj and obj['non_payload_mutations'] != 0:
        errs.append('non_payload_mutations must be 0')
    if 'scalar_id_relations' in obj and obj['scalar_id_relations'] != 0:
        errs.append('scalar_id_relations must be 0')
    return errs


OK = {'schema_id': 'acme-platform-graph', 'types_count': 18, 'mutations_count': 12, 'payload_types_present': True, 'auth_directives_present': True, 'non_payload_mutations': 0, 'scalar_id_relations': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'schema_id': 'x', 'types_count': 2, 'non_payload_mutations': 5, 'scalar_id_relations': 7}


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
