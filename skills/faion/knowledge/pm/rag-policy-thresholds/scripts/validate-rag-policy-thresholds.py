#!/usr/bin/env python3
"""validate-rag-policy-thresholds.py

Validate the RAGPolicy produced by the rag-policy-thresholds methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/rag-policy.json', 'title': 'RAGPolicy', 'type': 'object', 'required': ['project_id', 'header', 'signals', 'actions', 'review_log', 'colour_history'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'colour': {'enum': ['green', 'amber', 'red']}, 'signal_id': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'}, 'anchor': {'type': 'string', 'pattern': '^(incident-[A-Za-z0-9._-]+|postmortem-[A-Za-z0-9._-]+|policy://[^\\s]+|baseline-[A-Za-z0-9._-]+)$'}, 'signal_change': {'type': 'object', 'required': ['signal_id', 'reason'], 'properties': {'signal_id': {'$ref': '#/definitions/signal_id'}, 'reason': {'type': 'string', 'minLength': 10}, 'evidence': {'type': 'array', 'items': {'$ref': '#/definitions/anchor'}}}}}, 'properties': {'__faion_header__': {'type': 'object'}, 'project_id': {'type': 'string', 'minLength': 2}, 'header': {'type': 'object', 'required': ['owner', 'version', 'last_reviewed', 'reporting_cadence_days'], 'additionalProperties': False, 'properties': {'owner': {'type': 'object', 'required': ['role', 'person'], 'properties': {'role': {'type': 'string', 'minLength': 2}, 'person': {'type': 'string', 'minLength': 2}}}, 'version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}, 'last_reviewed': {'$ref': '#/definitions/date'}, 'reporting_cadence_days': {'type': 'integer', 'minimum': 1, 'maximum': 31}}}, 'signals': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['signal_id', 'unit', 'input_source', 'comparator', 'amber_threshold', 'red_threshold', 'evidence'], 'additionalProperties': False, 'properties': {'signal_id': {'$ref': '#/definitions/signal_id'}, 'unit': {'enum': ['percent', 'count', 'ratio', 'boolean']}, 'input_source': {'type': 'object', 'required': ['system', 'query'], 'properties': {'system': {'type': 'string', 'minLength': 2}, 'query': {'type': 'string', 'minLength': 3, 'not': {'pattern': '(?i)(estimate|gut|feel|consensus|opinion|ask the|check-in)'}}}}, 'comparator': {'enum': ['gt', 'lt', 'gte', 'lte', 'eq']}, 'amber_threshold': {'type': 'number'}, 'red_threshold': {'type': 'number'}, 'evidence': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'$ref': '#/definitions/anchor'}}}, 'allOf': [{'if': {'properties': {'signal_id': {'pattern': '^(schedule|budget)'}}}, 'then': {'properties': {'signal_id': {'pattern': '_variance_pct$'}, 'unit': {'const': 'percent'}}}}, {'if': {'properties': {'comparator': {'const': 'eq'}}}, 'then': {'properties': {'unit': {'const': 'boolean'}}}}]}}, 'actions': {'type': 'object', 'required': ['green', 'amber', 'red'], 'additionalProperties': False, 'properties': {'green': {'type': 'string', 'minLength': 5}, 'amber': {'type': 'object', 'required': ['step', 'deadline_hours'], 'properties': {'step': {'type': 'string', 'minLength': 10, 'not': {'pattern': '(?i)^(discuss|monitor|keep an eye|watch)'}}, 'deadline_hours': {'type': 'integer', 'minimum': 1}}}, 'red': {'type': 'object', 'required': ['playbook', 'first_step', 'within_hours', 'fires_at'], 'properties': {'playbook': {'type': 'string', 'minLength': 3}, 'first_step': {'type': 'string', 'minLength': 10, 'not': {'pattern': '(?i)^(discuss|monitor|keep an eye|watch)'}}, 'within_hours': {'type': 'integer', 'minimum': 1, 'maximum': 72}, 'fires_at': {'const': 'compute_time'}}}}}, 'review_log': {'type': 'array', 'items': {'type': 'object', 'required': ['logged_at', 'kind', 'person'], 'properties': {'logged_at': {'$ref': '#/definitions/date'}, 'kind': {'enum': ['review', 'override']}, 'person': {'type': 'string', 'minLength': 2}, 'version_after': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}, 'signals_removed': {'type': 'array', 'items': {'$ref': '#/definitions/signal_change'}}, 'signals_justified': {'type': 'array', 'items': {'$ref': '#/definitions/signal_change'}}, 'signals_added_or_tightened': {'type': 'array', 'items': {'allOf': [{'$ref': '#/definitions/signal_change'}, {'required': ['evidence'], 'properties': {'evidence': {'minItems': 1}}}]}}, 'cycle_date': {'$ref': '#/definitions/date'}, 'computed_colour': {'$ref': '#/definitions/colour'}, 'reported_colour': {'$ref': '#/definitions/colour'}, 'reason': {'type': 'string', 'minLength': 10}}, 'allOf': [{'if': {'properties': {'kind': {'const': 'review'}}}, 'then': {'required': ['version_after', 'signals_removed', 'signals_justified', 'signals_added_or_tightened']}}, {'if': {'properties': {'kind': {'const': 'override'}}}, 'then': {'required': ['cycle_date', 'computed_colour', 'reported_colour', 'reason']}}, {'if': {'properties': {'kind': {'const': 'override'}, 'computed_colour': {'const': 'red'}}, 'required': ['computed_colour']}, 'then': {'properties': {'reported_colour': {'const': 'red'}}}}]}}, 'colour_history': {'type': 'array', 'items': {'type': 'object', 'required': ['computed_at', 'policy_version', 'policy_last_reviewed', 'values', 'computed_colour', 'reported_colour'], 'additionalProperties': False, 'properties': {'computed_at': {'$ref': '#/definitions/date'}, 'policy_version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}, 'policy_last_reviewed': {'$ref': '#/definitions/date'}, 'values': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['signal_id', 'value'], 'properties': {'signal_id': {'$ref': '#/definitions/signal_id'}, 'value': {'type': 'number'}}}}, 'computed_colour': {'$ref': '#/definitions/colour'}, 'reported_colour': {'$ref': '#/definitions/colour'}, 'red_escalated_at': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}'}}, 'if': {'properties': {'computed_colour': {'const': 'red'}}}, 'then': {'required': ['red_escalated_at'], 'properties': {'reported_colour': {'const': 'red'}}}}}}}

OK = {'project_id': 'checkout', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'version': '1.4.0', 'last_reviewed': '2026-05-10', 'reporting_cadence_days': 7}, 'signals': [{'signal_id': 'schedule_variance_pct', 'unit': 'percent', 'input_source': {'system': 'Jira', 'query': "dashboard 'Checkout EV' panel 'SV%' = (EV - PV) / PV * 100"}, 'comparator': 'gt', 'amber_threshold': 10, 'red_threshold': 20, 'evidence': ['incident-2025-Q4-acme-overrun', 'policy://pmo/schedule-tolerance']}, {'signal_id': 'budget_variance_pct', 'unit': 'percent', 'input_source': {'system': 'NetSuite', 'query': "saved export 'checkout-cost-vs-plan' column CV%"}, 'comparator': 'gt', 'amber_threshold': 5, 'red_threshold': 15, 'evidence': ['policy://pmo/budget-tolerance']}, {'signal_id': 'defect_escape_rate', 'unit': 'ratio', 'input_source': {'system': 'Sentry', 'query': "saved search 'checkout prod new issues / releases' weekly"}, 'comparator': 'gt', 'amber_threshold': 0.05, 'red_threshold': 0.1, 'evidence': ['postmortem-2026-Q1-checkout-hotfix']}, {'signal_id': 'blockers_open_count', 'unit': 'count', 'input_source': {'system': 'Jira', 'query': 'project = CHK AND flagged = Impediment AND status != Done'}, 'comparator': 'gte', 'amber_threshold': 2, 'red_threshold': 4, 'evidence': ['baseline-chk-2026-q1-blockers']}], 'actions': {'green': 'continue the weekly cadence; record value, version and last_reviewed', 'amber': {'step': 'PM runs a mid-week health check with the tech lead and posts findings in the status thread', 'deadline_hours': 72}, 'red': {'playbook': 'distressed-project-rescue', 'first_step': 'sponsor notified and rescue playbook opened', 'within_hours': 4, 'fires_at': 'compute_time'}}, 'review_log': [{'logged_at': '2026-05-10', 'kind': 'review', 'person': 'olena.k', 'version_after': '1.4.0', 'signals_removed': [{'signal_id': 'pr_review_latency_hours', 'reason': 'no Amber or Red in Q4 2025 and Q1 2026'}], 'signals_justified': [{'signal_id': 'budget_variance_pct', 'reason': "no Amber in two periods but it is the sponsor's contractual tolerance"}], 'signals_added_or_tightened': [{'signal_id': 'defect_escape_rate', 'reason': 'Q1 hotfix incident was not flagged ahead; amber tightened from 0.08 to 0.05', 'evidence': ['postmortem-2026-Q1-checkout-hotfix']}]}, {'logged_at': '2026-05-18', 'kind': 'override', 'person': 'olena.k', 'cycle_date': '2026-05-18', 'computed_colour': 'amber', 'reported_colour': 'green', 'reason': 'Jira EV panel double-counted the sprint 14 carry-over; corrected SV% is 6'}], 'colour_history': [{'computed_at': '2026-05-18', 'policy_version': '1.4.0', 'policy_last_reviewed': '2026-05-10', 'values': [{'signal_id': 'schedule_variance_pct', 'value': 12}, {'signal_id': 'budget_variance_pct', 'value': 3}, {'signal_id': 'defect_escape_rate', 'value': 0.02}, {'signal_id': 'blockers_open_count', 'value': 1}], 'computed_colour': 'amber', 'reported_colour': 'green'}, {'computed_at': '2026-05-25', 'policy_version': '1.4.0', 'policy_last_reviewed': '2026-05-10', 'values': [{'signal_id': 'schedule_variance_pct', 'value': 22}, {'signal_id': 'budget_variance_pct', 'value': 4}, {'signal_id': 'defect_escape_rate', 'value': 0.03}, {'signal_id': 'blockers_open_count', 'value': 1}], 'computed_colour': 'red', 'reported_colour': 'red', 'red_escalated_at': '2026-05-25T10:40'}]}

BAD = {'project_id': 'checkout', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'version': '1.4.0', 'last_reviewed': '2026-05-10', 'reporting_cadence_days': 7}, 'signals': [{'signal_id': 'schedule_variance_pct', 'unit': 'percent', 'input_source': {'system': 'PM', 'query': 'PM estimate at the weekly sync'}, 'comparator': 'gt', 'amber_threshold': 'significant', 'red_threshold': 20, 'evidence': ['TBD']}, {'signal_id': 'test_coverage_pct', 'unit': 'percent', 'input_source': {'system': 'SonarQube', 'query': 'project CHK measure coverage'}, 'comparator': 'lt', 'amber_threshold': 60, 'red_threshold': 70, 'evidence': ['policy://eng/coverage-floor']}], 'actions': {'green': 'continue normal cadence', 'amber': {'step': 'discuss at the next sync', 'deadline_hours': 72}, 'red': {'playbook': 'distressed-project-rescue', 'first_step': 'sponsor notified and rescue playbook opened', 'within_hours': 4, 'fires_at': 'next_sync'}}, 'review_log': [{'logged_at': '2026-05-25', 'kind': 'override', 'person': 'olena.k', 'cycle_date': '2026-05-25', 'computed_colour': 'red', 'reported_colour': 'amber', 'reason': 'steering committee is on Thursday; the team is confident the slip recovers'}], 'colour_history': [{'computed_at': '2026-05-25', 'policy_version': '1.4.0', 'policy_last_reviewed': '2026-05-10', 'values': [{'signal_id': 'schedule_variance_pct', 'value': 22}, {'signal_id': 'test_coverage_pct', 'value': 80}], 'computed_colour': 'amber', 'reported_colour': 'amber'}]}


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


_CMP = {"gt": lambda v, t: v > t, "gte": lambda v, t: v >= t, "lt": lambda v, t: v < t,
        "lte": lambda v, t: v <= t, "eq": lambda v, t: v == t}
_RANK = {"green": 0, "amber": 1, "red": 2}


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _colour(sig, value):
    cmp = _CMP.get(sig.get("comparator"))
    if cmp is None or not isinstance(value, (int, float)):
        return None
    if cmp(value, sig["red_threshold"]):
        return "red"
    if cmp(value, sig["amber_threshold"]):
        return "amber"
    return "green"


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    header = obj.get("header") or {}
    signals = {s.get("signal_id"): s for s in obj.get("signals") or []}
    for sid, s in signals.items():
        a, r, c = s.get("amber_threshold"), s.get("red_threshold"), s.get("comparator")
        if c in ("gt", "gte") and not r > a:
            errs.append(f"signals[{sid}]: red_threshold {r} must be greater than amber_threshold {a} for {c} (r-red-strictly-beyond-amber)")
        elif c in ("lt", "lte") and not r < a:
            errs.append(f"signals[{sid}]: red_threshold {r} must be less than amber_threshold {a} for {c} (r-red-strictly-beyond-amber)")
        elif c == "eq" and r == a:
            errs.append(f"signals[{sid}]: eq thresholds must differ (r-red-strictly-beyond-amber)")
    cadence_hours = (header.get("reporting_cadence_days") or 0) * 24
    amber = (obj.get("actions") or {}).get("amber") or {}
    if cadence_hours and amber.get("deadline_hours", 0) > cadence_hours:
        errs.append(f"actions.amber.deadline_hours {amber.get('deadline_hours')} exceeds the {cadence_hours}h reporting cycle (r-red-action-named-and-time-bound)")
    overrides = {(e.get("cycle_date"), e.get("computed_colour"), e.get("reported_colour"))
                 for e in obj.get("review_log") or [] if e.get("kind") == "override"}
    for i, cyc in enumerate(obj.get("colour_history") or []):
        values = {v.get("signal_id"): v.get("value") for v in cyc.get("values") or []}
        missing = sorted(set(signals) - set(values))
        if missing:
            errs.append(f"colour_history[{i}]: no value for signals {missing}; every signal is computed each cycle (r-worst-signal-wins)")
        worst = "green"
        for sid, val in values.items():
            col = _colour(signals[sid], val) if sid in signals else None
            if col and _RANK[col] > _RANK[worst]:
                worst = col
        if _RANK.get(cyc.get("computed_colour"), -1) != _RANK[worst]:
            errs.append(f"colour_history[{i}]: computed_colour {cyc.get('computed_colour')!r} but the worst signal is {worst!r}; no averaging (r-worst-signal-wins)")
        if cyc.get("reported_colour") != cyc.get("computed_colour") and \
                (cyc.get("computed_at"), cyc.get("computed_colour"), cyc.get("reported_colour")) not in overrides:
            errs.append(f"colour_history[{i}]: reported {cyc.get('reported_colour')!r} differs from computed {cyc.get('computed_colour')!r} with no matching override entry in review_log (r-override-logged-never-downgrades-red)")
        ca, lr = _date(cyc.get("computed_at")), _date(cyc.get("policy_last_reviewed"))
        if ca and lr and (ca - lr).days > 90:
            errs.append(f"colour_history[{i}]: computed {(ca - lr).days} days after policy_last_reviewed; a policy older than 90 days is reviewed before it computes a colour (r-review-within-90-days-prunes-and-adds)")
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
        prog="validate-rag-policy-thresholds.py",
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
