#!/usr/bin/env python3
"""validate-remote-1-1-async-fallback.py

Validate the Async11Note produced by the remote-1-1-async-fallback methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/async-11-note.json', 'title': 'Async11Note', 'type': 'object', 'required': ['pair_id', 'cycle_iso', 'header', 'channel', 'sync_infeasibility', 'prompts', 'posting', 'ic_response', 'pm_ack', 'escalation'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'datetime': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'}, 'next_action': {'type': 'object', 'required': ['action', 'owner_role', 'deadline_sprint'], 'properties': {'action': {'type': 'string', 'minLength': 5}, 'owner_role': {'type': 'string', 'minLength': 2}, 'deadline_sprint': {'type': 'string', 'pattern': '^S[0-9]+$'}}}}, 'properties': {'__faion_header__': {'type': 'object'}, 'pair_id': {'type': 'string', 'pattern': '^[a-z0-9._-]+--[a-z0-9._-]+$'}, 'cycle_iso': {'type': 'string', 'pattern': '^[0-9]{4}-W[0-9]{2}$'}, 'header': {'type': 'object', 'required': ['owner', 'version', 'last_reviewed', 'response_window_business_hours'], 'additionalProperties': False, 'properties': {'owner': {'type': 'object', 'required': ['role', 'person'], 'properties': {'role': {'type': 'string', 'minLength': 2}, 'person': {'type': 'string', 'minLength': 2}}}, 'version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}, 'last_reviewed': {'$ref': '#/definitions/date'}, 'response_window_business_hours': {'type': 'integer', 'minimum': 24, 'maximum': 168}}}, 'channel': {'type': 'object', 'required': ['kind', 'visible_to', 'morale_shared_outside_pair'], 'properties': {'kind': {'enum': ['private_doc', 'dm', 'email']}, 'visible_to': {'type': 'array', 'minItems': 2, 'maxItems': 2, 'uniqueItems': True, 'items': {'enum': ['pm', 'ic']}}, 'morale_shared_outside_pair': {'const': False}}}, 'sync_infeasibility': {'type': 'object', 'required': ['reason', 'consecutive_async_cycles'], 'properties': {'reason': {'enum': ['no_overlapping_hours', 'temporary_leave', 'sickness', 'travel']}, 'consecutive_async_cycles': {'type': 'integer', 'minimum': 1, 'maximum': 3}, 'last_sync_call_cycle': {'type': 'string', 'pattern': '^[0-9]{4}-W[0-9]{2}$'}}}, 'prompts': {'type': 'object', 'required': ['blockers', 'decisions_needed', 'morale'], 'additionalProperties': False, 'properties': {'blockers': {'type': 'string', 'minLength': 10, 'pattern': '(?i)(wbs|ticket|id\\b)', 'not': {'pattern': '(?i)(anything to share|how is it going|how are things|all good)'}}, 'decisions_needed': {'type': 'string', 'minLength': 10, 'pattern': '(?i)(whom|who|owner)', 'not': {'pattern': '(?i)(anything to share|how is it going|how are things)'}}, 'morale': {'type': 'string', 'minLength': 10, 'allOf': [{'pattern': '(?i)workload'}, {'pattern': '(?i)autonomy'}, {'pattern': '(?i)clarity'}, {'pattern': '1-10|1 to 10'}]}}}, 'posting': {'type': 'object', 'required': ['ic_timezone', 'posted_at', 'window_closes_at', 'reminders_sent'], 'properties': {'ic_timezone': {'type': 'string', 'pattern': '^[A-Za-z_]+/[A-Za-z_/+-]+$|^UTC$'}, 'posted_at': {'anyOf': [{'$ref': '#/definitions/datetime'}, {'type': 'null'}]}, 'window_closes_at': {'anyOf': [{'$ref': '#/definitions/datetime'}, {'type': 'null'}]}, 'reminders_sent': {'type': 'integer', 'minimum': 0}}}, 'ic_response': {'type': 'object', 'required': ['status', 'received_at', 'blockers', 'decisions_needed', 'morale'], 'properties': {'status': {'enum': ['answered', 'unresponsive', 'paused']}, 'received_at': {'anyOf': [{'$ref': '#/definitions/datetime'}, {'type': 'null'}]}, 'authored_by': {'const': 'ic'}, 'blockers': {'type': 'string'}, 'decisions_needed': {'type': 'string'}, 'morale': {'type': 'string'}, 'leave_type': {'enum': ['vacation', 'parental', 'sick']}}, 'allOf': [{'if': {'properties': {'status': {'const': 'answered'}}}, 'then': {'required': ['authored_by'], 'properties': {'received_at': {'type': 'string'}, 'morale': {'pattern': '(?i)workload ?[0-9]+.*autonomy ?[0-9]+.*clarity ?[0-9]+'}}}}, {'if': {'properties': {'status': {'const': 'paused'}}}, 'then': {'required': ['leave_type'], 'properties': {'received_at': {'type': 'null'}}}}]}, 'pm_ack': {'type': 'object', 'required': ['acked_at', 'ack_business_hours_after_response', 'next_actions'], 'properties': {'acked_at': {'anyOf': [{'$ref': '#/definitions/datetime'}, {'type': 'null'}]}, 'ack_business_hours_after_response': {'type': ['integer', 'null'], 'minimum': 0, 'maximum': 24}, 'next_actions': {'type': 'array', 'items': {'$ref': '#/definitions/next_action'}}}}, 'escalation': {'type': 'object', 'required': ['count_before_cycle', 'unresponsive_count', 'action'], 'properties': {'count_before_cycle': {'type': 'integer', 'minimum': 0}, 'unresponsive_count': {'type': 'integer', 'minimum': 0}, 'action': {'enum': ['none', 'synchronous_reschedule', 'escalate_to_manager']}, 'sync_slot_offered_for_cycle': {'type': 'string', 'pattern': '^[0-9]{4}-W[0-9]{2}$'}, 'manager_packet': {'type': 'object', 'required': ['manager', 'unresponsive_count', 'last_acked_next_actions', 'includes_morale'], 'properties': {'manager': {'type': 'string', 'minLength': 2}, 'unresponsive_count': {'type': 'integer', 'minimum': 2}, 'last_acked_next_actions': {'type': 'array', 'items': {'$ref': '#/definitions/next_action'}}, 'includes_morale': {'const': False}}}}, 'allOf': [{'if': {'properties': {'unresponsive_count': {'const': 0}}}, 'then': {'properties': {'action': {'const': 'none'}}}}, {'if': {'properties': {'unresponsive_count': {'const': 1}}}, 'then': {'properties': {'action': {'const': 'synchronous_reschedule'}}, 'required': ['sync_slot_offered_for_cycle']}}, {'if': {'properties': {'unresponsive_count': {'minimum': 2}}}, 'then': {'properties': {'action': {'const': 'escalate_to_manager'}}, 'required': ['manager_packet']}}]}, 'review': {'type': 'object', 'required': ['computed_at', 'cycles_in_quarter', 'in_window_responses', 'response_rate', 'below_80_over_4_cycles', 'structural_decision', 'version_after'], 'properties': {'computed_at': {'$ref': '#/definitions/date'}, 'cycles_in_quarter': {'type': 'integer', 'minimum': 1}, 'in_window_responses': {'type': 'integer', 'minimum': 0}, 'response_rate': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'below_80_over_4_cycles': {'type': 'boolean'}, 'structural_decision': {'enum': ['none', 'change_response_window', 'restructure_pair', 'mandate_synchronous']}, 'version_after': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?$'}}, 'if': {'properties': {'below_80_over_4_cycles': {'const': True}}}, 'then': {'properties': {'structural_decision': {'enum': ['change_response_window', 'restructure_pair', 'mandate_synchronous']}}}}}}

OK = {'pair_id': 'olena.k--taras.v', 'cycle_iso': '2026-W21', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'version': '1.4.0', 'last_reviewed': '2026-04-07', 'response_window_business_hours': 48}, 'channel': {'kind': 'private_doc', 'visible_to': ['pm', 'ic'], 'morale_shared_outside_pair': False}, 'sync_infeasibility': {'reason': 'no_overlapping_hours', 'consecutive_async_cycles': 2, 'last_sync_call_cycle': '2026-W19'}, 'prompts': {'blockers': 'What is blocking your current sprint goals? Cite the WBS id or ticket and what is upstream of it.', 'decisions_needed': 'What decision are you waiting on, from whom, and by which date?', 'morale': 'Workload 1-10, autonomy 1-10, clarity 1-10, and anything else you want me to know.'}, 'posting': {'ic_timezone': 'Australia/Sydney', 'posted_at': '2026-05-18T09:00+10:00', 'window_closes_at': '2026-05-20T09:00+10:00', 'reminders_sent': 0}, 'ic_response': {'status': 'answered', 'received_at': '2026-05-19T16:30+10:00', 'authored_by': 'ic', 'blockers': 'PR review on WBS 4.2 stalled 3 days; waiting on backend-lead', 'decisions_needed': 'Token TTL for the session service; owner security-lead; needed before S14 planning', 'morale': 'workload 7, autonomy 8, clarity 6; clarity dropped because the S14 scope changed twice'}, 'pm_ack': {'acked_at': '2026-05-19T18:00+02:00', 'ack_business_hours_after_response': 6, 'next_actions': [{'action': 'Ask backend-lead to review the WBS 4.2 PR today or hand it to a second reviewer', 'owner_role': 'pm', 'deadline_sprint': 'S13'}, {'action': "Get security-lead's token TTL decision on the record before S14 planning", 'owner_role': 'pm', 'deadline_sprint': 'S14'}]}, 'escalation': {'count_before_cycle': 0, 'unresponsive_count': 0, 'action': 'none'}, 'review': {'computed_at': '2026-04-07', 'cycles_in_quarter': 12, 'in_window_responses': 11, 'response_rate': 0.9167, 'below_80_over_4_cycles': False, 'structural_decision': 'none', 'version_after': '1.4.0'}}

BAD = {'pair_id': 'olena.k--taras.v', 'cycle_iso': '2026-W21', 'header': {'owner': {'role': 'pm', 'person': 'olena.k'}, 'version': '1.4.0', 'last_reviewed': '2026-04-07', 'response_window_business_hours': 12}, 'channel': {'kind': 'private_doc', 'visible_to': ['pm', 'ic'], 'morale_shared_outside_pair': True}, 'sync_infeasibility': {'reason': 'no_overlapping_hours', 'consecutive_async_cycles': 5}, 'prompts': {'blockers': 'Anything to share this week?', 'decisions_needed': 'Any decisions pending?', 'morale': 'How is it going overall?'}, 'posting': {'ic_timezone': 'Australia/Sydney', 'posted_at': '2026-05-15T17:00+02:00', 'window_closes_at': '2026-05-16T05:00+02:00', 'reminders_sent': 3}, 'ic_response': {'status': 'unresponsive', 'received_at': None, 'blockers': '', 'decisions_needed': '', 'morale': ''}, 'pm_ack': {'acked_at': None, 'ack_business_hours_after_response': None, 'next_actions': []}, 'escalation': {'count_before_cycle': 2, 'unresponsive_count': 3, 'action': 'none', 'manager_packet': {'manager': 'sofia.r', 'unresponsive_count': 3, 'last_acked_next_actions': [], 'includes_morale': True}}}


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


_EMPTY = {"", "none", "nothing", "no", "n/a", "-"}


def _dt(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (TypeError, ValueError, AttributeError):
        return None


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    header, posting = obj.get("header") or {}, obj.get("posting") or {}
    resp, ack, esc = obj.get("ic_response") or {}, obj.get("pm_ack") or {}, obj.get("escalation") or {}
    status = resp.get("status")
    posted, closes, received = _dt(posting.get("posted_at")), _dt(posting.get("window_closes_at")), _dt(resp.get("received_at"))
    window = header.get("response_window_business_hours", 0)
    if posted and closes and (closes - posted).total_seconds() < window * 3600:
        errs.append(f"posting.window_closes_at is {(closes - posted).total_seconds() / 3600:.0f}h after posted_at; {window} business hours in the IC's timezone can never close sooner (r-response-window-in-ic-business-hours)")
    if status == "answered" and received and closes and received > closes:
        errs.append("ic_response: received_at is after window_closes_at; the cycle is unresponsive, not answered (r-empty-answer-ok-missing-field-is-unresponsive)")
    if status == "paused":
        if posting.get("posted_at") is not None or posting.get("reminders_sent", 0) > 0:
            errs.append("posting: a paused cycle is not posted and gets no reminders (r-formal-leave-pauses-the-cycle)")
        if esc.get("unresponsive_count") != esc.get("count_before_cycle"):
            errs.append(f"escalation: paused cycle moved unresponsive_count from {esc.get('count_before_cycle')} to {esc.get('unresponsive_count')} (r-formal-leave-pauses-the-cycle)")
    elif status == "answered":
        if esc.get("unresponsive_count") != 0:
            errs.append(f"escalation: an in-window answer resets unresponsive_count to 0, got {esc.get('unresponsive_count')} (r-escalation-ladder-reschedule-then-manager)")
        acked = _dt(ack.get("acked_at"))
        if acked is None or ack.get("ack_business_hours_after_response") is None:
            errs.append("pm_ack: answered cycle has no acked_at / ack_business_hours_after_response (r-pm-ack-within-24h-with-owned-actions)")
        elif received and acked < received:
            errs.append("pm_ack.acked_at is before ic_response.received_at (r-pm-ack-within-24h-with-owned-actions)")
        reported = [k for k in ("blockers", "decisions_needed") if (resp.get(k) or "").strip().lower() not in _EMPTY]
        if reported and not ack.get("next_actions"):
            errs.append(f"pm_ack.next_actions empty while the IC reported {reported}; a 'thanks, noted' ack is invalid (r-pm-ack-within-24h-with-owned-actions)")
    elif status == "unresponsive":
        if esc.get("unresponsive_count") != esc.get("count_before_cycle", 0) + 1:
            errs.append(f"escalation: unresponsive cycle must set unresponsive_count to count_before_cycle + 1 = {esc.get('count_before_cycle', 0) + 1}, got {esc.get('unresponsive_count')} (r-escalation-ladder-reschedule-then-manager)")
    lr, pd = _date(header.get("last_reviewed")), posted.date() if posted else None
    if lr and pd and (pd - lr).days > 90:
        errs.append(f"posting: note posted {(pd - lr).days} days after header.last_reviewed; review first (r-quarterly-response-rate-review)")
    review = obj.get("review")
    if isinstance(review, dict) and review.get("cycles_in_quarter"):
        want = review["in_window_responses"] / review["cycles_in_quarter"]
        if abs(review.get("response_rate", -1) - want) > 0.005:
            errs.append(f"review.response_rate {review.get('response_rate')} != {review['in_window_responses']}/{review['cycles_in_quarter']} = {want:.4f} (r-quarterly-response-rate-review)")
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
        prog="validate-remote-1-1-async-fallback.py",
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
