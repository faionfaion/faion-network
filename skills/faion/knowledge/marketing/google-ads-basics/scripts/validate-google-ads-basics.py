#!/usr/bin/env python3
"""validate-google-ads-basics.py — schema validator for the google-ads-basics methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/google-ads-basics.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'ad_groups': { 'items': { 'properties': { 'keyword_count': { 'maximum': 30,
                                                                               'minimum': 5,
                                                                               'type': 'integer'}},
                                            'required': ['name', 'theme', 'keyword_count'],
                                            'type': 'object'},
                                 'minItems': 1,
                                 'type': 'array'},
                  'billing': {'required': ['payment_method_verified', 'roles'], 'type': 'object'},
                  'campaign_types': { 'items': { 'enum': [ 'search',
                                                           'display',
                                                           'video',
                                                           'shopping',
                                                           'performance_max',
                                                           'discovery']},
                                      'minItems': 1,
                                      'type': 'array'},
                  'conversion_tracking': { 'required': ['events_defined', 'ga4_imported'],
                                           'type': 'object'},
                  'extensions': { 'items': { 'enum': [ 'sitelinks',
                                                       'callouts',
                                                       'structured_snippets',
                                                       'call',
                                                       'location',
                                                       'lead_form',
                                                       'image',
                                                       'promotion']},
                                  'minItems': 3,
                                  'type': 'array'}},
  'required': ['campaign_types', 'ad_groups', 'conversion_tracking', 'extensions', 'billing'],
  'type': 'object'}

OK = { 'ad_groups': [ {'keyword_count': 12, 'name': 'brand-search', 'theme': 'brand'},
                 {'keyword_count': 18, 'name': 'generic-saas', 'theme': 'saas-tools'}],
  'billing': {'payment_method_verified': True, 'roles': ['admin', 'manager']},
  'campaign_types': ['search', 'shopping'],
  'conversion_tracking': {'events_defined': ['Purchase', 'SignUp'], 'ga4_imported': True},
  'extensions': ['sitelinks', 'callouts', 'structured_snippets']}
BAD = { 'ad_groups': [{'keyword_count': 1, 'name': 'g1', 'theme': 'x'}],
  'billing': {},
  'campaign_types': ['performance_max'],
  'extensions': ['sitelinks']}


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
