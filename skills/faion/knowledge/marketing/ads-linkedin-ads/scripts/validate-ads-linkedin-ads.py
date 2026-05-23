#!/usr/bin/env python3
"""validate-ads-linkedin-ads.py — schema validator for the ads-linkedin-ads methodology artefact.

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

SCHEMA = { '$id': 'https://faion.net/schemas/ads-linkedin-ads.json',
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'properties': { 'audience': { 'required': ['matched_accounts', 'icp_filters', 'exclusions'],
                                'type': 'object'},
                  'bid_strategy': { 'enum': [ 'max_delivery',
                                              'cost_cap',
                                              'manual_cpc',
                                              'target_cost']},
                  'budget': {'required': ['daily', 'currency'], 'type': 'object'},
                  'creative_brief': {'required': ['hook', 'value_prop', 'cta'], 'type': 'object'},
                  'formats': { 'items': { 'enum': [ 'single_image',
                                                    'video',
                                                    'document',
                                                    'carousel',
                                                    'lead_form',
                                                    'conversation',
                                                    'message',
                                                    'text']},
                               'minItems': 1,
                               'type': 'array'},
                  'kpi': { 'required': ['target_cost_per_mql', 'target_mql_to_sql'],
                           'type': 'object'},
                  'objective': { 'enum': [ 'brand_awareness',
                                           'website_visits',
                                           'engagement',
                                           'video_views',
                                           'lead_generation',
                                           'website_conversions']}},
  'required': [ 'objective',
                'audience',
                'formats',
                'bid_strategy',
                'budget',
                'creative_brief',
                'kpi'],
  'type': 'object'}

OK = { 'audience': { 'exclusions': ['competitors_list', 'current_customers'],
                'icp_filters': { 'company_size': '201-1000',
                                 'function': ['engineering'],
                                 'seniority': ['director', 'vp']},
                'matched_accounts': 'acme_top500'},
  'bid_strategy': 'cost_cap',
  'budget': {'currency': 'USD', 'daily': 200},
  'creative_brief': { 'cta': 'Get the playbook',
                      'hook': 'Ship 2 weeks faster',
                      'value_prop': 'Faion-CLI cuts SDD planning to minutes'},
  'formats': ['single_image', 'lead_form'],
  'kpi': {'target_cost_per_mql': 80, 'target_mql_to_sql': 0.25},
  'objective': 'lead_generation'}
BAD = { 'budget': {'daily': 200},
  'creative_brief': {},
  'formats': [],
  'kpi': {},
  'objective': 'website_visits'}


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
