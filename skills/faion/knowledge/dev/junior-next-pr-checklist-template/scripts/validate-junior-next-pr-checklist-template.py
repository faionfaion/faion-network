#!/usr/bin/env python3
"""validate-junior-next-pr-checklist-template.py

Validate the next-PR checklist produced by the junior-next-pr-checklist-template methodology against the
draft-07 JSON Schema embedded in content/02-output-contract.xml. Stdlib-only;
the schema and both fixtures are inlined because `faion get-content` ships
this file alone.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (VIOLATION lines on stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/junior-next-pr-checklist-template.json', 'title': 'Junior next-PR checklist', 'type': 'object', 'required': ['junior', 'mentor', 'source_pr', 'items', 'blocking_item_count', 'deferred', 'retired', 'pairing_sessions', 'posting', 'review'], 'additionalProperties': False, 'properties': {'junior': {'type': 'string', 'minLength': 2}, 'mentor': {'type': 'string', 'minLength': 2}, 'source_pr': {'type': 'object', 'required': ['url', 'review_completed_on'], 'properties': {'url': {'type': 'string', 'pattern': '^https?://'}, 'review_completed_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}, 'previous_checklist_url': {'type': 'string', 'pattern': '^https?://'}, 'items': {'type': 'array', 'minItems': 3, 'maxItems': 7, 'items': {'type': 'object', 'required': ['id', 'check', 'origin_permalink', 'severity', 'standard', 'lint', 'status', 'ticked_by_junior'], 'properties': {'id': {'type': 'string', 'pattern': '^c[0-9]+$'}, 'check': {'type': 'string', 'minLength': 15, 'pattern': '^(?!.*\\b(be more|think about|try to|be careful|cleaner code)\\b).*$'}, 'origin_permalink': {'type': 'string', 'pattern': '^https?://.+#(discussion_r|issuecomment-|r|note_|L)[0-9]+'}, 'severity': {'type': 'string', 'enum': ['blocking', 'should']}, 'standard': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'type': 'string', 'enum': ['style_guide', 'adr', 'contributing', 'preference']}, 'reference': {'type': 'string', 'minLength': 3}, 'mentor_handle': {'type': 'string', 'minLength': 2}}, 'if': {'properties': {'kind': {'const': 'preference'}}}, 'then': {'required': ['mentor_handle']}, 'else': {'required': ['reference']}}, 'lint': {'type': 'object', 'required': ['machine_enforceable'], 'properties': {'machine_enforceable': {'type': 'boolean'}, 'rule': {'type': 'string', 'minLength': 3}, 'automation_ticket': {'type': 'string', 'minLength': 3}, 'prs_since_automation_landed': {'type': 'integer', 'minimum': 0, 'maximum': 1}}, 'if': {'properties': {'machine_enforceable': {'const': True}}}, 'then': {'required': ['rule', 'automation_ticket']}}, 'status': {'type': 'string', 'enum': ['new', 'carried', 'done']}, 'carried_count': {'type': 'integer', 'minimum': 1, 'maximum': 2}, 'ticked_by_junior': {'type': 'boolean'}}, 'allOf': [{'if': {'properties': {'status': {'const': 'carried'}}}, 'then': {'required': ['carried_count']}}, {'if': {'properties': {'standard': {'properties': {'kind': {'const': 'preference'}}, 'required': ['kind']}}}, 'then': {'properties': {'severity': {'const': 'should'}}}}]}}, 'blocking_item_count': {'type': 'integer', 'minimum': 0, 'maximum': 1}, 'deferred': {'type': 'array', 'items': {'type': 'object', 'required': ['check', 'origin_permalink'], 'properties': {'check': {'type': 'string', 'minLength': 15}, 'origin_permalink': {'type': 'string', 'pattern': '^https?://.+#(discussion_r|issuecomment-|r|note_|L)[0-9]+'}}}}, 'retired': {'type': 'array', 'items': {'type': 'object', 'required': ['check', 'consecutive_prs_ticked'], 'properties': {'check': {'type': 'string', 'minLength': 15}, 'consecutive_prs_ticked': {'type': 'integer', 'minimum': 2}}}}, 'pairing_sessions': {'type': 'array', 'items': {'type': 'object', 'required': ['check', 'carried_count', 'scheduled_on'], 'properties': {'check': {'type': 'string', 'minLength': 15}, 'carried_count': {'type': 'integer', 'minimum': 3}, 'scheduled_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}}, 'posting': {'type': 'object', 'required': ['junior_pastes_into_next_pr_description', 'ticks_authored_by', 'mentor_verifies_only'], 'properties': {'junior_pastes_into_next_pr_description': {'const': True}, 'ticks_authored_by': {'const': 'junior'}, 'mentor_verifies_only': {'const': True}}}, 'review': {'type': 'object', 'required': ['status', 'handed_to_junior_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_mentor_review', 'mentor_confirmed']}, 'mentor_confirmed_permalinks_and_severity_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'handed_to_junior_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'mentor_confirmed'}}}, 'then': {'required': ['mentor_confirmed_permalinks_and_severity_on']}}}}

OK = {'junior': '@priya', 'mentor': '@marek', 'source_pr': {'url': 'https://github.com/acme/billing-api/pull/412', 'review_completed_on': '2026-06-18'}, 'previous_checklist_url': 'https://github.com/acme/billing-api/pull/398#issuecomment-2210001', 'items': [{'id': 'c1', 'check': 'Every new database write in the PR runs inside a transaction or the PR description says why it does not', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893320011', 'severity': 'blocking', 'standard': {'kind': 'adr', 'reference': 'ADR-014 transactional boundaries'}, 'lint': {'machine_enforceable': False}, 'status': 'new', 'ticked_by_junior': False}, {'id': 'c2', 'check': 'The PR description links the ticket and lists the manual test that was run', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#issuecomment-2210377', 'severity': 'should', 'standard': {'kind': 'contributing', 'reference': 'CONTRIBUTING.md#pull-request-description'}, 'lint': {'machine_enforceable': False}, 'status': 'carried', 'carried_count': 1, 'ticked_by_junior': False}, {'id': 'c3', 'check': 'Every nullable parameter has an explicit guard or a `?` type annotation', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893321440', 'severity': 'should', 'standard': {'kind': 'style_guide', 'reference': 'docs/style-guide.md#nullability'}, 'lint': {'machine_enforceable': True, 'rule': 'mypy --strict-optional', 'automation_ticket': 'https://github.com/acme/billing-api/issues/419', 'prs_since_automation_landed': 0}, 'status': 'new', 'ticked_by_junior': False}, {'id': 'c4', 'check': 'Every new public function has a docstring stating its return type and raised exceptions', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893322905', 'severity': 'should', 'standard': {'kind': 'preference', 'mentor_handle': '@marek'}, 'lint': {'machine_enforceable': False}, 'status': 'new', 'ticked_by_junior': False}], 'blocking_item_count': 1, 'deferred': [{'check': 'Log lines in the payment path use the structured logger, not print', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893323112'}], 'retired': [{'check': 'Every new test file name starts with test_ and lives beside the module it tests', 'consecutive_prs_ticked': 2}], 'pairing_sessions': [], 'posting': {'junior_pastes_into_next_pr_description': True, 'ticks_authored_by': 'junior', 'mentor_verifies_only': True}, 'review': {'status': 'ready_for_mentor_review', 'handed_to_junior_by_agent': False}}

BAD = {'junior': '@priya', 'mentor': '@marek', 'source_pr': {'url': 'https://github.com/acme/billing-api/pull/412', 'review_completed_on': '2026-06-18'}, 'items': [{'id': 'c1', 'check': 'Be more careful with null handling and think about edge cases', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893321440', 'severity': 'blocking', 'standard': {'kind': 'preference', 'mentor_handle': '@marek'}, 'lint': {'machine_enforceable': False}, 'status': 'carried', 'carried_count': 4, 'ticked_by_junior': True}, {'id': 'c2', 'check': 'Imports are sorted and there is no trailing whitespace anywhere in the diff', 'origin_permalink': 'https://github.com/acme/billing-api/pull/412#discussion_r1893320011', 'severity': 'blocking', 'standard': {'kind': 'style_guide', 'reference': 'docs/style-guide.md#formatting'}, 'lint': {'machine_enforceable': True}, 'status': 'new', 'ticked_by_junior': True}], 'blocking_item_count': 2, 'deferred': [], 'retired': [], 'pairing_sessions': [], 'posting': {'junior_pastes_into_next_pr_description': False, 'ticks_authored_by': 'mentor', 'mentor_verifies_only': False}, 'review': {'status': 'mentor_confirmed', 'handed_to_junior_by_agent': True}}


def _is_type(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (
            isinstance(value, float) and value.is_integer())
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return True


def _check(node, schema, path, errs):
    """Draft-07 subset: $ref (local definitions), required, type, enum, const, pattern,
    minimum/maximum, exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
    uniqueItems, items, contains, properties, additionalProperties, allOf/anyOf/oneOf/not,
    if/then/else."""
    if schema is True:
        return
    if schema is False:
        errs.append(f"{path}: schema forbids any value here")
        return
    if "$ref" in schema:
        target = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            target = target[part]
        _check(node, target, path, errs)
        return
    if "const" in schema and node != schema["const"]:
        errs.append(f"{path}: must equal {schema['const']!r}, got {node!r}")
    if "enum" in schema and node not in schema["enum"]:
        errs.append(f"{path}: {node!r} not in enum {schema['enum']!r}")
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(node, x) for x in types):
            errs.append(f"{path}: expected {t}, got {type(node).__name__}")
            return
    if isinstance(node, dict):
        for k in schema.get("required", []):
            if k not in node:
                errs.append(f"{path}.{k}: missing required field")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in node:
                _check(node[k], sub, f"{path}.{k}", errs)
        addl = schema.get("additionalProperties", True)
        for k in node:
            if k not in props:
                if addl is False:
                    errs.append(f"{path}.{k}: additional property not allowed")
                elif isinstance(addl, dict):
                    _check(node[k], addl, f"{path}.{k}", errs)
    if isinstance(node, list):
        mn, mx = schema.get("minItems"), schema.get("maxItems")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: {len(node)} items, minItems={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: {len(node)} items, maxItems={mx}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(x, sort_keys=True) for x in node]
            if len(seen) != len(set(seen)):
                errs.append(f"{path}: items must be unique")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, item in enumerate(node):
                _check(item, items, f"{path}[{i}]", errs)
        if "contains" in schema and not any(not _probe(item, schema["contains"]) for item in node):
            errs.append(f"{path}: no item matches 'contains' {schema['contains']!r}")
    if isinstance(node, str):
        mn, mx = schema.get("minLength"), schema.get("maxLength")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: length {len(node)} below minLength={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: length {len(node)} above maxLength={mx}")
        pat = schema.get("pattern")
        if pat is not None and not re.search(pat, node):
            errs.append(f"{path}: {node!r} does not match pattern {pat!r}")
    if isinstance(node, (int, float)) and not isinstance(node, bool):
        for key, bad in (("minimum", lambda v: node < v), ("maximum", lambda v: node > v),
                         ("exclusiveMinimum", lambda v: node <= v),
                         ("exclusiveMaximum", lambda v: node >= v)):
            if key in schema and bad(schema[key]):
                errs.append(f"{path}: {node!r} violates {key}={schema[key]!r}")
    for sub in schema.get("allOf", []):
        _check(node, sub, path, errs)
    if "anyOf" in schema:
        if not any(not _probe(node, s) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema:
        hits = sum(1 for s in schema["oneOf"] if not _probe(node, s))
        if hits != 1:
            errs.append(f"{path}: matches {hits} of oneOf, need exactly 1")
    if "not" in schema and not _probe(node, schema["not"]):
        errs.append(f"{path}: matches forbidden 'not' schema")
    if "if" in schema:
        branch = "then" if not _probe(node, schema["if"]) else "else"
        if branch in schema:
            _check(node, schema[branch], path, errs)


def _probe(node, schema):
    tmp: list[str] = []
    _check(node, schema, "$", tmp)
    return tmp


def validate(obj) -> list[str]:
    errs: list[str] = []
    _check(obj, SCHEMA, "$", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-junior-next-pr-checklist-template.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run the contract's own examples and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
