#!/usr/bin/env python3
"""validate-freelancer-rate-raise-letter-template.py

Validate the rate-raise artefact produced by the freelancer-rate-raise-letter-template methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/freelancer-rate-raise-letter-template.json', 'title': 'Retainer rate-raise letter artefact', 'type': 'object', 'required': ['client', 'inputs_used', 'rate', 'schedule', 'justification', 'inflight_work', 'letter', 'prepared_concession', 'churn_risk', 'follow_up', 'acknowledgement'], 'additionalProperties': False, 'properties': {'client': {'type': 'object', 'required': ['name', 'contact_email', 'contract_notice_days'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'contact_email': {'type': 'string', 'pattern': '^[^@\\s]+@[^@\\s]+$'}, 'contract_notice_days': {'type': 'integer', 'minimum': 0}, 'renewal_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}, 'inputs_used': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['name', 'source'], 'properties': {'name': {'type': 'string', 'minLength': 3}, 'source': {'type': 'string', 'minLength': 3}}}}, 'rate': {'type': 'object', 'required': ['currency', 'unit', 'current', 'new', 'change_pct', 'is_range_or_open'], 'properties': {'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}, 'unit': {'type': 'string', 'enum': ['per_hour', 'per_day', 'per_month_retainer']}, 'current': {'type': 'number', 'exclusiveMinimum': 0}, 'new': {'type': 'number', 'exclusiveMinimum': 0}, 'change_pct': {'type': 'number'}, 'is_range_or_open': {'const': False}}}, 'schedule': {'type': 'object', 'required': ['letter_date', 'effective_date', 'days_to_effective', 'billing_cycles_to_effective', 'raises_in_last_12_months'], 'properties': {'letter_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'effective_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days_to_effective': {'type': 'integer', 'minimum': 30}, 'billing_cycles_to_effective': {'type': 'integer', 'minimum': 1}, 'raises_in_last_12_months': {'type': 'integer', 'minimum': 0}, 'scope_change_documented_at': {'type': 'string', 'minLength': 3}}, 'if': {'properties': {'raises_in_last_12_months': {'minimum': 1}}}, 'then': {'required': ['scope_change_documented_at']}}, 'justification': {'type': 'object', 'required': ['value_deltas', 'cpi_or_costs_is_sole_justification'], 'properties': {'value_deltas': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['kind', 'statement', 'input_name'], 'properties': {'kind': {'type': 'string', 'enum': ['deliverable', 'metric_moved', 'scope_added', 'capability_depended_on']}, 'statement': {'type': 'string', 'minLength': 15}, 'input_name': {'type': 'string', 'minLength': 3}}}}, 'cpi_or_costs_mentioned': {'type': 'boolean'}, 'cpi_or_costs_is_sole_justification': {'const': False}}}, 'inflight_work': {'type': 'array', 'items': {'type': 'object', 'required': ['reference', 'kind', 'completes_at_current_rate'], 'properties': {'reference': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['signed_sow', 'accepted_quote', 'prepaid_retainer_period']}, 'completes_at_current_rate': {'const': True}}}}, 'letter': {'type': 'object', 'required': ['word_count', 'opens_with_value_delivered', 'states_protected_work', 'closes_with_effective_and_follow_up_dates', 'banned_phrases_found', 'personal_cost_narrative', 'concession_in_letter'], 'properties': {'word_count': {'type': 'integer', 'minimum': 1, 'maximum': 250}, 'opens_with_value_delivered': {'const': True}, 'states_protected_work': {'const': True}, 'closes_with_effective_and_follow_up_dates': {'const': True}, 'banned_phrases_found': {'type': 'array', 'maxItems': 0, 'items': {'type': 'string'}}, 'personal_cost_narrative': {'const': False}, 'concession_in_letter': {'const': False}}}, 'prepared_concession': {'type': 'object', 'required': ['description', 'use_only_in_follow_up'], 'properties': {'description': {'type': 'string', 'minLength': 15}, 'use_only_in_follow_up': {'const': True}}}, 'churn_risk': {'type': 'object', 'required': ['class', 'revenue_share_pct_t12m', 'alternatives', 'recent_feedback', 'payment_behaviour'], 'properties': {'class': {'type': 'string', 'enum': ['stay', 'negotiate', 'churn']}, 'revenue_share_pct_t12m': {'type': 'number', 'minimum': 0, 'maximum': 100}, 'alternatives': {'type': 'string', 'minLength': 10}, 'recent_feedback': {'type': 'string', 'minLength': 5}, 'payment_behaviour': {'type': 'string', 'minLength': 5}, 'replacement_revenue_plan': {'type': 'object', 'required': ['pipeline'], 'properties': {'pipeline': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'expected_close_date', 'monthly_value'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'expected_close_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'monthly_value': {'type': 'number', 'exclusiveMinimum': 0}}}}}}}, 'if': {'properties': {'class': {'const': 'churn'}, 'revenue_share_pct_t12m': {'exclusiveMinimum': 30}}}, 'then': {'required': ['replacement_revenue_plan']}}, 'follow_up': {'type': 'object', 'required': ['date', 'days_after_letter', 'path_if_confirmed', 'path_if_no_reply', 'path_if_push_back'], 'properties': {'date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days_after_letter': {'const': 7}, 'path_if_confirmed': {'type': 'string', 'minLength': 10}, 'path_if_no_reply': {'type': 'string', 'minLength': 10}, 'path_if_push_back': {'type': 'string', 'minLength': 10}}}, 'acknowledgement': {'type': 'object', 'required': ['received_in_writing', 'new_rate_applied'], 'properties': {'received_in_writing': {'type': 'boolean'}, 'received_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'response_state': {'type': 'string', 'enum': ['confirmed', 'no_reply', 'push_back']}, 'new_rate_applied': {'type': 'boolean'}}, 'if': {'properties': {'new_rate_applied': {'const': True}}}, 'then': {'properties': {'received_in_writing': {'const': True}}, 'required': ['received_on']}}}}

OK = {'client': {'name': 'Acme Analytics Ltd', 'contact_email': 'dana@acme.example', 'contract_notice_days': 30, 'renewal_date': '2026-12-31'}, 'inputs_used': [{'name': 'retainer-msa-2025', 'source': 'contracts/acme/msa-2025.pdf#clause-9.3'}, {'name': 'engagement-log-q1-q2', 'source': 'engagements/acme/2026-log.md'}, {'name': 'revenue-t12m', 'source': 'finance/revenue-2025-07-to-2026-06.xlsx'}], 'rate': {'currency': 'EUR', 'unit': 'per_month_retainer', 'current': 6000, 'new': 6720, 'change_pct': 12, 'is_range_or_open': False}, 'schedule': {'letter_date': '2026-07-01', 'effective_date': '2026-09-01', 'days_to_effective': 62, 'billing_cycles_to_effective': 2, 'raises_in_last_12_months': 0}, 'justification': {'value_deltas': [{'kind': 'capability_depended_on', 'statement': 'Since March 2026 I own the release pipeline Acme previously paid an agency EUR 2,400 per month for', 'input_name': 'engagement-log-q1-q2'}, {'kind': 'metric_moved', 'statement': 'Deploy lead time fell from 9 days to 1 day between March and June 2026', 'input_name': 'engagement-log-q1-q2'}], 'cpi_or_costs_mentioned': False, 'cpi_or_costs_is_sole_justification': False}, 'inflight_work': [{'reference': 'SOW-2026-03 data-warehouse migration', 'kind': 'signed_sow', 'completes_at_current_rate': True}, {'reference': 'Retainer period July-August 2026 (prepaid)', 'kind': 'prepaid_retainer_period', 'completes_at_current_rate': True}], 'letter': {'word_count': 196, 'opens_with_value_delivered': True, 'states_protected_work': True, 'closes_with_effective_and_follow_up_dates': True, 'banned_phrases_found': [], 'personal_cost_narrative': False, 'concession_in_letter': False}, 'prepared_concession': {'description': 'Current rate held until 2026-12-31 against a prepaid six-month retainer invoiced in September', 'use_only_in_follow_up': True}, 'churn_risk': {'class': 'negotiate', 'revenue_share_pct_t12m': 18, 'alternatives': 'Could re-engage the agency at roughly 2x my retainer, or hire a platform engineer with a 3-month lead', 'recent_feedback': "Q2 review: 'the pipeline work changed how we ship'; NPS 9", 'payment_behaviour': 'Every retainer invoice paid within net 15 across 14 months'}, 'follow_up': {'date': '2026-07-08', 'days_after_letter': 7, 'path_if_confirmed': 'Send the updated retainer schedule (clause 9.3 variation) for e-signature', 'path_if_no_reply': 'Two-line reminder restating the 2026-09-01 effective date and asking for written confirmation', 'path_if_push_back': 'Offer the prepared concession once; if declined, propose a 30-minute scope call'}, 'acknowledgement': {'received_in_writing': True, 'received_on': '2026-07-06', 'response_state': 'confirmed', 'new_rate_applied': False}}

BAD = {'client': {'name': 'Acme Analytics Ltd', 'contact_email': 'dana@acme.example', 'contract_notice_days': 30}, 'inputs_used': [{'name': 'retainer-msa-2025', 'source': 'contracts/acme/msa-2025.pdf#clause-9.3'}, {'name': 'cpi-eurostat-2026-05', 'source': 'https://ec.europa.eu/eurostat'}], 'rate': {'currency': 'EUR', 'unit': 'per_month_retainer', 'current': 6000, 'new': 6600, 'change_pct': 10, 'is_range_or_open': True}, 'schedule': {'letter_date': '2026-07-01', 'effective_date': '2026-07-01', 'days_to_effective': 0, 'billing_cycles_to_effective': 0, 'raises_in_last_12_months': 1}, 'justification': {'value_deltas': [], 'cpi_or_costs_mentioned': True, 'cpi_or_costs_is_sole_justification': True}, 'inflight_work': [], 'letter': {'word_count': 410, 'opens_with_value_delivered': False, 'states_protected_work': False, 'closes_with_effective_and_follow_up_dates': False, 'banned_phrases_found': ['unfortunately', 'I hope this is okay'], 'personal_cost_narrative': True, 'concession_in_letter': True}, 'prepared_concession': {'description': 'If the new rate is a problem I can keep the old one for now', 'use_only_in_follow_up': False}, 'churn_risk': {'class': 'churn', 'revenue_share_pct_t12m': 42, 'alternatives': 'Unknown, never asked', 'recent_feedback': 'none on file', 'payment_behaviour': 'usually late'}, 'follow_up': {'date': '2026-08-15', 'days_after_letter': 45, 'path_if_confirmed': 'Invoice at the new rate', 'path_if_no_reply': 'Invoice at the new rate', 'path_if_push_back': 'See what they say'}, 'acknowledgement': {'received_in_writing': False, 'new_rate_applied': True}}


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
    """Draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
    exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems, uniqueItems,
    items, properties, additionalProperties, allOf/anyOf/oneOf/not, if/then/else."""
    if schema is True:
        return
    if schema is False:
        errs.append(f"{path}: schema forbids any value here")
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
        prog="validate-freelancer-rate-raise-letter-template.py",
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
