#!/usr/bin/env python3
"""validate-codemod-refactor-agent.py — validate the playbook-step artefact for the mr-codemod-refactor-agent methodology.

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

SCHEMA = json.loads(r"""{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/mr-codemod-refactor-agent.json", "type": "object", "required": ["refactor_id", "ast_tool", "sites_touched", "tests_after_batch", "reviewer_agent_separate"], "properties": {"refactor_id": {"type": "string"}, "ast_tool": {"enum": ["jscodeshift", "ts-morph", "ast-grep", "comby", "roslyn"]}, "sites_touched": {"type": "integer", "minimum": 20}, "tests_after_batch": {"const": true}, "reviewer_agent_separate": {"const": true}, "pr_documents_transform": {"const": true}, "codemod_path": {"type": "string"}}}""")
VALID_FIXTURE = json.loads(r"""{"refactor_id": "rename-user-id-to-uid", "ast_tool": "jscodeshift", "sites_touched": 142, "tests_after_batch": true, "reviewer_agent_separate": true, "pr_documents_transform": true, "codemod_path": "scripts/codemods/rename-user-id.ts"}""")
INVALID_FIXTURE = json.loads(r"""{"refactor_id": "x", "ast_tool": "sed", "sites_touched": 3, "tests_after_batch": false, "reviewer_agent_separate": false}""")


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
