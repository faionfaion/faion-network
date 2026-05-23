#!/usr/bin/env python3
"""validate-quarter-retro-synthesis.py — validate the report artefact for the kb-ai-assisted-quarter-retro-synthesis methodology.

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

SCHEMA = json.loads(r"""{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/ai-assisted-quarter-retro-synthesis.json", "type": "object", "required": ["quarter_metadata", "dora_deltas", "themes", "incidents_referenced", "action_items", "human_edit_pass"], "properties": {"quarter_metadata": {"type": "object", "required": ["quarter", "squads_count", "model", "finalized_at"], "properties": {"quarter": {"type": "string", "pattern": "^[0-9]{4}-Q[1-4]$"}, "squads_count": {"type": "integer", "minimum": 3}, "model": {"type": "string"}, "finalized_at": {"type": "string", "format": "date-time"}}}, "dora_deltas": {"type": "object", "required": ["lead_time", "change_failure_rate", "deploy_frequency", "mttr"], "properties": {"lead_time": {"type": "object", "required": ["prev", "curr", "source_row"]}, "change_failure_rate": {"type": "object"}, "deploy_frequency": {"type": "object"}, "mttr": {"type": "object"}}}, "themes": {"type": "array", "minItems": 3, "maxItems": 10, "items": {"type": "object", "required": ["title", "evidence_quotes", "severity", "recurrence_count"]}}, "incidents_referenced": {"type": "array", "items": {"type": "object", "required": ["incident_id", "postmortem_doc"]}}, "action_items": {"type": "array", "minItems": 5, "maxItems": 10, "items": {"type": "object", "required": ["title", "owner_role", "deadline", "success_criteria"]}}, "human_edit_pass": {"type": "object", "required": ["citation_check_passed"], "properties": {"citation_check_passed": {"const": true}}}}}""")
VALID_FIXTURE = json.loads(r"""{"quarter_metadata": {"quarter": "2026-Q1", "squads_count": 4, "model": "claude-opus-4-7", "finalized_at": "2026-04-15T10:00:00Z"}, "dora_deltas": {"lead_time": {"prev": 168, "curr": 144, "source_row": "snapshot.csv:42"}, "change_failure_rate": {"prev": 0.18, "curr": 0.12, "source_row": "snapshot.csv:43"}, "deploy_frequency": {"prev": 2.1, "curr": 3.4, "source_row": "snapshot.csv:44"}, "mttr": {"prev": 240, "curr": 180, "source_row": "snapshot.csv:45"}}, "themes": [{"title": "Theme 1", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "x", "source_doc": "r.md", "line_range": "L1"}, {"verbatim_text": "y", "source_doc": "r2.md", "line_range": "L2"}]}, {"title": "Theme 2", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "x", "source_doc": "r.md", "line_range": "L1"}, {"verbatim_text": "y", "source_doc": "r2.md", "line_range": "L2"}]}, {"title": "Theme 3", "severity": 2, "recurrence_count": 2, "evidence_quotes": [{"verbatim_text": "x", "source_doc": "r.md", "line_range": "L1"}, {"verbatim_text": "y", "source_doc": "r2.md", "line_range": "L2"}]}], "incidents_referenced": [{"incident_id": "INC-101", "postmortem_doc": "pm-101.md"}], "action_items": [{"title": "Act 1", "owner_role": "Lead 1", "deadline": "2026-06-30", "success_criteria": "Crit 1"}, {"title": "Act 2", "owner_role": "Lead 2", "deadline": "2026-06-30", "success_criteria": "Crit 2"}, {"title": "Act 3", "owner_role": "Lead 3", "deadline": "2026-06-30", "success_criteria": "Crit 3"}, {"title": "Act 4", "owner_role": "Lead 4", "deadline": "2026-06-30", "success_criteria": "Crit 4"}, {"title": "Act 5", "owner_role": "Lead 5", "deadline": "2026-06-30", "success_criteria": "Crit 5"}], "human_edit_pass": {"citation_check_passed": true}}""")
INVALID_FIXTURE = json.loads(r"""{"quarter_metadata": {"quarter": "Q1", "squads_count": 2}, "dora_deltas": {"lead_time": "improved"}, "themes": [], "action_items": [{"title": "Do stuff", "owner_role": "team", "deadline": "2030-01-01", "success_criteria": "x"}]}""")


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
