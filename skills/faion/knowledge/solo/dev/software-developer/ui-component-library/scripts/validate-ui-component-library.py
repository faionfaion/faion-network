#!/usr/bin/env python3
"""validate-ui-component-library.py

Validate an artefact produced by the ui-component-library methodology against the JSON
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

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/ui-component-library.json", "type": "object", "required": ["layers", "storybook", "a11y", "visual_regression", "release_process"], "properties": {"layers": {"type": "array", "minItems": 4, "items": {"type": "string", "enum": ["tokens", "primitives", "patterns", "templates"]}}, "storybook": {"type": "object", "required": ["enabled", "states_required"]}, "a11y": {"type": "object", "required": ["tool", "gate"]}, "visual_regression": {"type": "object", "required": ["tool", "gate"]}, "release_process": {"type": "object", "required": ["semver", "changelog"]}, "deprecation_window_minors": {"type": "integer", "minimum": 1}}}')
REQUIRED = SCHEMA.get("required", [])


def validate(obj) -> list[str]:
    errs: list[str] = []
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
            elif t == "boolean" and not isinstance(v, bool):
                errs.append(f"field {k} must be boolean")
            if "enum" in spec and v not in spec["enum"]:
                errs.append(f"field {k} must be one of {spec['enum']}")
            if t == "array" and isinstance(v, list):
                if "minItems" in spec and len(v) < spec["minItems"]:
                    errs.append(f"field {k} must have minItems={spec['minItems']}")
            if t == "object" and isinstance(v, dict):
                for rk in spec.get("required", []):
                    if rk not in v:
                        errs.append(f"field {k}.{rk} missing")
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
        return "x"
    if t == "integer":
        return spec.get("minimum", 1)
    if t == "number":
        return 0
    if t == "boolean":
        return True
    if t == "array":
        return []
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
        # Ensure minItems satisfied for arrays
        if spec.get("type") == "array" and spec.get("minItems", 0) > 0:
            inner = spec.get("items", {"type": "string"})
            good[k] = [_placeholder(inner) for _ in range(spec["minItems"])]
    if validate(good):
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(validate(good)) + "\n")
        return 1
    if not validate({}):
        sys.stderr.write("self-test: empty fixture accepted\n"); return 1
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
