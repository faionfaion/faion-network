#!/usr/bin/env python3
"""validate-seven-performance-domains.py

Validate the `spec` artefact for the `seven-performance-domains` methodology against the
JSON Schema embedded in `content/02-output-contract.xml`. Stdlib-only — no
external pip dependencies.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            show this message

Exit codes:
    0 = valid artefact
    1 = invalid artefact (violations listed on stderr)
    2 = usage error / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/seven-performance-domains.json', 'title': 'Seven Performance Domains (PMBOK 8)', 'type': 'object', 'additionalProperties': False, 'required': ['slug', 'sections', 'approved_by'], 'properties': {'slug': {'type': 'string', 'const': 'seven-performance-domains'}, 'sections': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['title', 'body'], 'properties': {'title': {'type': 'string', 'minLength': 3}, 'body': {'type': 'string', 'minLength': 10}}}}, 'approved_by': {'type': 'string'}, 'approved_at': {'type': 'string'}}}

OK_FIXTURE = {'slug': 'seven-performance-domains', 'sections': [{'title': 'Scope', 'body': 'In: A, B, C. Out: D.'}, {'title': 'Acceptance', 'body': 'Measurable thresholds per deliverable.'}], 'approved_by': 'Sponsor', 'approved_at': '2026-05-23'}

BAD_FIXTURE = {'slug': 'seven-performance-domains', 'sections': [{'title': 'x'}]}

PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b")


def _walk(node, path, errs, schema):
    if not isinstance(schema, dict):
        return
    if "type" in schema:
        t = schema["type"]
        if t == "object" and not isinstance(node, dict):
            errs.append(f"{path}: expected object, got {type(node).__name__}")
            return
        if t == "array" and not isinstance(node, list):
            errs.append(f"{path}: expected array, got {type(node).__name__}")
            return
        if t == "string" and not isinstance(node, str):
            errs.append(f"{path}: expected string, got {type(node).__name__}")
            return
        if t == "integer" and not isinstance(node, int):
            errs.append(f"{path}: expected integer, got {type(node).__name__}")
            return
        if t == "boolean" and not isinstance(node, bool):
            errs.append(f"{path}: expected boolean, got {type(node).__name__}")
            return
    if isinstance(node, dict):
        required = schema.get("required", [])
        for k in required:
            if k not in node:
                errs.append(f"{path}: missing required field `{k}`")
        props = schema.get("properties", {})
        for k, v in node.items():
            sub_schema = props.get(k)
            if sub_schema is None:
                continue
            if "const" in sub_schema and v != sub_schema["const"]:
                errs.append(f"{path}.{k}: expected const `{sub_schema['const']}`, got `{v}`")
                continue
            if "enum" in sub_schema and v not in sub_schema["enum"]:
                errs.append(f"{path}.{k}: value `{v}` not in enum {sub_schema['enum']}")
                continue
            if isinstance(v, str):
                if "minLength" in sub_schema and len(v) < sub_schema["minLength"]:
                    errs.append(f"{path}.{k}: length {len(v)} < minLength {sub_schema['minLength']}")
                if PLACEHOLDER_RE.search(v):
                    errs.append(f"{path}.{k}: contains placeholder text (TBD/TODO/FIXME/XXX)")
            if isinstance(v, int) and not isinstance(v, bool):
                if "minimum" in sub_schema and v < sub_schema["minimum"]:
                    errs.append(f"{path}.{k}: value {v} < minimum {sub_schema['minimum']}")
                if "maximum" in sub_schema and v > sub_schema["maximum"]:
                    errs.append(f"{path}.{k}: value {v} > maximum {sub_schema['maximum']}")
            _walk(v, f"{path}.{k}", errs, sub_schema)
    elif isinstance(node, list):
        item_schema = schema.get("items", {})
        min_items = schema.get("minItems")
        if min_items is not None and len(node) < min_items:
            errs.append(f"{path}: array length {len(node)} < minItems {min_items}")
        for i, item in enumerate(node):
            _walk(item, f"{path}[{i}]", errs, item_schema)


def validate(obj) -> list:
    errs = []
    _walk(obj, "$", errs, SCHEMA)
    return errs


def self_test() -> int:
    errs_ok = validate(OK_FIXTURE)
    errs_bad = validate(BAD_FIXTURE)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
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
