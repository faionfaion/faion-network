#!/usr/bin/env python3
"""validate-north-star-metric.py

Validate the NSM decision record produced by the north-star-metric methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/north-star-metric.json', 'title': 'North Star Metric decision record', 'type': 'object', 'required': ['product_name', 'decided_on', 'candidates', 'chosen_nsm', 'definition', 'validation', 'runner_ups', 'input_metrics', 'gaming_risks', 'change_control'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'score': {'type': 'integer', 'minimum': 1, 'maximum': 5}, 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'product_name': {'type': 'string', 'minLength': 2}, 'decided_on': {'$ref': '#/definitions/date'}, 'candidates': {'type': 'array', 'minItems': 3, 'items': {'type': 'object', 'required': ['name', 'counts', 'scores', 'total'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 3}, 'counts': {'type': 'string', 'enum': ['value_event', 'revenue', 'signups', 'registered_users', 'pageviews', 'sessions', 'mau']}, 'scores': {'type': 'object', 'required': ['customer_value', 'leading_indicator_of_revenue', 'actionable_within_quarter', 'understandable_without_data_team', 'measurable_today'], 'additionalProperties': False, 'properties': {'customer_value': {'$ref': '#/definitions/score'}, 'leading_indicator_of_revenue': {'$ref': '#/definitions/score'}, 'actionable_within_quarter': {'$ref': '#/definitions/score'}, 'understandable_without_data_team': {'$ref': '#/definitions/score'}, 'measurable_today': {'$ref': '#/definitions/score'}}}, 'total': {'type': 'integer', 'minimum': 5, 'maximum': 25}}}}, 'chosen_nsm': {'type': 'object', 'required': ['name', 'is_highest_scoring'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 3}, 'is_highest_scoring': {'type': 'boolean'}, 'not_highest_because': {'type': 'string', 'minLength': 20}}, 'if': {'properties': {'is_highest_scoring': {'const': False}}}, 'then': {'required': ['not_highest_because']}}, 'definition': {'type': 'object', 'required': ['events', 'unit', 'window', 'threshold', 'inclusions', 'exclusions', 'dashboard_url'], 'additionalProperties': False, 'properties': {'events': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'$ref': '#/definitions/event_name'}}, 'unit': {'type': 'string', 'enum': ['users', 'accounts', 'teams', 'transactions']}, 'window': {'type': 'string', 'enum': ['daily', 'weekly', '28_day']}, 'threshold': {'type': 'number', 'exclusiveMinimum': 0}, 'inclusions': {'type': 'array', 'items': {'type': 'string', 'minLength': 3}}, 'exclusions': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 3}}, 'dashboard_url': {'type': 'string', 'pattern': '^https?://'}}}, 'validation': {'type': 'object', 'required': ['method', 'cohort_size', 'period_start', 'period_end', 'outcome', 'rate_above', 'rate_below', 'delta', 'result', 'run_date'], 'additionalProperties': False, 'properties': {'method': {'const': 'above_vs_below_threshold_cohort'}, 'cohort_size': {'type': 'integer', 'minimum': 1}, 'period_start': {'$ref': '#/definitions/date'}, 'period_end': {'$ref': '#/definitions/date'}, 'outcome': {'type': 'string', 'enum': ['retained', 'converted_to_paid']}, 'rate_above': {'$ref': '#/definitions/rate'}, 'rate_below': {'$ref': '#/definitions/rate'}, 'delta': {'type': 'number', 'exclusiveMinimum': 0, 'maximum': 1}, 'result': {'type': 'string', 'enum': ['yes', 'no', 'inconclusive']}, 'run_date': {'$ref': '#/definitions/date'}}}, 'runner_ups': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['name', 'disposition'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 3}, 'disposition': {'type': 'string', 'enum': ['input_metric', 'rejected']}, 'rejection_reason': {'type': 'string', 'minLength': 20}}, 'if': {'properties': {'disposition': {'const': 'rejected'}}}, 'then': {'required': ['rejection_reason']}}}, 'input_metrics': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'items': {'type': 'object', 'required': ['name', 'dimension', 'owning_team', 'current_value', 'target', 'movable_within_quarter'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 3}, 'dimension': {'type': 'string', 'enum': ['breadth', 'depth', 'frequency', 'efficiency']}, 'owning_team': {'type': 'string', 'minLength': 2}, 'current_value': {'type': 'number'}, 'target': {'type': 'number'}, 'movable_within_quarter': {'const': True}}}}, 'gaming_risks': {'type': 'object', 'required': ['vectors', 'inflatable_by_spend_alone'], 'additionalProperties': False, 'properties': {'vectors': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['vector', 'guard'], 'additionalProperties': False, 'properties': {'vector': {'type': 'string', 'enum': ['paid_signups', 'notification_spam', 'internal_or_bot_activity', 'threshold_lowering', 'other']}, 'guard': {'type': 'object', 'required': ['kind', 'detail'], 'additionalProperties': False, 'properties': {'kind': {'type': 'string', 'enum': ['definition_exclusion', 'paired_quality_metric', 'paired_retention_metric', 'threshold_review_rule']}, 'detail': {'type': 'string', 'minLength': 10}}}}}}, 'inflatable_by_spend_alone': {'const': False}}}, 'change_control': {'type': 'object', 'required': ['previous_record', 'series_break_date', 'next_review_date'], 'additionalProperties': False, 'properties': {'previous_record': {'type': ['string', 'null'], 'minLength': 3}, 'series_break_date': {'anyOf': [{'type': 'null'}, {'$ref': '#/definitions/date'}]}, 'next_review_date': {'$ref': '#/definitions/date'}}, 'if': {'properties': {'previous_record': {'type': 'string'}}}, 'then': {'properties': {'series_break_date': {'type': 'string'}}}}}}

OK = {'product_name': 'Trellis', 'decided_on': '2026-07-20', 'candidates': [{'name': 'weekly teams completing at least one project', 'counts': 'value_event', 'scores': {'customer_value': 5, 'leading_indicator_of_revenue': 5, 'actionable_within_quarter': 4, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 24}, {'name': 'weekly active teams', 'counts': 'mau', 'scores': {'customer_value': 3, 'leading_indicator_of_revenue': 3, 'actionable_within_quarter': 4, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 20}, {'name': 'weekly signups', 'counts': 'signups', 'scores': {'customer_value': 1, 'leading_indicator_of_revenue': 2, 'actionable_within_quarter': 5, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 18}, {'name': 'MRR', 'counts': 'revenue', 'scores': {'customer_value': 2, 'leading_indicator_of_revenue': 1, 'actionable_within_quarter': 2, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 15}], 'chosen_nsm': {'name': 'weekly teams completing at least one project', 'is_highest_scoring': True}, 'definition': {'events': ['project_completed'], 'unit': 'teams', 'window': 'weekly', 'threshold': 1, 'inclusions': ['free and paid workspaces', 'projects with at least two members'], 'exclusions': ['internal workspaces (domain trellis.example)', 'test data flagged is_test', 'workspaces created in the current week'], 'dashboard_url': 'https://analytics.example.com/dashboards/nsm-weekly-completing-teams'}, 'validation': {'method': 'above_vs_below_threshold_cohort', 'cohort_size': 4200, 'period_start': '2026-05-01', 'period_end': '2026-06-30', 'outcome': 'retained', 'rate_above': 0.62, 'rate_below': 0.21, 'delta': 0.41, 'result': 'yes', 'run_date': '2026-07-15'}, 'runner_ups': [{'name': 'weekly active teams', 'disposition': 'input_metric'}, {'name': 'weekly signups', 'disposition': 'rejected', 'rejection_reason': 'can be bought with acquisition spend and says nothing about value received; loses on customer value and leading indicator'}, {'name': 'MRR', 'disposition': 'rejected', 'rejection_reason': 'lags value by months and is moved by pricing and packaging rather than by the product; kept as the outcome the NSM is validated against'}], 'input_metrics': [{'name': 'weekly active teams', 'dimension': 'breadth', 'owning_team': 'growth', 'current_value': 310, 'target': 400, 'movable_within_quarter': True}, {'name': 'projects completed per active team', 'dimension': 'depth', 'owning_team': 'product', 'current_value': 1.8, 'target': 2.5, 'movable_within_quarter': True}, {'name': 'share of teams active on 3 or more days a week', 'dimension': 'frequency', 'owning_team': 'lifecycle', 'current_value': 0.44, 'target': 0.55, 'movable_within_quarter': True}, {'name': 'median days from workspace creation to first completed project', 'dimension': 'efficiency', 'owning_team': 'onboarding', 'current_value': 4.2, 'target': 2.5, 'movable_within_quarter': True}], 'gaming_risks': {'vectors': [{'vector': 'notification_spam', 'guard': {'kind': 'paired_retention_metric', 'detail': 'week-8 team retention is reported next to the NSM; a rising NSM with flat retention triggers a review'}}, {'vector': 'internal_or_bot_activity', 'guard': {'kind': 'definition_exclusion', 'detail': 'internal workspaces and is_test data are excluded in the definition; projects completed by integration bots do not count'}}, {'vector': 'threshold_lowering', 'guard': {'kind': 'threshold_review_rule', 'detail': 'the threshold of one completed project changes only through a new decision record with a series-break date'}}], 'inflatable_by_spend_alone': False}, 'change_control': {'previous_record': None, 'series_break_date': None, 'next_review_date': '2027-07-15'}}

BAD = {'product_name': 'Trellis', 'decided_on': '2026-07-20', 'candidates': [{'name': 'MRR', 'counts': 'revenue', 'scores': {'customer_value': 2, 'leading_indicator_of_revenue': 1, 'actionable_within_quarter': 2, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 22}, {'name': 'weekly signups', 'counts': 'signups', 'scores': {'customer_value': 1, 'leading_indicator_of_revenue': 2, 'actionable_within_quarter': 5, 'understandable_without_data_team': 5, 'measurable_today': 5}, 'total': 18}], 'chosen_nsm': {'name': 'MRR', 'is_highest_scoring': False}, 'definition': {'events': [], 'unit': 'dollars', 'window': 'monthly', 'threshold': 0, 'inclusions': [], 'exclusions': [], 'dashboard_url': 'see finance'}, 'validation': {'method': 'correlates_with_retention', 'cohort_size': 0, 'period_start': '2026-05-01', 'period_end': '2026-06-30', 'outcome': 'retained', 'rate_above': 0.5, 'rate_below': 0.5, 'delta': 0, 'result': 'inconclusive', 'run_date': '2026-07-15'}, 'runner_ups': [{'name': 'weekly signups', 'disposition': 'secondary_nsm'}], 'input_metrics': [{'name': 'grow MRR', 'dimension': 'revenue', 'owning_team': 'everyone', 'current_value': 120000, 'target': 200000, 'movable_within_quarter': False}], 'gaming_risks': {'vectors': [], 'inflatable_by_spend_alone': True}, 'change_control': {'previous_record': 'nsm-2024-01', 'series_break_date': None, 'next_review_date': '2029-01-01'}}


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


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    cands = [c for c in obj.get("candidates") or [] if isinstance(c, dict)]
    by_name = {c.get("name"): c for c in cands}
    for n, c in enumerate(cands):
        sc = c.get("scores") or {}
        vals = [sc.get(k) for k in ("customer_value", "leading_indicator_of_revenue", "actionable_within_quarter", "understandable_without_data_team", "measurable_today")]
        if all(_num(v) for v in vals) and c.get("total") != sum(vals):
            errs.append(f"candidates[{n}].total {c.get('total')} is not the sum of its five scores = {sum(vals)} (r-candidates-scored-against-criteria)")
    ch = obj.get("chosen_nsm") or {}
    name = ch.get("name")
    if name not in by_name:
        errs.append(f"chosen_nsm.name {name!r} is not one of the candidates (r-candidates-scored-against-criteria)")
    else:
        if by_name[name].get("counts") != "value_event":
            errs.append(f"chosen_nsm {name!r} counts {by_name[name].get('counts')}; the NSM must count a customer value event (r-nsm-counts-value-delivered)")
        totals = [c.get("total") for c in cands if _num(c.get("total"))]
        if totals and _num(by_name[name].get("total")):
            highest = by_name[name]["total"] >= max(totals)
            if ch.get("is_highest_scoring") != highest:
                errs.append(f"chosen_nsm.is_highest_scoring {ch.get('is_highest_scoring')} disagrees with the scores (chosen {by_name[name]['total']}, best {max(totals)}) (r-candidates-scored-against-criteria)")
    v = obj.get("validation") or {}
    if _num(v.get("rate_above")) and _num(v.get("rate_below")) and _num(v.get("delta")) and abs(v["delta"] - (v["rate_above"] - v["rate_below"])) > 0.0051:
        errs.append(f"validation.delta {v['delta']} is not rate_above - rate_below = {v['rate_above'] - v['rate_below']:.3f} (r-nsm-validated-against-retention)")
    if v.get("result") in ("no", "inconclusive"):
        errs.append(f"validation.result {v['result']}: an NSM is adopted only on a yes from the cohort comparison (r-nsm-validated-against-retention)")
    ps, pe, rd = _d(v.get("period_start")), _d(v.get("period_end")), _d(v.get("run_date"))
    if ps and pe and pe <= ps:
        errs.append("validation.period_end is not after period_start (r-nsm-validated-against-retention)")
    if pe and rd and rd < pe:
        errs.append(f"validation.run_date {rd} precedes period_end {pe} (r-nsm-validated-against-retention)")
    runner = {r.get("name"): r for r in obj.get("runner_ups") or [] if isinstance(r, dict)}
    inputs = {i.get("name") for i in obj.get("input_metrics") or [] if isinstance(i, dict)}
    for c in cands:
        if c.get("name") != name and c.get("name") not in runner:
            errs.append(f"candidate {c.get('name')!r} is neither the chosen NSM nor listed in runner_ups (r-single-nsm)")
    for rn, r in runner.items():
        if rn == name:
            errs.append(f"runner_ups lists the chosen NSM {rn!r}; exactly one NSM (r-single-nsm)")
        if rn not in by_name:
            errs.append(f"runner_ups entry {rn!r} is not a candidate (r-single-nsm)")
        if r.get("disposition") == "input_metric" and rn not in inputs:
            errs.append(f"runner-up {rn!r} is placed as an input metric but does not appear in input_metrics (r-input-metrics-tree)")
    d0, nr = _d(obj.get("decided_on")), _d((obj.get("change_control") or {}).get("next_review_date"))
    if d0 and nr:
        if (nr - d0).days > 365:
            errs.append(f"change_control.next_review_date {nr} is {(nr - d0).days} days after decided_on; the NSM is reviewed at least yearly (r-nsm-change-is-a-new-record)")
        if nr <= d0:
            errs.append("change_control.next_review_date is not after decided_on (r-nsm-change-is-a-new-record)")
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
        prog="validate-north-star-metric.py",
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
