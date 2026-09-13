#!/usr/bin/env python3
"""validate-quit-day-job-trigger-contract.py

Validate the quit-day-job contract produced by the quit-day-job-trigger-contract methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/quit-day-job-trigger-contract.json', 'title': 'Quit day job trigger contract', 'type': 'object', 'required': ['header', 'trigger', 'runway_co_condition', 'gates', 'reversal', 'conclusion', 'review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'semver': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+\\.[0-9]+$'}, 'share': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'money': {'type': 'number', 'exclusiveMinimum': 0}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'header': {'type': 'object', 'required': ['version', 'committed_on', 'post_hoc', 'change_log'], 'additionalProperties': False, 'properties': {'version': {'$ref': '#/definitions/semver'}, 'committed_on': {'$ref': '#/definitions/date'}, 'post_hoc': {'type': 'boolean'}, 'change_log': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['version', 'date', 'reason'], 'additionalProperties': False, 'properties': {'version': {'$ref': '#/definitions/semver'}, 'date': {'$ref': '#/definitions/date'}, 'reason': {'type': 'string', 'minLength': 5}}}}}}, 'trigger': {'type': 'object', 'required': ['metric', 'provider', 'report_name', 'currency', 'threshold', 'consecutive_month_ends'], 'additionalProperties': False, 'properties': {'metric': {'const': 'net_mrr'}, 'provider': {'type': 'string', 'enum': ['stripe_billing', 'baremetrics', 'chartmogul', 'profitwell', 'other_named_provider']}, 'report_name': {'type': 'string', 'minLength': 3}, 'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}, 'threshold': {'$ref': '#/definitions/money'}, 'consecutive_month_ends': {'type': 'integer', 'minimum': 3}}}, 'runway_co_condition': {'type': 'object', 'required': ['min_months', 'savings', 'monthly_burn', 'burn_includes', 'computed_on', 'months'], 'additionalProperties': False, 'properties': {'min_months': {'type': 'number', 'exclusiveMinimum': 0}, 'savings': {'type': 'number', 'minimum': 0}, 'monthly_burn': {'$ref': '#/definitions/money'}, 'burn_includes': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['self_employment_tax', 'health_insurance', 'business_costs', 'living_costs']}, 'allOf': [{'contains': {'const': 'self_employment_tax'}}, {'contains': {'const': 'health_insurance'}}, {'contains': {'const': 'business_costs'}}]}, 'computed_on': {'$ref': '#/definitions/date'}, 'months': {'type': 'number', 'minimum': 0}}}, 'gates': {'type': 'object', 'required': ['max_single_customer_share', 'max_gross_mrr_churn_monthly'], 'additionalProperties': False, 'properties': {'max_single_customer_share': {'type': 'number', 'exclusiveMinimum': 0, 'maximum': 1}, 'max_gross_mrr_churn_monthly': {'type': 'number', 'exclusiveMinimum': 0, 'maximum': 1}}}, 'reversal': {'type': 'object', 'required': ['mrr_below', 'consecutive_month_ends', 'runway_below_months'], 'additionalProperties': False, 'properties': {'mrr_below': {'$ref': '#/definitions/money'}, 'consecutive_month_ends': {'type': 'integer', 'minimum': 2}, 'runway_below_months': {'type': 'number', 'exclusiveMinimum': 0}}}, 'conclusion': {'type': 'object', 'required': ['statement', 'action', 'date_rule', 'notice_period_days', 'inform_order', 'evidence_links'], 'additionalProperties': False, 'properties': {'statement': {'type': 'string', 'minLength': 40, 'not': {'pattern': '(?i)when ready|when it feels right|when needed'}}, 'action': {'type': 'string', 'enum': ['resign', 'reduce_to_part_time']}, 'date_rule': {'type': 'string', 'minLength': 20}, 'notice_period_days': {'type': 'integer', 'minimum': 0}, 'inform_order': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 3}}, 'evidence_links': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['url', 'kind', 'covers_month_end'], 'additionalProperties': False, 'properties': {'url': {'type': 'string', 'pattern': '^(https?://|repo:|file:)'}, 'kind': {'type': 'string', 'enum': ['provider_mrr_report', 'provider_export', 'runway_model']}, 'covers_month_end': {'$ref': '#/definitions/date'}}}}}}, 'review': {'type': 'object', 'required': ['cadence', 'last_run_at', 'entries'], 'additionalProperties': False, 'properties': {'cadence': {'type': 'string', 'enum': ['monthly', 'quarterly']}, 'last_run_at': {'$ref': '#/definitions/date'}, 'entries': {'type': 'array', 'items': {'type': 'object', 'required': ['run_at', 'readings', 'runway_months', 'top_customer_share', 'gross_churn_monthly', 'verdict'], 'additionalProperties': False, 'properties': {'run_at': {'$ref': '#/definitions/date'}, 'readings': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['month_end', 'net_mrr'], 'additionalProperties': False, 'properties': {'month_end': {'$ref': '#/definitions/date'}, 'net_mrr': {'type': 'number', 'minimum': 0}}}}, 'runway_months': {'type': 'number', 'minimum': 0}, 'top_customer_share': {'$ref': '#/definitions/share'}, 'gross_churn_monthly': {'$ref': '#/definitions/share'}, 'verdict': {'type': 'string', 'enum': ['not_fired', 'window_in_progress', 'fired', 'reversal_triggered']}, 'window_count': {'type': 'integer', 'minimum': 1}}, 'if': {'properties': {'verdict': {'const': 'window_in_progress'}}}, 'then': {'required': ['window_count']}}}}}}}

OK = {'header': {'version': '1.0.0', 'committed_on': '2026-02-01', 'post_hoc': False, 'change_log': [{'version': '1.0.0', 'date': '2026-02-01', 'reason': 'initial contract, committed before any qualifying month-end'}]}, 'trigger': {'metric': 'net_mrr', 'provider': 'stripe_billing', 'report_name': 'Stripe Billing MRR report', 'currency': 'USD', 'threshold': 4000, 'consecutive_month_ends': 3}, 'runway_co_condition': {'min_months': 12, 'savings': 40600, 'monthly_burn': 3100, 'burn_includes': ['living_costs', 'self_employment_tax', 'health_insurance', 'business_costs'], 'computed_on': '2026-08-31', 'months': 13.1}, 'gates': {'max_single_customer_share': 0.2, 'max_gross_mrr_churn_monthly': 0.05}, 'reversal': {'mrr_below': 3000, 'consecutive_month_ends': 2, 'runway_below_months': 6}, 'conclusion': {'statement': 'Resign effective the first of the month after the third consecutive month-end at or above 4,000 USD net MRR with runway at or above 12 months and both gates inside their limits; give 30 days notice; tell my partner first, then my manager, then customers.', 'action': 'resign', 'date_rule': 'effective the first of the month after the third qualifying month-end', 'notice_period_days': 30, 'inform_order': ['partner', 'manager', 'customers'], 'evidence_links': [{'url': 'https://dashboard.stripe.com/billing/reports/mrr', 'kind': 'provider_mrr_report', 'covers_month_end': '2026-08-31'}, {'url': 'repo:finance/runway-model-2026-Q3.xlsx', 'kind': 'runway_model', 'covers_month_end': '2026-08-31'}]}, 'review': {'cadence': 'quarterly', 'last_run_at': '2026-09-01', 'entries': [{'run_at': '2026-06-01', 'readings': [{'month_end': '2026-03-31', 'net_mrr': 3480}, {'month_end': '2026-04-30', 'net_mrr': 3720}, {'month_end': '2026-05-31', 'net_mrr': 3910}], 'runway_months': 12.4, 'top_customer_share': 0.12, 'gross_churn_monthly': 0.031, 'verdict': 'not_fired'}, {'run_at': '2026-09-01', 'readings': [{'month_end': '2026-06-30', 'net_mrr': 4150}, {'month_end': '2026-07-31', 'net_mrr': 4300}, {'month_end': '2026-08-31', 'net_mrr': 4420}], 'runway_months': 13.1, 'top_customer_share': 0.11, 'gross_churn_monthly': 0.028, 'verdict': 'fired'}]}}

BAD = {'header': {'version': '1.0.0', 'committed_on': '2026-07-03', 'post_hoc': False, 'change_log': [{'version': '1.0.0', 'date': '2026-07-03', 'reason': 'wrote it up after the big month'}]}, 'trigger': {'metric': 'gross_cash', 'provider': 'spreadsheet', 'report_name': 'my sheet', 'currency': 'USD', 'threshold': 4000, 'consecutive_month_ends': 1}, 'runway_co_condition': {'min_months': 12, 'savings': 18000, 'monthly_burn': 1500, 'burn_includes': ['living_costs'], 'computed_on': '2026-07-03', 'months': 12}, 'gates': {'max_single_customer_share': 1, 'max_gross_mrr_churn_monthly': 1}, 'reversal': {'mrr_below': 4000, 'consecutive_month_ends': 1, 'runway_below_months': 0}, 'conclusion': {'statement': 'Quit when ready.', 'action': 'resign', 'date_rule': 'soon', 'notice_period_days': 0, 'inform_order': [], 'evidence_links': [{'url': 'screenshot.png', 'kind': 'spreadsheet_screenshot', 'covers_month_end': '2026-06-30'}]}, 'review': {'cadence': 'quarterly', 'last_run_at': '2026-09-01', 'entries': [{'run_at': '2026-09-01', 'readings': [], 'runway_months': 12, 'top_customer_share': 0.71, 'gross_churn_monthly': 0.09, 'verdict': 'fired'}]}}


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
    tr = obj.get("trigger") or {}
    thr, n = tr.get("threshold"), tr.get("consecutive_month_ends")
    rw = obj.get("runway_co_condition") or {}
    sv, burn, months = rw.get("savings"), rw.get("monthly_burn"), rw.get("months")
    if _num(sv) and _num(burn) and burn > 0 and _num(months) and abs(months - sv / burn) > 0.051:
        errs.append(f"runway_co_condition.months {months} is not savings / monthly_burn = {sv / burn:.1f} (r-runway-co-condition)")
    rv = obj.get("reversal") or {}
    if _num(thr) and _num(rv.get("mrr_below")) and rv["mrr_below"] >= thr:
        errs.append(f"reversal.mrr_below {rv['mrr_below']} is not strictly below trigger.threshold {thr}; trigger and reversal would flip-flop (r-reversal-hysteresis)")
    review = obj.get("review") or {}
    entries = [e for e in review.get("entries") or [] if isinstance(e, dict)]
    runs = [d for d in (_d(e.get("run_at")) for e in entries) if d]
    lra = _d(review.get("last_run_at"))
    if runs and lra and lra != max(runs):
        errs.append(f"review.last_run_at {lra} is not the latest review entry {max(runs)} (r-quarterly-review-records-readings)")
    readings = sorted(((r.get("month_end"), r.get("net_mrr")) for e in entries for r in e.get("readings") or [] if isinstance(r, dict) and _d(r.get("month_end")) and _num(r.get("net_mrr"))), key=lambda x: x[0])
    for me, _ in readings:
        d = _d(me)
        nxt = (d.replace(day=28) + __import__("datetime").timedelta(days=4)).replace(day=1)
        if (nxt - __import__("datetime").timedelta(days=1)) != d:
            errs.append(f"reading {me} is not a month-end date (r-consecutive-months-window)")
    hdr = obj.get("header") or {}
    co = _d(hdr.get("committed_on"))
    first_q = next((_d(me) for me, v in readings if _num(thr) and v >= thr), None)
    if co and first_q and co > first_q and hdr.get("post_hoc") is not True:
        errs.append(f"header.committed_on {co} is after the first qualifying month-end {first_q}; the contract must be labelled post_hoc (r-precommit-before-threshold)")
    gates = obj.get("gates") or {}
    for e in entries:
        rs = [r for r in e.get("readings") or [] if isinstance(r, dict) and _num(r.get("net_mrr"))]
        count = 0
        for r in reversed(rs):
            if _num(thr) and r["net_mrr"] >= thr:
                count += 1
            else:
                break
        v = e.get("verdict")
        gate_ok = (_num(gates.get("max_single_customer_share")) and _num(e.get("top_customer_share")) and e["top_customer_share"] <= gates["max_single_customer_share"]
                   and _num(gates.get("max_gross_mrr_churn_monthly")) and _num(e.get("gross_churn_monthly")) and e["gross_churn_monthly"] <= gates["max_gross_mrr_churn_monthly"])
        if v == "fired":
            if isinstance(n, int) and count < n:
                errs.append(f"review entry {e.get('run_at')}: verdict fired with {count} consecutive qualifying month-ends, trigger needs {n} (r-consecutive-months-window)")
            if not gate_ok:
                errs.append(f"review entry {e.get('run_at')}: verdict fired while a concentration or churn gate is exceeded (r-concentration-and-churn-gate)")
            if _num(e.get("runway_months")) and _num(rw.get("min_months")) and e["runway_months"] < rw["min_months"]:
                errs.append(f"review entry {e.get('run_at')}: verdict fired with runway {e['runway_months']} below the floor of {rw['min_months']} months (r-runway-co-condition)")
        if v == "window_in_progress" and isinstance(e.get("window_count"), int) and e["window_count"] != count:
            errs.append(f"review entry {e.get('run_at')}: window_count {e['window_count']} but the readings show {count} consecutive qualifying month-ends (r-consecutive-months-window)")
        if v == "not_fired" and isinstance(n, int) and count >= n and gate_ok and _num(e.get("runway_months")) and _num(rw.get("min_months")) and e["runway_months"] >= rw["min_months"]:
            errs.append(f"review entry {e.get('run_at')}: verdict not_fired although {count} consecutive qualifying month-ends, runway and gates all satisfy the trigger (r-quarterly-review-records-readings)")
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
        prog="validate-quit-day-job-trigger-contract.py",
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
