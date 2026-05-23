#!/usr/bin/env python3
"""validate-devops-aws-service-selection.py

Validate the decision-record artefact for the devops-aws-service-selection methodology against the
JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in good/bad fixtures (no external file needed)
    --help            this message

Outputs:
    stdout 'OK' on pass; stderr 'VIOLATION:' lines on fail.

Exit codes:
    0 = valid
    1 = invalid (one or more VIOLATION lines emitted)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/devops-aws-service-selection.json", "type": "object", "required": ["workload", "compute", "database", "wa_pillars_evaluated", "gap_list"], "properties": {"workload": {"type": "string", "minLength": 1}, "compute": {"type": "object", "required": ["choice", "architecture", "rationale"], "properties": {"choice": {"enum": ["lambda", "fargate", "eks", "ec2"]}, "architecture": {"enum": ["arm64", "x86_64"]}, "rationale": {"type": "string", "minLength": 20}}}, "database": {"type": "object", "required": ["choice", "rationale"], "properties": {"choice": {"enum": ["dynamodb", "aurora-serverless-v2", "rds", "elasticache", "opensearch", "none"]}, "rationale": {"type": "string", "minLength": 20}}}, "wa_pillars_evaluated": {"type": "array", "items": {"enum": ["operational_excellence", "security", "reliability", "performance_efficiency", "cost_optimization", "sustainability"]}, "minItems": 6}, "gap_list": {"type": "array"}}}')
REQUIRED = ['workload', 'compute', 'database', 'wa_pillars_evaluated', 'gap_list']


def _check(obj, schema, path):
    """Lightweight JSON Schema draft-07 subset: required, type, enum, minLength,
    maxLength, minimum, maximum, minItems, pattern, const, properties, items,
    contains, not.enum."""
    errs = []
    if not isinstance(schema, dict):
        return errs
    t = schema.get("type")
    if t:
        if t == "object" and not isinstance(obj, dict):
            return [f"{path or '<root>'}: type expected object got {type(obj).__name__}"]
        if t == "array" and not isinstance(obj, list):
            return [f"{path or '<root>'}: type expected array got {type(obj).__name__}"]
        if t == "string" and not isinstance(obj, str):
            return [f"{path or '<root>'}: type expected string got {type(obj).__name__}"]
        if t == "integer" and (not isinstance(obj, int) or isinstance(obj, bool)):
            return [f"{path or '<root>'}: type expected integer"]
        if t == "number" and (not isinstance(obj, (int, float)) or isinstance(obj, bool)):
            return [f"{path or '<root>'}: type expected number"]
        if t == "boolean" and not isinstance(obj, bool):
            return [f"{path or '<root>'}: type expected boolean"]
    if "const" in schema:
        if obj != schema["const"]:
            errs.append(f"{path or '<root>'}: const expected {schema['const']!r} got {obj!r}")
    if "enum" in schema:
        if obj not in schema["enum"]:
            errs.append(f"{path or '<root>'}: enum violation, got {obj!r} not in {schema['enum']}")
    if "not" in schema and "enum" in schema["not"]:
        if obj in schema["not"]["enum"]:
            errs.append(f"{path or '<root>'}: not.enum violation, {obj!r} forbidden")
    if isinstance(obj, str):
        if "minLength" in schema and len(obj) < schema["minLength"]:
            errs.append(f"{path or '<root>'}: minLength {schema['minLength']}, got {len(obj)}")
        if "maxLength" in schema and len(obj) > schema["maxLength"]:
            errs.append(f"{path or '<root>'}: maxLength {schema['maxLength']}, got {len(obj)}")
        if "pattern" in schema and not re.search(schema["pattern"], obj):
            errs.append(f"{path or '<root>'}: pattern {schema['pattern']!r} unmatched")
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if "minimum" in schema and obj < schema["minimum"]:
            errs.append(f"{path or '<root>'}: minimum {schema['minimum']}, got {obj}")
        if "maximum" in schema and obj > schema["maximum"]:
            errs.append(f"{path or '<root>'}: maximum {schema['maximum']}, got {obj}")
    if isinstance(obj, list):
        if "minItems" in schema and len(obj) < schema["minItems"]:
            errs.append(f"{path or '<root>'}: minItems {schema['minItems']}, got {len(obj)}")
        if "items" in schema:
            for i, v in enumerate(obj):
                errs.extend(_check(v, schema["items"], f"{path}[{i}]"))
        if "contains" in schema:
            if not any(not _check(v, schema["contains"], "") for v in obj):
                errs.append(f"{path or '<root>'}: contains constraint unsatisfied")
    if isinstance(obj, dict):
        for k in schema.get("required", []):
            if k not in obj:
                errs.append(f"{path or '<root>'}: missing required field '{k}'")
        for k, sub in schema.get("properties", {}).items():
            if k in obj:
                errs.extend(_check(obj[k], sub, f"{path}.{k}" if path else k))
    return errs


def validate(obj) -> list:
    return _check(obj, SCHEMA, "")


OK = json.loads('{"workload": "checkout-api", "compute": {"choice": "lambda", "architecture": "arm64", "rationale": "Spiky <15min handler; scale-to-zero saves cost."}, "database": {"choice": "dynamodb", "rationale": "Key-value access pattern; on-demand removes capacity planning."}, "wa_pillars_evaluated": ["operational_excellence", "security", "reliability", "performance_efficiency", "cost_optimization", "sustainability"], "gap_list": []}')
BAD = json.loads('{"workload": "checkout-api", "compute": {"choice": "lambda", "architecture": "x86_64", "rationale": ""}, "database": {"choice": "dynamodb", "rationale": "we wanted"}, "wa_pillars_evaluated": ["security"], "gap_list": []}')


def self_test() -> int:
    e = validate(OK)
    if e:
        sys.stderr.write("self-test FAIL: good fixture rejected:\n")
        for x in e:
            sys.stderr.write(f"  {x}\n")
        return 1
    e = validate(BAD)
    if not e:
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
