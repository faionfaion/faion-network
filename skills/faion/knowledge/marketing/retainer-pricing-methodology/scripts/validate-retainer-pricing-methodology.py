#!/usr/bin/env python3
"""validate-retainer-pricing-methodology.py

Validate the retainer spec produced by the retainer-pricing-methodology methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/retainer-pricing-methodology.json', 'title': 'Retainer Pricing Methodology spec', 'type': 'object', 'required': ['client_name', 'start_date', 'shape', 'pricing', 'scope', 'term', 'billing', 'hourly_phase_out', 'capacity', 'outcome_review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'hours': {'type': 'number', 'minimum': 0}, 'money': {'type': 'number', 'exclusiveMinimum': 0}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'client_name': {'type': 'string', 'minLength': 2}, 'start_date': {'$ref': '#/definitions/date'}, 'shape': {'type': 'object', 'required': ['kind'], 'additionalProperties': False, 'properties': {'kind': {'type': 'string', 'enum': ['block_of_hours', 'outcome_based', 'availability', 'hybrid']}, 'block_of_hours': {'type': 'object', 'required': ['prepaid_hours_per_month', 'rollover', 'overage_hourly_rate'], 'additionalProperties': False, 'properties': {'prepaid_hours_per_month': {'type': 'number', 'exclusiveMinimum': 0}, 'rollover': {'type': 'string', 'enum': ['none', 'one_period', 'capped']}, 'rollover_cap_hours': {'type': 'number', 'exclusiveMinimum': 0}, 'overage_hourly_rate': {'$ref': '#/definitions/money'}}, 'if': {'properties': {'rollover': {'const': 'capped'}}}, 'then': {'required': ['rollover_cap_hours']}}, 'outcome_based': {'type': 'object', 'required': ['deliverables_per_period'], 'additionalProperties': False, 'properties': {'deliverables_per_period': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 5}}}}, 'availability': {'type': 'object', 'required': ['response_time_business_hours', 'max_monthly_load_hours'], 'additionalProperties': False, 'properties': {'response_time_business_hours': {'type': 'number', 'exclusiveMinimum': 0}, 'max_monthly_load_hours': {'type': 'number', 'exclusiveMinimum': 0}}}, 'hybrid': {'type': 'object', 'required': ['invoicing_shape', 'scope_dispute_clause'], 'additionalProperties': False, 'properties': {'invoicing_shape': {'type': 'string', 'enum': ['block_of_hours', 'outcome_based', 'availability']}, 'scope_dispute_clause': {'type': 'string', 'minLength': 20}}}}, 'allOf': [{'if': {'properties': {'kind': {'const': 'block_of_hours'}}}, 'then': {'required': ['block_of_hours']}}, {'if': {'properties': {'kind': {'const': 'outcome_based'}}}, 'then': {'required': ['outcome_based']}}, {'if': {'properties': {'kind': {'const': 'availability'}}}, 'then': {'required': ['availability']}}, {'if': {'properties': {'kind': {'const': 'hybrid'}}}, 'then': {'required': ['hybrid']}}]}, 'pricing': {'type': 'object', 'required': ['expected_monthly_hours', 'hourly_rate', 'currency', 'monthly_price', 'multiple', 'concession'], 'additionalProperties': False, 'properties': {'expected_monthly_hours': {'type': 'number', 'exclusiveMinimum': 0}, 'hourly_rate': {'$ref': '#/definitions/money'}, 'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}, 'monthly_price': {'$ref': '#/definitions/money'}, 'multiple': {'type': 'number', 'exclusiveMinimum': 0}, 'concession': {'anyOf': [{'type': 'null'}, {'type': 'string', 'enum': ['twelve_month_minimum_term', 'full_term_prepaid']}]}}, 'if': {'properties': {'multiple': {'exclusiveMaximum': 1.3}}}, 'then': {'properties': {'concession': {'type': 'string'}}}}, 'scope': {'type': 'object', 'required': ['inclusions', 'exclusions', 'turnaround', 'included_meetings_per_month'], 'additionalProperties': False, 'properties': {'inclusions': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 5}}, 'exclusions': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 5}}, 'turnaround': {'type': 'object', 'required': ['value', 'unit'], 'additionalProperties': False, 'properties': {'value': {'type': 'number', 'exclusiveMinimum': 0}, 'unit': {'type': 'string', 'enum': ['business_hours', 'business_days']}}}, 'included_meetings_per_month': {'type': 'integer', 'minimum': 0}}}, 'term': {'type': 'object', 'required': ['minimum_months', 'notice_days', 'price_review_date'], 'additionalProperties': False, 'properties': {'minimum_months': {'type': 'integer', 'minimum': 3}, 'notice_days': {'type': 'integer', 'minimum': 30}, 'price_review_date': {'$ref': '#/definitions/date'}}}, 'billing': {'type': 'object', 'required': ['timing', 'invoice_days_before_period_start', 'payment_due', 'payment_terms_days'], 'additionalProperties': False, 'properties': {'timing': {'const': 'in_advance'}, 'invoice_days_before_period_start': {'type': 'integer', 'minimum': 0}, 'payment_due': {'const': 'before_period_start'}, 'payment_terms_days': {'type': 'integer', 'minimum': 0}}}, 'hourly_phase_out': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['avg_billed_hours_last_3_months', 'avg_monthly_spend_last_3_months', 'cutover_date', 'parallel_billing_periods'], 'additionalProperties': False, 'properties': {'avg_billed_hours_last_3_months': {'$ref': '#/definitions/hours'}, 'avg_monthly_spend_last_3_months': {'$ref': '#/definitions/money'}, 'cutover_date': {'$ref': '#/definitions/date'}, 'parallel_billing_periods': {'type': 'integer', 'minimum': 0, 'maximum': 1}}}]}, 'capacity': {'type': 'object', 'required': ['available_billable_hours_per_month', 'committed_hours_other_retainers', 'committed_hours_this_retainer', 'total_after_signing'], 'additionalProperties': False, 'properties': {'available_billable_hours_per_month': {'type': 'number', 'exclusiveMinimum': 0}, 'committed_hours_other_retainers': {'$ref': '#/definitions/hours'}, 'committed_hours_this_retainer': {'type': 'number', 'exclusiveMinimum': 0}, 'total_after_signing': {'type': 'number', 'exclusiveMinimum': 0}}}, 'outcome_review': {'type': 'object', 'required': ['scheduled_date', 'findings'], 'additionalProperties': False, 'properties': {'scheduled_date': {'$ref': '#/definitions/date'}, 'findings': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['held_on', 'still_active_without_renegotiation', 'periods', 'effective_hourly_rate', 'action'], 'additionalProperties': False, 'properties': {'held_on': {'$ref': '#/definitions/date'}, 'still_active_without_renegotiation': {'type': 'boolean'}, 'periods': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['period', 'paid_hours', 'actual_hours'], 'additionalProperties': False, 'properties': {'period': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}$'}, 'paid_hours': {'type': 'number', 'exclusiveMinimum': 0}, 'actual_hours': {'$ref': '#/definitions/hours'}}}}, 'effective_hourly_rate': {'$ref': '#/definitions/money'}, 'action': {'type': 'string', 'enum': ['none', 're_scope', 'rate_increase', 'address_usage']}}}]}}}}}

OK = {'client_name': 'Nordlicht GmbH', 'start_date': '2026-10-01', 'shape': {'kind': 'block_of_hours', 'block_of_hours': {'prepaid_hours_per_month': 40, 'rollover': 'one_period', 'overage_hourly_rate': 150}}, 'pricing': {'expected_monthly_hours': 40, 'hourly_rate': 120, 'currency': 'EUR', 'monthly_price': 6240, 'multiple': 1.3, 'concession': None}, 'scope': {'inclusions': ['maintenance of the Django order service and its CI', 'dependency and security updates', 'bug fixes on existing features', 'monthly performance and cost report'], 'exclusions': ['new feature builds beyond 4 hours of effort', 'emergency weekend work', 'third-party licence and hosting costs', 'meetings beyond the included count'], 'turnaround': {'value': 2, 'unit': 'business_days'}, 'included_meetings_per_month': 2}, 'term': {'minimum_months': 6, 'notice_days': 30, 'price_review_date': '2027-09-01'}, 'billing': {'timing': 'in_advance', 'invoice_days_before_period_start': 7, 'payment_due': 'before_period_start', 'payment_terms_days': 7}, 'hourly_phase_out': {'avg_billed_hours_last_3_months': 38, 'avg_monthly_spend_last_3_months': 4560, 'cutover_date': '2026-10-01', 'parallel_billing_periods': 0}, 'capacity': {'available_billable_hours_per_month': 120, 'committed_hours_other_retainers': 60, 'committed_hours_this_retainer': 40, 'total_after_signing': 100}, 'outcome_review': {'scheduled_date': '2027-04-01', 'findings': None}}

BAD = {'client_name': 'Nordlicht GmbH', 'start_date': '2026-10-01', 'shape': {'kind': 'availability'}, 'pricing': {'expected_monthly_hours': 40, 'hourly_rate': 120, 'currency': 'EUR', 'monthly_price': 4560, 'multiple': 0.95, 'concession': None}, 'scope': {'inclusions': ['whatever comes up'], 'exclusions': [], 'turnaround': {'value': 0, 'unit': 'asap'}, 'included_meetings_per_month': 0}, 'term': {'minimum_months': 1, 'notice_days': 0, 'price_review_date': '2029-10-01'}, 'billing': {'timing': 'in_arrears', 'invoice_days_before_period_start': 0, 'payment_due': 'net_60_after_period', 'payment_terms_days': 60}, 'hourly_phase_out': {'avg_billed_hours_last_3_months': 38, 'avg_monthly_spend_last_3_months': 4560, 'cutover_date': '2026-06-01', 'parallel_billing_periods': 3}, 'capacity': {'available_billable_hours_per_month': 120, 'committed_hours_other_retainers': 100, 'committed_hours_this_retainer': 40, 'total_after_signing': 120}, 'outcome_review': {'scheduled_date': '2028-01-01', 'findings': None}}


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


def _add_months(d: _date, n: int) -> _date:
    y, m = divmod(d.month - 1 + n, 12)
    return _date(d.year + y, m + 1, min(d.day, 28))


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    start = _d(obj.get("start_date"))
    pr = obj.get("pricing") or {}
    h, r, p, mult = pr.get("expected_monthly_hours"), pr.get("hourly_rate"), pr.get("monthly_price"), pr.get("multiple")
    if all(_num(x) for x in (h, r, p, mult)) and h * r > 0 and abs(mult - p / (h * r)) > 0.0051:
        errs.append(f"pricing.multiple {mult} is not monthly_price / (expected_monthly_hours x hourly_rate) = {p / (h * r):.2f} (r-rate-floor-1-3x-hourly-equivalent)")
    sh = obj.get("shape") or {}
    if sh.get("kind") == "availability":
        ml = (sh.get("availability") or {}).get("max_monthly_load_hours")
        if _num(ml) and _num(h) and abs(h - ml) > 0.0051:
            errs.append(f"pricing.expected_monthly_hours {h} must equal availability.max_monthly_load_hours {ml} for an availability retainer (r-rate-floor-1-3x-hourly-equivalent)")
    if sh.get("kind") == "block_of_hours":
        ph = (sh.get("block_of_hours") or {}).get("prepaid_hours_per_month")
        if _num(ph) and _num(h) and abs(h - ph) > 0.0051:
            errs.append(f"pricing.expected_monthly_hours {h} must equal block_of_hours.prepaid_hours_per_month {ph} (r-retainer-shape-named)")
    term = obj.get("term") or {}
    prd = _d(term.get("price_review_date"))
    if start and prd and prd > _add_months(start, 12):
        errs.append(f"term.price_review_date {prd} is more than 12 months after start_date {start} (r-term-notice-and-price-review)")
    po = obj.get("hourly_phase_out")
    if isinstance(po, dict):
        spend = po.get("avg_monthly_spend_last_3_months")
        if _num(spend) and _num(p) and pr.get("concession") is None and p < 1.3 * spend - 0.005:
            errs.append(f"monthly_price {p} is below 1.3 x the client's 3-month average spend {spend} = {1.3 * spend:.2f} with no concession (r-hourly-phase-out-plan)")
        cut = _d(po.get("cutover_date"))
        if start and cut and cut < start:
            errs.append(f"hourly_phase_out.cutover_date {cut} precedes start_date {start} (r-hourly-phase-out-plan)")
    cap = obj.get("capacity") or {}
    av, oth, this, tot = cap.get("available_billable_hours_per_month"), cap.get("committed_hours_other_retainers"), cap.get("committed_hours_this_retainer"), cap.get("total_after_signing")
    if all(_num(x) for x in (oth, this, tot)) and abs(tot - (oth + this)) > 0.0051:
        errs.append(f"capacity.total_after_signing {tot} is not other {oth} + this {this} = {oth + this} (r-capacity-not-oversold)")
    if _num(av) and _num(oth) and _num(this) and oth + this > av + 0.0051:
        errs.append(f"capacity: {oth} + {this} = {oth + this} committed hours exceed {av} available; do not sign (r-capacity-not-oversold)")
    if _num(this) and _num(h) and abs(this - h) > 0.0051:
        errs.append(f"capacity.committed_hours_this_retainer {this} must equal pricing.expected_monthly_hours {h} (r-capacity-not-oversold)")
    orv = obj.get("outcome_review") or {}
    sd = _d(orv.get("scheduled_date"))
    if start and sd and abs((sd - _add_months(start, 6)).days) > 7:
        errs.append(f"outcome_review.scheduled_date {sd} is not 6 months after start_date {start} (r-six-month-outcome-review)")
    f = orv.get("findings")
    if isinstance(f, dict):
        periods = [x for x in f.get("periods") or [] if isinstance(x, dict)]
        last2 = periods[-2:]
        if len(last2) == 2 and all(_num(x.get("paid_hours")) and _num(x.get("actual_hours")) for x in last2):
            over = all(x["actual_hours"] > x["paid_hours"] for x in last2)
            under = all(x["actual_hours"] < 0.5 * x["paid_hours"] for x in last2)
            if over and f.get("action") not in ("re_scope", "rate_increase"):
                errs.append("outcome_review.findings: actual hours exceeded paid hours in 2 consecutive periods; action must be re_scope or rate_increase (r-six-month-outcome-review)")
            if under and f.get("action") != "address_usage":
                errs.append("outcome_review.findings: actual hours below 50 percent of paid hours in 2 consecutive periods; action must be address_usage (r-six-month-outcome-review)")
        actual = [x.get("actual_hours") for x in periods if _num(x.get("actual_hours"))]
        if actual and sum(actual) > 0 and _num(p) and _num(f.get("effective_hourly_rate")):
            want = p * len(actual) / sum(actual)
            if abs(f["effective_hourly_rate"] - want) > max(0.5, 0.01 * want):
                errs.append(f"outcome_review.findings.effective_hourly_rate {f['effective_hourly_rate']} is not monthly_price / mean actual hours = {want:.2f} (r-six-month-outcome-review)")
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
        prog="validate-retainer-pricing-methodology.py",
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
