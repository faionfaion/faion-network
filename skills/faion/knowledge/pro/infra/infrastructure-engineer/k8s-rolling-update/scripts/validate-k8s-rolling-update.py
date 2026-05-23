#!/usr/bin/env python3
"""validate-k8s-rolling-update.py

Validate the output artefact for the `k8s-rolling-update` methodology against the JSON
Schema (draft-07) declared in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to candidate JSON artefact
    --self-test       run built-in OK / BAD fixtures
    --help            show this message

Exit codes:
    0 = valid
    1 = schema violation(s)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/k8s-rolling-update.json', 'type': 'object', 'required': ['service', 'strategy_type', 'max_unavailable', 'max_surge', 'min_ready_seconds', 'progress_deadline_seconds', 'pdb', 'owner', 'produced_at'], 'properties': {'service': {'type': 'string', 'pattern': '^[a-z][a-z0-9-]+$'}, 'strategy_type': {'enum': ['RollingUpdate', 'Recreate']}, 'max_unavailable': {'type': 'string'}, 'max_surge': {'type': 'string'}, 'min_ready_seconds': {'type': 'integer', 'minimum': 0}, 'progress_deadline_seconds': {'type': 'integer', 'maximum': 600}, 'pdb': {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'min_available': {'type': 'string'}, 'max_unavailable': {'type': 'string'}}}, 'owner': {'type': 'object', 'required': ['name', 'role'], 'properties': {'name': {'type': 'string'}, 'role': {'type': 'string'}}}, 'produced_at': {'type': 'string', 'format': 'date-time'}}, 'additionalProperties': True}


def _check_type(val, expected):
    if expected == "object":
        return isinstance(val, dict)
    if expected == "array":
        return isinstance(val, list)
    if expected == "string":
        return isinstance(val, str)
    if expected == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if expected == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if expected == "boolean":
        return isinstance(val, bool)
    return True


def _validate(node, schema, path):
    errs = []
    if "enum" in schema and node not in schema["enum"]:
        errs.append(f"{path}: value not in enum {schema['enum']}")
        return errs
    if "const" in schema and node != schema["const"]:
        errs.append(f"{path}: value != const {schema['const']!r}")
        return errs
    t = schema.get("type")
    if t and not _check_type(node, t):
        errs.append(f"{path}: expected {t}, got {type(node).__name__}")
        return errs
    if t == "object":
        for req in schema.get("required", []):
            if req not in node:
                errs.append(f"{path}: missing required field '{req}'")
        for k, sub in schema.get("properties", {}).items():
            if k in node:
                errs.extend(_validate(node[k], sub, f"{path}.{k}"))
    elif t == "array":
        mi = schema.get("minItems")
        if mi is not None and len(node) < mi:
            errs.append(f"{path}: array shorter than minItems={mi}")
        item_sch = schema.get("items")
        if item_sch:
            for i, item in enumerate(node):
                errs.extend(_validate(item, item_sch, f"{path}[{i}]"))
    elif t == "string":
        if "pattern" in schema and not re.match(schema["pattern"], node):
            errs.append(f"{path}: string does not match pattern {schema['pattern']!r}")
        if "minLength" in schema and len(node) < schema["minLength"]:
            errs.append(f"{path}: shorter than minLength={schema['minLength']}")
        if "maxLength" in schema and len(node) > schema["maxLength"]:
            errs.append(f"{path}: longer than maxLength={schema['maxLength']}")
    elif t == "integer":
        if "minimum" in schema and node < schema["minimum"]:
            errs.append(f"{path}: integer below minimum={schema['minimum']}")
        if "maximum" in schema and node > schema["maximum"]:
            errs.append(f"{path}: integer above maximum={schema['maximum']}")
    return errs


def validate(obj):
    return _validate(obj, SCHEMA, "$")


OK = {'service': 'acme-api', 'strategy_type': 'RollingUpdate', 'max_unavailable': '25%', 'max_surge': '25%', 'min_ready_seconds': 30, 'progress_deadline_seconds': 600, 'pdb': {'name': 'acme-api-pdb', 'min_available': '50%'}, 'owner': {'name': 'Olha Petrenko', 'role': 'platform lead'}, 'produced_at': '2026-05-23T10:00:00Z'}
BAD = {'service': 'api', 'strategy_type': 'Recreate'}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("FAIL: OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to candidate JSON artefact")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
