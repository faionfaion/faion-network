#!/usr/bin/env python3
"""validate-retro-format-rotation-guide.py

Validate the RotationGuide produced by the retro-format-rotation-guide methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/retro-format-rotation-guide.json', 'title': 'RotationGuide', 'type': 'object', 'required': ['team_id', 'owner', 'guide_date', 'history', 'format_last_used', 'team_state', 'stale_formats', 'refresh_trend', 'outcome_review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'format': {'enum': ['start-stop-continue', 'sailboat', '4ls', 'timeline', 'anonymous-async', 'mad-sad-glad', 'lean-coffee']}, 'count': {'type': 'integer', 'minimum': 0}}, 'properties': {'__faion_header__': {'type': 'object'}, 'team_id': {'type': 'string', 'minLength': 2}, 'owner': {'type': 'string', 'minLength': 2, 'pattern': '^[^#@]+$', 'not': {'pattern': '(?i)^(team|everyone|the team|all|tbd|channel)$'}}, 'guide_date': {'$ref': '#/definitions/date'}, 'history': {'type': 'array', 'maxItems': 3, 'items': {'type': 'object', 'required': ['retro_date', 'instance_ref', 'format', 'action_items', 'participants', 'silent_participants'], 'properties': {'retro_date': {'$ref': '#/definitions/date'}, 'instance_ref': {'type': 'string', 'minLength': 5}, 'format': {'$ref': '#/definitions/format'}, 'action_items': {'$ref': '#/definitions/count'}, 'participants': {'$ref': '#/definitions/count'}, 'silent_participants': {'$ref': '#/definitions/count'}}}}, 'format_last_used': {'type': 'object', 'required': ['start-stop-continue', 'sailboat', '4ls', 'timeline', 'anonymous-async', 'mad-sad-glad', 'lean-coffee'], 'additionalProperties': {'anyOf': [{'$ref': '#/definitions/date'}, {'type': 'null'}]}}, 'team_state': {'type': 'object', 'required': ['distribution', 'fatigue_signal'], 'properties': {'distribution': {'enum': ['async', 'hybrid', 'in-person']}, 'fatigue_signal': {'enum': ['fresh', 'rotating', 'fatigued']}}}, 'stale_formats': {'type': 'array', 'items': {'type': 'object', 'required': ['format', 'signal'], 'properties': {'format': {'$ref': '#/definitions/format'}, 'signal': {'enum': ['twice_in_last_3', 'action_items_dropped_over_50pct', 'two_or_more_silent_participants']}}}}, 'refresh_trend': {'type': 'object', 'required': ['consecutive_rotations_without_refresh', 'escalation'], 'properties': {'consecutive_rotations_without_refresh': {'type': 'integer', 'minimum': 0, 'maximum': 2}, 'escalation': {'enum': ['none', 'fatigue_is_not_a_format_problem']}, 'team_health_route': {'enum': ['team-morale-pulse-survey', 'solo-burnout-tripwires']}}, 'if': {'properties': {'consecutive_rotations_without_refresh': {'const': 2}}}, 'then': {'properties': {'escalation': {'const': 'fatigue_is_not_a_format_problem'}}, 'required': ['team_health_route']}}, 'skip': {'const': 'history < 3'}, 'pick': {'type': 'object', 'required': ['next_format', 'tie_breaker', 'exception_recorded', 'next_format_last_used', 'anonymous_async_input'], 'properties': {'next_format': {'$ref': '#/definitions/format'}, 'tie_breaker': {'enum': ['no_repeat_only', 'async_pool', 'async_pool_exhausted', 'fatigued_12_month_lookback', 'in_person_sailboat_or_lean_coffee', 'reflective_mid_cycle_4ls']}, 'exception_recorded': {'type': 'boolean'}, 'next_format_last_used': {'anyOf': [{'$ref': '#/definitions/date'}, {'type': 'null'}]}, 'anonymous_async_input': {'type': 'boolean'}}, 'if': {'properties': {'exception_recorded': {'const': True}}}, 'then': {'properties': {'tie_breaker': {'const': 'async_pool_exhausted'}}}}, 'rationale': {'type': 'string', 'minLength': 20, 'not': {'pattern': '(?i)(everyone likes it|seemed right|we always)'}}, 'outcome_review': {'type': 'object', 'required': ['cadence', 'last_run_at'], 'properties': {'cadence': {'enum': ['next-retro', 'monthly', 'quarterly']}, 'last_run_at': {'$ref': '#/definitions/date'}}}}, 'allOf': [{'if': {'properties': {'history': {'maxItems': 2}}}, 'then': {'required': ['skip'], 'not': {'required': ['pick']}}}, {'if': {'properties': {'history': {'minItems': 3}, 'refresh_trend': {'properties': {'escalation': {'const': 'none'}}}}, 'required': ['refresh_trend']}, 'then': {'required': ['pick', 'rationale']}}, {'if': {'properties': {'refresh_trend': {'properties': {'escalation': {'const': 'fatigue_is_not_a_format_problem'}}}}, 'required': ['refresh_trend']}, 'then': {'not': {'required': ['pick']}}}, {'if': {'properties': {'team_state': {'properties': {'distribution': {'const': 'async'}}}}, 'required': ['pick']}, 'then': {'properties': {'pick': {'properties': {'next_format': {'not': {'enum': ['mad-sad-glad', 'lean-coffee']}}, 'anonymous_async_input': {'const': True}}}}}}, {'if': {'properties': {'team_state': {'properties': {'fatigue_signal': {'const': 'fatigued'}}}}, 'required': ['pick']}, 'then': {'properties': {'pick': {'properties': {'tie_breaker': {'const': 'fatigued_12_month_lookback'}}}}}}]}

OK = {'team_id': 'platform', 'owner': 'Ruslan', 'guide_date': '2026-05-16', 'history': [{'retro_date': '2026-05-09', 'instance_ref': 'retros/platform/2026-05-09.json', 'format': 'sailboat', 'action_items': 4, 'participants': 8, 'silent_participants': 0}, {'retro_date': '2026-04-25', 'instance_ref': 'retros/platform/2026-04-25.json', 'format': '4ls', 'action_items': 6, 'participants': 8, 'silent_participants': 0}, {'retro_date': '2026-04-11', 'instance_ref': 'retros/platform/2026-04-11.json', 'format': 'mad-sad-glad', 'action_items': 5, 'participants': 7, 'silent_participants': 1}], 'format_last_used': {'start-stop-continue': '2025-11-14', 'sailboat': '2026-05-09', '4ls': '2026-04-25', 'timeline': None, 'anonymous-async': None, 'mad-sad-glad': '2026-04-11', 'lean-coffee': '2026-03-28'}, 'team_state': {'distribution': 'async', 'fatigue_signal': 'rotating'}, 'stale_formats': [], 'refresh_trend': {'consecutive_rotations_without_refresh': 1, 'escalation': 'none'}, 'pick': {'next_format': 'anonymous-async', 'tie_breaker': 'async_pool', 'exception_recorded': False, 'next_format_last_used': None, 'anonymous_async_input': True}, 'rationale': "Last three were sailboat, 4ls and mad-sad-glad, all live formats; distribution is now async since Carol moved to Lisbon, fatigue signal rotating. The async pool tie-breaker decides: anonymous-async is outside the last three, never used by this team, and the only pick that gets Lisbon's cards in.", 'outcome_review': {'cadence': 'next-retro', 'last_run_at': '2026-05-09'}}

BAD = {'team_id': 'platform', 'owner': 'team', 'guide_date': '2026-05-16', 'history': [{'retro_date': '2026-05-09', 'instance_ref': 'from memory', 'format': 'sailboat', 'action_items': 1, 'participants': 8, 'silent_participants': 3}, {'retro_date': '2026-04-25', 'instance_ref': 'from memory', 'format': 'sailboat', 'action_items': 3, 'participants': 8, 'silent_participants': 2}, {'retro_date': '2026-04-11', 'instance_ref': 'retros/platform/2026-04-11.json', 'format': 'sailboat', 'action_items': 6, 'participants': 8, 'silent_participants': 0}], 'format_last_used': {'start-stop-continue': '2026-01-16', 'sailboat': '2026-05-09', '4ls': '2025-12-05', 'timeline': None, 'anonymous-async': None, 'mad-sad-glad': '2026-02-13', 'lean-coffee': '2026-03-13'}, 'team_state': {'distribution': 'async', 'fatigue_signal': 'fatigued'}, 'stale_formats': [], 'refresh_trend': {'consecutive_rotations_without_refresh': 0, 'escalation': 'none'}, 'pick': {'next_format': 'lean-coffee', 'tie_breaker': 'in_person_sailboat_or_lean_coffee', 'exception_recorded': False, 'next_format_last_used': '2026-03-13', 'anonymous_async_input': False}, 'rationale': 'Everyone likes it and lean-coffee is a change.', 'outcome_review': {'cadence': 'next-retro', 'last_run_at': '2026-05-09'}}


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


_ASYNC_POOL = {"anonymous-async", "sailboat", "4ls", "start-stop-continue", "timeline"}


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _stale(history):
    found = {}
    formats = [h.get("format") for h in history]
    for f in set(formats):
        if formats.count(f) >= 2:
            found.setdefault(f, "twice_in_last_3")
    for newer, older in zip(history, history[1:]):
        if newer.get("format") == older.get("format") and older.get("action_items", 0) and \
                newer.get("action_items", 0) < 0.5 * older.get("action_items", 0):
            found.setdefault(newer["format"], "action_items_dropped_over_50pct")
    if history and history[0].get("silent_participants", 0) >= 2:
        found.setdefault(history[0].get("format"), "two_or_more_silent_participants")
    return found


def _refreshed(newer, older):
    contrib = lambda h: h.get("participants", 0) - h.get("silent_participants", 0)
    return newer.get("action_items", 0) > older.get("action_items", 0) or contrib(newer) > contrib(older)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    history = obj.get("history") or []
    dates = [_date(h.get("retro_date")) for h in history]
    if all(dates) and dates != sorted(dates, reverse=True):
        errs.append("history must be newest first by retro_date (r-history-read-from-committed-instances)")
    last_used = obj.get("format_last_used") or {}
    for h in history:
        f = h.get("format")
        lu = _date(last_used.get(f))
        rd = _date(h.get("retro_date"))
        if rd and (lu is None or lu < rd):
            errs.append(f"format_last_used[{f}] = {last_used.get(f)!r} is earlier than the {rd} instance that used it (r-history-read-from-committed-instances)")
    stale = _stale(history)
    declared = {s.get("format"): s.get("signal") for s in obj.get("stale_formats") or []}
    for f, sig in stale.items():
        if f not in declared:
            errs.append(f"stale_formats: {f!r} is stale by signal {sig} and is not listed (r-stale-format-detector-three-signals)")
    for f in declared:
        if f not in stale:
            errs.append(f"stale_formats: {f!r} is listed but no signal fires for it (r-stale-format-detector-three-signals)")
    hist_formats = [h.get("format") for h in history]
    without = 0
    for newer, older in zip(history, history[1:]):
        if newer.get("format") != older.get("format") and newer.get("format") not in stale and not _refreshed(newer, older):
            without += 1
        else:
            break
    trend = obj.get("refresh_trend") or {}
    if trend.get("consecutive_rotations_without_refresh") != min(without, 2):
        errs.append(f"refresh_trend.consecutive_rotations_without_refresh {trend.get('consecutive_rotations_without_refresh')} != {min(without, 2)} computed from the history counts (r-two-rotations-without-refresh-escalate-to-team-health)")
    pick = obj.get("pick")
    if not isinstance(pick, dict):
        return errs
    nf = pick.get("next_format")
    ts = obj.get("team_state") or {}
    if nf in stale:
        errs.append(f"pick.next_format {nf!r} is stale for this team ({stale[nf]}) (r-stale-format-detector-three-signals)")
    if nf in hist_formats:
        pool_left = _ASYNC_POOL - set(hist_formats) - set(stale)
        if not (ts.get("distribution") == "async" and pick.get("tie_breaker") == "async_pool_exhausted" and not pool_left):
            errs.append(f"pick.next_format {nf!r} is in the last three {hist_formats} and the async pool is not exhausted (r-no-repeat-in-last-3)")
    rationale = (obj.get("rationale") or "").lower()
    for needed in [*hist_formats, ts.get("distribution"), ts.get("fatigue_signal")]:
        if needed and needed.lower() not in rationale:
            errs.append(f"rationale does not mention {needed!r}; it must name the three previous formats, the distribution and the fatigue signal (r-rationale-names-history-state-and-tiebreaker)")
    if pick.get("exception_recorded") and "exception" not in rationale:
        errs.append("rationale must record the async-pool exception it relies on (r-no-repeat-in-last-3)")
    lu = last_used.get(nf)
    if pick.get("next_format_last_used") != lu:
        errs.append(f"pick.next_format_last_used {pick.get('next_format_last_used')!r} != format_last_used[{nf}] {lu!r} (r-fatigued-team-picks-format-unused-12-months)")
    if ts.get("fatigue_signal") == "fatigued":
        gd, lud = _date(obj.get("guide_date")), _date(lu)
        if lud and gd and (gd - lud).days < 365:
            errs.append(f"pick.next_format {nf!r} was used {(gd - lud).days} days ago; a fatigued team needs a format unused for 12 months or never (r-fatigued-team-picks-format-unused-12-months)")
        if not (("never" in rationale) if lu is None else (str(lu) in rationale)):
            errs.append("rationale must state when the picked format was last used (or that it never was) (r-fatigued-team-picks-format-unused-12-months)")
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
        prog="validate-retro-format-rotation-guide.py",
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
