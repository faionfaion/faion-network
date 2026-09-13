#!/usr/bin/env python3
"""validate-single-channel-bet-selector.py

Validate the channel-bet record produced by the single-channel-bet-selector methodology against the
draft-07 JSON Schema embedded in content/02-output-contract.xml, plus the
cross-field rules from content/01-core-rules.xml the schema cannot express. Stdlib-only;
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/single-channel-bet-selector.json', 'title': 'Single Channel Bet Selector decision record', 'type': 'object', 'required': ['selected_on', 'rubric_location', 'working_channel_exists', 'icp_sample', 'candidates', 'outcome', 'bet', 'no_bet_route', 'parking_lot'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'score': {'type': 'integer', 'minimum': 1, 'maximum': 5}, 'tactic': {'type': 'string', 'minLength': 12, 'not': {'enum': ['social', 'outbound', 'content', 'paid', 'ads', 'seo', 'email', 'events', 'community', 'partnerships', 'pr']}}, 'taxonomy_channel': {'type': 'string', 'enum': ['targeting_blogs', 'publicity', 'unconventional_pr', 'search_engine_marketing', 'social_and_display_ads', 'offline_ads', 'seo', 'content_marketing', 'email_marketing', 'engineering_as_marketing', 'viral_marketing', 'business_development', 'sales', 'affiliate_programs', 'existing_platforms', 'trade_shows', 'offline_events', 'speaking_engagements', 'community_building']}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'selected_on': {'$ref': '#/definitions/date'}, 'rubric_location': {'type': 'string', 'minLength': 8}, 'working_channel_exists': {'const': False}, 'icp_sample': {'type': 'object', 'required': ['paying_customers', 'qualified_conversations'], 'additionalProperties': False, 'properties': {'paying_customers': {'type': 'integer', 'minimum': 0}, 'qualified_conversations': {'type': 'integer', 'minimum': 0}}, 'anyOf': [{'properties': {'paying_customers': {'minimum': 5}}}, {'properties': {'qualified_conversations': {'minimum': 50}}}]}, 'candidates': {'type': 'array', 'minItems': 3, 'maxItems': 6, 'items': {'type': 'object', 'required': ['channel', 'taxonomy_channel', 'founder_fit', 'icp_density', 'icp_density_sample', 'early_traction', 'unsolicited_inbound_count', 'total', 'clears_bar'], 'additionalProperties': False, 'properties': {'channel': {'$ref': '#/definitions/tactic'}, 'taxonomy_channel': {'$ref': '#/definitions/taxonomy_channel'}, 'founder_fit': {'$ref': '#/definitions/score'}, 'icp_density': {'$ref': '#/definitions/score'}, 'icp_density_sample': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['observed', 'of'], 'additionalProperties': False, 'properties': {'observed': {'type': 'integer', 'minimum': 0}, 'of': {'type': 'integer', 'minimum': 5}}}]}, 'early_traction': {'$ref': '#/definitions/score'}, 'unsolicited_inbound_count': {'type': 'integer', 'minimum': 0}, 'total': {'type': 'integer', 'minimum': 3, 'maximum': 15}, 'clears_bar': {'type': 'boolean'}}, 'if': {'properties': {'icp_density_sample': {'type': 'null'}}}, 'then': {'properties': {'icp_density': {'const': 1}}}}}, 'outcome': {'type': 'string', 'enum': ['bet', 'no_bet']}, 'bet': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['channel', 'start_date', 'end_date', 'weekly_unit', 'checkpoints', 'kill_criterion'], 'additionalProperties': False, 'properties': {'channel': {'$ref': '#/definitions/tactic'}, 'start_date': {'$ref': '#/definitions/date'}, 'end_date': {'$ref': '#/definitions/date'}, 'weekly_unit': {'type': 'object', 'required': ['count', 'unit'], 'additionalProperties': False, 'properties': {'count': {'type': 'integer', 'minimum': 1}, 'unit': {'type': 'string', 'minLength': 5}}}, 'checkpoints': {'type': 'array', 'minItems': 2, 'maxItems': 2, 'items': {'type': 'object', 'required': ['week', 'metric', 'expected'], 'additionalProperties': False, 'properties': {'week': {'type': 'integer', 'enum': [4, 8]}, 'metric': {'type': 'string', 'minLength': 3}, 'expected': {'type': 'number', 'minimum': 0}}}, 'allOf': [{'contains': {'properties': {'week': {'const': 4}}}}, {'contains': {'properties': {'week': {'const': 8}}}}]}, 'kill_criterion': {'type': 'object', 'required': ['week', 'written_on', 'conditions', 'action', 'revised'], 'additionalProperties': False, 'properties': {'week': {'const': 12}, 'written_on': {'$ref': '#/definitions/date'}, 'conditions': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['metric', 'operator', 'value'], 'additionalProperties': False, 'properties': {'metric': {'type': 'string', 'minLength': 3}, 'operator': {'type': 'string', 'enum': ['<', '<=']}, 'value': {'type': 'number', 'minimum': 0}}}}, 'action': {'const': 'rerun_rubric_with_result_as_early_traction'}, 'revised': {'const': False}}}}}]}, 'no_bet_route': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['route', 'highest_scorer'], 'additionalProperties': False, 'properties': {'route': {'type': 'string', 'enum': ['discovery', 'instrument_highest_scorer']}, 'highest_scorer': {'$ref': '#/definitions/tactic'}}}]}, 'parking_lot': {'type': 'object', 'required': ['channels', 'active_work_allowed'], 'additionalProperties': False, 'properties': {'channels': {'type': 'array', 'items': {'type': 'object', 'required': ['channel', 'total'], 'additionalProperties': False, 'properties': {'channel': {'$ref': '#/definitions/tactic'}, 'total': {'type': 'integer', 'minimum': 3, 'maximum': 15}}}}, 'active_work_allowed': {'const': False}}}}, 'allOf': [{'if': {'properties': {'outcome': {'const': 'bet'}}}, 'then': {'properties': {'bet': {'type': 'object'}, 'no_bet_route': {'type': 'null'}}}}, {'if': {'properties': {'outcome': {'const': 'no_bet'}}}, 'then': {'properties': {'bet': {'type': 'null'}, 'no_bet_route': {'type': 'object'}}}}]}

OK = {'selected_on': '2026-09-14', 'rubric_location': 'repo:founder-ops/decisions/2026-09-14-channel-bet.md', 'working_channel_exists': False, 'icp_sample': {'paying_customers': 11, 'qualified_conversations': 23}, 'candidates': [{'channel': 'LinkedIn founder posts on ops-team tooling', 'taxonomy_channel': 'content_marketing', 'founder_fit': 4, 'icp_density': 4, 'icp_density_sample': {'observed': 7, 'of': 11}, 'early_traction': 4, 'unsolicited_inbound_count': 3, 'total': 12, 'clears_bar': True}, {'channel': 'cold email to operations managers at 50-200 person logistics firms', 'taxonomy_channel': 'sales', 'founder_fit': 3, 'icp_density': 3, 'icp_density_sample': {'observed': 4, 'of': 11}, 'early_traction': 2, 'unsolicited_inbound_count': 0, 'total': 8, 'clears_bar': False}, {'channel': 'SEO comparison pages against the two incumbent tools', 'taxonomy_channel': 'seo', 'founder_fit': 2, 'icp_density': 3, 'icp_density_sample': {'observed': 3, 'of': 11}, 'early_traction': 1, 'unsolicited_inbound_count': 0, 'total': 6, 'clears_bar': False}, {'channel': 'answering questions in two ops-manager Slack communities', 'taxonomy_channel': 'community_building', 'founder_fit': 4, 'icp_density': 2, 'icp_density_sample': {'observed': 2, 'of': 11}, 'early_traction': 2, 'unsolicited_inbound_count': 1, 'total': 8, 'clears_bar': False}], 'outcome': 'bet', 'bet': {'channel': 'LinkedIn founder posts on ops-team tooling', 'start_date': '2026-09-14', 'end_date': '2026-12-13', 'weekly_unit': {'count': 3, 'unit': 'LinkedIn posts of 150 to 300 words on an ops-team tooling problem'}, 'checkpoints': [{'week': 4, 'metric': 'profile visits per week', 'expected': 400}, {'week': 8, 'metric': 'demo requests to date', 'expected': 4}], 'kill_criterion': {'week': 12, 'written_on': '2026-09-14', 'conditions': [{'metric': 'qualified demo requests', 'operator': '<', 'value': 10}, {'metric': 'new paying customers', 'operator': '<', 'value': 1}], 'action': 'rerun_rubric_with_result_as_early_traction', 'revised': False}}, 'no_bet_route': None, 'parking_lot': {'channels': [{'channel': 'cold email to operations managers at 50-200 person logistics firms', 'total': 8}, {'channel': 'SEO comparison pages against the two incumbent tools', 'total': 6}, {'channel': 'answering questions in two ops-manager Slack communities', 'total': 8}], 'active_work_allowed': False}}

BAD = {'selected_on': '2026-09-14', 'rubric_location': 'slack', 'working_channel_exists': False, 'icp_sample': {'paying_customers': 2, 'qualified_conversations': 9}, 'candidates': [{'channel': 'social', 'taxonomy_channel': 'content_marketing', 'founder_fit': 5, 'icp_density': 5, 'icp_density_sample': None, 'early_traction': 2, 'unsolicited_inbound_count': 0, 'total': 13, 'clears_bar': True}, {'channel': 'cold email to operations managers', 'taxonomy_channel': 'sales', 'founder_fit': 3, 'icp_density': 3, 'icp_density_sample': {'observed': 1, 'of': 2}, 'early_traction': 2, 'unsolicited_inbound_count': 0, 'total': 8, 'clears_bar': False}], 'outcome': 'bet', 'bet': {'channel': 'social', 'start_date': '2026-09-14', 'end_date': '2027-01-14', 'weekly_unit': {'count': 0, 'unit': 'post when inspired'}, 'checkpoints': [{'week': 12, 'metric': 'revenue', 'expected': 5000}], 'kill_criterion': {'week': 12, 'written_on': '2026-11-30', 'conditions': [{'metric': 'it feels like it is working', 'operator': '<', 'value': 1}], 'action': 'keep going one more month', 'revised': True}}, 'no_bet_route': None, 'parking_lot': {'channels': [], 'active_work_allowed': True}}


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


from datetime import date as _date


def _d(s):
    try:
        return _date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    cands = [c for c in obj.get("candidates") or [] if isinstance(c, dict)]
    by_name = {}
    for n, c in enumerate(cands):
        axes = [c.get("founder_fit"), c.get("icp_density"), c.get("early_traction")]
        if all(isinstance(a, int) for a in axes):
            if c.get("total") != sum(axes):
                errs.append(f"candidates[{n}].total {c.get('total')} is not founder_fit + icp_density + early_traction = {sum(axes)} (r-three-axis-scoring)")
            clears = sum(axes) >= 12 and min(axes) >= 3
            if c.get("clears_bar") is not clears:
                errs.append(f"candidates[{n}].clears_bar {c.get('clears_bar')} disagrees with the rubric (total {sum(axes)}, lowest axis {min(axes)}; needs 12 and 3) (r-threshold-12-of-15-and-per-axis-floor)")
        smp = c.get("icp_density_sample")
        if isinstance(smp, dict) and isinstance(smp.get("observed"), int) and isinstance(smp.get("of"), int) and smp["observed"] > smp["of"]:
            errs.append(f"candidates[{n}].icp_density_sample observed {smp['observed']} exceeds the sample {smp['of']} (r-icp-density-cites-sample)")
        by_name[c.get("channel")] = c
    sel = _d(obj.get("selected_on"))
    bet = obj.get("bet")
    if isinstance(bet, dict):
        ch = bet.get("channel")
        if ch not in by_name:
            errs.append(f"bet.channel {ch!r} is not one of the candidates (r-one-channel-parking-lot)")
        elif not by_name[ch].get("clears_bar"):
            errs.append(f"bet.channel {ch!r} does not clear 12 of 15 with every axis at 3; return no bet (r-threshold-12-of-15-and-per-axis-floor)")
        sd, ed = _d(bet.get("start_date")), _d(bet.get("end_date"))
        if sd and ed and (ed - sd).days != 90:
            errs.append(f"bet.end_date is {(ed - sd).days} days after start_date; the bet is exactly 90 days (r-one-channel-parking-lot)")
        if sel and sd and sd < sel:
            errs.append("bet.start_date precedes selected_on (r-written-rubric-single-page)")
        wo = _d((bet.get("kill_criterion") or {}).get("written_on"))
        if sel and wo and wo != sel:
            errs.append(f"kill_criterion.written_on {wo} is not the selection day {sel} (r-precommitted-kill-criterion)")
        parked = {p.get("channel"): p.get("total") for p in (obj.get("parking_lot") or {}).get("channels") or [] if isinstance(p, dict)}
        for name, c in by_name.items():
            if name == ch:
                if name in parked:
                    errs.append(f"parking_lot lists the chosen channel {name!r} (r-one-channel-parking-lot)")
                continue
            if name not in parked:
                errs.append(f"candidate {name!r} is missing from parking_lot.channels (r-one-channel-parking-lot)")
            elif parked[name] != c.get("total"):
                errs.append(f"parking_lot total {parked[name]} for {name!r} is not the rubric total {c.get('total')} (r-one-channel-parking-lot)")
    else:
        if any(c.get("clears_bar") for c in cands):
            errs.append("outcome no_bet while a candidate clears the bar (r-threshold-12-of-15-and-per-axis-floor)")
        route = obj.get("no_bet_route") or {}
        totals = [(c.get("total"), c.get("channel")) for c in cands if isinstance(c.get("total"), int)]
        if totals and route.get("highest_scorer") != max(totals)[1]:
            errs.append(f"no_bet_route.highest_scorer {route.get('highest_scorer')!r} is not the top total {max(totals)[1]!r} (r-threshold-12-of-15-and-per-axis-floor)")
    return errs


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(obj, SCHEMA, "$", errs)
    if not errs:
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
        prog="validate-single-channel-bet-selector.py",
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
