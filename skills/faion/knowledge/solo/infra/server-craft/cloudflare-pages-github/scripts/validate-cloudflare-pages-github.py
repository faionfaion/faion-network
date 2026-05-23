#!/usr/bin/env python3
"""validate-cloudflare-pages-github.py

Validate the output artefact for the `cloudflare-pages-github` methodology against the JSON Schema
(draft-07) declared in content/02-output-contract.xml. Stdlib-only.

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

SCHEMA = {   '$schema': 'http://json-schema.org/draft-07/schema#',
    '$id': 'https://faion.net/schemas/cloudflare-pages-github.json',
    'type': 'object',
    'required': [   'slug',
                    'title',
                    'owner',
                    'trigger',
                    'evidence',
                    'produced_at',
                    'findings',
                    'recommendations'],
    'properties': {   'slug': {'type': 'string', 'pattern': '^[a-z][a-z0-9-]+$'},
                      'title': {'type': 'string', 'minLength': 3, 'maxLength': 200},
                      'owner': {   'type': 'object',
                                   'required': ['name', 'role'],
                                   'properties': {   'name': {'type': 'string', 'minLength': 2},
                                                     'role': {'type': 'string', 'minLength': 2}}},
                      'trigger': {   'type': 'object',
                                     'required': ['kind', 'value'],
                                     'properties': {   'kind': {   'enum': [   'event',
                                                                               'threshold',
                                                                               'schedule']},
                                                       'value': {   'type': 'string',
                                                                    'minLength': 2}}},
                      'last_reviewed': {'type': 'string', 'format': 'date'},
                      'evidence': {   'type': 'array',
                                      'items': {   'type': 'object',
                                                   'required': ['claim', 'link'],
                                                   'properties': {   'claim': {'type': 'string'},
                                                                     'link': {   'type': 'string',
                                                                                 'format': 'uri'}}},
                                      'minItems': 1},
                      'produced_at': {'type': 'string', 'format': 'date-time'},
                      'findings': {   'type': 'array',
                                      'minItems': 1,
                                      'items': {   'type': 'object',
                                                   'required': ['id', 'summary'],
                                                   'properties': {   'id': {'type': 'string'},
                                                                     'summary': {   'type': 'string'}}}},
                      'recommendations': {   'type': 'array',
                                             'minItems': 1,
                                             'items': {'type': 'string'}}},
    'additionalProperties': True}


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
    t = schema.get("type")
    if t and not _check_type(node, t):
        errs.append(f"{path}: expected {t}, got {type(node).__name__}")
        return errs
    if t == "object":
        for req in schema.get("required", []):
            if req not in node:
                errs.append(f"{path}: missing required field {req!r}")
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
    return errs


def validate(obj):
    return _validate(obj, SCHEMA, "$")


OK = {   'slug': 'cloudflare-pages-github',
    'title': 'Cloudflare Pages + GitHub',
    'owner': {'name': 'Ruslan Faion', 'role': 'platform lead'},
    'trigger': {'kind': 'schedule', 'value': 'weekly:monday-09:00-utc'},
    'last_reviewed': '2026-05-23',
    'evidence': [   {   'claim': 'configuration verified in dry run',
                        'link': 'https://wiki.faion.net/runs/2026-05-23'}],
    'produced_at': '2026-05-23T10:00:00Z',
    'findings': [{'id': 'f1', 'summary': 'baseline established; no drift detected'}],
    'recommendations': ['schedule next review at the cadence interval']}
BAD = {'slug': 'BAD_SLUG', 'owner': 'someone'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("FAIL: OK fixture rejected\n")
        for e in errs_ok:
            sys.stderr.write(f"  {e}\n")
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
