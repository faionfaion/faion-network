#!/usr/bin/env python3
"""validate-growth-viral-loops.py

Validate the artefact produced by the growth-viral-loops methodology against the JSON Schema
(draft-07) embedded in content/02-output-contract.xml, plus the cross-field rules from
content/01-core-rules.xml the schema cannot express. Stdlib-only, self-contained.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#',
 '$id': 'https://faion.net/schemas/growth-viral-loops.json',
 'title': 'Growth Viral Loops spec',
 'type': 'object',
 'required': ['loop_name',
              'primary_loop',
              'k_factor',
              'cycle_time',
              'projection',
              'k_target',
              'invitee_path',
              'friction_experiments',
              'events',
              'retention',
              'incentive',
              'consent_and_disclosure'],
 'additionalProperties': False,
 'definitions': {'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1},
                 'measured': {'type': 'object',
                              'required': ['value', 'window_days', 'sample_size'],
                              'additionalProperties': False,
                              'properties': {'value': {'type': 'number', 'minimum': 0},
                                             'window_days': {'type': 'integer', 'minimum': 1},
                                             'sample_size': {'type': 'integer', 'minimum': 1}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'loop_name': {'type': 'string', 'minLength': 3},
                'primary_loop': {'type': 'object',
                                 'required': ['share_event',
                                              'kind',
                                              'value_to_inviter',
                                              'secondary_loop'],
                                 'additionalProperties': False,
                                 'properties': {'share_event': {'allOf': [{'$ref': '#/definitions/event_name'},
                                                                          {'not': {'enum': ['invite_modal_shown',
                                                                                            'refer_page_viewed',
                                                                                            'referral_page_viewed',
                                                                                            'invite_friends_modal']}}]},
                                                'kind': {'const': 'inherent'},
                                                'value_to_inviter': {'type': 'string',
                                                                     'minLength': 20},
                                                'secondary_loop': {'anyOf': [{'type': 'null'},
                                                                             {'type': 'object',
                                                                              'required': ['surface',
                                                                                           'k'],
                                                                              'additionalProperties': False,
                                                                              'properties': {'surface': {'type': 'string',
                                                                                                         'enum': ['invite_modal',
                                                                                                                  'referral_page']},
                                                                                             'k': {'type': 'number',
                                                                                                   'minimum': 0}}}]}}},
                'k_factor': {'type': 'object',
                             'required': ['invites_per_active_user',
                                          'accept_rate_per_invite',
                                          'k',
                                          'cycles_measured'],
                             'additionalProperties': False,
                             'properties': {'invites_per_active_user': {'$ref': '#/definitions/measured'},
                                            'accept_rate_per_invite': {'allOf': [{'$ref': '#/definitions/measured'},
                                                                                 {'properties': {'value': {'maximum': 1}}}]},
                                            'k': {'type': 'number', 'minimum': 0},
                                            'cycles_measured': {'type': 'integer', 'minimum': 2}}},
                'cycle_time': {'type': 'object',
                               'required': ['days', 'method', 'sample_size'],
                               'additionalProperties': False,
                               'properties': {'days': {'type': 'number', 'exclusiveMinimum': 0},
                                              'method': {'const': 'send_to_first_send_timestamps'},
                                              'sample_size': {'type': 'integer', 'minimum': 1}}},
                'projection': {'type': 'object',
                               'required': ['starting_users',
                                            'days',
                                            'projected_users',
                                            'ignores_churn'],
                               'additionalProperties': False,
                               'properties': {'starting_users': {'type': 'integer', 'minimum': 1},
                                              'days': {'type': 'integer', 'minimum': 30},
                                              'projected_users': {'type': 'integer', 'minimum': 1},
                                              'ignores_churn': {'const': True}}},
                'k_target': {'type': 'object',
                             'required': ['current_k', 'target_k', 'kind', 'benchmark'],
                             'additionalProperties': False,
                             'properties': {'current_k': {'type': 'number', 'minimum': 0},
                                            'target_k': {'type': 'number', 'exclusiveMinimum': 0},
                                            'kind': {'type': 'string',
                                                     'enum': ['self_sustaining', 'increment']},
                                            'benchmark': {'type': 'object',
                                                          'required': ['range_low',
                                                                       'range_high',
                                                                       'source'],
                                                          'additionalProperties': False,
                                                          'properties': {'range_low': {'type': 'number',
                                                                                       'minimum': 0},
                                                                         'range_high': {'type': 'number',
                                                                                        'minimum': 0},
                                                                         'source': {'type': 'string',
                                                                                    'minLength': 10}}}},
                             'if': {'properties': {'current_k': {'exclusiveMaximum': 0.4}}},
                             'then': {'properties': {'target_k': {'maximum': 1},
                                                     'kind': {'const': 'increment'}}}},
                'invitee_path': {'type': 'array',
                                 'minItems': 1,
                                 'maxItems': 3,
                                 'items': {'type': 'object',
                                           'required': ['name', 'conversion'],
                                           'additionalProperties': False,
                                           'properties': {'name': {'type': 'string',
                                                                   'minLength': 3},
                                                          'conversion': {'$ref': '#/definitions/rate'}}}},
                'friction_experiments': {'type': 'array',
                                         'minItems': 1,
                                         'items': {'type': 'object',
                                                   'required': ['name',
                                                                'target_step',
                                                                'current_conversion',
                                                                'expected_conversion'],
                                                   'additionalProperties': False,
                                                   'properties': {'name': {'type': 'string',
                                                                           'minLength': 10},
                                                                  'target_step': {'type': 'string',
                                                                                  'minLength': 3},
                                                                  'current_conversion': {'$ref': '#/definitions/rate'},
                                                                  'expected_conversion': {'$ref': '#/definitions/rate'}}}},
                'events': {'type': 'array',
                           'minItems': 5,
                           'items': {'type': 'object',
                                     'required': ['name', 'keys'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['invite_shown',
                                                                      'invite_sent',
                                                                      'invite_opened',
                                                                      'invite_accepted',
                                                                      'invitee_activated']},
                                                    'keys': {'type': 'array',
                                                             'items': {'type': 'string'},
                                                             'allOf': [{'contains': {'const': 'invite_id'}},
                                                                       {'contains': {'const': 'inviter_user_id'}}]}}}},
                'retention': {'type': 'object',
                              'required': ['invitee_d30', 'organic_d30'],
                              'additionalProperties': False,
                              'properties': {'invitee_d30': {'$ref': '#/definitions/rate'},
                                             'organic_d30': {'$ref': '#/definitions/rate'}}},
                'incentive': {'anyOf': [{'type': 'null'},
                                        {'type': 'object',
                                         'required': ['referrer_reward',
                                                      'invitee_reward',
                                                      'trigger_milestone',
                                                      'window_days',
                                                      'max_rewards_per_referrer_per_12_months',
                                                      'self_referral_block',
                                                      'excludes_existing_and_past_users'],
                                         'additionalProperties': False,
                                         'properties': {'referrer_reward': {'type': 'string',
                                                                            'minLength': 3},
                                                        'invitee_reward': {'type': 'string',
                                                                           'minLength': 3},
                                                        'trigger_milestone': {'allOf': [{'$ref': '#/definitions/event_name'},
                                                                                        {'not': {'enum': ['signup',
                                                                                                          'signup_completed',
                                                                                                          'account_created',
                                                                                                          'invite_accepted']}}]},
                                                        'window_days': {'type': 'integer',
                                                                        'minimum': 1},
                                                        'max_rewards_per_referrer_per_12_months': {'type': 'integer',
                                                                                                   'minimum': 1},
                                                        'self_referral_block': {'type': 'array',
                                                                                'items': {'type': 'string',
                                                                                          'enum': ['device_fingerprint',
                                                                                                   'ip',
                                                                                                   'payment_instrument',
                                                                                                   'normalised_email']},
                                                                                'allOf': [{'contains': {'const': 'device_fingerprint'}},
                                                                                          {'contains': {'const': 'ip'}},
                                                                                          {'contains': {'const': 'payment_instrument'}}]},
                                                        'excludes_existing_and_past_users': {'const': True}}}]},
                'consent_and_disclosure': {'type': 'object',
                                           'required': ['recipient_source',
                                                        'casl_express_consent',
                                                        'gdpr_lawful_basis',
                                                        'compensation_disclosure'],
                                           'additionalProperties': False,
                                           'properties': {'recipient_source': {'type': 'string',
                                                                               'enum': ['entered_by_inviter',
                                                                                        'consented_contact_import']},
                                                          'casl_express_consent': {'const': True},
                                                          'gdpr_lawful_basis': {'type': 'string',
                                                                                'enum': ['consent',
                                                                                         'contract',
                                                                                         'legitimate_interest']},
                                                          'compensation_disclosure': {'type': 'string',
                                                                                      'enum': ['not_applicable',
                                                                                               'message',
                                                                                               'landing_page',
                                                                                               'both']}}}}}

OK = {'loop_name': 'board collaboration loop',
 'primary_loop': {'share_event': 'board_shared',
                  'kind': 'inherent',
                  'value_to_inviter': 'the inviter needs the collaborator on the board to finish '
                                      'the work; sharing is the product action, not a favour',
                  'secondary_loop': None},
 'k_factor': {'invites_per_active_user': {'value': 1.8, 'window_days': 30, 'sample_size': 12400},
              'accept_rate_per_invite': {'value': 0.36, 'window_days': 30, 'sample_size': 22300},
              'k': 0.648,
              'cycles_measured': 3},
 'cycle_time': {'days': 6, 'method': 'send_to_first_send_timestamps', 'sample_size': 4100},
 'projection': {'starting_users': 1000, 'days': 90, 'projected_users': 2838, 'ignores_churn': True},
 'k_target': {'current_k': 0.648,
              'target_k': 0.8,
              'kind': 'increment',
              'benchmark': {'range_low': 0.05,
                            'range_high': 0.2,
                            'source': 'widely cited practitioner benchmarks for B2B SaaS, as '
                                      'listed in templates/loop-projection.py'}},
 'invitee_path': [{'name': 'open invite link', 'conversion': 0.62},
                  {'name': 'create account', 'conversion': 0.58},
                  {'name': 'first board edit', 'conversion': 0.78}],
 'friction_experiments': [{'name': 'remove the email verification gate before the first board edit',
                           'target_step': 'create account',
                           'current_conversion': 0.58,
                           'expected_conversion': 0.75},
                          {'name': 'open the shared board read-only before account creation',
                           'target_step': 'open invite link',
                           'current_conversion': 0.62,
                           'expected_conversion': 0.7}],
 'events': [{'name': 'invite_shown', 'keys': ['invite_id', 'inviter_user_id', 'board_id']},
            {'name': 'invite_sent', 'keys': ['invite_id', 'inviter_user_id', 'board_id']},
            {'name': 'invite_opened', 'keys': ['invite_id', 'inviter_user_id']},
            {'name': 'invite_accepted',
             'keys': ['invite_id', 'inviter_user_id', 'invitee_user_id']},
            {'name': 'invitee_activated',
             'keys': ['invite_id', 'inviter_user_id', 'invitee_user_id']}],
 'retention': {'invitee_d30': 0.41, 'organic_d30': 0.38},
 'incentive': None,
 'consent_and_disclosure': {'recipient_source': 'entered_by_inviter',
                            'casl_express_consent': True,
                            'gdpr_lawful_basis': 'legitimate_interest',
                            'compensation_disclosure': 'not_applicable'}}

BAD = {'loop_name': 'refer a friend',
 'primary_loop': {'share_event': 'invite_modal_shown',
                  'kind': 'incentivised',
                  'value_to_inviter': 'the inviter gets a 10 USD credit',
                  'secondary_loop': None},
 'k_factor': {'invites_per_active_user': {'value': 0, 'window_days': 30, 'sample_size': 1},
              'accept_rate_per_invite': {'value': 0, 'window_days': 30, 'sample_size': 1},
              'k': 0.7,
              'cycles_measured': 1},
 'cycle_time': {'days': 7, 'method': 'estimated', 'sample_size': 1},
 'projection': {'starting_users': 1000,
                'days': 90,
                'projected_users': 12000,
                'ignores_churn': False},
 'k_target': {'current_k': 0.15,
              'target_k': 1.2,
              'kind': 'self_sustaining',
              'benchmark': {'range_low': 0.1, 'range_high': 0.3, 'source': 'a blog'}},
 'invitee_path': [{'name': 'open link', 'conversion': 0.6},
                  {'name': 'landing page', 'conversion': 0.7},
                  {'name': 'create account', 'conversion': 0.55},
                  {'name': 'verify email', 'conversion': 0.7},
                  {'name': 'onboarding survey', 'conversion': 0.8}],
 'friction_experiments': [{'name': 'improve onboarding',
                           'target_step': 'onboarding',
                           'current_conversion': 0.8,
                           'expected_conversion': 0.8}],
 'events': [{'name': 'invite_sent', 'keys': ['user_id']},
            {'name': 'invite_accepted', 'keys': ['user_id']}],
 'retention': {'invitee_d30': 0.12, 'organic_d30': 0.38},
 'incentive': {'referrer_reward': '10 USD credit',
               'invitee_reward': '10 USD credit',
               'trigger_milestone': 'signup_completed',
               'window_days': 30,
               'max_rewards_per_referrer_per_12_months': 1000,
               'self_referral_block': ['ip'],
               'excludes_existing_and_past_users': False},
 'consent_and_disclosure': {'recipient_source': 'contact_import_without_consent',
                            'casl_express_consent': False,
                            'gdpr_lawful_basis': 'consent',
                            'compensation_disclosure': 'not_applicable'}}


# --------------------------------------------------------------------------
# draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
# exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
# minProperties/maxProperties, uniqueItems, items, contains, properties,
# additionalProperties, allOf/anyOf/oneOf/not, if/then/else, local $ref
# (#/definitions/...). Enough for every constraint the contract declares.
# --------------------------------------------------------------------------

_TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _check(schema: dict, value, path: str, errs: list[str]) -> None:
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{path or '$'}: schema forbids any value")
        return
    if "$ref" in schema:
        node = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        merged = dict(node)
        merged.update({k: v for k, v in schema.items() if k != "$ref"})
        schema = merged
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPES[x](value) for x in types):
            errs.append(f"{path or '$'}: expected type {'/'.join(types)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path or '$'}: {value!r} not in {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path or '$'}: must equal {schema['const']!r}, got {value!r}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path or '$'}: {value!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path or '$'}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{path or '$'}: longer than maxLength {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path or '$'}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path or '$'}: {value} above maximum {schema['maximum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errs.append(f"{path or '$'}: {value} not above exclusiveMinimum {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errs.append(f"{path or '$'}: {value} not below exclusiveMaximum {schema['exclusiveMaximum']}")
        if "multipleOf" in schema and abs(round(value / schema["multipleOf"]) * schema["multipleOf"] - value) > 1e-9:
            errs.append(f"{path or '$'}: {value} is not a multiple of {schema['multipleOf']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path or '$'}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path or '$'}: more than maxItems {schema['maxItems']}")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errs.append(f"{path or '$'}: items are not unique")
        if "items" in schema:
            if isinstance(schema["items"], list):
                for i, (sub, item) in enumerate(zip(schema["items"], value)):
                    _check(sub, item, f"{path}[{i}]", errs)
            else:
                for i, item in enumerate(value):
                    _check(schema["items"], item, f"{path}[{i}]", errs)
        if "contains" in schema:
            if not any(_ok(schema["contains"], item) for item in value):
                errs.append(f"{path or '$'}: no element satisfies `contains`")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path or '$'}: missing required field {k!r}")
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errs.append(f"{path or '$'}: fewer than minProperties {schema['minProperties']}")
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            errs.append(f"{path or '$'}: more than maxProperties {schema['maxProperties']}")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in value:
                _check(sub, value[k], f"{path}.{k}" if path else k, errs)
        ap = schema.get("additionalProperties", True)
        if ap is False:
            for k in value:
                if k not in props:
                    errs.append(f"{path or '$'}: additional property {k!r} not allowed")
        elif isinstance(ap, dict):
            for k in value:
                if k not in props:
                    _check(ap, value[k], f"{path}.{k}" if path else k, errs)
    for sub in schema.get("allOf", []):
        _check(sub, value, path, errs)
    if "anyOf" in schema and not any(_ok(s, value) for s in schema["anyOf"]):
        errs.append(f"{path or '$'}: matches none of anyOf")
    if "oneOf" in schema and sum(_ok(s, value) for s in schema["oneOf"]) != 1:
        errs.append(f"{path or '$'}: must match exactly one of oneOf")
    if "not" in schema and _ok(schema["not"], value):
        errs.append(f"{path or '$'}: matches forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _ok(schema["if"], value) else "else"
        if branch in schema:
            _check(schema[branch], value, path, errs)


def _ok(schema, value) -> bool:
    tmp: list[str] = []
    _check(schema, value, "", tmp)
    return not tmp

def _project(starting_users: int, k: float, cycle_days: float, days: int) -> float:
    """Same model as templates/loop-projection.py: no churn, geometric below K 1."""
    cycles = days / cycle_days
    if k >= 1:
        return starting_users * (k ** cycles)
    return starting_users * (1 - k ** (cycles + 1)) / (1 - k)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    kf = obj.get("k_factor") or {}
    i = (kf.get("invites_per_active_user") or {}).get("value")
    c = (kf.get("accept_rate_per_invite") or {}).get("value")
    k = kf.get("k")
    if isinstance(i, (int, float)) and isinstance(c, (int, float)) and isinstance(k, (int, float)):
        want = round(i * c, 3)
        if abs(k - want) > 0.00051:
            errs.append(f"k_factor.k {k} is not invites_per_active_user x accept_rate_per_invite = {want} (r-k-factor-decomposed)")
    kt = obj.get("k_target") or {}
    if isinstance(k, (int, float)) and isinstance(kt.get("current_k"), (int, float)) and abs(kt["current_k"] - k) > 0.00051:
        errs.append(f"k_target.current_k {kt['current_k']} differs from k_factor.k {k} (r-k-target-anchored-to-baseline)")
    if isinstance(kt.get("target_k"), (int, float)):
        want_kind = "self_sustaining" if kt["target_k"] >= 1 else "increment"
        if kt.get("kind") != want_kind:
            errs.append(f"k_target.kind must be {want_kind!r} for target_k {kt['target_k']} (r-k-target-anchored-to-baseline)")
        if isinstance(kt.get("current_k"), (int, float)) and kt["target_k"] <= kt["current_k"]:
            errs.append(f"k_target.target_k {kt['target_k']} is not above current_k {kt['current_k']} (r-k-target-anchored-to-baseline)")
    ct = (obj.get("cycle_time") or {}).get("days")
    pr = obj.get("projection") or {}
    if isinstance(k, (int, float)) and isinstance(ct, (int, float)) and ct > 0 and isinstance(pr.get("starting_users"), int) and isinstance(pr.get("days"), int):
        want = _project(pr["starting_users"], k, ct, pr["days"])
        if isinstance(pr.get("projected_users"), int) and abs(pr["projected_users"] - want) > max(1.0, 0.01 * want):
            errs.append(f"projection.projected_users {pr['projected_users']} is not what templates/loop-projection.py gives for K {k} and a {ct}-day cycle over {pr['days']} days: {want:.0f} (r-cycle-time-measured-and-projected)")
    steps = {s.get("name"): s.get("conversion") for s in obj.get("invitee_path") or [] if isinstance(s, dict)}
    for n, e in enumerate(obj.get("friction_experiments") or []):
        if e.get("target_step") not in steps:
            errs.append(f"friction_experiments[{n}].target_step {e.get('target_step')!r} is not a step of invitee_path (r-friction-steps-capped)")
        elif isinstance(e.get("current_conversion"), (int, float)) and abs(e["current_conversion"] - steps[e["target_step"]]) > 0.0051:
            errs.append(f"friction_experiments[{n}].current_conversion {e['current_conversion']} is not the measured conversion {steps[e['target_step']]} of step {e['target_step']!r} (r-friction-steps-capped)")
        if isinstance(e.get("expected_conversion"), (int, float)) and isinstance(e.get("current_conversion"), (int, float)) and e["expected_conversion"] <= e["current_conversion"]:
            errs.append(f"friction_experiments[{n}]: expected_conversion must be above current_conversion (r-friction-steps-capped)")
    names = {e.get("name") for e in obj.get("events") or []}
    for want in ("invite_shown", "invite_sent", "invite_opened", "invite_accepted", "invitee_activated"):
        if want not in names:
            errs.append(f"events: {want} is missing; all five loop events are required (r-loop-events-instrumented)")
    inc = obj.get("incentive")
    cd = obj.get("consent_and_disclosure") or {}
    if inc is not None and cd.get("compensation_disclosure") == "not_applicable":
        errs.append("consent_and_disclosure.compensation_disclosure is not_applicable while the loop pays a reward; disclose it in the message or on the landing page (r-referral-consent-and-disclosure)")
    return errs


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(SCHEMA, obj, "", errs)
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
        prog="validate-growth-viral-loops.py",
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
