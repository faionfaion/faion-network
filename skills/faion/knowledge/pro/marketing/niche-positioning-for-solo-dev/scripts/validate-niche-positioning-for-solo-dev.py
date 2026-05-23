#!/usr/bin/env python3
"""validate-niche-positioning-for-solo-dev.py

Validate the artefact produced by the niche-positioning-for-solo-dev methodology against the JSON
Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (one valid + one invalid)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (one or more VIOLATION lines on stderr)
    2 = usage / file unreadable / not JSON
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/niche-positioning-for-solo-dev.json', 'type': 'object', 'required': ['artefact_id', 'template_version', 'owner', 'decision', 'context', 'alternatives', 'consequences', 'exit_criteria'], 'properties': {'artefact_id': {'type': 'string'}, 'template_version': {'type': 'string'}, 'owner': {'type': 'string', 'minLength': 1}, 'decision': {'type': 'string'}, 'context': {'type': 'string'}, 'alternatives': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}, 'consequences': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}, 'exit_criteria': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}}}

VALID_FIXTURE = {'artefact_id': 'niche-positioning-for-solo-dev-2026-Q2', 'template_version': '1.1.0', 'owner': 'founder@faion.net', 'decision': 'Primary platform: Toptal. Secondary: Contra brand-page.', 'context': "Rate band $150-220/hr, lane = 'Stripe integration for Shopify Plus stores', 3 past projects match.", 'alternatives': ['Upwork primary (rejected — rate-band mismatch)', 'Direct outreach only (rejected — slower ramp)', 'Braintrust primary (rejected — exclusivity clause)'], 'consequences': ['6-week ramp on Toptal application + screening', 'Contra brand-page bi-monthly post cadence', 'Refuse non-Shopify Stripe work for 6 months'], 'exit_criteria': ['< 3 inbound from lane in 6 months => repivot', 'Toptal screening fails => switch to Arc + direct outreach']}
INVALID_FIXTURE = {'artefact_id': 'niche-positioning-for-solo-dev-2026-Q2', 'owner': '', 'decision': '', 'alternatives': [], 'consequences': [], 'exit_criteria': []}


def _check_type(value, declared):
    if declared == "object":
        return isinstance(value, dict)
    if declared == "array":
        return isinstance(value, list)
    if declared == "string":
        return isinstance(value, str)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "null":
        return value is None
    return True


def _walk(node, schema, path, errs):
    if "enum" in schema:
        if node not in schema["enum"]:
            errs.append(f"{path}: value {node!r} not in enum {schema['enum']}")
            return
    declared = schema.get("type")
    if declared and not _check_type(node, declared):
        errs.append(f"{path}: expected {declared}, got {type(node).__name__}")
        return
    if declared == "object" and isinstance(node, dict):
        for key in schema.get("required", []):
            if key not in node:
                errs.append(f"{path}.{key}: missing required field")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in node:
                _walk(node[key], sub, f"{path}.{key}", errs)
    if declared == "array" and isinstance(node, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(node) < min_items:
            errs.append(f"{path}: array has {len(node)} items, minItems={min_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(node):
                _walk(item, item_schema, f"{path}[{i}]", errs)
    if declared == "string" and isinstance(node, str):
        max_len = schema.get("maxLength")
        min_len = schema.get("minLength")
        if max_len is not None and len(node) > max_len:
            errs.append(f"{path}: string length {len(node)} exceeds maxLength={max_len}")
        if min_len is not None and len(node) < min_len:
            errs.append(f"{path}: string length {len(node)} below minLength={min_len}")


def validate(obj):
    errs: list[str] = []
    if not isinstance(obj, (dict, list, str, int, float, bool)) and obj is not None:
        return ["root must be JSON value"]
    _walk(obj, SCHEMA, "$", errs)
    return errs


def _self_test() -> int:
    if validate(VALID_FIXTURE):
        sys.stderr.write("valid fixture rejected unexpectedly\n")
        return 1
    if not validate(INVALID_FIXTURE):
        sys.stderr.write("invalid fixture accepted unexpectedly\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="Path to artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
