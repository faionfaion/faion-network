#!/usr/bin/env python3
"""validate-rust-testing-ci-toolchain.py

Validate the output artefact for the rust-testing-ci-toolchain methodology against the embedded
JSON Schema (draft-07 subset) from content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in valid/invalid fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable / unparseable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA: dict[str, Any] = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/rust-testing-ci-toolchain.json", "type": "object", "required": ["nextest_config_path", "ci_workflow_path", "tools_pinned", "cache_keys", "miri_gated"], "properties": {"nextest_config_path": {"type": "string", "pattern": "nextest\\\\.toml$"}, "ci_workflow_path": {"type": "string", "pattern": "^\\\\.github/workflows/.*\\\\.ya?ml$"}, "tools_pinned": {"type": "array", "items": {"type": "object", "required": ["name", "version"], "properties": {"name": {"enum": ["cargo-nextest", "cargo-llvm-cov", "cargo-miri"]}, "version": {"type": "string", "minLength": 1}}}, "minItems": 2}, "cache_keys": {"type": "array", "items": {"type": "string"}, "minItems": 1}, "miri_gated": {"type": "boolean"}, "coverage_hard_gate": {"const": false}}}')
VALID_FIXTURE: dict[str, Any] = json.loads('{"nextest_config_path": ".config/nextest.toml", "ci_workflow_path": ".github/workflows/test.yml", "tools_pinned": [{"name": "cargo-nextest", "version": "0.9.78"}, {"name": "cargo-llvm-cov", "version": "0.6.11"}], "cache_keys": ["v2-cargo-${{ hashFiles(\'Cargo.lock\') }}"], "miri_gated": true, "coverage_hard_gate": false}')
INVALID_FIXTURE: dict[str, Any] = json.loads('{"nextest_config_path": "nextest.toml", "ci_workflow_path": "test.yml", "tools_pinned": [], "cache_keys": [], "miri_gated": false, "coverage_hard_gate": true}')


def _check_type(value: Any, t: Any) -> bool:
    types = t if isinstance(t, list) else [t]
    for ty in types:
        if ty == "object" and isinstance(value, dict):
            return True
        if ty == "array" and isinstance(value, list):
            return True
        if ty == "string" and isinstance(value, str):
            return True
        if ty == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if ty == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if ty == "boolean" and isinstance(value, bool):
            return True
        if ty == "null" and value is None:
            return True
    return False


def _validate(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errs: list[str] = []
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: value {value!r} not in enum {schema['enum']}")
    if "type" in schema and not _check_type(value, schema["type"]):
        errs.append(f"{path}: expected type {schema['type']!r}, got {type(value).__name__}")
    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errs.append(f"{path}: missing required field {req!r}")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in value:
                errs.extend(_validate(value[k], sub, f"{path}.{k}"))
    if isinstance(value, list):
        items = schema.get("items")
        if items:
            for i, v in enumerate(value):
                errs.extend(_validate(v, items, f"{path}[{i}]"))
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path}: minItems {schema['minItems']}, got {len(value)}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path}: maxItems {schema['maxItems']}, got {len(value)}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path}: minLength {schema['minLength']}, got {len(value)}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{path}: maxLength {schema['maxLength']}, got {len(value)}")
        if "pattern" in schema:
            try:
                if not re.search(schema["pattern"], value):
                    errs.append(f"{path}: pattern {schema['pattern']!r} did not match {value!r}")
            except re.error as e:
                errs.append(f"{path}: invalid pattern: {e}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path}: minimum {schema['minimum']}, got {value}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path}: maximum {schema['maximum']}, got {value}")
    return errs


def validate(obj: Any) -> list[str]:
    return _validate(obj, SCHEMA)


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        for e in errs_ok:
            sys.stderr.write(f"  {e}\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
