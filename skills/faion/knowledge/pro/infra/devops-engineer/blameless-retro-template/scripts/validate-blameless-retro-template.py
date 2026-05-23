#!/usr/bin/env python3
"""validate-blameless-retro-template.py

Validate the report artefact for the blameless-retro-template methodology against the
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

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/blameless-retro-template.json", "type": "object", "required": ["incident_id", "retro_date", "facilitator", "participants", "timeline_pre_read_link", "contributing_factors", "action_items", "meta_round_notes", "publication_url", "published_within_48h"], "properties": {"incident_id": {"type": "string", "minLength": 1}, "retro_date": {"type": "string", "pattern": "^\\\\d{4}-\\\\d{2}-\\\\d{2}$"}, "facilitator": {"type": "string", "minLength": 1}, "participants": {"type": "array", "minItems": 3, "items": {"type": "object", "required": ["name", "role"], "properties": {"name": {"type": "string"}, "role": {"type": "string"}}}}, "timeline_pre_read_link": {"type": "string", "minLength": 1}, "contributing_factors": {"type": "array", "minItems": 3, "items": {"type": "object", "required": ["factor_text", "category", "evidence_ref"], "properties": {"factor_text": {"type": "string", "minLength": 1}, "category": {"enum": ["detection-gap", "comms-gap", "mitigation-gap", "tooling-gap", "knowledge-gap", "dependency-failure", "other"]}, "evidence_ref": {"type": "string", "minLength": 1}}}}, "action_items": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["text", "owner", "target_date", "tracking_ticket"], "properties": {"text": {"type": "string", "minLength": 1}, "owner": {"type": "string", "minLength": 1, "not": {"enum": ["team", "TBD", ""]}}, "target_date": {"type": "string", "pattern": "^\\\\d{4}-\\\\d{2}-\\\\d{2}$"}, "tracking_ticket": {"type": "string", "minLength": 1}}}}, "meta_round_notes": {"type": "string", "minLength": 1}, "publication_url": {"type": "string", "minLength": 1}, "published_within_48h": {"type": "boolean", "const": true}}}')
REQUIRED = ['incident_id', 'retro_date', 'facilitator', 'participants', 'timeline_pre_read_link', 'contributing_factors', 'action_items', 'meta_round_notes', 'publication_url', 'published_within_48h']


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


OK = json.loads('{"incident_id": "INC-2026-042", "retro_date": "2026-05-23", "facilitator": "jane.s", "participants": [{"name": "alex.k", "role": "responder"}, {"name": "bob.r", "role": "subsystem-owner"}, {"name": "lin.p", "role": "downstream-consumer"}], "timeline_pre_read_link": "https://wiki/inc-042-draft", "contributing_factors": [{"factor_text": "deploy pipeline allowed --skip-tests outside hotfix context", "category": "tooling-gap", "evidence_ref": "log#L42"}, {"factor_text": "alert latency 12 min from first error to page", "category": "detection-gap", "evidence_ref": "alert-history"}, {"factor_text": "no Friday-late-deploy soft-block in CI", "category": "tooling-gap", "evidence_ref": "ci-config"}], "action_items": [{"text": "Replace --skip-tests with hotfix-mode requiring incident-id", "owner": "alex.k", "target_date": "2026-06-15", "tracking_ticket": "JIRA-1234"}], "meta_round_notes": "Almost learned: ownerless flags persist across reorgs.", "publication_url": "https://wiki/inc-042-final", "published_within_48h": true}')
BAD = json.loads('{"incident_id": "INC-2026-042", "retro_date": "2026-05-23", "facilitator": "alex.k", "participants": [{"name": "alex.k", "role": "responder"}], "timeline_pre_read_link": "", "contributing_factors": [{"factor_text": "Bob skipped tests", "category": "knowledge-gap", "evidence_ref": ""}], "action_items": [{"text": "Bob will be more careful", "owner": "team", "target_date": "2025-01-01", "tracking_ticket": ""}], "meta_round_notes": "", "publication_url": "", "published_within_48h": false}')


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
