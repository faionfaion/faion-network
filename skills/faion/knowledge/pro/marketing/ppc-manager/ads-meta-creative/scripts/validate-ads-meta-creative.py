#!/usr/bin/env python3
"""validate-ads-meta-creative.py — schema validator for the ads-meta-creative methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/ads-meta-creative.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'cta': { 'pattern': '^(Get|See|Start|Try|Save|Book|Join|Learn|Download|Watch) ',
                           'type': 'string'},
                  'formats': { 'items': {'enum': ['1:1', '4:5', '9:16']},
                               'minItems': 1,
                               'type': 'array'},
                  'funnel_stage': {'enum': ['tofu', 'mofu', 'bofu', 'retention']},
                  'hook': {'maxLength': 120, 'minLength': 8, 'type': 'string'},
                  'refresh_cadence_days': {'maximum': 14, 'minimum': 5, 'type': 'integer'},
                  'value_prop': {'maxLength': 60, 'type': 'string'},
                  'variants': { 'items': { 'required': ['id', 'format', 'hook_variant'],
                                           'type': 'object'},
                                'maxItems': 5,
                                'minItems': 3,
                                'type': 'array'}},
  'required': [ 'funnel_stage',
                'hook',
                'value_prop',
                'cta',
                'variants',
                'formats',
                'refresh_cadence_days'],
  'type': 'object'}

OK = { 'cta': 'Get the playbook',
  'formats': ['1:1', '4:5', '9:16'],
  'funnel_stage': 'mofu',
  'hook': 'Still planning sprints by hand?',
  'refresh_cadence_days': 7,
  'value_prop': 'Ship 10x faster with SDD',
  'variants': [ {'format': '9:16', 'hook_variant': 'still planning by hand?', 'id': 'v1'},
                {'format': '4:5', 'hook_variant': 'your roadmap is a graveyard', 'id': 'v2'},
                {'format': '1:1', 'hook_variant': 'shipped 3x faster with SDD', 'id': 'v3'}]}
BAD = { 'cta': 'Pricing',
  'formats': ['16:9'],
  'funnel_stage': 'tofu',
  'hook': 'Buy',
  'refresh_cadence_days': 30,
  'value_prop': 'We are great',
  'variants': [{'id': 'v1'}]}


def _check_type(value, expected):
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "null": type(None),
    }
    target = mapping.get(expected)
    if target is None:
        return True
    if expected == "integer" and isinstance(value, bool):
        return False
    return isinstance(value, target)


def _validate_node(value, schema_node, path, errors):
    if not isinstance(schema_node, dict):
        return
    t = schema_node.get("type")
    if t and not _check_type(value, t):
        errors.append(f"{path or '$'}: expected {t}, got {type(value).__name__}")
        return
    if "enum" in schema_node and value not in schema_node["enum"]:
        errors.append(f"{path or '$'}: value {value!r} not in enum")
    if t == "object":
        req = schema_node.get("required", [])
        props = schema_node.get("properties", {})
        for r in req:
            if r not in value:
                errors.append(f"{path or '$'}.{r}: missing required field")
        for k, sub in (value or {}).items():
            if k in props:
                _validate_node(sub, props[k], f"{path}.{k}", errors)
    elif t == "array":
        items_schema = schema_node.get("items")
        min_items = schema_node.get("minItems")
        max_items = schema_node.get("maxItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path or '$'}: array length {len(value)} < minItems {min_items}")
        if max_items is not None and len(value) > max_items:
            errors.append(f"{path or '$'}: array length {len(value)} > maxItems {max_items}")
        if items_schema:
            for i, it in enumerate(value):
                _validate_node(it, items_schema, f"{path}[{i}]", errors)


def validate(obj):
    errors: list[str] = []
    _validate_node(obj, SCHEMA, "", errors)
    return errors


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAILED: valid fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run built-in self-test against fixtures")
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
    except Exception as exc:
        sys.stderr.write(f"unreadable JSON: {exc}\n")
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
