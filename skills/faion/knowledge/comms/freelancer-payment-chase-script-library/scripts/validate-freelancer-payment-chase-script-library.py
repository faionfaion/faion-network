#!/usr/bin/env python3
"""validate-freelancer-payment-chase-script-library.py

Validate the chase ladder produced by the freelancer-payment-chase-script-library methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/freelancer-payment-chase-script-library.json', 'title': 'Payment chase ladder for one invoice', 'type': 'object', 'required': ['invoice', 'parties', 'contract', 'rungs', 'status', 'send_log', 'renewal_terms_change'], 'additionalProperties': False, 'properties': {'invoice': {'type': 'object', 'required': ['invoice_id', 'amount', 'currency', 'invoice_date', 'due_date', 'payment_terms_clause_id', 'invoice_link'], 'properties': {'invoice_id': {'type': 'string', 'minLength': 1}, 'amount': {'type': 'number', 'exclusiveMinimum': 0}, 'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}, 'invoice_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'due_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'payment_terms_clause_id': {'type': 'string', 'minLength': 1}, 'invoice_link': {'type': 'string', 'minLength': 1}}}, 'parties': {'type': 'object', 'required': ['freelancer', 'client'], 'properties': {'freelancer': {'type': 'object', 'required': ['legal_name', 'address'], 'properties': {'legal_name': {'type': 'string', 'minLength': 3}, 'address': {'type': 'string', 'minLength': 10}}}, 'client': {'type': 'object', 'required': ['legal_name', 'address', 'sponsor_contact', 'finance_contact'], 'properties': {'legal_name': {'type': 'string', 'minLength': 3}, 'address': {'type': 'string', 'minLength': 10}, 'sponsor_contact': {'type': 'string', 'pattern': '^[^@\\s]+@[^@\\s]+$'}, 'finance_contact': {'type': 'string', 'pattern': '^[^@\\s]+@[^@\\s]+$'}}}}}, 'contract': {'type': 'object', 'required': ['written_notice_channel', 'late_payment_basis', 'legal_handoff_contact'], 'properties': {'written_notice_channel': {'type': 'string', 'enum': ['email', 'registered_post', 'email_and_registered_post', 'courier']}, 'late_payment_basis': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'type': 'string', 'enum': ['contract_clause', 'statute', 'none']}, 'reference': {'type': 'string', 'minLength': 5}, 'rate': {'type': 'string', 'minLength': 2}, 'fixed_fee': {'type': 'number', 'minimum': 0}}, 'if': {'properties': {'kind': {'enum': ['contract_clause', 'statute']}}}, 'then': {'required': ['reference', 'rate']}}, 'legal_handoff_contact': {'type': 'string', 'minLength': 3}}}, 'rungs': {'type': 'array', 'minItems': 3, 'maxItems': 3, 'items': {'type': 'object', 'required': ['rung', 'offset_days', 'scheduled_date', 'recipients', 'days_overdue_on_send', 'invoice_attached', 'mentions_fee_or_consequence', 'mentions_legal_action'], 'properties': {'rung': {'type': 'string', 'enum': ['polite', 'firm', 'legal']}, 'offset_days': {'type': 'integer', 'enum': [3, 10, 30]}, 'scheduled_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'recipients': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'pattern': '^[^@\\s]+@[^@\\s]+$'}}, 'days_overdue_on_send': {'type': 'integer', 'minimum': 3}, 'invoice_attached': {'const': True}, 'mentions_fee_or_consequence': {'type': 'boolean'}, 'mentions_legal_action': {'type': 'boolean'}, 'word_count': {'type': 'integer', 'minimum': 1}, 'asks_confirmed_payment_date': {'type': 'boolean'}, 'pay_by_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'pay_by_within_days': {'type': 'integer', 'minimum': 1, 'maximum': 7}, 'consequence_reference': {'type': 'string', 'minLength': 5}, 'ledger_total_with_interest': {'type': 'number', 'exclusiveMinimum': 0}, 'final_deadline_days': {'type': 'integer', 'minimum': 7, 'maximum': 14}, 'next_step': {'type': 'string', 'enum': ['collections_agency', 'small_claims', 'county_court_claim', 'statutory_demand']}, 'without_prejudice': {'type': 'boolean'}, 'channels': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'enum': ['email', 'registered_post', 'courier']}}}, 'allOf': [{'if': {'properties': {'rung': {'const': 'polite'}}}, 'then': {'required': ['word_count', 'asks_confirmed_payment_date'], 'properties': {'offset_days': {'const': 3}, 'word_count': {'maximum': 120}, 'asks_confirmed_payment_date': {'const': True}, 'mentions_fee_or_consequence': {'const': False}, 'mentions_legal_action': {'const': False}}}}, {'if': {'properties': {'rung': {'const': 'firm'}}}, 'then': {'required': ['pay_by_date', 'pay_by_within_days', 'consequence_reference'], 'properties': {'offset_days': {'const': 10}, 'recipients': {'minItems': 2}, 'mentions_fee_or_consequence': {'const': True}, 'mentions_legal_action': {'const': False}}}}, {'if': {'properties': {'rung': {'const': 'legal'}}}, 'then': {'required': ['ledger_total_with_interest', 'final_deadline_days', 'next_step', 'without_prejudice', 'channels'], 'properties': {'offset_days': {'const': 30}, 'without_prejudice': {'const': True}, 'mentions_legal_action': {'const': True}}}}]}}, 'status': {'type': 'object', 'required': ['payment_status', 'dispute_raised', 'outstanding_balance', 'halted'], 'properties': {'payment_status': {'type': 'string', 'enum': ['unpaid', 'partial', 'paid_in_full']}, 'dispute_raised': {'type': 'boolean'}, 'outstanding_balance': {'type': 'number', 'minimum': 0}, 'halted': {'type': 'boolean'}, 'halt_reason': {'type': 'string', 'enum': ['paid_in_full', 'dispute_raised', 'ladder_exhausted']}}, 'allOf': [{'if': {'properties': {'halted': {'const': True}}}, 'then': {'required': ['halt_reason']}}, {'if': {'properties': {'payment_status': {'const': 'paid_in_full'}}}, 'then': {'properties': {'halted': {'const': True}, 'outstanding_balance': {'const': 0}}}}, {'if': {'properties': {'dispute_raised': {'const': True}}}, 'then': {'properties': {'halted': {'const': True}}}}]}, 'send_log': {'type': 'array', 'items': {'type': 'object', 'required': ['invoice_id', 'rung', 'send_date', 'channel', 'recipients', 'response'], 'properties': {'invoice_id': {'type': 'string', 'minLength': 1}, 'rung': {'type': 'string', 'enum': ['polite', 'firm', 'legal']}, 'send_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'channel': {'type': 'string', 'enum': ['email', 'registered_post', 'courier']}, 'recipients': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}, 'response': {'oneOf': [{'const': 'none'}, {'type': 'object', 'required': ['date', 'gist'], 'properties': {'date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'gist': {'type': 'string', 'minLength': 5}}}]}}}}, 'days_to_pay': {'type': ['integer', 'null'], 'minimum': 0}, 'renewal_terms_change': {'type': 'string', 'enum': ['shorter_net_terms', 'deposit', 'milestone_billing', 'none', 'pending_renewal']}}}

OK = {'invoice': {'invoice_id': '2026-041', 'amount': 4800, 'currency': 'GBP', 'invoice_date': '2026-05-31', 'due_date': '2026-06-15', 'payment_terms_clause_id': 'MSA 7.2 (net 15)', 'invoice_link': 'https://invoices.faion.example/2026-041.pdf'}, 'parties': {'freelancer': {'legal_name': 'Ruslan Faion', 'address': '12 Example Road, Lisbon 1000-001, Portugal'}, 'client': {'legal_name': 'Acme Analytics Ltd', 'address': '1 Acme Way, London EC1A 1AA, United Kingdom', 'sponsor_contact': 'dana@acme.example', 'finance_contact': 'ap@acme.example'}}, 'contract': {'written_notice_channel': 'email_and_registered_post', 'late_payment_basis': {'kind': 'statute', 'reference': 'Late Payment of Commercial Debts (Interest) Act 1998', 'rate': '8% over Bank of England base rate plus GBP 70 fixed compensation', 'fixed_fee': 70}, 'legal_handoff_contact': 'collections@smallclaimsdesk.example'}, 'rungs': [{'rung': 'polite', 'offset_days': 3, 'scheduled_date': '2026-06-18', 'recipients': ['dana@acme.example'], 'days_overdue_on_send': 3, 'invoice_attached': True, 'mentions_fee_or_consequence': False, 'mentions_legal_action': False, 'word_count': 84, 'asks_confirmed_payment_date': True}, {'rung': 'firm', 'offset_days': 10, 'scheduled_date': '2026-06-25', 'recipients': ['dana@acme.example', 'ap@acme.example'], 'days_overdue_on_send': 10, 'invoice_attached': True, 'mentions_fee_or_consequence': True, 'mentions_legal_action': False, 'pay_by_date': '2026-07-01', 'pay_by_within_days': 6, 'consequence_reference': 'Statutory interest under the Late Payment of Commercial Debts (Interest) Act 1998 at 8% over base rate from 2026-06-16'}, {'rung': 'legal', 'offset_days': 30, 'scheduled_date': '2026-07-15', 'recipients': ['dana@acme.example', 'ap@acme.example'], 'days_overdue_on_send': 30, 'invoice_attached': True, 'mentions_fee_or_consequence': True, 'mentions_legal_action': True, 'ledger_total_with_interest': 4921.4, 'final_deadline_days': 14, 'next_step': 'county_court_claim', 'without_prejudice': True, 'channels': ['email', 'registered_post']}], 'status': {'payment_status': 'paid_in_full', 'dispute_raised': False, 'outstanding_balance': 0, 'halted': True, 'halt_reason': 'paid_in_full'}, 'send_log': [{'invoice_id': '2026-041', 'rung': 'polite', 'send_date': '2026-06-18', 'channel': 'email', 'recipients': ['dana@acme.example'], 'response': {'date': '2026-06-19', 'gist': 'Sorry, stuck in approvals; will be paid this week'}}], 'days_to_pay': 20, 'renewal_terms_change': 'deposit'}

BAD = {'invoice': {'invoice_id': '2026-041', 'amount': 4800, 'currency': 'GBP', 'invoice_date': '2026-05-31', 'due_date': '2026-06-15', 'payment_terms_clause_id': 'MSA 7.2 (net 15)', 'invoice_link': 'https://invoices.faion.example/2026-041.pdf'}, 'parties': {'freelancer': {'legal_name': 'Ruslan Faion', 'address': '12 Example Road, Lisbon 1000-001, Portugal'}, 'client': {'legal_name': 'Acme Analytics Ltd', 'address': '1 Acme Way, London EC1A 1AA, United Kingdom', 'sponsor_contact': 'dana@acme.example', 'finance_contact': 'ap@acme.example'}}, 'contract': {'written_notice_channel': 'email', 'late_payment_basis': {'kind': 'none'}, 'legal_handoff_contact': 'collections@smallclaimsdesk.example'}, 'rungs': [{'rung': 'polite', 'offset_days': 1, 'scheduled_date': '2026-06-16', 'recipients': ['dana@acme.example'], 'days_overdue_on_send': 3, 'invoice_attached': True, 'mentions_fee_or_consequence': True, 'mentions_legal_action': True, 'word_count': 240, 'asks_confirmed_payment_date': False}, {'rung': 'firm', 'offset_days': 10, 'scheduled_date': '2026-06-25', 'recipients': ['dana@acme.example'], 'days_overdue_on_send': 10, 'invoice_attached': True, 'mentions_fee_or_consequence': True, 'mentions_legal_action': False, 'pay_by_date': '2026-07-20', 'pay_by_within_days': 25, 'consequence_reference': '5% weekly late fee'}], 'status': {'payment_status': 'paid_in_full', 'dispute_raised': False, 'outstanding_balance': 4800, 'halted': False}, 'send_log': [], 'days_to_pay': None, 'renewal_terms_change': 'none'}


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
        prog="validate-freelancer-payment-chase-script-library.py",
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
