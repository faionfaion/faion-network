#!/usr/bin/env python3
"""validate-agency-risk-register-template.py

Validate the agency risk register produced by the agency-risk-register-template methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/agency-risk-register-template.json', 'title': 'Agency risk register (Monday refresh)', 'type': 'object', 'required': ['agency', 'refresh', 'concentration', 'rows', 'closed'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'score': {'type': 'integer', 'minimum': 1, 'maximum': 5}, 'share': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'person': {'type': 'string', 'minLength': 3, 'not': {'enum': ['team', 'ops', 'everyone', 'tbd', 'the team', 'management']}}, 'risk_class': {'type': 'string', 'enum': ['revenue_concentration', 'key_person', 'fx_currency', 'contractor_classification', 'pipeline_thinness', 'regulatory']}, 'currency_shares': {'type': 'object', 'minProperties': 1, 'propertyNames': {'pattern': '^[A-Z]{3}$'}, 'additionalProperties': {'$ref': '#/definitions/share'}}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'agency': {'type': 'object', 'required': ['name', 'headcount'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 2}, 'headcount': {'type': 'integer', 'minimum': 3, 'maximum': 25}}}, 'refresh': {'type': 'object', 'required': ['date', 'minutes', 'consecutive_overruns', 'split_or_prune_required', 'action_note'], 'additionalProperties': False, 'properties': {'date': {'$ref': '#/definitions/date'}, 'minutes': {'type': 'object', 'required': ['scores_update', 'top5_walk', 'action_note', 'total'], 'additionalProperties': False, 'properties': {'scores_update': {'type': 'integer', 'minimum': 0}, 'top5_walk': {'type': 'integer', 'minimum': 0}, 'action_note': {'type': 'integer', 'minimum': 0}, 'total': {'type': 'integer', 'minimum': 1}}}, 'consecutive_overruns': {'type': 'integer', 'minimum': 0}, 'split_or_prune_required': {'type': 'boolean'}, 'action_note': {'type': 'string', 'minLength': 20}}, 'if': {'properties': {'consecutive_overruns': {'minimum': 2}}}, 'then': {'properties': {'split_or_prune_required': {'const': True}}}}, 'concentration': {'type': 'object', 'required': ['source', 'trailing_days', 'recomputed_on', 'clients'], 'additionalProperties': False, 'properties': {'source': {'const': 'billing_export'}, 'trailing_days': {'const': 90}, 'recomputed_on': {'$ref': '#/definitions/date'}, 'clients': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'share'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 2}, 'share': {'$ref': '#/definitions/share'}}}}}}, 'rows': {'type': 'array', 'minItems': 6, 'allOf': [{'contains': {'properties': {'class': {'const': 'revenue_concentration'}}}}, {'contains': {'properties': {'class': {'const': 'key_person'}}}}, {'contains': {'properties': {'class': {'const': 'fx_currency'}}}}, {'contains': {'properties': {'class': {'const': 'contractor_classification'}}}}, {'contains': {'properties': {'class': {'const': 'pipeline_thinness'}}}}, {'contains': {'properties': {'class': {'const': 'regulatory'}}}}], 'items': {'type': 'object', 'required': ['id', 'class', 'description', 'likelihood', 'impact', 'score', 'owner', 'trigger', 'details', 'response'], 'additionalProperties': False, 'properties': {'id': {'type': 'string', 'pattern': '^R-[0-9]{2,}$'}, 'class': {'$ref': '#/definitions/risk_class'}, 'description': {'type': 'string', 'minLength': 15}, 'likelihood': {'$ref': '#/definitions/score'}, 'impact': {'$ref': '#/definitions/score'}, 'score': {'type': 'integer', 'minimum': 1, 'maximum': 25}, 'owner': {'$ref': '#/definitions/person'}, 'trigger': {'type': 'string', 'minLength': 25}, 'details': {'type': 'object', 'additionalProperties': False, 'properties': {'client': {'type': 'string', 'minLength': 2}, 'share': {'$ref': '#/definitions/share'}, 'item': {'type': 'string', 'minLength': 5}, 'holder': {'$ref': '#/definitions/person'}, 'remediation_owner': {'$ref': '#/definitions/person'}, 'deadline': {'$ref': '#/definitions/date'}, 'revenue_share_by_currency': {'$ref': '#/definitions/currency_shares'}, 'cost_share_by_currency': {'$ref': '#/definitions/currency_shares'}, 'contractors': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'jurisdiction', 'test', 'outcome'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'minLength': 2}, 'jurisdiction': {'type': 'string', 'minLength': 2}, 'test': {'type': 'string', 'minLength': 5}, 'outcome': {'type': 'string', 'enum': ['contractor', 'employee_risk', 'unresolved']}, 'fix_due': {'$ref': '#/definitions/date'}}, 'if': {'properties': {'outcome': {'enum': ['employee_risk', 'unresolved']}}}, 'then': {'required': ['fix_due']}}}, 'weighted_pipeline': {'type': 'number', 'minimum': 0}, 'monthly_cost_base': {'type': 'number', 'exclusiveMinimum': 0}, 'months_of_coverage': {'type': 'number', 'minimum': 0}, 'trigger_below_months': {'type': 'number', 'exclusiveMinimum': 0}, 'regulation': {'type': 'string', 'minLength': 3}}}, 'response': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['kind'], 'additionalProperties': False, 'properties': {'kind': {'type': 'string', 'enum': ['mitigation', 'acceptance']}, 'action': {'type': 'string', 'minLength': 10}, 'owner': {'$ref': '#/definitions/person'}, 'due_date': {'$ref': '#/definitions/date'}, 'signed_by': {'$ref': '#/definitions/person'}, 'signed_on': {'$ref': '#/definitions/date'}}, 'allOf': [{'if': {'properties': {'kind': {'const': 'mitigation'}}}, 'then': {'required': ['action', 'owner', 'due_date']}}, {'if': {'properties': {'kind': {'const': 'acceptance'}}}, 'then': {'required': ['signed_by', 'signed_on']}}]}]}}, 'allOf': [{'if': {'properties': {'class': {'const': 'revenue_concentration'}}}, 'then': {'properties': {'details': {'required': ['client', 'share']}}}}, {'if': {'properties': {'class': {'const': 'key_person'}}}, 'then': {'properties': {'details': {'required': ['item', 'holder', 'remediation_owner', 'deadline']}}}}, {'if': {'properties': {'class': {'const': 'fx_currency'}}}, 'then': {'properties': {'details': {'required': ['revenue_share_by_currency', 'cost_share_by_currency']}}}}, {'if': {'properties': {'class': {'const': 'contractor_classification'}}}, 'then': {'properties': {'details': {'required': ['contractors']}}}}, {'if': {'properties': {'class': {'const': 'pipeline_thinness'}}}, 'then': {'properties': {'details': {'required': ['weighted_pipeline', 'monthly_cost_base', 'months_of_coverage', 'trigger_below_months']}}}}, {'if': {'properties': {'class': {'const': 'regulatory'}}}, 'then': {'properties': {'details': {'required': ['regulation']}}}}, {'if': {'properties': {'score': {'minimum': 15}}}, 'then': {'properties': {'response': {'type': 'object'}}}}]}}, 'closed': {'type': 'array', 'items': {'type': 'object', 'required': ['id', 'class', 'description', 'closed_on', 'lesson'], 'additionalProperties': False, 'properties': {'id': {'type': 'string', 'pattern': '^R-[0-9]{2,}$'}, 'class': {'$ref': '#/definitions/risk_class'}, 'description': {'type': 'string', 'minLength': 15}, 'closed_on': {'$ref': '#/definitions/date'}, 'lesson': {'type': 'string', 'minLength': 15}}}}}}

OK = {'agency': {'name': 'Brightline Studio', 'headcount': 6}, 'refresh': {'date': '2026-09-14', 'minutes': {'scores_update': 5, 'top5_walk': 15, 'action_note': 8, 'total': 28}, 'consecutive_overruns': 0, 'split_or_prune_required': False, 'action_note': 'Client A at 47 percent: Dana sends proposals to Harbor Logistics and Vireo by Friday; AWS root hand-over to Priya scheduled for 2026-09-30; USD/EUR mismatch accepted for this quarter pending the hedging quote.'}, 'concentration': {'source': 'billing_export', 'trailing_days': 90, 'recomputed_on': '2026-09-14', 'clients': [{'name': 'Client A', 'share': 0.47}, {'name': 'Client B', 'share': 0.22}, {'name': 'Client C', 'share': 0.12}, {'name': 'others', 'share': 0.19}]}, 'rows': [{'id': 'R-01', 'class': 'revenue_concentration', 'description': 'Client A is 47 percent of trailing-90-day revenue', 'likelihood': 4, 'impact': 5, 'score': 20, 'owner': 'Dana Kovac', 'trigger': 'Client A misses two invoices in a row or cancels the weekly sync', 'details': {'client': 'Client A', 'share': 0.47}, 'response': {'kind': 'mitigation', 'action': 'send proposals to Harbor Logistics and Vireo', 'owner': 'Dana Kovac', 'due_date': '2026-09-18'}}, {'id': 'R-02', 'class': 'revenue_concentration', 'description': 'Client B is 22 percent of trailing-90-day revenue', 'likelihood': 3, 'impact': 3, 'score': 9, 'owner': 'Dana Kovac', 'trigger': 'Client B retainer not renewed 30 days before its 2026-12-31 end date', 'details': {'client': 'Client B', 'share': 0.22}, 'response': None}, {'id': 'R-03', 'class': 'key_person', 'description': 'AWS root credentials and the deploy pipeline are known only to Marko', 'likelihood': 3, 'impact': 4, 'score': 12, 'owner': 'Dana Kovac', 'trigger': 'Marko unavailable for more than 5 working days with no backup holder', 'details': {'item': 'AWS root credentials and deploy pipeline', 'holder': 'Marko Ilic', 'remediation_owner': 'Priya Nair', 'deadline': '2026-09-30'}, 'response': None}, {'id': 'R-04', 'class': 'fx_currency', 'description': '60 percent of revenue billed in USD against 90 percent of costs in EUR', 'likelihood': 4, 'impact': 3, 'score': 12, 'owner': 'Dana Kovac', 'trigger': "EUR/USD moves more than 5 percent against the quarter's opening rate", 'details': {'revenue_share_by_currency': {'USD': 0.6, 'EUR': 0.4}, 'cost_share_by_currency': {'EUR': 0.9, 'USD': 0.1}}, 'response': None}, {'id': 'R-05', 'class': 'contractor_classification', 'description': 'One cross-border contractor on a 30-hour week for a single client', 'likelihood': 2, 'impact': 4, 'score': 8, 'owner': 'Dana Kovac', 'trigger': 'Contractor exceeds 35 hours a week for 8 weeks or loses the right to substitute', 'details': {'contractors': [{'name': 'Ana Ferreira', 'jurisdiction': 'Portugal', 'test': 'control, substitution and financial risk (recibos verdes regime)', 'outcome': 'contractor'}]}, 'response': None}, {'id': 'R-06', 'class': 'pipeline_thinness', 'description': 'Stage-weighted pipeline covers 3.5 months of the cost base', 'likelihood': 3, 'impact': 4, 'score': 12, 'owner': 'Dana Kovac', 'trigger': 'Weighted coverage below 3 months at any Monday refresh', 'details': {'weighted_pipeline': 210000, 'monthly_cost_base': 60000, 'months_of_coverage': 3.5, 'trigger_below_months': 3}, 'response': None}, {'id': 'R-07', 'class': 'regulatory', 'description': 'GDPR processor agreements not yet signed with two clients', 'likelihood': 2, 'impact': 3, 'score': 6, 'owner': 'Priya Nair', 'trigger': 'A client audit request or a data incident arrives before both agreements are signed', 'details': {'regulation': 'GDPR Article 28 processor agreements'}, 'response': None}], 'closed': [{'id': 'R-00', 'class': 'key_person', 'description': 'Domain registrar account held only by the founder', 'closed_on': '2026-08-31', 'lesson': 'Shared credentials go into the password manager on day one, not after the first scare'}]}

BAD = {'agency': {'name': 'Brightline Studio', 'headcount': 6}, 'refresh': {'date': '2026-09-16', 'minutes': {'scores_update': 10, 'top5_walk': 45, 'action_note': 20, 'total': 60}, 'consecutive_overruns': 2, 'split_or_prune_required': False, 'action_note': 'Reviewed everything, nothing new.'}, 'concentration': {'source': 'founder_estimate', 'trailing_days': 365, 'recomputed_on': '2026-06-01', 'clients': [{'name': 'Client A', 'share': 0.47}]}, 'rows': [{'id': 'R-01', 'class': 'revenue_concentration', 'description': 'Client A might churn at some point', 'likelihood': 4, 'impact': 5, 'score': 18, 'owner': 'team', 'trigger': 'if things get worse', 'details': {'client': 'Client A', 'share': 0.3}, 'response': None}, {'id': 'R-02', 'class': 'key_person', 'description': 'We should cross-train on the deploy pipeline', 'likelihood': 3, 'impact': 4, 'score': 12, 'owner': 'ops', 'trigger': 'someone leaves', 'details': {'item': 'deploy pipeline', 'holder': 'Marko Ilic'}, 'response': None}, {'id': 'R-03', 'class': 'fx_currency', 'description': 'Some USD exposure on a couple of clients', 'likelihood': 3, 'impact': 3, 'score': 9, 'owner': 'Dana Kovac', 'trigger': 'the dollar moves a lot against the euro', 'details': {}, 'response': None}, {'id': 'R-04', 'class': 'pipeline_thinness', 'description': 'Pipeline feels thin for the autumn', 'likelihood': 3, 'impact': 4, 'score': 12, 'owner': 'Dana Kovac', 'trigger': 'we notice there is not enough work', 'details': {'weighted_pipeline': 120000, 'monthly_cost_base': 60000, 'months_of_coverage': 4, 'trigger_below_months': 3}, 'response': None}, {'id': 'P-17', 'class': 'project_scope_slip', 'description': 'Sprint 4 of the Client C build is two weeks late', 'likelihood': 4, 'impact': 2, 'score': 8, 'owner': 'Marko Ilic', 'trigger': 'Sprint 5 also slips by more than a week', 'details': {}, 'response': None}, {'id': 'P-18', 'class': 'project_vendor', 'description': 'Payment gateway vendor slow on the Client B integration', 'likelihood': 3, 'impact': 2, 'score': 6, 'owner': 'Marko Ilic', 'trigger': 'Vendor misses the next scheduled delivery date too', 'details': {}, 'response': None}], 'closed': []}


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
    rf = obj.get("refresh") or {}
    rd = _d(rf.get("date"))
    if rd and rd.weekday() != 0:
        errs.append(f"refresh.date {rd} is not a Monday (r-thirty-minute-monday)")
    mins = rf.get("minutes") or {}
    parts = [mins.get(k) for k in ("scores_update", "top5_walk", "action_note")]
    if all(isinstance(p, int) for p in parts) and isinstance(mins.get("total"), int):
        if mins["total"] != sum(parts):
            errs.append(f"refresh.minutes.total {mins['total']} is not scores_update + top5_walk + action_note = {sum(parts)} (r-thirty-minute-monday)")
        if mins["total"] > 30:
            errs.append(f"refresh.minutes.total {mins['total']} exceeds the 30-minute timebox; count it as an overrun (r-thirty-minute-monday)")
    conc = obj.get("concentration") or {}
    if rd and _d(conc.get("recomputed_on")) and _d(conc["recomputed_on"]) != rd:
        errs.append(f"concentration.recomputed_on {conc['recomputed_on']} is not the refresh date {rd}; recompute every Monday (r-concentration-90d-auto-score)")
    rows = [r for r in obj.get("rows") or [] if isinstance(r, dict)]
    conc_rows = {(r.get("details") or {}).get("client"): r for r in rows if r.get("class") == "revenue_concentration"}
    for c in conc.get("clients") or []:
        name, share = c.get("name"), c.get("share")
        if not _num(share) or name == "others":
            continue
        if share > 0.20 and name not in conc_rows:
            errs.append(f"client {name!r} is {share:.0%} of trailing-90-day revenue and has no revenue_concentration row (r-concentration-90d-auto-score)")
            continue
        if name in conc_rows:
            row = conc_rows[name]
            if _num((row.get("details") or {}).get("share")) and abs(row["details"]["share"] - share) > 0.0051:
                errs.append(f"row {row.get('id')} share {row['details']['share']} differs from the recomputed {share} for {name!r} (r-concentration-90d-auto-score)")
            if share >= 0.40 and isinstance(row.get("score"), int) and row["score"] < 15:
                errs.append(f"row {row.get('id')}: {name!r} at {share:.0%} must score at least 15, has {row['score']} (r-concentration-90d-auto-score)")
    for r in rows:
        rid = r.get("id")
        l, i, s = r.get("likelihood"), r.get("impact"), r.get("score")
        if all(isinstance(x, int) for x in (l, i, s)) and s != l * i:
            errs.append(f"row {rid}: score {s} is not likelihood {l} x impact {i} = {l * i} (r-eight-column-row)")
        det = r.get("details") or {}
        for key in ("revenue_share_by_currency", "cost_share_by_currency"):
            shares = det.get(key)
            if isinstance(shares, dict) and shares and abs(sum(v for v in shares.values() if _num(v)) - 1) > 0.011:
                errs.append(f"row {rid}: {key} adds to {sum(shares.values()):.2f}, not 1 (r-cross-border-rows-quantified)")
        wp, mc, moc = det.get("weighted_pipeline"), det.get("monthly_cost_base"), det.get("months_of_coverage")
        if _num(wp) and _num(mc) and mc > 0 and _num(moc) and abs(moc - wp / mc) > 0.051:
            errs.append(f"row {rid}: months_of_coverage {moc} is not weighted_pipeline / monthly_cost_base = {wp / mc:.1f} (r-pipeline-months-of-coverage)")
        dl = _d(det.get("deadline"))
        if rd and dl and dl < rd:
            errs.append(f"row {rid}: key-person remediation deadline {dl} is already past at the {rd} refresh (r-key-person-bus-factor-dated)")
        resp = r.get("response")
        if isinstance(resp, dict) and resp.get("kind") == "mitigation" and rd:
            due = _d(resp.get("due_date"))
            if due and not (0 <= (due - rd).days <= 6):
                errs.append(f"row {rid}: mitigation due {due} is outside the refresh week starting {rd} (r-score-15-action-or-signed-acceptance)")
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
        prog="validate-agency-risk-register-template.py",
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
