#!/usr/bin/env python3
"""validate-retro-facilitation-multistyle.py

Validate the RetroInstance produced by the retro-facilitation-multistyle methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/retro-facilitation-multistyle.json', 'title': 'RetroInstance', 'type': 'object', 'required': ['retro_date', 'next_retro_date', 'iteration_length_days', 'format', 'previous_formats', 'selection_rationale', 'team_state', 'participation', 'opening', 'previous_actions_review', 'action_items', 'timebox', 'outcome_review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'format': {'enum': ['mad-sad-glad', '4ls', 'sailboat', 'lean-coffee', 'anonymous-async']}, 'person': {'type': 'string', 'minLength': 2, 'pattern': '^[^#@]+$', 'not': {'pattern': '(?i)^(team|everyone|the team|all|tbd|channel)$'}}, 'counts': {'type': 'object', 'required': ['cards', 'attendance'], 'properties': {'cards': {'type': 'integer', 'minimum': 0}, 'attendance': {'type': 'integer', 'minimum': 0}}}}, 'properties': {'__faion_header__': {'type': 'object'}, 'retro_date': {'$ref': '#/definitions/date'}, 'next_retro_date': {'$ref': '#/definitions/date'}, 'iteration_length_days': {'type': 'integer', 'minimum': 5, 'maximum': 31}, 'format': {'$ref': '#/definitions/format'}, 'previous_formats': {'type': 'array', 'maxItems': 2, 'items': {'$ref': '#/definitions/format'}}, 'selection_rationale': {'type': 'string', 'minLength': 20, 'not': {'pattern': '(?i)(we always do this|team likes it)'}}, 'team_state': {'type': 'object', 'required': ['distribution', 'fatigue_signal', 'timezones', 'all_participants_on_live_call'], 'properties': {'distribution': {'enum': ['async', 'hybrid', 'in-person']}, 'fatigue_signal': {'enum': ['fresh', 'rotating', 'fatigued']}, 'timezones': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string', 'pattern': '^[A-Za-z_]+/[A-Za-z_/+-]+$|^UTC$'}}, 'all_participants_on_live_call': {'type': 'boolean'}}}, 'participation': {'$ref': '#/definitions/counts'}, 'previous_participation': {'$ref': '#/definitions/counts'}, 'opening': {'type': 'object', 'required': ['prime_directive_read', 'safety_check', 'switched_to_anonymous_input', 'non_member_manager_in_discussion'], 'properties': {'prime_directive_read': {'const': True}, 'safety_check': {'type': 'object', 'required': ['anonymous', 'scale', 'median'], 'properties': {'anonymous': {'const': True}, 'scale': {'const': '1-5'}, 'median': {'type': 'number', 'minimum': 1, 'maximum': 5}}}, 'switched_to_anonymous_input': {'type': 'boolean'}, 'non_member_manager_in_discussion': {'const': False}}, 'if': {'properties': {'safety_check': {'properties': {'median': {'exclusiveMaximum': 3}}}}}, 'then': {'properties': {'switched_to_anonymous_input': {'const': True}}}}, 'previous_actions_review': {'type': 'array', 'items': {'type': 'object', 'required': ['text', 'owner', 'status', 'previously_carried_over'], 'properties': {'text': {'type': 'string', 'minLength': 5}, 'owner': {'$ref': '#/definitions/person'}, 'status': {'enum': ['done', 'not_done_carried_over', 'dropped']}, 'previously_carried_over': {'type': 'boolean'}, 'reason': {'type': 'string', 'minLength': 5}}, 'allOf': [{'if': {'properties': {'status': {'enum': ['not_done_carried_over', 'dropped']}}}, 'then': {'required': ['reason']}}, {'if': {'properties': {'previously_carried_over': {'const': True}}}, 'then': {'properties': {'status': {'enum': ['done', 'dropped']}}}}]}}, 'action_items': {'type': 'array', 'minItems': 1, 'maxItems': 3, 'items': {'type': 'object', 'required': ['text', 'owner', 'evidence_link', 'due_date'], 'properties': {'text': {'type': 'string', 'minLength': 5}, 'owner': {'$ref': '#/definitions/person'}, 'evidence_link': {'type': 'string', 'pattern': '^https?://\\S+/(issues|pull|pulls|browse|merge_requests|issue)/\\S+$'}, 'due_date': {'$ref': '#/definitions/date'}}}}, 'discussion_notes': {'type': 'array', 'items': {'type': 'string', 'minLength': 5}}, 'anonymous_async': {'type': 'object', 'required': ['tool_stores_author_identity', 'window_start', 'window_end', 'working_days_in_window_per_timezone', 'clustered_before_recap', 'attribution_requests', 'recap'], 'properties': {'tool_stores_author_identity': {'const': False}, 'window_start': {'$ref': '#/definitions/date'}, 'window_end': {'$ref': '#/definitions/date'}, 'working_days_in_window_per_timezone': {'type': 'object', 'additionalProperties': {'type': 'integer', 'minimum': 1}}, 'clustered_before_recap': {'const': True}, 'attribution_requests': {'const': 0}, 'recap': {'type': 'object', 'required': ['mode'], 'properties': {'mode': {'enum': ['live_all_timezones', 'recorded_open_for_comment']}, 'comment_window_working_days': {'type': 'integer', 'minimum': 1}}, 'if': {'properties': {'mode': {'const': 'recorded_open_for_comment'}}}, 'then': {'required': ['comment_window_working_days']}}}}, 'lean_coffee': {'type': 'object', 'required': ['topics_dot_voted_before_discussion', 'topics'], 'properties': {'topics_dot_voted_before_discussion': {'const': True}, 'topics': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['title', 'votes', 'timebox_minutes', 'extensions'], 'properties': {'title': {'type': 'string', 'minLength': 3}, 'votes': {'type': 'integer', 'minimum': 0}, 'timebox_minutes': {'type': 'integer', 'minimum': 1}, 'extensions': {'type': 'integer', 'minimum': 0, 'maximum': 2}}}}}}, 'timebox': {'type': 'object', 'required': ['published_before_start', 'minutes', 'actual_minutes', 'overran'], 'properties': {'published_before_start': {'const': True}, 'minutes': {'type': 'integer', 'minimum': 15, 'maximum': 180}, 'actual_minutes': {'type': 'integer', 'minimum': 0}, 'overran': {'type': 'boolean'}}}, 'outcome_review': {'type': 'object', 'required': ['cadence', 'last_run_at'], 'properties': {'cadence': {'enum': ['next-retro', 'monthly', 'quarterly']}, 'last_run_at': {'$ref': '#/definitions/date'}}}}, 'allOf': [{'if': {'properties': {'team_state': {'properties': {'distribution': {'const': 'async'}}}}}, 'then': {'properties': {'format': {'const': 'anonymous-async'}}}}, {'if': {'properties': {'format': {'const': 'lean-coffee'}}}, 'then': {'required': ['lean_coffee'], 'properties': {'team_state': {'properties': {'distribution': {'enum': ['in-person', 'hybrid']}, 'all_participants_on_live_call': {'const': True}}}}}}, {'if': {'properties': {'format': {'const': 'anonymous-async'}}}, 'then': {'required': ['anonymous_async']}}]}

OK = {'retro_date': '2026-05-23', 'next_retro_date': '2026-06-06', 'iteration_length_days': 14, 'format': 'anonymous-async', 'previous_formats': ['sailboat', '4ls'], 'selection_rationale': 'Distribution is async across Europe/Kyiv, Europe/Lisbon and Europe/London, so anonymous-async is the only format that gets the Lisbon outsource cards in; fatigue signal is rotating and the last two retros were sailboat and 4ls, so this also rotates.', 'team_state': {'distribution': 'async', 'fatigue_signal': 'rotating', 'timezones': ['Europe/Kyiv', 'Europe/Lisbon', 'Europe/London'], 'all_participants_on_live_call': False}, 'participation': {'cards': 23, 'attendance': 9}, 'previous_participation': {'cards': 17, 'attendance': 8}, 'opening': {'prime_directive_read': True, 'safety_check': {'anonymous': True, 'scale': '1-5', 'median': 4}, 'switched_to_anonymous_input': False, 'non_member_manager_in_discussion': False}, 'previous_actions_review': [{'text': 'Add a staging smoke test before the Friday deploy', 'owner': 'Dmytro', 'status': 'done', 'previously_carried_over': False}, {'text': 'Write the on-call handover template', 'owner': 'Ana', 'status': 'not_done_carried_over', 'previously_carried_over': False, 'reason': 'Ana was on the incident rotation both weeks; carried over once with a new due date'}], 'action_items': [{'text': 'Move the backend deploy window to 16:00 UTC so Lisbon is not deploying after hours', 'owner': 'Carol', 'evidence_link': 'https://github.com/acme/platform/issues/482', 'due_date': '2026-05-30'}, {'text': 'Write the on-call handover template (carried over)', 'owner': 'Ana', 'evidence_link': 'https://github.com/acme/platform/issues/471', 'due_date': '2026-06-05'}], 'discussion_notes': ['Sprint review slot moves earlier for Kyiv; no owner yet, revisit next retro'], 'anonymous_async': {'tool_stores_author_identity': False, 'window_start': '2026-05-20', 'window_end': '2026-05-22', 'working_days_in_window_per_timezone': {'Europe/Kyiv': 2, 'Europe/Lisbon': 2, 'Europe/London': 2}, 'clustered_before_recap': True, 'attribution_requests': 0, 'recap': {'mode': 'recorded_open_for_comment', 'comment_window_working_days': 1}}, 'timebox': {'published_before_start': True, 'minutes': 60, 'actual_minutes': 55, 'overran': False}, 'outcome_review': {'cadence': 'next-retro', 'last_run_at': '2026-05-23'}}

BAD = {'retro_date': '2026-05-23', 'next_retro_date': '2026-06-06', 'iteration_length_days': 14, 'format': 'mad-sad-glad', 'previous_formats': ['mad-sad-glad', 'mad-sad-glad'], 'selection_rationale': 'We always do this one and the team likes it.', 'team_state': {'distribution': 'async', 'fatigue_signal': 'fatigued', 'timezones': ['Europe/Kyiv', 'Europe/Lisbon', 'Europe/London'], 'all_participants_on_live_call': False}, 'participation': {'cards': 6, 'attendance': 4}, 'opening': {'prime_directive_read': False, 'safety_check': {'anonymous': False, 'scale': '1-5', 'median': 2}, 'switched_to_anonymous_input': False, 'non_member_manager_in_discussion': True}, 'previous_actions_review': [], 'action_items': [{'text': 'Fix deploys', 'owner': 'team', 'evidence_link': 'https://acme.slack.com/archives/C01/p1', 'due_date': '2026-07-15'}, {'text': 'Improve communication', 'owner': 'everyone', 'evidence_link': 'https://github.com/acme/platform/issues/490', 'due_date': '2026-06-30'}, {'text': 'Write more tests', 'owner': 'Dmytro', 'evidence_link': 'https://github.com/acme/platform/issues/491', 'due_date': '2026-06-05'}, {'text': 'Update the runbook', 'owner': 'Ana', 'evidence_link': 'https://github.com/acme/platform/issues/492', 'due_date': '2026-06-05'}], 'timebox': {'published_before_start': False, 'minutes': 150, 'actual_minutes': 150, 'overran': False}, 'outcome_review': {'cadence': 'next-retro', 'last_run_at': '2026-02-14'}}


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
    ts = obj.get("team_state") or {}
    fmt, prev = obj.get("format"), obj.get("previous_formats") or []
    rationale = (obj.get("selection_rationale") or "").lower()
    for needed in [ts.get("distribution"), ts.get("fatigue_signal"), *prev]:
        if needed and needed.lower() not in rationale:
            errs.append(f"selection_rationale does not mention {needed!r}; it must name the distribution, the fatigue signal and the previous two formats (r-rationale-names-distribution-fatigue-and-history)")
    fatigue = ts.get("fatigue_signal")
    if fatigue == "fatigued" and fmt in prev:
        errs.append(f"format {fmt!r} was used in one of the last two retros {prev} and the team is fatigued (r-fatigued-team-rotates-format)")
    elif fatigue == "rotating" and prev and fmt == prev[0]:
        errs.append(f"format {fmt!r} repeats the previous retro's format while rotating (r-fatigued-team-rotates-format)")
    if len(prev) == 2 and prev[0] == prev[1] == fmt:
        p, q = obj.get("participation") or {}, obj.get("previous_participation")
        if fatigue != "fresh" or not q or (p.get("cards", 0) < q.get("cards", 0) and p.get("attendance", 0) < q.get("attendance", 0)):
            errs.append(f"format {fmt!r} for the third time in a row needs fatigue_signal fresh and participation at or above the previous retro (r-fatigued-team-rotates-format)")
    rd, nrd = _date(obj.get("retro_date")), _date(obj.get("next_retro_date"))
    lra = _date((obj.get("outcome_review") or {}).get("last_run_at"))
    if rd and lra != rd:
        errs.append(f"outcome_review.last_run_at {lra} must equal retro_date {rd}; the status walk of the previous actions sets it (r-previous-actions-reviewed-before-new-ones)")
    for i, a in enumerate(obj.get("action_items") or []):
        dd = _date(a.get("due_date"))
        if dd and nrd and dd > nrd:
            errs.append(f"action_items[{i}].due_date {dd} is after next_retro_date {nrd} (r-action-items-one-to-three-owned-dated-linked)")
    aa = obj.get("anonymous_async")
    if fmt == "anonymous-async" and isinstance(aa, dict):
        ws, we = _date(aa.get("window_start")), _date(aa.get("window_end"))
        if ws and we and we <= ws:
            errs.append("anonymous_async.window_end must be after window_start (r-anonymous-async-window-and-clustering)")
        days = aa.get("working_days_in_window_per_timezone") or {}
        for tz in ts.get("timezones") or []:
            if days.get(tz, 0) < 1:
                errs.append(f"anonymous_async: timezone {tz} has no full working day in the collection window (r-anonymous-async-window-and-clustering)")
    tb = obj.get("timebox") or {}
    days = obj.get("iteration_length_days") or 0
    cap = min(180, max(90, 6 * days)) if days else 0
    if cap and tb.get("minutes", 0) > cap:
        errs.append(f"timebox.minutes {tb.get('minutes')} exceeds {cap} for a {days}-day iteration (3 hours per month, proportional, 90 for a two-week sprint) (r-timebox-published-and-held)")
    if "actual_minutes" in tb and tb.get("overran") != (tb.get("actual_minutes", 0) > tb.get("minutes", 0)):
        errs.append(f"timebox.overran {tb.get('overran')} disagrees with actual_minutes {tb.get('actual_minutes')} vs minutes {tb.get('minutes')} (r-timebox-published-and-held)")
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
        prog="validate-retro-facilitation-multistyle.py",
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
