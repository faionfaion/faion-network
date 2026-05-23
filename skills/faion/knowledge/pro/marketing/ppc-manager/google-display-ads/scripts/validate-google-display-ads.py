#!/usr/bin/env python3
"""validate-google-display-ads.py — schema validator for the google-display-ads methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/google-display-ads.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'audiences': { 'items': { 'enum': [ 'in_market',
                                                      'affinity',
                                                      'custom_intent',
                                                      'remarketing',
                                                      'similar']},
                                 'minItems': 3,
                                 'type': 'array'},
                  'creative_set': { 'items': { 'enum': [ 'responsive_display',
                                                         'native',
                                                         'image_300x250',
                                                         'image_728x90',
                                                         'image_320x50',
                                                         'html5']},
                                    'minItems': 3,
                                    'type': 'array'},
                  'frequency_cap': { 'properties': { 'per_day': { 'maximum': 10,
                                                                  'minimum': 1,
                                                                  'type': 'integer'},
                                                     'per_week': { 'maximum': 30,
                                                                   'minimum': 5,
                                                                   'type': 'integer'}},
                                     'required': ['per_day', 'per_week'],
                                     'type': 'object'},
                  'kpi': {'required': ['cpa_ceiling', 'cpm_floor'], 'type': 'object'},
                  'placement_exclusions': { 'required': [ 'mobile_apps_excluded',
                                                          'low_quality_list_applied'],
                                            'type': 'object'}},
  'required': ['audiences', 'placement_exclusions', 'creative_set', 'frequency_cap', 'kpi'],
  'type': 'object'}

OK = { 'audiences': ['in_market', 'affinity', 'remarketing'],
  'creative_set': ['responsive_display', 'native', 'image_300x250', 'image_728x90'],
  'frequency_cap': {'per_day': 5, 'per_week': 15},
  'kpi': {'cpa_ceiling': 50, 'cpm_floor': 4},
  'placement_exclusions': {'low_quality_list_applied': True, 'mobile_apps_excluded': True}}
BAD = { 'audiences': ['in_market'],
  'creative_set': ['responsive_display'],
  'frequency_cap': {'per_day': 50},
  'kpi': {},
  'placement_exclusions': {'low_quality_list_applied': False, 'mobile_apps_excluded': False}}


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
