#!/usr/bin/env python3
"""validate-instagram-ads.py — schema validator for the instagram-ads methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/instagram-ads.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'creative_strategy': { 'properties': { 'cold_content_type': { 'enum': [ 'ugc',
                                                                                          'creator',
                                                                                          'polished_brand']},
                                                         'primary_format': { 'enum': [ '9:16',
                                                                                       '4:5',
                                                                                       '1:1']}},
                                         'required': ['primary_format', 'cold_content_type'],
                                         'type': 'object'},
                  'frequency_caps': { 'properties': { 'cold_per_week': { 'maximum': 3,
                                                                         'type': 'integer'},
                                                      'retarget_per_week': { 'maximum': 5,
                                                                             'type': 'integer'}},
                                      'required': ['cold_per_week', 'retarget_per_week'],
                                      'type': 'object'},
                  'placements': { 'properties': { 'reels_pct': { 'maximum': 100,
                                                                 'minimum': 60,
                                                                 'type': 'integer'}},
                                  'required': ['reels_pct', 'stories_pct', 'feed_pct'],
                                  'type': 'object'},
                  'shopping_tags': {'required': ['enabled'], 'type': 'object'}},
  'required': ['placements', 'creative_strategy', 'frequency_caps', 'shopping_tags'],
  'type': 'object'}

OK = { 'creative_strategy': {'cold_content_type': 'ugc', 'primary_format': '9:16'},
  'frequency_caps': {'cold_per_week': 3, 'retarget_per_week': 5},
  'placements': {'feed_pct': 20, 'reels_pct': 60, 'stories_pct': 20},
  'shopping_tags': {'enabled': True}}
BAD = { 'creative_strategy': {'cold_content_type': 'polished_brand', 'primary_format': '1:1'},
  'frequency_caps': {'cold_per_week': 10, 'retarget_per_week': 20},
  'placements': {'feed_pct': 90, 'reels_pct': 10, 'stories_pct': 0},
  'shopping_tags': {}}


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
