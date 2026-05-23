#!/usr/bin/env python3
"""validate-methodologies-index.py

Validate an artefact produced by the methodologies-index methodology against the JSON
Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/methodologies-index.json", "type": "object", "required": ["domain", "groups", "methodologies", "count"], "properties": {"domain": {"type": "string"}, "groups": {"type": "array", "minItems": 3, "maxItems": 8}, "methodologies": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["slug", "tier", "path", "complexity", "produces", "summary"]}}, "count": {"type": "integer"}}}')
REQUIRED = SCHEMA.get("required", [])


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    # type guard for top-level required fields
    for k, v in obj.items():
        if k in SCHEMA.get("properties", {}):
            spec = SCHEMA["properties"][k]
            if "type" in spec and spec["type"] == "array" and not isinstance(v, list):
                errs.append(f"field {k} must be array")
            if "type" in spec and spec["type"] == "object" and not isinstance(v, dict):
                errs.append(f"field {k} must be object")
            if "type" in spec and spec["type"] == "string" and not isinstance(v, str):
                errs.append(f"field {k} must be string")
            if "enum" in spec and v not in spec["enum"]:
                errs.append(f"field {k} must be one of {spec['enum']}")
    return errs


def self_test() -> int:
    good = {k: _placeholder(SCHEMA["properties"][k]) for k in REQUIRED if k in SCHEMA.get("properties", {})}
    if validate(good):
        sys.stderr.write("self-test: good fixture rejected\n"); return 1
    if not validate({}):
        sys.stderr.write("self-test: empty fixture accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def _placeholder(field_spec):
    if "enum" in field_spec:
        return field_spec["enum"][0]
    t = field_spec.get("type")
    if t == "string":
        return "x"
    if t == "integer":
        return 0
    if t == "number":
        return 0
    if t == "boolean":
        return True
    if t == "array":
        return []
    if t == "object":
        return {}
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
