#!/usr/bin/env python3
"""validate-growth-referral-programs.py

Validate the referral-programme spec produced by the growth-referral-programs methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/growth-referral-programs.json', 'title': 'Growth Referral Programs spec', 'type': 'object', 'required': ['programme_name', 'nps_gate', 'trigger_event', 'qualifying_event', 'incentive', 'fraud_guard', 'k_factor', 'attribution', 'lifecycle', 'disclosure'], 'additionalProperties': False, 'definitions': {'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'}, 'not_signup': {'not': {'enum': ['signup', 'signup_completed', 'sign_up', 'account_created', 'account_creation', 'registration_completed', 'first_screen_viewed', 'welcome_screen_viewed', 'onboarding_started']}}, 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'reward': {'type': 'object', 'required': ['kind', 'amount', 'currency'], 'additionalProperties': False, 'properties': {'kind': {'type': 'string', 'enum': ['account_credit', 'discount', 'cash', 'free_months']}, 'amount': {'type': 'number', 'exclusiveMinimum': 0}, 'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}}}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'programme_name': {'type': 'string', 'minLength': 3}, 'nps_gate': {'type': 'object', 'required': ['metric', 'score', 'sample_size', 'population', 'measured_on', 'age_days'], 'additionalProperties': False, 'properties': {'metric': {'type': 'string', 'enum': ['nps', 'willingness_to_recommend']}, 'score': {'type': 'number', 'minimum': -100, 'maximum': 100}, 'sample_size': {'type': 'integer', 'minimum': 1}, 'population': {'const': 'active_users'}, 'measured_on': {'$ref': '#/definitions/date'}, 'age_days': {'type': 'integer', 'minimum': 0, 'maximum': 90}}, 'if': {'properties': {'metric': {'const': 'nps'}}}, 'then': {'properties': {'score': {'minimum': 30}}}}, 'trigger_event': {'type': 'object', 'required': ['name', 'reach_share', 'instrumented'], 'additionalProperties': False, 'properties': {'name': {'allOf': [{'$ref': '#/definitions/event_name'}, {'$ref': '#/definitions/not_signup'}]}, 'reach_share': {'$ref': '#/definitions/rate'}, 'instrumented': {'const': True}}}, 'qualifying_event': {'type': 'object', 'required': ['kind', 'name', 'stated_on_landing_page', 'stated_in_every_email'], 'additionalProperties': False, 'properties': {'kind': {'type': 'string', 'enum': ['first_paid_order', 'activation_milestone']}, 'name': {'allOf': [{'$ref': '#/definitions/event_name'}, {'$ref': '#/definitions/not_signup'}]}, 'minimum_order_value': {'type': 'number', 'exclusiveMinimum': 0}, 'stated_on_landing_page': {'const': True}, 'stated_in_every_email': {'const': True}}, 'if': {'properties': {'kind': {'const': 'first_paid_order'}}}, 'then': {'required': ['minimum_order_value']}}, 'incentive': {'type': 'object', 'required': ['referrer_reward', 'referee_reward', 'reward_cost_per_qualified_referee', 'blended_paid_cac', 'margin_basis', 'margin_basis_value', 'max_reward_share_of_basis'], 'additionalProperties': False, 'properties': {'referrer_reward': {'$ref': '#/definitions/reward'}, 'referee_reward': {'$ref': '#/definitions/reward'}, 'reward_cost_per_qualified_referee': {'type': 'number', 'exclusiveMinimum': 0}, 'blended_paid_cac': {'type': 'number', 'exclusiveMinimum': 0}, 'margin_basis': {'type': 'string', 'enum': ['first_order_gross_margin', 'expected_ltv']}, 'margin_basis_value': {'type': 'number', 'exclusiveMinimum': 0}, 'max_reward_share_of_basis': {'type': 'number', 'exclusiveMinimum': 0, 'maximum': 1}}}, 'fraud_guard': {'type': 'object', 'required': ['referee_must_be_new_account', 'one_referral_per_email', 'one_referral_per_payment_instrument', 'self_referral_signals', 'email_normalisation', 'reward_hold_days', 'reward_hold_covers', 'idempotency_key'], 'additionalProperties': False, 'properties': {'referee_must_be_new_account': {'const': True}, 'one_referral_per_email': {'const': True}, 'one_referral_per_payment_instrument': {'const': True}, 'self_referral_signals': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['payment_instrument', 'device_fingerprint', 'ip', 'normalised_email']}, 'allOf': [{'contains': {'const': 'payment_instrument'}}, {'contains': {'const': 'device_fingerprint'}}, {'contains': {'const': 'ip'}}, {'contains': {'const': 'normalised_email'}}]}, 'email_normalisation': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['plus_addressing', 'dot_variants']}, 'allOf': [{'contains': {'const': 'plus_addressing'}}, {'contains': {'const': 'dot_variants'}}]}, 'reward_hold_days': {'type': 'integer', 'minimum': 1}, 'reward_hold_covers': {'type': 'string', 'enum': ['refund_window', 'chargeback_window']}, 'idempotency_key': {'type': 'array', 'minItems': 3, 'maxItems': 3, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['referrer_id', 'referee_id', 'qualifying_event']}}}}, 'k_factor': {'type': 'object', 'required': ['invites', 'active_referrers', 'referee_signups', 'invites_per_referrer', 'conversion_per_invite', 'k', 'cycle_time_days', 'presented_as', 'cac_multiplier', 'netted_of_reward_cost'], 'additionalProperties': False, 'properties': {'invites': {'type': 'integer', 'minimum': 500}, 'active_referrers': {'type': 'integer', 'minimum': 50}, 'referee_signups': {'type': 'integer', 'minimum': 0}, 'invites_per_referrer': {'type': 'number', 'minimum': 0}, 'conversion_per_invite': {'$ref': '#/definitions/rate'}, 'k': {'type': 'number', 'minimum': 0}, 'cycle_time_days': {'type': 'number', 'exclusiveMinimum': 0}, 'presented_as': {'type': 'string', 'enum': ['cac_multiplier', 'viral_growth']}, 'cac_multiplier': {'type': 'number', 'minimum': 1}, 'netted_of_reward_cost': {'const': True}}, 'if': {'properties': {'k': {'exclusiveMaximum': 1}}}, 'then': {'properties': {'presented_as': {'const': 'cac_multiplier'}}}}, 'attribution': {'type': 'object', 'required': ['per_user_code', 'landing_page_accepts_param', 'email_accepts_param', 'capture_methods', 'persisted_server_side_at', 'utm_only'], 'additionalProperties': False, 'properties': {'per_user_code': {'const': True}, 'landing_page_accepts_param': {'const': True}, 'email_accepts_param': {'const': True}, 'capture_methods': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['url_parameter', 'first_party_cookie', 'code_at_signup']}}, 'persisted_server_side_at': {'const': 'referee_account_creation'}, 'utm_only': {'const': False}}}, 'lifecycle': {'type': 'object', 'required': ['announcement', 'reminder', 'confirmation', 'promises_reward_before_qualifying_event'], 'additionalProperties': False, 'properties': {'announcement': {'type': 'object', 'required': ['send_on'], 'additionalProperties': False, 'properties': {'send_on': {'$ref': '#/definitions/event_name'}}}, 'reminder': {'type': 'object', 'required': ['after_days', 'audience', 'max_sends'], 'additionalProperties': False, 'properties': {'after_days': {'type': 'integer', 'minimum': 1}, 'audience': {'const': 'zero_referrals'}, 'max_sends': {'const': 1}}}, 'confirmation': {'type': 'object', 'required': ['send_on', 'recipients'], 'additionalProperties': False, 'properties': {'send_on': {'const': 'qualifying_event'}, 'recipients': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['referrer', 'referee']}, 'allOf': [{'contains': {'const': 'referrer'}}, {'contains': {'const': 'referee'}}]}}}, 'promises_reward_before_qualifying_event': {'const': False}}}, 'disclosure': {'type': 'object', 'required': ['reward_disclosed_on_shared_content', 'terms_url', 'terms_cover', 'earnings_claims'], 'additionalProperties': False, 'properties': {'reward_disclosed_on_shared_content': {'const': True}, 'terms_url': {'type': 'string', 'pattern': '^https?://'}, 'terms_cover': {'type': 'array', 'minItems': 4, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['qualifying_event', 'reward_timing', 'exclusions', 'fraud_reversal']}}, 'earnings_claims': {'type': 'array', 'items': {'type': 'object', 'required': ['claim', 'period', 'verified'], 'additionalProperties': False, 'properties': {'claim': {'type': 'string', 'minLength': 5}, 'period': {'type': 'string', 'minLength': 4}, 'verified': {'const': True}}}}}}}}

OK = {'programme_name': 'give 20 get 20', 'nps_gate': {'metric': 'nps', 'score': 42, 'sample_size': 640, 'population': 'active_users', 'measured_on': '2026-08-14', 'age_days': 30}, 'trigger_event': {'name': 'first_successful_export', 'reach_share': 0.57, 'instrumented': True}, 'qualifying_event': {'kind': 'first_paid_order', 'name': 'first_paid_order', 'minimum_order_value': 50, 'stated_on_landing_page': True, 'stated_in_every_email': True}, 'incentive': {'referrer_reward': {'kind': 'account_credit', 'amount': 20, 'currency': 'USD'}, 'referee_reward': {'kind': 'discount', 'amount': 20, 'currency': 'USD'}, 'reward_cost_per_qualified_referee': 40, 'blended_paid_cac': 95, 'margin_basis': 'first_order_gross_margin', 'margin_basis_value': 126, 'max_reward_share_of_basis': 0.35}, 'fraud_guard': {'referee_must_be_new_account': True, 'one_referral_per_email': True, 'one_referral_per_payment_instrument': True, 'self_referral_signals': ['payment_instrument', 'device_fingerprint', 'ip', 'normalised_email'], 'email_normalisation': ['plus_addressing', 'dot_variants'], 'reward_hold_days': 30, 'reward_hold_covers': 'refund_window', 'idempotency_key': ['referrer_id', 'referee_id', 'qualifying_event']}, 'k_factor': {'invites': 4200, 'active_referrers': 850, 'referee_signups': 630, 'invites_per_referrer': 4.94, 'conversion_per_invite': 0.15, 'k': 0.741, 'cycle_time_days': 9, 'presented_as': 'cac_multiplier', 'cac_multiplier': 3.86, 'netted_of_reward_cost': True}, 'attribution': {'per_user_code': True, 'landing_page_accepts_param': True, 'email_accepts_param': True, 'capture_methods': ['url_parameter', 'first_party_cookie', 'code_at_signup'], 'persisted_server_side_at': 'referee_account_creation', 'utm_only': False}, 'lifecycle': {'announcement': {'send_on': 'first_successful_export'}, 'reminder': {'after_days': 14, 'audience': 'zero_referrals', 'max_sends': 1}, 'confirmation': {'send_on': 'qualifying_event', 'recipients': ['referrer', 'referee']}, 'promises_reward_before_qualifying_event': False}, 'disclosure': {'reward_disclosed_on_shared_content': True, 'terms_url': 'https://example.com/referral-terms', 'terms_cover': ['qualifying_event', 'reward_timing', 'exclusions', 'fraud_reversal'], 'earnings_claims': [{'claim': "this month's top referrer has earned 300 USD", 'period': '2026-08', 'verified': True}]}}

BAD = {'programme_name': 'refer a friend', 'nps_gate': {'metric': 'nps', 'score': 22, 'sample_size': 40, 'population': 'active_users', 'measured_on': '2025-06-01', 'age_days': 400}, 'trigger_event': {'name': 'signup', 'reach_share': 1, 'instrumented': True}, 'qualifying_event': {'kind': 'activation_milestone', 'name': 'account_created', 'stated_on_landing_page': False, 'stated_in_every_email': False}, 'incentive': {'referrer_reward': {'kind': 'account_credit', 'amount': 20, 'currency': 'USD'}, 'referee_reward': {'kind': 'discount', 'amount': 0, 'currency': 'USD'}, 'reward_cost_per_qualified_referee': 20, 'blended_paid_cac': 15, 'margin_basis': 'first_order_gross_margin', 'margin_basis_value': 18, 'max_reward_share_of_basis': 0.5}, 'fraud_guard': {'referee_must_be_new_account': False, 'one_referral_per_email': True, 'one_referral_per_payment_instrument': False, 'self_referral_signals': ['ip'], 'email_normalisation': [], 'reward_hold_days': 0, 'reward_hold_covers': 'none', 'idempotency_key': ['referrer_id']}, 'k_factor': {'invites': 30, 'active_referrers': 6, 'referee_signups': 4, 'invites_per_referrer': 5, 'conversion_per_invite': 0.133, 'k': 0.9, 'cycle_time_days': 7, 'presented_as': 'viral_growth', 'cac_multiplier': 1, 'netted_of_reward_cost': False}, 'attribution': {'per_user_code': False, 'landing_page_accepts_param': True, 'email_accepts_param': False, 'capture_methods': ['utm_source'], 'persisted_server_side_at': 'analytics_session', 'utm_only': True}, 'lifecycle': {'announcement': {'send_on': 'signup'}, 'reminder': {'after_days': 3, 'audience': 'all_users', 'max_sends': 4}, 'confirmation': {'send_on': 'signup', 'recipients': ['referrer']}, 'promises_reward_before_qualifying_event': True}, 'disclosure': {'reward_disclosed_on_shared_content': False, 'terms_url': '', 'terms_cover': ['reward_timing'], 'earnings_claims': [{'claim': 'top referrer earned 300 USD', 'period': '', 'verified': False}]}}


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


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    inc = obj.get("incentive") or {}
    a = (inc.get("referrer_reward") or {}).get("amount")
    b = (inc.get("referee_reward") or {}).get("amount")
    cost = inc.get("reward_cost_per_qualified_referee")
    if _num(a) and _num(b) and _num(cost) and abs(cost - (a + b)) > 0.005:
        errs.append(f"incentive.reward_cost_per_qualified_referee {cost} is not referrer {a} + referee {b} = {a + b} (r-double-sided-incentive-within-unit-economics)")
    cac = inc.get("blended_paid_cac")
    if _num(cost) and _num(cac) and cost > cac:
        errs.append(f"incentive.reward_cost_per_qualified_referee {cost} exceeds blended_paid_cac {cac}; do not launch as designed (r-double-sided-incentive-within-unit-economics)")
    basis, share = inc.get("margin_basis_value"), inc.get("max_reward_share_of_basis")
    if _num(cost) and _num(basis) and _num(share) and cost > share * basis + 0.005:
        errs.append(f"incentive.reward_cost_per_qualified_referee {cost} exceeds {share} x {inc.get('margin_basis')} {basis} = {share * basis:.2f} (r-double-sided-incentive-within-unit-economics)")
    kf = obj.get("k_factor") or {}
    inv, ref, sig = kf.get("invites"), kf.get("active_referrers"), kf.get("referee_signups")
    i, c, k = kf.get("invites_per_referrer"), kf.get("conversion_per_invite"), kf.get("k")
    if _num(inv) and _num(ref) and ref > 0 and _num(i) and abs(i - inv / ref) > 0.0051:
        errs.append(f"k_factor.invites_per_referrer {i} is not invites / active_referrers = {inv / ref:.2f} (r-k-factor-computed-on-500-plus-invites)")
    if _num(inv) and _num(sig) and inv > 0 and _num(c) and abs(c - sig / inv) > 0.00051:
        errs.append(f"k_factor.conversion_per_invite {c} is not referee_signups / invites = {sig / inv:.3f} (r-k-factor-computed-on-500-plus-invites)")
    if _num(i) and _num(c) and _num(k) and abs(k - i * c) > 0.0051:
        errs.append(f"k_factor.k {k} is not invites_per_referrer x conversion_per_invite = {i * c:.3f} (r-k-factor-computed-on-500-plus-invites)")
    if _num(k) and k < 1 and _num(kf.get("cac_multiplier")):
        want = 1 / (1 - k)
        if abs(kf["cac_multiplier"] - want) > 0.0051:
            errs.append(f"k_factor.cac_multiplier {kf['cac_multiplier']} is not 1 / (1 - k) = {want:.2f} (r-k-factor-computed-on-500-plus-invites)")
    trig = (obj.get("trigger_event") or {}).get("name")
    ann = ((obj.get("lifecycle") or {}).get("announcement") or {}).get("send_on")
    if isinstance(trig, str) and isinstance(ann, str) and trig != ann:
        errs.append(f"lifecycle.announcement.send_on {ann!r} is not the trigger event {trig!r} (r-lifecycle-sequence-trigger-reminder-confirmation)")
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
        prog="validate-growth-referral-programs.py",
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
