#!/usr/bin/env python3
"""validate-product-led-growth.py

Validate an output artefact for the `product-led-growth` methodology against the JSON Schema
(draft-07) defined in `content/02-output-contract.xml`. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (valid + invalid)
    --help            this message

Exit codes:
    0 = artefact valid against schema
    1 = artefact invalid (violations on stderr)
    2 = usage / unreadable / bad JSON
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = json.loads(r"""{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://faion.net/schemas/plg-spec.json",
    "type": "object",
    "required": [
        "product",
        "aha_moment",
        "pql_criteria",
        "upgrade_triggers",
        "free_tier_jtbd"
    ],
    "properties": {
        "product": {
            "type": "string"
        },
        "aha_moment": {
            "type": "object",
            "required": [
                "event",
                "median_time_seconds"
            ],
            "properties": {
                "event": {
                    "type": "string"
                },
                "median_time_seconds": {
                    "type": "integer",
                    "maximum": 300
                }
            }
        },
        "pql_criteria": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": [
                    "signal",
                    "threshold"
                ]
            }
        },
        "upgrade_triggers": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "limit_hit",
                    "prompt"
                ]
            },
            "minItems": 1
        },
        "free_tier_jtbd": {
            "type": "string",
            "minLength": 20
        },
        "sales_assist_optional": {
            "type": "boolean",
            "const": true
        }
    }
}""")

VALID_FIXTURE = json.loads(r"""{
  "product": "Faion",
  "aha_moment": {
    "event": "first-get-content",
    "median_time_seconds": 240
  },
  "pql_criteria": [
    {
      "signal": "workspaces",
      "threshold": 2
    },
    {
      "signal": "invited_collaborators",
      "threshold": 1
    }
  ],
  "upgrade_triggers": [
    {
      "limit_hit": "monthly-search-cap",
      "prompt": "Upgrade to keep searching"
    }
  ],
  "free_tier_jtbd": "Search and read free-tier methodologies offline.",
  "sales_assist_optional": true
}""")

INVALID_FIXTURE = json.loads(r"""{
  "product": "x",
  "aha_moment": {
    "event": "signup",
    "median_time_seconds": 600
  }
}""")


def _check_type(value, expected) -> bool:
    if isinstance(expected, list):
        return any(_check_type(value, e) for e in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate(obj, schema, path="$") -> list:
    errs: list = []
    if not isinstance(schema, dict):
        return errs
    t = schema.get("type")
    if t and not _check_type(obj, t):
        errs.append(f"{path}: type mismatch (expected {t})")
        return errs
    if "enum" in schema and obj not in schema["enum"]:
        errs.append(f"{path}: value {obj!r} not in enum {schema['enum']}")
    if "const" in schema and obj != schema["const"]:
        errs.append(f"{path}: value {obj!r} != const {schema['const']!r}")
    if isinstance(obj, dict):
        for r in schema.get("required", []):
            if r not in obj:
                errs.append(f"{path}: missing required key {r}")
        props = schema.get("properties", {})
        addl = schema.get("additionalProperties")
        for k, v in obj.items():
            if k in props:
                errs += _validate(v, props[k], f"{path}.{k}")
            elif isinstance(addl, dict):
                errs += _validate(v, addl, f"{path}.{k}")
    if isinstance(obj, list):
        mn = schema.get("minItems")
        mx = schema.get("maxItems")
        if mn is not None and len(obj) < mn:
            errs.append(f"{path}: array length {len(obj)} < minItems {mn}")
        if mx is not None and len(obj) > mx:
            errs.append(f"{path}: array length {len(obj)} > maxItems {mx}")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, v in enumerate(obj):
                errs += _validate(v, items, f"{path}[{i}]")
    if isinstance(obj, str):
        pat = schema.get("pattern")
        if pat and not re.search(pat, obj):
            errs.append(f"{path}: string {obj!r} does not match pattern {pat!r}")
        ml = schema.get("minLength")
        if ml is not None and len(obj) < ml:
            errs.append(f"{path}: string length {len(obj)} < minLength {ml}")
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        mn = schema.get("minimum")
        mx = schema.get("maximum")
        emn = schema.get("exclusiveMinimum")
        emx = schema.get("exclusiveMaximum")
        if mn is not None and obj < mn:
            errs.append(f"{path}: value {obj} < minimum {mn}")
        if mx is not None and obj > mx:
            errs.append(f"{path}: value {obj} > maximum {mx}")
        if emn is not None and obj <= emn:
            errs.append(f"{path}: value {obj} <= exclusiveMinimum {emn}")
        if emx is not None and obj >= emx:
            errs.append(f"{path}: value {obj} >= exclusiveMaximum {emx}")
    return errs


def validate(obj) -> list:
    return _validate(obj, SCHEMA)


def self_test() -> int:
    errs_valid = validate(VALID_FIXTURE)
    if errs_valid:
        sys.stderr.write("self-test FAIL: valid fixture rejected:\n")
        for e in errs_valid:
            sys.stderr.write(f"  {e}\n")
        return 1
    errs_invalid = validate(INVALID_FIXTURE)
    if not errs_invalid:
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write(
        f"self-test OK (valid clean; invalid produced {len(errs_invalid)} violations)\n"
    )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--file", type=str, help="path to artefact JSON")
    p.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = p.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        p.print_help()
        return 2
    path = Path(args.file)
    if not path.is_file():
        sys.stderr.write(f"not a file: {path}\n")
        return 2
    try:
        obj = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"bad JSON: {e}\n")
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
