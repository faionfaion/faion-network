#!/usr/bin/env python3
"""validate-programmatic-seo-patterns.py — schema validator for the programmatic-seo-patterns methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/programmatic-seo-patterns.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'data_source': { 'properties': {'quality_pct': {'minimum': 80, 'type': 'number'}},
                                   'required': ['provider', 'refresh_cadence_days', 'quality_pct'],
                                   'type': 'object'},
                  'indexability_tiers': { 'required': ['tier_1', 'tier_2', 'tier_3'],
                                          'type': 'object'},
                  'intent_template_map': { 'items': { 'required': ['intent', 'template_id'],
                                                      'type': 'object'},
                                           'minItems': 1,
                                           'type': 'array'},
                  'internal_link_graph': { 'required': ['sibling_pattern', 'parent_pattern'],
                                           'type': 'object'},
                  'owner': {'type': 'string'},
                  'thin_content_threshold': { 'properties': { 'min_data_points': { 'minimum': 2,
                                                                                   'type': 'integer'},
                                                              'min_words': { 'minimum': 300,
                                                                             'type': 'integer'}},
                                              'required': [ 'min_words',
                                                            'min_data_points',
                                                            'schema_required'],
                                              'type': 'object'}},
  'required': [ 'data_source',
                'intent_template_map',
                'thin_content_threshold',
                'indexability_tiers',
                'internal_link_graph',
                'owner'],
  'type': 'object'}

OK = { 'data_source': {'provider': 'internal_db', 'quality_pct': 95, 'refresh_cadence_days': 30},
  'indexability_tiers': {'tier_1': 'indexed+sitemap', 'tier_2': 'indexed', 'tier_3': 'noindex'},
  'intent_template_map': [ {'intent': 'comparison', 'template_id': 'tpl-vs'},
                           {'intent': 'listing', 'template_id': 'tpl-list'}],
  'internal_link_graph': { 'parent_pattern': 'category-parent-1',
                           'sibling_pattern': 'category-siblings-5'},
  'owner': 'seo-lead@faion.net',
  'thin_content_threshold': {'min_data_points': 2, 'min_words': 300, 'schema_required': True}}
BAD = { 'data_source': {'provider': 'csv', 'quality_pct': 40},
  'indexability_tiers': {},
  'intent_template_map': [],
  'internal_link_graph': {},
  'owner': '',
  'thin_content_threshold': {'min_data_points': 1, 'min_words': 100}}


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
