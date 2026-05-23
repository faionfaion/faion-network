#!/usr/bin/env python3
"""validate-symbol-index-fresh-tags.py — validate the config artefact for the kb-symbol-index-fresh-tags methodology.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = json.loads(r"""{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/kb-symbol-index-fresh-tags.json", "type": "object", "required": ["index_tool", "index_path", "refresh_strategy", "ci_gate"], "properties": {"index_tool": {"enum": ["serena", "scip", "ctags", "sourcegraph"]}, "index_path": {"type": "string"}, "refresh_strategy": {"type": "object", "required": ["on_precommit", "on_ci_full"], "properties": {"on_precommit": {"enum": ["incremental", "full", "disabled"]}, "on_ci_full": {"enum": ["scheduled", "every_pr"]}}}, "ci_gate": {"type": "object", "required": ["fail_on_stale"], "properties": {"fail_on_stale": {"const": true}}}, "query_interface": {"enum": ["json-cli", "lsp", "scip-rpc"]}}}""")
VALID_FIXTURE = json.loads(r"""{"index_tool": "ctags", "index_path": ".symbol-index/tags", "refresh_strategy": {"on_precommit": "incremental", "on_ci_full": "scheduled"}, "ci_gate": {"fail_on_stale": true}, "query_interface": "json-cli"}""")
INVALID_FIXTURE = json.loads(r"""{"index_tool": "grep", "ci_gate": {"fail_on_stale": false}}""")


def _check_required(obj, schema, path, errs):
    if not isinstance(obj, dict):
        errs.append(f"{path}: expected object, got {type(obj).__name__}")
        return
    for req in schema.get("required", []):
        if req not in obj:
            errs.append(f"{path}: missing required key '{req}'")
    props = schema.get("properties", {})
    for k, v in obj.items():
        if k in props:
            _check_node(v, props[k], f"{path}.{k}", errs)


def _check_node(node, sch, path, errs):
    if not isinstance(sch, dict):
        return
    t = sch.get("type")
    if "const" in sch and node != sch["const"]:
        errs.append(f"{path}: expected const {sch['const']!r}, got {node!r}")
    if "enum" in sch and node not in sch["enum"]:
        errs.append(f"{path}: value {node!r} not in enum {sch['enum']}")
    if t == "object":
        _check_required(node, sch, path, errs)
    elif t == "array":
        if not isinstance(node, list):
            errs.append(f"{path}: expected array")
            return
        if "minItems" in sch and len(node) < sch["minItems"]:
            errs.append(f"{path}: minItems {sch['minItems']}, got {len(node)}")
        if "maxItems" in sch and len(node) > sch["maxItems"]:
            errs.append(f"{path}: maxItems {sch['maxItems']}, got {len(node)}")
        if sch.get("uniqueItems") and len(set(map(repr, node))) != len(node):
            errs.append(f"{path}: items not unique")
        items_sch = sch.get("items")
        if items_sch:
            for i, it in enumerate(node):
                _check_node(it, items_sch, f"{path}[{i}]", errs)
    elif t == "integer":
        if not isinstance(node, int) or isinstance(node, bool):
            errs.append(f"{path}: expected integer")
            return
        if "minimum" in sch and node < sch["minimum"]:
            errs.append(f"{path}: value {node} < minimum {sch['minimum']}")
        if "maximum" in sch and node > sch["maximum"]:
            errs.append(f"{path}: value {node} > maximum {sch['maximum']}")
    elif t == "number":
        if not isinstance(node, (int, float)) or isinstance(node, bool):
            errs.append(f"{path}: expected number")
            return
    elif t == "string":
        if not isinstance(node, str):
            errs.append(f"{path}: expected string")
            return
        if "pattern" in sch and not re.search(sch["pattern"], node):
            errs.append(f"{path}: does not match pattern {sch['pattern']}")
    elif t == "boolean":
        if not isinstance(node, bool):
            errs.append(f"{path}: expected boolean")


def validate(obj) -> list[str]:
    errs: list[str] = []
    _check_node(obj, SCHEMA, "$", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
