#!/usr/bin/env python3
"""validate-load-balancing-concepts.py

Validate the decision-record artefact for the load-balancing-concepts methodology against the
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

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/load-balancing-concepts.json", "type": "object", "required": ["service", "layer", "algorithm", "health_check", "persistence", "ha_topology", "rationale"], "properties": {"service": {"type": "string", "minLength": 1}, "layer": {"enum": ["L4", "L7", "DNS", "Global"]}, "algorithm": {"enum": ["round-robin", "weighted-round-robin", "ip-hash", "least-connections", "weighted-least-connections", "least-response-time", "random"]}, "health_check": {"type": "object", "required": ["type", "interval_s", "timeout_s", "healthy_threshold", "unhealthy_threshold"], "properties": {"type": {"enum": ["tcp", "http", "https", "grpc", "custom"]}, "path": {"type": "string"}, "interval_s": {"type": "integer", "minimum": 5, "maximum": 60}, "timeout_s": {"type": "integer", "minimum": 1, "maximum": 30}, "healthy_threshold": {"type": "integer", "minimum": 1, "maximum": 10}, "unhealthy_threshold": {"type": "integer", "minimum": 1, "maximum": 10}}}, "persistence": {"enum": ["none", "externalised-redis", "externalised-db", "sticky-cookie", "sticky-ip-hash"]}, "ha_topology": {"enum": ["active-active", "active-passive", "multi-region-gslb", "single"]}, "rationale": {"type": "string", "minLength": 30}}}')
REQUIRED = ['service', 'layer', 'algorithm', 'health_check', 'persistence', 'ha_topology', 'rationale']


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


OK = json.loads('{"service": "checkout-api", "layer": "L7", "algorithm": "least-connections", "health_check": {"type": "http", "path": "/health", "interval_s": 15, "timeout_s": 5, "healthy_threshold": 2, "unhealthy_threshold": 3}, "persistence": "externalised-redis", "ha_topology": "active-active", "rationale": "WebSocket + REST mix needs L7 routing; session state in Redis to keep backends interchangeable; bursty checkout traffic so least-connections to balance long-lived calls."}')
BAD = json.loads('{"service": "checkout-api", "layer": "L4", "algorithm": "round-robin", "health_check": {"type": "tcp", "interval_s": 60, "timeout_s": 30, "healthy_threshold": 1, "unhealthy_threshold": 1}, "persistence": "sticky-ip-hash", "ha_topology": "single"}')


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
