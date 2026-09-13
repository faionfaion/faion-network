#!/usr/bin/env python3
"""validate-graceful-offboard-script.py

Validate the offboard artefact produced by the graceful-offboard-script methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/graceful-offboard-script.json', 'title': 'Agency-side client offboard artefact', 'type': 'object', 'required': ['client', 'qbr_source', 'bad_fit_signals', 'contract', 'script', 'handover', 'alternatives', 'delivery', 'feedback_request', 'internal_record'], 'additionalProperties': False, 'properties': {'client': {'type': 'object', 'required': ['name', 'account_owner', 'sponsor_contact'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'account_owner': {'type': 'string', 'minLength': 3}, 'sponsor_contact': {'type': 'string', 'pattern': '^[^@\\s]+@[^@\\s]+$'}}}, 'qbr_source': {'type': 'string', 'minLength': 5}, 'bad_fit_signals': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['kind', 'value', 'target', 'period'], 'properties': {'kind': {'type': 'string', 'enum': ['gross_margin_below_target', 'out_of_scope_requests_above_cap', 'days_to_pay_above_terms', 'hours_over_budget', 'satisfaction_below_threshold']}, 'value': {'type': 'number'}, 'target': {'type': 'number'}, 'period': {'type': 'string', 'minLength': 4}, 'consecutive_quarters': {'type': 'integer', 'minimum': 1}}, 'if': {'properties': {'kind': {'const': 'gross_margin_below_target'}}}, 'then': {'required': ['consecutive_quarters'], 'properties': {'consecutive_quarters': {'minimum': 2}}}}}, 'contract': {'type': 'object', 'required': ['termination_clause_id', 'notice_days', 'decision_date', 'last_service_date', 'days_notice_given', 'prepaid_period'], 'properties': {'termination_clause_id': {'type': 'string', 'minLength': 2}, 'notice_days': {'type': 'integer', 'minimum': 0}, 'minimum_term_end': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'decision_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'last_service_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days_notice_given': {'type': 'integer', 'minimum': 0}, 'prepaid_period': {'type': 'object', 'required': ['exists', 'disposition'], 'properties': {'exists': {'type': 'boolean'}, 'disposition': {'type': 'string', 'enum': ['delivered_in_full', 'refunded', 'not_applicable']}, 'amount': {'type': 'number', 'minimum': 0}}, 'if': {'properties': {'exists': {'const': True}}}, 'then': {'properties': {'disposition': {'enum': ['delivered_in_full', 'refunded']}}}}}}, 'script': {'type': 'object', 'required': ['framing', 'fit_statement', 'states_last_service_date', 'banned_phrases_found', 'client_criticism_found'], 'properties': {'framing': {'const': 'fit_and_alignment'}, 'fit_statement': {'type': 'string', 'minLength': 30}, 'states_last_service_date': {'const': True}, 'banned_phrases_found': {'type': 'array', 'maxItems': 0, 'items': {'type': 'string'}}, 'client_criticism_found': {'const': False}}}, 'handover': {'type': 'object', 'required': ['assets', 'transition_support'], 'properties': {'assets': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'kind', 'owned_by', 'transfer_method', 'transfer_date', 'conditioned_on_payment'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['account_credentials', 'domain_dns', 'ad_account', 'analytics_account', 'source_repository', 'design_files', 'content', 'documentation', 'other']}, 'owned_by': {'type': 'string', 'enum': ['client', 'agency']}, 'transfer_method': {'type': 'string', 'minLength': 3}, 'transfer_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'conditioned_on_payment': {'type': 'boolean'}, 'conditioning_clause_id': {'type': 'string', 'minLength': 2}}, 'if': {'properties': {'conditioned_on_payment': {'const': True}}}, 'then': {'required': ['conditioning_clause_id']}}}, 'transition_support': {'type': 'object', 'required': ['days', 'cost'], 'properties': {'days': {'type': 'integer', 'minimum': 1}, 'cost': {'type': 'string', 'enum': ['included', 'at_named_rate']}, 'rate': {'type': 'string', 'minLength': 3}}, 'if': {'properties': {'cost': {'const': 'at_named_rate'}}}, 'then': {'required': ['rate']}}}}, 'alternatives': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['provider', 'matched_need', 'confirmed_on', 'confirmed_via', 'warm_introduction_offered'], 'properties': {'provider': {'type': 'string', 'minLength': 2}, 'matched_need': {'type': 'string', 'minLength': 10}, 'confirmed_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'confirmed_via': {'type': 'string', 'enum': ['call', 'email', 'meeting', 'message']}, 'warm_introduction_offered': {'const': True}}}}, 'delivery': {'type': 'object', 'required': ['live_conversation', 'written_follow_up', 'email_only'], 'properties': {'live_conversation': {'type': 'object', 'required': ['date', 'channel', 'delivered_by'], 'properties': {'date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'channel': {'type': 'string', 'enum': ['call', 'video_call', 'in_person_meeting']}, 'delivered_by': {'type': 'string', 'minLength': 3}}}, 'written_follow_up': {'type': 'object', 'required': ['date', 'business_days_after_conversation', 'contains_only_what_was_said', 'includes_handover_plan'], 'properties': {'date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'business_days_after_conversation': {'type': 'integer', 'minimum': 0, 'maximum': 1}, 'contains_only_what_was_said': {'const': True}, 'includes_handover_plan': {'const': True}}}, 'email_only': {'const': False}}}, 'feedback_request': {'type': 'object', 'required': ['scheduled_date', 'days_after_last_service', 'promoter_action', 'non_promoter_action'], 'properties': {'scheduled_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days_after_last_service': {'const': 30}, 'promoter_action': {'type': 'string', 'enum': ['ask_for_testimonial', 'ask_for_referral', 'ask_for_testimonial_and_referral']}, 'non_promoter_action': {'const': 'thank_and_ask_one_question_no_argument'}, 'response': {'type': 'object', 'required': ['nps_score', 'action_taken'], 'properties': {'nps_score': {'type': 'integer', 'minimum': 0, 'maximum': 10}, 'action_taken': {'type': 'string', 'minLength': 5}}}}}, 'internal_record': {'type': 'object', 'required': ['root_cause_category', 'intake_change', 'flagged_for_review'], 'properties': {'root_cause_category': {'type': 'string', 'enum': ['pricing_and_margin', 'scope_and_expectations', 'capability_fit', 'communication_and_working_style', 'payment_behaviour']}, 'intake_change': {'type': 'string', 'minLength': 3}, 'flagged_for_review': {'type': 'boolean'}, 'reviewer': {'type': 'string', 'minLength': 3}}, 'if': {'properties': {'intake_change': {'enum': ['none', 'None', 'NONE', 'n/a', 'N/A', '-']}}}, 'then': {'properties': {'flagged_for_review': {'const': True}}, 'required': ['reviewer']}}}}

OK = {'client': {'name': 'Northwind Retail', 'account_owner': 'maria@agency.example', 'sponsor_contact': 'tom@northwind.example'}, 'qbr_source': 'qbr/2026-q2/northwind.xlsx', 'bad_fit_signals': [{'kind': 'gross_margin_below_target', 'value': 11, 'target': 30, 'period': '2025-Q4 to 2026-Q2', 'consecutive_quarters': 3}, {'kind': 'out_of_scope_requests_above_cap', 'value': 14, 'target': 4, 'period': '2026-Q2'}], 'contract': {'termination_clause_id': 'MSA 14.2', 'notice_days': 30, 'decision_date': '2026-06-05', 'last_service_date': '2026-07-10', 'days_notice_given': 35, 'prepaid_period': {'exists': True, 'disposition': 'delivered_in_full', 'amount': 3200}}, 'script': {'framing': 'fit_and_alignment', 'fit_statement': 'Your roadmap has moved toward in-store systems integration; we are built for e-commerce growth work, and you will get more from a partner whose core is integration.', 'states_last_service_date': True, 'banned_phrases_found': [], 'client_criticism_found': False}, 'handover': {'assets': [{'name': 'Google Ads account 123-456-7890', 'kind': 'ad_account', 'owned_by': 'client', 'transfer_method': 'admin access transferred to tom@northwind.example, agency access removed', 'transfer_date': '2026-07-03', 'conditioned_on_payment': False}, {'name': 'northwind.example DNS at Cloudflare', 'kind': 'domain_dns', 'owned_by': 'client', 'transfer_method': "zone ownership moved to client's Cloudflare account", 'transfer_date': '2026-07-06', 'conditioned_on_payment': False}, {'name': 'GA4 property 987654321', 'kind': 'analytics_account', 'owned_by': 'client', 'transfer_method': 'client made Administrator, agency demoted then removed', 'transfer_date': '2026-07-03', 'conditioned_on_payment': False}, {'name': 'github.com/agency/northwind-storefront', 'kind': 'source_repository', 'owned_by': 'client', 'transfer_method': 'repository transferred to client GitHub org', 'transfer_date': '2026-07-08', 'conditioned_on_payment': False}, {'name': 'Figma: Northwind design system', 'kind': 'design_files', 'owned_by': 'client', 'transfer_method': 'file ownership transferred to client Figma team', 'transfer_date': '2026-07-08', 'conditioned_on_payment': False}, {'name': 'Runbooks and campaign documentation', 'kind': 'documentation', 'owned_by': 'client', 'transfer_method': 'exported to client Google Drive folder', 'transfer_date': '2026-07-09', 'conditioned_on_payment': False}], 'transition_support': {'days': 30, 'cost': 'included'}}, 'alternatives': [{'provider': 'Bridgeport Systems', 'matched_need': "ERP and POS integration for mid-size retail, the direction Northwind's roadmap is taking", 'confirmed_on': '2026-06-02', 'confirmed_via': 'call', 'warm_introduction_offered': True}], 'delivery': {'live_conversation': {'date': '2026-06-05', 'channel': 'video_call', 'delivered_by': 'maria@agency.example'}, 'written_follow_up': {'date': '2026-06-05', 'business_days_after_conversation': 0, 'contains_only_what_was_said': True, 'includes_handover_plan': True}, 'email_only': False}, 'feedback_request': {'scheduled_date': '2026-08-09', 'days_after_last_service': 30, 'promoter_action': 'ask_for_testimonial_and_referral', 'non_promoter_action': 'thank_and_ask_one_question_no_argument'}, 'internal_record': {'root_cause_category': 'scope_and_expectations', 'intake_change': 'Qualification call now asks for a scope-change budget and a named change-approver; retainers without both are not signed', 'flagged_for_review': False}}

BAD = {'client': {'name': 'Northwind Retail', 'account_owner': 'maria@agency.example', 'sponsor_contact': 'tom@northwind.example'}, 'qbr_source': 'qbr/2026-q2/northwind.xlsx', 'bad_fit_signals': [{'kind': 'gross_margin_below_target', 'value': 11, 'target': 30, 'period': '2026-Q2', 'consecutive_quarters': 1}], 'contract': {'termination_clause_id': 'MSA 14.2', 'notice_days': 30, 'decision_date': '2026-06-05', 'last_service_date': '2026-06-19', 'days_notice_given': 14, 'prepaid_period': {'exists': True, 'disposition': 'not_applicable'}}, 'script': {'framing': 'apology', 'fit_statement': 'We have not been able to give you the service you deserve and your team has been hard to work with.', 'states_last_service_date': False, 'banned_phrases_found': ['we have not been able to', 'your team has been'], 'client_criticism_found': True}, 'handover': {'assets': [{'name': 'Google Ads account 123-456-7890', 'kind': 'ad_account', 'owned_by': 'client', 'transfer_method': 'on request after final invoice is paid', 'transfer_date': '2026-06-19', 'conditioned_on_payment': True}], 'transition_support': {'days': 0, 'cost': 'at_named_rate'}}, 'alternatives': [], 'delivery': {'live_conversation': {'date': '2026-06-05', 'channel': 'video_call', 'delivered_by': 'maria@agency.example'}, 'written_follow_up': {'date': '2026-06-12', 'business_days_after_conversation': 5, 'contains_only_what_was_said': False, 'includes_handover_plan': False}, 'email_only': True}, 'feedback_request': {'scheduled_date': '2026-06-19', 'days_after_last_service': 0, 'promoter_action': 'ask_for_referral', 'non_promoter_action': 'explain_why_they_are_wrong'}, 'internal_record': {'root_cause_category': 'capability_fit', 'intake_change': 'none', 'flagged_for_review': False}}


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
        prog="validate-graceful-offboard-script.py",
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
