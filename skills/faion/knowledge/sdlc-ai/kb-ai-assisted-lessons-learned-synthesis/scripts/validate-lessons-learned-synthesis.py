#!/usr/bin/env python3
"""validate-lessons-learned-synthesis.py — validate the report artefact for the kb-ai-assisted-lessons-learned-synthesis methodology.

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

SCHEMA = json.loads(r"""{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/ai-assisted-lessons-learned-synthesis.json", "type": "object", "required": ["synthesis_metadata", "themes", "action_items", "human_edit_pass"], "properties": {"synthesis_metadata": {"type": "object", "required": ["window_start", "window_end", "retros_ingested_count", "model", "human_editor", "finalized_at"], "properties": {"window_start": {"type": "string", "format": "date"}, "window_end": {"type": "string", "format": "date"}, "retros_ingested_count": {"type": "integer", "minimum": 5}, "model": {"type": "string"}, "human_editor": {"type": "string"}, "finalized_at": {"type": "string", "format": "date-time"}}}, "themes": {"type": "array", "minItems": 3, "maxItems": 12, "items": {"type": "object", "required": ["theme_id", "title", "severity", "recurrence_count", "evidence_quotes"], "properties": {"theme_id": {"type": "string"}, "title": {"type": "string"}, "severity": {"type": "integer", "enum": [0, 1, 2, 3]}, "recurrence_count": {"type": "integer", "minimum": 2}, "evidence_quotes": {"type": "array", "minItems": 2, "items": {"type": "object", "required": ["verbatim_text", "source_doc", "line_range"], "properties": {"verbatim_text": {"type": "string"}, "source_doc": {"type": "string"}, "line_range": {"type": "string"}}}}}}}, "action_items": {"type": "array", "minItems": 5, "maxItems": 10, "items": {"type": "object", "required": ["title", "owner_role", "deadline", "success_criteria"], "properties": {"title": {"type": "string"}, "owner_role": {"type": "string", "not": {"enum": ["team", "we", "everyone", ""]}}, "deadline": {"type": "string", "format": "date"}, "success_criteria": {"type": "string"}}}}, "human_edit_pass": {"type": "object", "required": ["citation_check_passed"], "properties": {"citation_check_passed": {"type": "boolean", "const": true}}}}}""")
VALID_FIXTURE = json.loads(r"""{"synthesis_metadata": {"window_start": "2025-01-01", "window_end": "2026-04-30", "retros_ingested_count": 8, "model": "claude-opus-4-7", "human_editor": "Jane Doe (Delivery Lead)", "finalized_at": "2026-05-22T10:00:00Z"}, "themes": [{"theme_id": "t-001", "title": "Discovery \u2192 spec handoff timing", "severity": 3, "recurrence_count": 4, "evidence_quotes": [{"verbatim_text": "Spec arrived 2 weeks after discovery ended", "source_doc": "project-A-retro.md", "line_range": "L42-43"}, {"verbatim_text": "Discovery panel was unreachable for clarification", "source_doc": "project-G-retro.md", "line_range": "L17-18"}]}, {"theme_id": "t-002", "title": "Theme 2", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "q2a", "source_doc": "r2.md", "line_range": "L1-2"}, {"verbatim_text": "q2b", "source_doc": "r2b.md", "line_range": "L3-4"}]}, {"theme_id": "t-003", "title": "Theme 3", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "q3a", "source_doc": "r3.md", "line_range": "L1-2"}, {"verbatim_text": "q3b", "source_doc": "r3b.md", "line_range": "L3-4"}]}, {"theme_id": "t-004", "title": "Theme 4", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "q4a", "source_doc": "r4.md", "line_range": "L1-2"}, {"verbatim_text": "q4b", "source_doc": "r4b.md", "line_range": "L3-4"}]}], "action_items": [{"title": "Action 1", "owner_role": "Role 1", "deadline": "2026-08-31", "success_criteria": "Metric 1 hits target"}, {"title": "Action 2", "owner_role": "Role 2", "deadline": "2026-08-31", "success_criteria": "Metric 2 hits target"}, {"title": "Action 3", "owner_role": "Role 3", "deadline": "2026-08-31", "success_criteria": "Metric 3 hits target"}, {"title": "Action 4", "owner_role": "Role 4", "deadline": "2026-08-31", "success_criteria": "Metric 4 hits target"}, {"title": "Action 5", "owner_role": "Role 5", "deadline": "2026-08-31", "success_criteria": "Metric 5 hits target"}], "human_edit_pass": {"citation_check_passed": true}}""")
INVALID_FIXTURE = json.loads(r"""{"themes": [{"title": "Communication issues", "severity": 2, "recurrence_count": 1, "evidence_quotes": []}], "action_items": [{"title": "Improve things", "owner_role": "team", "deadline": "2027-12-31", "success_criteria": "Better"}]}""")


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
