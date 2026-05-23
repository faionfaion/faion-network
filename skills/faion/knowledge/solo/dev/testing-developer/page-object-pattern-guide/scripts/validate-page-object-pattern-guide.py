#!/usr/bin/env python3
"""validate-page-object-pattern-guide.py

Validate an artefact produced by the page-object-pattern-guide methodology against the JSON
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

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/page-object-pattern-guide.json", "type": "object", "required": ["artefact_id", "owner", "framework", "pages", "locator_hierarchy", "version", "last_reviewed"], "properties": {"artefact_id": {"type": "string", "minLength": 1}, "owner": {"type": "string", "minLength": 1}, "framework": {"type": "string", "enum": ["playwright", "cypress", "webdriverio"]}, "pages": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["name", "actions"], "properties": {"name": {"type": "string"}, "actions": {"type": "array", "minItems": 1, "items": {"type": "string"}}}}}, "locator_hierarchy": {"type": "array", "minItems": 1, "items": {"type": "string", "enum": ["role", "test-id", "label", "text", "css", "xpath"]}}, "implicit_waits_banned": {"type": "boolean"}, "contract_test_path": {"type": "string"}, "version": {"type": "string", "minLength": 1}, "last_reviewed": {"type": "string", "minLength": 1}}}')
REQUIRED = SCHEMA.get("required", [])


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    props = SCHEMA.get("properties", {})
    for k, v in obj.items():
        if k in props:
            spec = props[k]
            t = spec.get("type")
            if t == "array" and not isinstance(v, list):
                errs.append(f"field {k} must be array")
            elif t == "object" and not isinstance(v, dict):
                errs.append(f"field {k} must be object")
            elif t == "string" and not isinstance(v, str):
                errs.append(f"field {k} must be string")
            elif t == "integer" and not isinstance(v, int):
                errs.append(f"field {k} must be integer")
            elif t == "number" and not isinstance(v, (int, float)):
                errs.append(f"field {k} must be number")
            elif t == "boolean" and not isinstance(v, bool):
                errs.append(f"field {k} must be boolean")
            if "enum" in spec and v not in spec["enum"]:
                errs.append(f"field {k} must be one of {spec['enum']}")
            if t == "array" and isinstance(v, list):
                if "minItems" in spec and len(v) < spec["minItems"]:
                    errs.append(f"field {k} must have minItems={spec['minItems']}")
            if t == "string" and isinstance(v, str):
                if "minLength" in spec and len(v) < spec["minLength"]:
                    errs.append(f"field {k} below minLength {spec['minLength']}")
                if "pattern" in spec:
                    import re as _re
                    if not _re.search(spec["pattern"], v):
                        errs.append(f"field {k} fails pattern {spec['pattern']}")
            if t == "integer" and isinstance(v, int):
                if "minimum" in spec and v < spec["minimum"]:
                    errs.append(f"field {k} below minimum {spec['minimum']}")
                if "maximum" in spec and v > spec["maximum"]:
                    errs.append(f"field {k} above maximum {spec['maximum']}")
    return errs


def _placeholder(spec):
    if "enum" in spec:
        return spec["enum"][0]
    t = spec.get("type")
    if t == "string":
        return "x" * max(spec.get("minLength", 1), 1)
    if t == "integer":
        return spec.get("minimum", 1)
    if t == "number":
        return 0.0
    if t == "boolean":
        return True
    if t == "array":
        inner = spec.get("items", {"type": "string"})
        n = max(spec.get("minItems", 0), 1)
        return [_placeholder(inner) for _ in range(n)]
    if t == "object":
        out = {}
        for rk in spec.get("required", []):
            out[rk] = _placeholder(spec.get("properties", {}).get(rk, {"type": "string"}))
        return out
    return None


def self_test() -> int:
    good = {}
    for k in REQUIRED:
        spec = SCHEMA.get("properties", {}).get(k, {"type": "string"})
        good[k] = _placeholder(spec)
    errs = validate(good)
    if errs:
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(errs) + "\n")
        return 1
    if not validate({}):
        sys.stderr.write("self-test: empty fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
