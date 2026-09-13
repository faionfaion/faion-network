#!/usr/bin/env python3
"""validate-ramp-task-difficulty-ladder.py

Validate the RampLadder produced by the ramp-task-difficulty-ladder methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/ramp-task-difficulty-ladder.json', 'title': 'RampLadder', 'type': 'object', 'required': ['team', 'header', 'rungs', 'ramps', 'outcome_review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'days': {'type': 'number', 'exclusiveMinimum': 0}, 'rung_no': {'type': 'integer', 'minimum': 1}, 'support': {'enum': ['full_pairing', 'pair_on_pr', 'review_on_pr', 'review_on_design', 'scheduled_check_ins']}, 'ticket_ref': {'type': 'string', 'pattern': '^(https?://\\S+|[A-Z][A-Z0-9]+-[0-9]+|#[0-9]+)$'}}, 'properties': {'__faion_header__': {'type': 'object'}, 'team': {'type': 'string', 'minLength': 2}, 'header': {'type': 'object', 'required': ['owner', 'version', 'last_reviewed', 'ramp_window_days', 'review_cadence', 'rung_label_prefix'], 'additionalProperties': False, 'properties': {'owner': {'type': 'string', 'pattern': '^[a-z][a-z0-9-]*:[a-z0-9._-]+$'}, 'version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+\\.[0-9]+$'}, 'last_reviewed': {'$ref': '#/definitions/date'}, 'ramp_window_days': {'type': 'integer', 'minimum': 5, 'maximum': 60}, 'review_cadence': {'enum': ['monthly', 'quarterly']}, 'rung_label_prefix': {'type': 'string', 'pattern': '^[a-z][a-z0-9/_-]*$'}}}, 'rungs': {'type': 'array', 'minItems': 4, 'items': {'type': 'object', 'required': ['rung', 'name', 'ticket_pattern', 'expected_duration_days', 'buddy_support', 'evidence', 'tagged_tickets'], 'additionalProperties': False, 'properties': {'rung': {'$ref': '#/definitions/rung_no'}, 'name': {'type': 'string', 'minLength': 3, 'not': {'pattern': '(?i)(story point|t-shirt|\\beasy\\b|\\bmedium\\b|\\bhard\\b)'}}, 'ticket_pattern': {'type': 'object', 'required': ['files_touched_max', 'modules_crossed_max', 'behind_feature_flag', 'design_review_required', 'examples'], 'properties': {'files_touched_max': {'type': 'integer', 'minimum': 1}, 'modules_crossed_max': {'type': 'integer', 'minimum': 1}, 'behind_feature_flag': {'type': 'boolean'}, 'design_review_required': {'type': 'boolean'}, 'examples': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 5, 'not': {'pattern': '(?i)([0-9]+ ?(story )?points?|t-shirt|\\beasy\\b|\\bmedium\\b|\\bhard\\b)'}}}}}, 'expected_duration_days': {'type': 'object', 'required': ['min', 'max'], 'properties': {'min': {'$ref': '#/definitions/days'}, 'max': {'$ref': '#/definitions/days'}}}, 'buddy_support': {'$ref': '#/definitions/support'}, 'evidence': {'type': 'object', 'required': ['status'], 'properties': {'status': {'enum': ['validated', 'unvalidated']}, 'not_applicable': {'const': 'unvalidated'}, 'merged_ref': {'$ref': '#/definitions/ticket_ref'}, 'completed_by_newcomer': {'type': 'string', 'minLength': 2}, 'actual_duration_days': {'$ref': '#/definitions/days'}}, 'if': {'properties': {'status': {'const': 'validated'}}}, 'then': {'required': ['merged_ref', 'completed_by_newcomer', 'actual_duration_days']}, 'else': {'required': ['not_applicable']}}, 'tagged_tickets': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['ref', 'label', 'on_critical_path', 'deadline_inside_ramp_window'], 'properties': {'ref': {'$ref': '#/definitions/ticket_ref'}, 'label': {'type': 'string', 'pattern': '^[a-z][a-z0-9/_-]*[0-9]+$'}, 'on_critical_path': {'type': 'boolean'}, 'deadline_inside_ramp_window': {'type': 'boolean'}}}}}, 'allOf': [{'if': {'properties': {'rung': {'const': 1}}}, 'then': {'properties': {'expected_duration_days': {'properties': {'max': {'maximum': 1}}}, 'buddy_support': {'const': 'full_pairing'}}}}, {'if': {'properties': {'rung': {'maximum': 2}}}, 'then': {'properties': {'tagged_tickets': {'items': {'properties': {'on_critical_path': {'const': False}, 'deadline_inside_ramp_window': {'const': False}}}}}}}]}}, 'ramps': {'type': 'array', 'items': {'type': 'object', 'required': ['newcomer', 'start_date', 'tickets_tagged_on', 'progression', 'time_to_first_pr_days', 'rung_reached_on_last_day'], 'additionalProperties': False, 'properties': {'newcomer': {'type': 'string', 'minLength': 2}, 'start_date': {'$ref': '#/definitions/date'}, 'tickets_tagged_on': {'$ref': '#/definitions/date'}, 'progression': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['rung', 'ticket', 'merged_on', 'actual_duration_days'], 'properties': {'rung': {'$ref': '#/definitions/rung_no'}, 'ticket': {'$ref': '#/definitions/ticket_ref'}, 'merged_on': {'$ref': '#/definitions/date'}, 'actual_duration_days': {'$ref': '#/definitions/days'}, 'reclassified_to_rung': {'$ref': '#/definitions/rung_no'}}}}, 'time_to_first_pr_days': {'type': 'number', 'minimum': 0}, 'rung_reached_on_last_day': {'$ref': '#/definitions/rung_no'}}}}, 'outcome_review': {'type': 'object', 'required': ['last_run', 'next_due', 'ramps_reviewed', 'median_time_to_first_pr_days', 'per_rung', 'version_bumped'], 'additionalProperties': False, 'properties': {'last_run': {'$ref': '#/definitions/date'}, 'next_due': {'$ref': '#/definitions/date'}, 'ramps_reviewed': {'type': 'integer', 'minimum': 0}, 'median_time_to_first_pr_days': {'type': 'number', 'minimum': 0}, 'per_rung': {'type': 'array', 'items': {'type': 'object', 'required': ['rung', 'median_actual_days', 'within_band', 'consecutive_out_of_band_cycles', 'action'], 'properties': {'rung': {'$ref': '#/definitions/rung_no'}, 'median_actual_days': {'type': ['number', 'null']}, 'within_band': {'type': 'boolean'}, 'consecutive_out_of_band_cycles': {'type': 'integer', 'minimum': 0}, 'action': {'enum': ['none', 'rebanded', 'pattern_rewritten']}}, 'if': {'properties': {'within_band': {'const': False}}}, 'then': {'properties': {'action': {'enum': ['rebanded', 'pattern_rewritten']}}}}}, 'version_bumped': {'type': 'boolean'}}}}}

OK = {'team': 'payments-platform', 'header': {'owner': 'tech-lead:alice.m', 'version': '1.2.0', 'last_reviewed': '2026-06-30', 'ramp_window_days': 10, 'review_cadence': 'quarterly', 'rung_label_prefix': 'ramp/rung-'}, 'rungs': [{'rung': 1, 'name': 'read-only change that ships', 'ticket_pattern': {'files_touched_max': 1, 'modules_crossed_max': 1, 'behind_feature_flag': False, 'design_review_required': False, 'examples': ['docs typo fix in README', 'dependency patch bump', 'add a log line']}, 'expected_duration_days': {'min': 0.25, 'max': 1}, 'buddy_support': 'full_pairing', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/payments/pull/812', 'completed_by_newcomer': 'dmytro.k', 'actual_duration_days': 0.4}, 'tagged_tickets': [{'ref': 'PAY-2210', 'label': 'ramp/rung-1', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2214', 'label': 'ramp/rung-1', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}, {'rung': 2, 'name': 'single-file change', 'ticket_pattern': {'files_touched_max': 1, 'modules_crossed_max': 1, 'behind_feature_flag': False, 'design_review_required': False, 'examples': ['rename a function and its call sites in one file', 'add a unit test for an existing helper']}, 'expected_duration_days': {'min': 1, 'max': 2}, 'buddy_support': 'pair_on_pr', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/payments/pull/819', 'completed_by_newcomer': 'dmytro.k', 'actual_duration_days': 1.5}, 'tagged_tickets': [{'ref': 'PAY-2218', 'label': 'ramp/rung-2', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2221', 'label': 'ramp/rung-2', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}, {'rung': 3, 'name': 'single-module change behind a flag', 'ticket_pattern': {'files_touched_max': 5, 'modules_crossed_max': 1, 'behind_feature_flag': True, 'design_review_required': False, 'examples': ['new read endpoint in the refunds module behind refunds_v2 flag']}, 'expected_duration_days': {'min': 2, 'max': 3}, 'buddy_support': 'review_on_pr', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/payments/pull/831', 'completed_by_newcomer': 'dmytro.k', 'actual_duration_days': 2.5}, 'tagged_tickets': [{'ref': 'PAY-2230', 'label': 'ramp/rung-3', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2233', 'label': 'ramp/rung-3', 'on_critical_path': True, 'deadline_inside_ramp_window': False}]}, {'rung': 4, 'name': 'cross-module change with design review', 'ticket_pattern': {'files_touched_max': 12, 'modules_crossed_max': 2, 'behind_feature_flag': True, 'design_review_required': True, 'examples': ['small refactor across refunds and ledger modules']}, 'expected_duration_days': {'min': 3, 'max': 5}, 'buddy_support': 'review_on_design', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/payments/pull/840', 'completed_by_newcomer': 'dmytro.k', 'actual_duration_days': 4}, 'tagged_tickets': [{'ref': 'PAY-2240', 'label': 'ramp/rung-4', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2241', 'label': 'ramp/rung-4', 'on_critical_path': False, 'deadline_inside_ramp_window': True}]}, {'rung': 5, 'name': 'end-to-end feature slice', 'ticket_pattern': {'files_touched_max': 25, 'modules_crossed_max': 3, 'behind_feature_flag': True, 'design_review_required': True, 'examples': ['partial-refund flow from API to ledger entry behind a flag']}, 'expected_duration_days': {'min': 5, 'max': 10}, 'buddy_support': 'scheduled_check_ins', 'evidence': {'status': 'unvalidated', 'not_applicable': 'unvalidated'}, 'tagged_tickets': [{'ref': 'PAY-2250', 'label': 'ramp/rung-5', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2252', 'label': 'ramp/rung-5', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}], 'ramps': [{'newcomer': 'dmytro.k', 'start_date': '2026-04-06', 'tickets_tagged_on': '2026-03-30', 'progression': [{'rung': 1, 'ticket': 'PAY-2101', 'merged_on': '2026-04-06', 'actual_duration_days': 0.4}, {'rung': 2, 'ticket': 'PAY-2105', 'merged_on': '2026-04-08', 'actual_duration_days': 1.5}, {'rung': 3, 'ticket': 'PAY-2112', 'merged_on': '2026-04-13', 'actual_duration_days': 2.5}, {'rung': 4, 'ticket': 'PAY-2120', 'merged_on': '2026-04-17', 'actual_duration_days': 4}], 'time_to_first_pr_days': 1, 'rung_reached_on_last_day': 4}, {'newcomer': 'iryna.s', 'start_date': '2026-05-11', 'tickets_tagged_on': '2026-05-06', 'progression': [{'rung': 1, 'ticket': 'PAY-2210', 'merged_on': '2026-05-11', 'actual_duration_days': 0.5}, {'rung': 2, 'ticket': 'PAY-2218', 'merged_on': '2026-05-13', 'actual_duration_days': 1.5}, {'rung': 3, 'ticket': 'PAY-2230', 'merged_on': '2026-05-21', 'actual_duration_days': 7, 'reclassified_to_rung': 4}], 'time_to_first_pr_days': 1, 'rung_reached_on_last_day': 3}], 'outcome_review': {'last_run': '2026-06-30', 'next_due': '2026-09-30', 'ramps_reviewed': 2, 'median_time_to_first_pr_days': 1, 'per_rung': [{'rung': 1, 'median_actual_days': 0.45, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}, {'rung': 2, 'median_actual_days': 1.5, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}, {'rung': 3, 'median_actual_days': 4.75, 'within_band': False, 'consecutive_out_of_band_cycles': 1, 'action': 'pattern_rewritten'}, {'rung': 4, 'median_actual_days': 4, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}, {'rung': 5, 'median_actual_days': None, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}], 'version_bumped': True}}

BAD = {'team': 'payments-platform', 'header': {'owner': 'tech-lead:alice.m', 'version': '1.2.0', 'last_reviewed': '2026-06-30', 'ramp_window_days': 10, 'review_cadence': 'quarterly', 'rung_label_prefix': 'ramp/rung-'}, 'rungs': [{'rung': 1, 'name': 'easy (1-2 story points)', 'ticket_pattern': {'files_touched_max': 1, 'modules_crossed_max': 1, 'behind_feature_flag': False, 'design_review_required': False, 'examples': ['any 1-point ticket']}, 'expected_duration_days': {'min': 1, 'max': 2}, 'buddy_support': 'full_pairing', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/onboarding-kata/pull/3', 'completed_by_newcomer': 'dmytro.k', 'actual_duration_days': 1}, 'tagged_tickets': [{'ref': 'PAY-2210', 'label': 'ramp/rung-1', 'on_critical_path': True, 'deadline_inside_ramp_window': True}, {'ref': 'PAY-2214', 'label': 'ramp/rung-1', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}, {'rung': 2, 'name': 'medium', 'ticket_pattern': {'files_touched_max': 3, 'modules_crossed_max': 1, 'behind_feature_flag': False, 'design_review_required': False, 'examples': ['rename a function and its call sites']}, 'expected_duration_days': {'min': 1, 'max': 2}, 'buddy_support': 'scheduled_check_ins', 'evidence': {'status': 'validated', 'merged_ref': 'https://github.com/acme/payments/pull/700', 'completed_by_newcomer': 'alice.m', 'actual_duration_days': 0.5}, 'tagged_tickets': [{'ref': 'PAY-2218', 'label': 'ramp/rung-2', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}, {'rung': 3, 'name': 'single-module change behind a flag', 'ticket_pattern': {'files_touched_max': 5, 'modules_crossed_max': 1, 'behind_feature_flag': True, 'design_review_required': False, 'examples': ['new read endpoint behind a flag']}, 'expected_duration_days': {'min': 2, 'max': 3}, 'buddy_support': 'review_on_pr', 'evidence': {'status': 'unvalidated'}, 'tagged_tickets': [{'ref': 'PAY-2230', 'label': 'ramp/rung-3', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2233', 'label': 'ramp/rung-3', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}, {'rung': 4, 'name': 'cross-module migration', 'ticket_pattern': {'files_touched_max': 12, 'modules_crossed_max': 2, 'behind_feature_flag': True, 'design_review_required': True, 'examples': ['ledger schema migration']}, 'expected_duration_days': {'min': 3, 'max': 12}, 'buddy_support': 'review_on_design', 'evidence': {'status': 'unvalidated', 'not_applicable': 'unvalidated'}, 'tagged_tickets': [{'ref': 'PAY-2240', 'label': 'ramp/rung-4', 'on_critical_path': False, 'deadline_inside_ramp_window': False}, {'ref': 'PAY-2241', 'label': 'ramp/rung-4', 'on_critical_path': False, 'deadline_inside_ramp_window': False}]}], 'ramps': [{'newcomer': 'iryna.s', 'start_date': '2026-05-11', 'tickets_tagged_on': '2026-05-12', 'progression': [{'rung': 1, 'ticket': 'PAY-2210', 'merged_on': '2026-05-15', 'actual_duration_days': 4}, {'rung': 4, 'ticket': 'PAY-2240', 'merged_on': '2026-05-29', 'actual_duration_days': 9}], 'time_to_first_pr_days': 5, 'rung_reached_on_last_day': 4}], 'outcome_review': {'last_run': '2026-06-30', 'next_due': '2027-01-15', 'ramps_reviewed': 1, 'median_time_to_first_pr_days': 5, 'per_rung': [{'rung': 1, 'median_actual_days': 4, 'within_band': False, 'consecutive_out_of_band_cycles': 2, 'action': 'none'}, {'rung': 2, 'median_actual_days': None, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}, {'rung': 3, 'median_actual_days': None, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}, {'rung': 4, 'median_actual_days': 9, 'within_band': True, 'consecutive_out_of_band_cycles': 0, 'action': 'none'}], 'version_bumped': False}}


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


_SUPPORT_RANK = {"full_pairing": 0, "pair_on_pr": 1, "review_on_pr": 2, "review_on_design": 3, "scheduled_check_ins": 4}
_CADENCE_MAX_DAYS = {"monthly": 31, "quarterly": 92}


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    header = obj.get("header") or {}
    rungs = sorted(obj.get("rungs") or [], key=lambda r: r.get("rung", 0))
    numbers = [r.get("rung") for r in rungs]
    if numbers != list(range(1, len(rungs) + 1)):
        errs.append(f"rungs: numbered {numbers}, expected 1..{len(rungs)} without gaps (r-durations-monotonic-rung1-under-a-day)")
    bands = {r.get("rung"): r.get("expected_duration_days") or {} for r in rungs}
    prev_max, prev_rank = None, -1
    for r in rungs:
        n, band = r.get("rung"), r.get("expected_duration_days") or {}
        if band.get("max", 0) < band.get("min", 0):
            errs.append(f"rungs[{n}]: expected_duration_days.max {band.get('max')} below min {band.get('min')} (r-durations-monotonic-rung1-under-a-day)")
        if prev_max is not None and band.get("max", 0) < prev_max:
            errs.append(f"rungs[{n}]: upper bound {band.get('max')} below rung {n - 1}'s {prev_max}; bands must be non-decreasing (r-durations-monotonic-rung1-under-a-day)")
        prev_max = band.get("max", 0)
        rank = _SUPPORT_RANK.get(r.get("buddy_support"), -1)
        if rank < prev_rank:
            errs.append(f"rungs[{n}]: buddy_support {r.get('buddy_support')!r} is more support than the rung below; support only fades up the ladder (r-buddy-support-fades-per-rung)")
        prev_rank = rank
        prefix = header.get("rung_label_prefix", "")
        for t in r.get("tagged_tickets") or []:
            if t.get("label") != f"{prefix}{n}":
                errs.append(f"rungs[{n}]: ticket {t.get('ref')} labelled {t.get('label')!r}, expected {prefix}{n!r} (r-tickets-tagged-before-start-date)")
    if rungs:
        top = rungs[-1]
        if (top.get("expected_duration_days") or {}).get("max", 0) > header.get("ramp_window_days", 0):
            errs.append(f"rungs[{top.get('rung')}]: upper bound {top['expected_duration_days'].get('max')} exceeds ramp_window_days {header.get('ramp_window_days')} (r-durations-monotonic-rung1-under-a-day)")
        if top.get("buddy_support") != "scheduled_check_ins":
            errs.append(f"rungs[{top.get('rung')}]: top rung buddy_support must be scheduled_check_ins, got {top.get('buddy_support')!r} (r-buddy-support-fades-per-rung)")
    for i, ramp in enumerate(obj.get("ramps") or []):
        sd, td = _date(ramp.get("start_date")), _date(ramp.get("tickets_tagged_on"))
        if sd and td and td > sd:
            errs.append(f"ramps[{i}]: tickets tagged on {td}, after the start date {sd} (r-tickets-tagged-before-start-date)")
        prev = 0
        for j, step in enumerate(ramp.get("progression") or []):
            n = step.get("rung", 0)
            if n > prev + 1:
                errs.append(f"ramps[{i}].progression[{j}]: rung {n} after rung {prev}; one merged ticket per rung, no skips (r-promotion-requires-completed-rung)")
            prev = max(prev, n)
            band_max = bands.get(n, {}).get("max")
            if band_max and step.get("actual_duration_days", 0) > 2 * band_max and "reclassified_to_rung" not in step:
                errs.append(f"ramps[{i}].progression[{j}]: {step.get('actual_duration_days')} days is past twice rung {n}'s upper bound {band_max} and the ticket was not reclassified (r-promotion-requires-completed-rung)")
    review = obj.get("outcome_review") or {}
    lr, nd = _date(review.get("last_run")), _date(review.get("next_due"))
    limit = _CADENCE_MAX_DAYS.get(header.get("review_cadence"), 92)
    if lr and nd and (nd - lr).days > limit:
        errs.append(f"outcome_review: next_due {nd} is {(nd - lr).days} days after last_run; {header.get('review_cadence')} cadence allows {limit} (r-outcome-review-regrades-rungs)")
    for k, pr in enumerate(review.get("per_rung") or []):
        band, med = bands.get(pr.get("rung"), {}), pr.get("median_actual_days")
        if med is not None and band:
            inside = band.get("min", 0) <= med <= band.get("max", 0)
            if inside != pr.get("within_band"):
                errs.append(f"outcome_review.per_rung[{k}]: median {med} against band {band.get('min')}-{band.get('max')} is {'inside' if inside else 'outside'}, within_band says {pr.get('within_band')} (r-outcome-review-regrades-rungs)")
        if pr.get("consecutive_out_of_band_cycles", 0) >= 2 and (pr.get("action") == "none" or not review.get("version_bumped")):
            errs.append(f"outcome_review.per_rung[{k}]: rung {pr.get('rung')} out of band for {pr.get('consecutive_out_of_band_cycles')} cycles; a review that changes nothing is invalid (r-outcome-review-regrades-rungs)")
        if pr.get("action") != "none" and not review.get("version_bumped"):
            errs.append(f"outcome_review.per_rung[{k}]: rung re-banded or rewritten but version_bumped is false (r-outcome-review-regrades-rungs)")
    if review.get("median_time_to_first_pr_days", 0) > 3:
        r1 = next((p for p in review.get("per_rung") or [] if p.get("rung") == 1), {})
        if r1.get("action", "none") == "none":
            errs.append(f"outcome_review: median_time_to_first_pr_days {review.get('median_time_to_first_pr_days')} is over the 3-day tolerance and rung 1 was not rewritten (r-rung1-merges-to-main)")
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
        prog="validate-ramp-task-difficulty-ladder.py",
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
