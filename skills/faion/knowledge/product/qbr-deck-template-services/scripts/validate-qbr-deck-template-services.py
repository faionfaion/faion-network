#!/usr/bin/env python3
"""validate-qbr-deck-template-services.py

Validate an output artefact for the `qbr-deck-template-services` methodology against the JSON Schema
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
    "$id": "https://faion.net/schemas/qbr-deck.json",
    "type": "object",
    "required": [
        "client",
        "quarter",
        "slides",
        "asks"
    ],
    "properties": {
        "client": {
            "type": "string"
        },
        "quarter": {
            "type": "string",
            "pattern": "^\\d{4}-Q[1-4]$"
        },
        "slides": {
            "type": "array",
            "minItems": 10,
            "maxItems": 10,
            "items": {
                "type": "object",
                "required": [
                    "n",
                    "title",
                    "owner",
                    "evidence_anchors"
                ],
                "properties": {
                    "n": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "title": {
                        "type": "string"
                    },
                    "owner": {
                        "type": "string"
                    },
                    "evidence_anchors": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 1
                    }
                }
            }
        },
        "asks": {
            "type": "array",
            "minItems": 1,
            "maxItems": 3,
            "items": {
                "type": "string"
            }
        },
        "outcome_review_included": {
            "type": "boolean",
            "const": true
        }
    }
}""")

VALID_FIXTURE = json.loads(r"""{
  "client": "acme",
  "quarter": "2026-Q2",
  "slides": [
    {
      "n": 1,
      "title": "cover",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 2,
      "title": "outcomes",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 3,
      "title": "metrics",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 4,
      "title": "wins",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 5,
      "title": "risks",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 6,
      "title": "asks",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 7,
      "title": "finance",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 8,
      "title": "retention",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 9,
      "title": "next-quarter",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    },
    {
      "n": 10,
      "title": "owners",
      "owner": "ruslan",
      "evidence_anchors": [
        "https://dashboard"
      ]
    }
  ],
  "asks": [
    "intro to CTO peer"
  ],
  "outcome_review_included": true
}""")

INVALID_FIXTURE = json.loads(r"""{
  "client": "acme",
  "quarter": "Q2",
  "slides": [
    {
      "n": 1,
      "title": "cover"
    }
  ],
  "asks": []
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
