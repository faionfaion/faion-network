#!/usr/bin/env python3
"""validate-raci-ai-assisted.py

Validate the RACIMatrix produced by the raci-ai-assisted methodology against the
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
import datetime as dt
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/raci-matrix.json', 'title': 'RACIMatrix', 'type': 'object', 'required': ['project_id', 'header', 'roster', 'wbs_open_leaves', 'rows', 'review_log'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'wbs_id': {'type': 'string', 'pattern': '^[0-9]+(\\.[0-9]+)*$'}, 'role_id': {'type': 'string', 'pattern': '^[A-Za-z0-9][A-Za-z0-9_-]*$', 'not': {'enum': ['team', 'Team', 'TEAM', 'tbd', 'TBD', 'various', 'ai', 'AI', 'agent', 'automation', 'bot']}}, 'anchor': {'type': 'string', 'pattern': '^(charter#[A-Za-z0-9._-]+|wbs-dict#[0-9]+(\\.[0-9]+)*|stakeholders#[A-Za-z0-9._-]+)$'}, 'wbs_id_list': {'type': 'array', 'items': {'$ref': '#/definitions/wbs_id'}, 'uniqueItems': True}}, 'properties': {'__faion_header__': {'type': 'object'}, 'project_id': {'type': 'string', 'minLength': 2}, 'header': {'type': 'object', 'required': ['owner', 'status', 'trigger', 'version', 'last_reviewed'], 'additionalProperties': False, 'properties': {'owner': {'type': 'object', 'required': ['role', 'person'], 'properties': {'role': {'$ref': '#/definitions/role_id'}, 'person': {'type': 'string', 'minLength': 2}}}, 'status': {'enum': ['draft', 'published']}, 'trigger': {'enum': ['kickoff', 'roster_delta', 'quarterly_review']}, 'version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}, 'last_reviewed': {'$ref': '#/definitions/date'}}}, 'roster': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'object', 'required': ['role', 'person'], 'properties': {'role': {'$ref': '#/definitions/role_id'}, 'person': {'type': 'string', 'minLength': 2}}}}, 'wbs_open_leaves': {'$ref': '#/definitions/wbs_id_list', 'minItems': 1}, 'rows': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['wbs_id', 'deliverable', 'responsible', 'accountable', 'consulted', 'informed', 'evidence', 'status'], 'additionalProperties': False, 'properties': {'wbs_id': {'$ref': '#/definitions/wbs_id'}, 'deliverable': {'type': 'string', 'minLength': 2}, 'responsible': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'$ref': '#/definitions/role_id'}}, 'accountable': {'$ref': '#/definitions/role_id'}, 'consulted': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/role_id'}}, 'informed': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/role_id'}}, 'evidence': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/anchor'}}, 'status': {'enum': ['anchored', 'proposed', 'orphaned']}, 'over_consultation_reviewed': {'type': 'boolean'}}, 'if': {'properties': {'status': {'const': 'anchored'}}}, 'then': {'properties': {'evidence': {'minItems': 1}}}}}, 'roster_delta': {'type': 'object', 'required': ['change', 'role', 'person', 'effective_date', 'refresh_deadline', 'rows_changed', 'rows_orphaned', 'rows_reassigned'], 'additionalProperties': False, 'properties': {'change': {'enum': ['join', 'leave', 'role_change']}, 'role': {'$ref': '#/definitions/role_id'}, 'person': {'type': 'string', 'minLength': 2}, 'effective_date': {'$ref': '#/definitions/date'}, 'refresh_deadline': {'$ref': '#/definitions/date'}, 'rows_changed': {'$ref': '#/definitions/wbs_id_list'}, 'rows_orphaned': {'$ref': '#/definitions/wbs_id_list'}, 'rows_reassigned': {'type': 'array', 'items': {'type': 'object', 'required': ['wbs_id', 'column', 'role', 'evidence'], 'properties': {'wbs_id': {'$ref': '#/definitions/wbs_id'}, 'column': {'enum': ['responsible', 'accountable', 'consulted', 'informed']}, 'role': {'$ref': '#/definitions/role_id'}, 'evidence': {'type': 'array', 'minItems': 1, 'items': {'$ref': '#/definitions/anchor'}}}}}}}, 'review_log': {'type': 'array', 'items': {'type': 'object', 'required': ['reviewed_at', 'kind'], 'properties': {'reviewed_at': {'$ref': '#/definitions/date'}, 'kind': {'enum': ['publish', 'quarterly_review']}, 'notification': {'type': 'object', 'required': ['channel', 'sent_on', 'recipients'], 'properties': {'channel': {'type': 'string', 'minLength': 1}, 'sent_on': {'$ref': '#/definitions/date'}, 'recipients': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['role', 'person', 'rows'], 'properties': {'role': {'$ref': '#/definitions/role_id'}, 'person': {'type': 'string', 'minLength': 2}, 'rows': {'$ref': '#/definitions/wbs_id_list', 'minItems': 1}}}}}}, 'rows_removed': {'type': 'integer', 'minimum': 0}, 'rows_reassigned': {'type': 'integer', 'minimum': 0}, 'rows_still_proposed': {'type': 'integer', 'minimum': 0}}, 'allOf': [{'if': {'properties': {'kind': {'const': 'publish'}}}, 'then': {'required': ['notification']}}, {'if': {'properties': {'kind': {'const': 'quarterly_review'}}}, 'then': {'required': ['rows_removed', 'rows_reassigned', 'rows_still_proposed']}}]}}}, 'allOf': [{'if': {'properties': {'header': {'properties': {'status': {'const': 'published'}}}}}, 'then': {'properties': {'rows': {'items': {'properties': {'status': {'const': 'anchored'}}}}, 'review_log': {'minItems': 1, 'contains': {'properties': {'kind': {'const': 'publish'}}, 'required': ['kind']}}}}}, {'if': {'properties': {'header': {'properties': {'trigger': {'const': 'roster_delta'}}}}}, 'then': {'required': ['roster_delta']}}, {'if': {'properties': {'header': {'properties': {'trigger': {'const': 'quarterly_review'}}}}}, 'then': {'properties': {'review_log': {'minItems': 1, 'contains': {'properties': {'kind': {'const': 'quarterly_review'}}, 'required': ['kind']}}}}}]}

OK = {'project_id': 'checkout', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'status': 'published', 'trigger': 'roster_delta', 'version': '1.4.0', 'last_reviewed': '2026-05-10'}, 'roster': [{'role': 'pm', 'person': 'olena.k'}, {'role': 'backend-lead', 'person': 'ihor.m'}, {'role': 'backend-engineer', 'person': 'taras.v'}, {'role': 'appsec-lead', 'person': 'maksym.d'}], 'wbs_open_leaves': ['2.1', '2.2'], 'rows': [{'wbs_id': '2.1', 'deliverable': 'Login endpoint', 'responsible': ['backend-engineer'], 'accountable': 'backend-lead', 'consulted': ['appsec-lead'], 'informed': ['pm'], 'evidence': ['charter#auth-scope', 'wbs-dict#2.1'], 'status': 'anchored'}, {'wbs_id': '2.2', 'deliverable': 'Rate limiting', 'responsible': ['backend-engineer'], 'accountable': 'backend-lead', 'consulted': [], 'informed': ['pm', 'appsec-lead'], 'evidence': ['wbs-dict#2.2'], 'status': 'anchored'}], 'roster_delta': {'change': 'leave', 'role': 'security-lead', 'person': 'dana.r', 'effective_date': '2026-05-15', 'refresh_deadline': '2026-05-15', 'rows_changed': ['2.1', '2.2'], 'rows_orphaned': [], 'rows_reassigned': [{'wbs_id': '2.1', 'column': 'consulted', 'role': 'appsec-lead', 'evidence': ['stakeholders#appsec-lead']}, {'wbs_id': '2.2', 'column': 'informed', 'role': 'appsec-lead', 'evidence': ['stakeholders#appsec-lead']}]}, 'review_log': [{'reviewed_at': '2026-02-03', 'kind': 'publish', 'notification': {'channel': '#checkout', 'sent_on': '2026-02-03', 'recipients': [{'role': 'backend-lead', 'person': 'ihor.m', 'rows': ['2.1', '2.2']}, {'role': 'backend-engineer', 'person': 'taras.v', 'rows': ['2.1', '2.2']}]}}, {'reviewed_at': '2026-05-10', 'kind': 'publish', 'notification': {'channel': '#checkout', 'sent_on': '2026-05-10', 'recipients': [{'role': 'backend-lead', 'person': 'ihor.m', 'rows': ['2.1', '2.2']}, {'role': 'backend-engineer', 'person': 'taras.v', 'rows': ['2.1', '2.2']}]}}]}

BAD = {'project_id': 'checkout', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'status': 'published', 'trigger': 'roster_delta', 'version': '1.4.0', 'last_reviewed': '2026-05-10'}, 'roster': [{'role': 'pm', 'person': 'olena.k'}, {'role': 'backend-lead', 'person': 'ihor.m'}, {'role': 'backend-engineer', 'person': 'taras.v'}], 'wbs_open_leaves': ['2.1', '2.2'], 'rows': [{'wbs_id': '2', 'deliverable': 'Backend', 'responsible': ['backend-engineer'], 'accountable': 'backend-lead, pm', 'consulted': ['security-lead', 'pm'], 'informed': ['pm'], 'evidence': [], 'status': 'anchored'}, {'wbs_id': '2.1', 'deliverable': 'Login endpoint', 'responsible': ['backend-engineer'], 'accountable': 'backend-lead', 'consulted': ['security-lead'], 'informed': ['pm'], 'evidence': ['charter#auth-scope'], 'status': 'proposed'}], 'review_log': [{'reviewed_at': '2026-05-10', 'kind': 'publish'}]}


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


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    header = obj.get("header") or {}
    trigger = header.get("trigger")
    rows = obj.get("rows") or []
    roster_roles = {r.get("role") for r in obj.get("roster") or []}
    open_leaves = set(obj.get("wbs_open_leaves") or [])
    row_ids = [r.get("wbs_id") for r in rows]
    if len(row_ids) != len(set(row_ids)):
        errs.append("rows: duplicate wbs_id; one row per open leaf (r-rows-bind-to-wbs-leaves)")
    for leaf in sorted(open_leaves - set(row_ids)):
        errs.append(f"rows: open WBS leaf {leaf} has no row (r-rows-bind-to-wbs-leaves)")
    for wid in row_ids:
        if any(other != wid and other.startswith(wid + ".") for other in row_ids):
            errs.append(f"rows: {wid} is a summary node (parent of another row); only leaves get rows (r-rows-bind-to-wbs-leaves)")
        if trigger == "quarterly_review" and wid not in open_leaves:
            errs.append(f"rows: {wid} is not an open leaf; the quarterly review removes closed-leaf rows (r-quarterly-review-90-days)")
    ra_roles: set[str] = set()
    for i, row in enumerate(rows):
        cols = {"responsible": list(row.get("responsible") or []), "accountable": [row.get("accountable")],
                "consulted": list(row.get("consulted") or []), "informed": list(row.get("informed") or [])}
        seen: dict[str, str] = {}
        for col, roles in cols.items():
            for role in roles:
                if role in seen:
                    errs.append(f"rows[{i}]: role {role!r} in both {seen[role]} and {col} (r-one-column-per-role-per-row)")
                seen[role] = col
        missing = sorted(set(seen) - roster_roles)
        if missing and row.get("status") != "orphaned":
            errs.append(f"rows[{i}]: roles {missing} not in roster and row not 'orphaned' (r-responsible-in-roster)")
        if len(cols["consulted"]) > len(cols["responsible"]) and row.get("over_consultation_reviewed") is not True:
            errs.append(f"rows[{i}]: consulted ({len(cols['consulted'])}) longer than responsible ({len(cols['responsible'])}) and not reviewed by the PM (r-one-column-per-role-per-row)")
        ra_roles.update(cols["responsible"])
        ra_roles.add(row.get("accountable"))
    delta = obj.get("roster_delta")
    if trigger == "roster_delta" and isinstance(delta, dict):
        eff, dl, lr = _date(delta.get("effective_date")), _date(delta.get("refresh_deadline")), _date(header.get("last_reviewed"))
        if eff and dl:
            want = eff + dt.timedelta(days=7) if delta.get("change") == "join" else eff
            if dl != want:
                errs.append(f"roster_delta.refresh_deadline {dl} must be {want} (last day for leave / role_change, first week for join) (r-trigger-enum-and-roster-delta)")
        if dl and lr and lr > dl:
            errs.append(f"header.last_reviewed {lr} is after roster_delta.refresh_deadline {dl} (r-trigger-enum-and-roster-delta)")
    log = obj.get("review_log") or []
    if header.get("status") == "published":
        pubs = [e for e in log if e.get("kind") == "publish"]
        if pubs:
            notified = {r.get("role") for r in (pubs[-1].get("notification") or {}).get("recipients") or []}
            for role in sorted(ra_roles - notified):
                errs.append(f"review_log: latest publish entry did not notify {role!r}, which holds R or A (r-notify-assignees-on-publish)")
    proposed = sum(1 for r in rows if r.get("status") == "proposed")
    for j, e in enumerate(log):
        if e.get("kind") == "quarterly_review" and j == len(log) - 1 and e.get("rows_still_proposed") != proposed:
            errs.append(f"review_log[{j}].rows_still_proposed {e.get('rows_still_proposed')} != {proposed} proposed rows (r-quarterly-review-90-days)")
    return errs


def validate(obj) -> list[str]:
    errs: list[str] = []
    _check(obj, SCHEMA, "$", errs)
    if not errs and isinstance(obj, dict):
        errs.extend(extra(obj))
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
        prog="validate-raci-ai-assisted.py",
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
