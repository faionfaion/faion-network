#!/usr/bin/env python3
"""validate-growth-experiment-design.py

Validate the artefact produced by the growth-experiment-design methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/growth-experiment-design.json',
 'title': 'Growth Experiment Design spec',
 'type': 'object',
 'required': ['experiment_id',
              'hypothesis',
              'guardrails',
              'ice',
              'sample_size',
              'assignment',
              'instrumentation',
              'schedule',
              'srm_check',
              'status',
              'write_up',
              'counts_toward_velocity'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'score': {'type': 'integer', 'minimum': 1, 'maximum': 10},
                 'pct': {'type': 'number'}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'experiment_id': {'type': 'string', 'pattern': '^exp-[a-z0-9]+(-[a-z0-9]+)*$'},
                'hypothesis': {'type': 'object',
                               'required': ['change',
                                            'segment',
                                            'primary_metric',
                                            'minimum_effect_pct',
                                            'mechanism'],
                               'additionalProperties': False,
                               'properties': {'change': {'type': 'string', 'minLength': 10},
                                              'segment': {'type': 'string', 'minLength': 3},
                                              'primary_metric': {'type': 'string',
                                                                 'minLength': 3,
                                                                 'not': {'enum': ['engagement',
                                                                                  'activation',
                                                                                  'growth',
                                                                                  'usage',
                                                                                  'satisfaction']}},
                                              'minimum_effect_pct': {'type': 'number',
                                                                     'exclusiveMinimum': 0},
                                              'mechanism': {'type': 'string', 'minLength': 15}}},
                'guardrails': {'type': 'array',
                               'minItems': 3,
                               'items': {'type': 'object',
                                         'required': ['name', 'category', 'stop_threshold'],
                                         'additionalProperties': False,
                                         'properties': {'name': {'type': 'string', 'minLength': 3},
                                                        'category': {'type': 'string',
                                                                     'enum': ['revenue_or_conversion',
                                                                              'retention',
                                                                              'performance_or_error']},
                                                        'stop_threshold': {'type': 'string',
                                                                           'minLength': 3}}}},
                'ice': {'type': 'object',
                        'required': ['impact',
                                     'confidence',
                                     'ease',
                                     'criteria_ref',
                                     'confidence_evidence',
                                     'backlog_rank'],
                        'additionalProperties': False,
                        'properties': {'impact': {'$ref': '#/definitions/score'},
                                       'confidence': {'$ref': '#/definitions/score'},
                                       'ease': {'$ref': '#/definitions/score'},
                                       'criteria_ref': {'type': 'string', 'minLength': 3},
                                       'confidence_evidence': {'type': ['string', 'null'],
                                                               'minLength': 10},
                                       'backlog_rank': {'type': 'integer', 'minimum': 1}},
                        'if': {'properties': {'confidence': {'minimum': 4}}},
                        'then': {'properties': {'confidence_evidence': {'type': 'string'}}}},
                'sample_size': {'type': 'object',
                                'required': ['baseline_rate',
                                             'minimum_detectable_effect_pct',
                                             'alpha',
                                             'power',
                                             'required_per_variant',
                                             'eligible_daily_traffic',
                                             'duration_weeks'],
                                'additionalProperties': False,
                                'properties': {'baseline_rate': {'type': 'number',
                                                                 'exclusiveMinimum': 0,
                                                                 'exclusiveMaximum': 1},
                                               'minimum_detectable_effect_pct': {'type': 'number',
                                                                                 'exclusiveMinimum': 0},
                                               'alpha': {'const': 0.05},
                                               'power': {'const': 0.8},
                                               'required_per_variant': {'type': 'integer',
                                                                        'minimum': 1},
                                               'eligible_daily_traffic': {'type': 'integer',
                                                                          'minimum': 1},
                                               'duration_weeks': {'type': 'integer',
                                                                  'minimum': 1,
                                                                  'maximum': 8}}},
                'assignment': {'type': 'object',
                               'required': ['platform',
                                            'design',
                                            'hash_key',
                                            'control_variant',
                                            'allocation'],
                               'additionalProperties': False,
                               'properties': {'platform': {'type': 'string',
                                                           'enum': ['launchdarkly',
                                                                    'statsig',
                                                                    'unleash',
                                                                    'growthbook',
                                                                    'optimizely',
                                                                    'internal']},
                                              'design': {'const': 'randomised_controlled'},
                                              'hash_key': {'type': 'string',
                                                           'enum': ['user_id', 'account_id']},
                                              'control_variant': {'type': 'string', 'minLength': 1},
                                              'allocation': {'type': 'array',
                                                             'minItems': 2,
                                                             'items': {'type': 'object',
                                                                       'required': ['variant',
                                                                                    'percent'],
                                                                       'additionalProperties': False,
                                                                       'properties': {'variant': {'type': 'string',
                                                                                                  'minLength': 1},
                                                                                      'percent': {'type': 'number',
                                                                                                  'exclusiveMinimum': 0,
                                                                                                  'maximum': 100}}}}}},
                'instrumentation': {'type': 'object',
                                    'required': ['exposure_event',
                                                 'exposure_logged_at',
                                                 'analytics_destination',
                                                 'metric_events',
                                                 'playback'],
                                    'additionalProperties': False,
                                    'properties': {'exposure_event': {'$ref': '#/definitions/event_name'},
                                                   'exposure_logged_at': {'const': 'variant_seen'},
                                                   'analytics_destination': {'type': 'string',
                                                                             'minLength': 3},
                                                   'metric_events': {'type': 'array',
                                                                     'minItems': 1,
                                                                     'items': {'$ref': '#/definitions/event_name'}},
                                                   'playback': {'type': 'object',
                                                                'required': ['cohort',
                                                                             'status',
                                                                             'performed_on',
                                                                             'events_verified'],
                                                                'additionalProperties': False,
                                                                'properties': {'cohort': {'type': 'string',
                                                                                          'enum': ['staging',
                                                                                                   'one_percent']},
                                                                               'status': {'type': 'string',
                                                                                          'enum': ['pending',
                                                                                                   'passed']},
                                                                               'performed_on': {'anyOf': [{'$ref': '#/definitions/date'},
                                                                                                          {'type': 'null'}]},
                                                                               'events_verified': {'type': 'array',
                                                                                                   'items': {'$ref': '#/definitions/event_name'}}}}}},
                'schedule': {'type': 'object',
                             'required': ['launch_date', 'stop_date', 'sequential_method'],
                             'additionalProperties': False,
                             'properties': {'launch_date': {'$ref': '#/definitions/date'},
                                            'stop_date': {'$ref': '#/definitions/date'},
                                            'sequential_method': {'type': ['string', 'null'],
                                                                  'minLength': 3}}},
                'srm_check': {'type': 'object',
                              'required': ['status', 'chi_square_p', 'invalidates_below'],
                              'additionalProperties': False,
                              'properties': {'status': {'type': 'string',
                                                        'enum': ['pending', 'passed', 'failed']},
                                             'chi_square_p': {'type': ['number', 'null'],
                                                              'minimum': 0,
                                                              'maximum': 1},
                                             'invalidates_below': {'const': 0.001}},
                              'if': {'properties': {'status': {'enum': ['passed', 'failed']}}},
                              'then': {'properties': {'chi_square_p': {'type': 'number'}}}},
                'status': {'type': 'string',
                           'enum': ['designed',
                                    'playback_passed',
                                    'running',
                                    'stopped',
                                    'written_up']},
                'write_up': {'anyOf': [{'type': 'null'},
                                       {'type': 'object',
                                        'required': ['date',
                                                     'log_entry',
                                                     'decision',
                                                     'primary_effect',
                                                     'guardrail_results',
                                                     'srm_p',
                                                     'belief_changed'],
                                        'additionalProperties': False,
                                        'properties': {'date': {'$ref': '#/definitions/date'},
                                                       'log_entry': {'type': 'string',
                                                                     'minLength': 3},
                                                       'decision': {'type': 'string',
                                                                    'enum': ['ship',
                                                                             'iterate',
                                                                             'kill']},
                                                       'primary_effect': {'type': 'object',
                                                                          'required': ['observed_pct',
                                                                                       'ci_low_pct',
                                                                                       'ci_high_pct'],
                                                                          'additionalProperties': False,
                                                                          'properties': {'observed_pct': {'type': 'number'},
                                                                                         'ci_low_pct': {'type': 'number'},
                                                                                         'ci_high_pct': {'type': 'number'}}},
                                                       'guardrail_results': {'type': 'array',
                                                                             'minItems': 3,
                                                                             'items': {'type': 'object',
                                                                                       'required': ['name',
                                                                                                    'observed',
                                                                                                    'breached'],
                                                                                       'additionalProperties': False,
                                                                                       'properties': {'name': {'type': 'string',
                                                                                                               'minLength': 3},
                                                                                                      'observed': {'type': 'string',
                                                                                                                   'minLength': 1},
                                                                                                      'breached': {'type': 'boolean'}}}},
                                                       'srm_p': {'type': 'number',
                                                                 'minimum': 0,
                                                                 'maximum': 1},
                                                       'belief_changed': {'type': 'string',
                                                                          'minLength': 20}}}]},
                'counts_toward_velocity': {'type': 'boolean'}}}

OK = {'experiment_id': 'exp-checkout-trust-badges',
 'hypothesis': {'change': 'show payment-provider trust badges under the card form',
                'segment': 'first-time buyers on web checkout',
                'primary_metric': 'checkout_to_paid conversion rate',
                'minimum_effect_pct': 5,
                'mechanism': 'first-time buyers abandon at the card form because they doubt the '
                             'payment is secure'},
 'guardrails': [{'name': 'average order value',
                 'category': 'revenue_or_conversion',
                 'stop_threshold': 'drop of 3 percent or more versus control'},
                {'name': '30-day repeat purchase rate',
                 'category': 'retention',
                 'stop_threshold': 'drop of 2 points or more versus control'},
                {'name': 'checkout page p95 load time',
                 'category': 'performance_or_error',
                 'stop_threshold': 'above 2.5 s or error rate above 0.5 percent'}],
 'ice': {'impact': 7,
         'confidence': 6,
         'ease': 8,
         'criteria_ref': 'growth/ice-criteria.md',
         'confidence_evidence': 'exp-checkout-copy-2025q4 moved the same step by 3 percent; 14 of '
                                '20 exit-survey answers cite payment security',
         'backlog_rank': 2},
 'sample_size': {'baseline_rate': 0.042,
                 'minimum_detectable_effect_pct': 5,
                 'alpha': 0.05,
                 'power': 0.8,
                 'required_per_variant': 143000,
                 'eligible_daily_traffic': 15000,
                 'duration_weeks': 3},
 'assignment': {'platform': 'statsig',
                'design': 'randomised_controlled',
                'hash_key': 'user_id',
                'control_variant': 'control',
                'allocation': [{'variant': 'control', 'percent': 50},
                               {'variant': 'trust_badges', 'percent': 50}]},
 'instrumentation': {'exposure_event': 'checkout_card_form_viewed',
                     'exposure_logged_at': 'variant_seen',
                     'analytics_destination': 'BigQuery dataset analytics.events',
                     'metric_events': ['order_paid',
                                       'order_paid_value',
                                       'repeat_order_paid',
                                       'checkout_page_timing',
                                       'checkout_error'],
                     'playback': {'cohort': 'one_percent',
                                  'status': 'passed',
                                  'performed_on': '2026-03-02',
                                  'events_verified': ['checkout_card_form_viewed',
                                                      'order_paid',
                                                      'order_paid_value',
                                                      'repeat_order_paid',
                                                      'checkout_page_timing',
                                                      'checkout_error']}},
 'schedule': {'launch_date': '2026-03-04', 'stop_date': '2026-03-25', 'sequential_method': None},
 'srm_check': {'status': 'passed', 'chi_square_p': 0.41, 'invalidates_below': 0.001},
 'status': 'written_up',
 'write_up': {'date': '2026-03-30',
              'log_entry': 'growth/experiment-log.md#exp-checkout-trust-badges',
              'decision': 'ship',
              'primary_effect': {'observed_pct': 6.8, 'ci_low_pct': 1.9, 'ci_high_pct': 11.7},
              'guardrail_results': [{'name': 'average order value',
                                     'observed': '+0.4 percent',
                                     'breached': False},
                                    {'name': '30-day repeat purchase rate',
                                     'observed': '-0.3 points',
                                     'breached': False},
                                    {'name': 'checkout page p95 load time',
                                     'observed': '1.9 s, error rate 0.2 percent',
                                     'breached': False}],
              'srm_p': 0.41,
              'belief_changed': 'Payment-security doubt, not price, is the main reason first-time '
                                'buyers leave the card form.'},
 'counts_toward_velocity': True}

BAD = {'experiment_id': 'exp-new-onboarding',
 'hypothesis': {'change': 'launch the redesigned onboarding flow',
                'segment': 'all new users',
                'primary_metric': 'engagement',
                'minimum_effect_pct': 0,
                'mechanism': 'a better onboarding will make users more engaged'},
 'guardrails': [{'name': 'support tickets',
                 'category': 'performance_or_error',
                 'stop_threshold': 'noticeable increase'}],
 'ice': {'impact': 9,
         'confidence': 8,
         'ease': 5,
         'criteria_ref': 'growth/ice-criteria.md',
         'confidence_evidence': None,
         'backlog_rank': 1},
 'sample_size': {'baseline_rate': 0.31,
                 'minimum_detectable_effect_pct': 3,
                 'alpha': 0.1,
                 'power': 0.8,
                 'required_per_variant': 4000,
                 'eligible_daily_traffic': 600,
                 'duration_weeks': 10},
 'assignment': {'platform': 'internal',
                'design': 'pre_post',
                'hash_key': 'session_id',
                'control_variant': 'last_week',
                'allocation': [{'variant': 'new_onboarding', 'percent': 100}]},
 'instrumentation': {'exposure_event': 'onboarding_assigned',
                     'exposure_logged_at': 'assignment',
                     'analytics_destination': 'Amplitude',
                     'metric_events': ['session_started'],
                     'playback': {'cohort': 'staging',
                                  'status': 'pending',
                                  'performed_on': None,
                                  'events_verified': []}},
 'schedule': {'launch_date': '2026-03-04', 'stop_date': '2026-03-08', 'sequential_method': None},
 'srm_check': {'status': 'pending', 'chi_square_p': None, 'invalidates_below': 0.001},
 'status': 'running',
 'write_up': None,
 'counts_toward_velocity': True}


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

import math
from datetime import date, timedelta


def _d(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    hyp = obj.get("hypothesis") or {}
    cats = {g.get("category") for g in obj.get("guardrails") or []}
    for c in ("revenue_or_conversion", "retention", "performance_or_error"):
        if c not in cats:
            errs.append(f"guardrails: no guardrail of category {c!r} (r-one-primary-metric-plus-guardrails)")
    ss = obj.get("sample_size") or {}
    if ss.get("minimum_detectable_effect_pct") != hyp.get("minimum_effect_pct"):
        errs.append("sample_size.minimum_detectable_effect_pct must equal hypothesis.minimum_effect_pct (r-sample-size-computed-before-launch)")
    p, mde = ss.get("baseline_rate"), ss.get("minimum_detectable_effect_pct")
    if p and mde:
        delta = p * mde / 100.0
        need = 2 * (1.96 + 0.8416) ** 2 * p * (1 - p) / (delta ** 2)
        if ss.get("required_per_variant", 0) < 0.8 * need:
            errs.append(f"sample_size.required_per_variant {ss.get('required_per_variant')} is below the {math.ceil(need)} that baseline {p}, MDE {mde} percent, alpha 0.05 and power 0.8 imply (r-sample-size-computed-before-launch)")
    alloc = (obj.get("assignment") or {}).get("allocation") or []
    total = sum(a.get("percent", 0) for a in alloc)
    if alloc and abs(total - 100) > 0.01:
        errs.append(f"assignment.allocation percentages sum to {total}, not 100 (r-control-group-randomised-by-flag)")
    names = {a.get("variant") for a in alloc}
    ctrl = (obj.get("assignment") or {}).get("control_variant")
    if alloc and ctrl not in names:
        errs.append(f"assignment.control_variant {ctrl!r} is not one of the allocated variants (r-control-group-randomised-by-flag)")
    if alloc and ss.get("required_per_variant") and ss.get("eligible_daily_traffic"):
        smallest = min(a.get("percent", 0) for a in alloc) / 100.0
        if smallest > 0:
            days = ss["required_per_variant"] / (ss["eligible_daily_traffic"] * smallest)
            weeks = max(1, math.ceil(days / 7))
            if ss.get("duration_weeks") != weeks and weeks <= 8:
                errs.append(f"sample_size.duration_weeks must be {weeks}: {ss['required_per_variant']} per variant at {ss['eligible_daily_traffic']} eligible users/day and a {smallest:.0%} smallest allocation, rounded up to whole weeks (r-sample-size-computed-before-launch)")
            if weeks > 8:
                errs.append(f"the smallest allocation needs {weeks} weeks; redesign for a larger effect, a broader segment or a proxy metric instead of launching (r-sample-size-computed-before-launch)")
    sched = obj.get("schedule") or {}
    launch, stop = _d(sched.get("launch_date")), _d(sched.get("stop_date"))
    if launch and stop and ss.get("duration_weeks") and stop < launch + timedelta(weeks=ss["duration_weeks"]):
        errs.append(f"schedule.stop_date {stop} is earlier than launch_date plus {ss['duration_weeks']} weeks ({launch + timedelta(weeks=ss['duration_weeks'])}) (r-fixed-stop-date-no-peeking-srm-check)")
    inst = obj.get("instrumentation") or {}
    pb = inst.get("playback") or {}
    if pb.get("status") == "passed":
        wanted = [inst.get("exposure_event")] + list(inst.get("metric_events") or [])
        missing = [e for e in wanted if e not in (pb.get("events_verified") or [])]
        if missing:
            errs.append(f"instrumentation.playback.events_verified lacks {missing}; every exposure and metric event must land with experiment and variant id before ramp (r-instrumentation-playback-before-ramp)")
        if not pb.get("performed_on"):
            errs.append("instrumentation.playback.performed_on is required once the playback passed (r-instrumentation-playback-before-ramp)")
    status = obj.get("status")
    srm = obj.get("srm_check") or {}
    if status in ("running", "stopped", "written_up") and pb.get("status") != "passed":
        errs.append(f"status {status!r} with playback.status {pb.get('status')!r}: no ramp above the smoke-test cohort before the playback passes (r-instrumentation-playback-before-ramp)")
    if status in ("stopped", "written_up") and srm.get("status") == "pending":
        errs.append(f"status {status!r} with srm_check.status pending: record the SRM check before any result is read (r-fixed-stop-date-no-peeking-srm-check)")
    pval = srm.get("chi_square_p")
    if isinstance(pval, (int, float)):
        if pval < 0.001 and srm.get("status") != "failed":
            errs.append(f"srm_check.chi_square_p {pval} is below 0.001 but status is {srm.get('status')!r}; the run is invalid (r-fixed-stop-date-no-peeking-srm-check)")
        if pval >= 0.001 and srm.get("status") == "failed":
            errs.append(f"srm_check.status failed with chi_square_p {pval} at or above 0.001 (r-fixed-stop-date-no-peeking-srm-check)")
    wu = obj.get("write_up")
    if status == "written_up" and wu is None:
        errs.append("status written_up requires a write_up (r-write-up-every-experiment)")
    if wu is not None and status != "written_up":
        errs.append(f"write_up present but status is {status!r}, not written_up (r-write-up-every-experiment)")
    if obj.get("counts_toward_velocity") and wu is None:
        errs.append("counts_toward_velocity is true without a write_up; unwritten experiments do not count (r-write-up-every-experiment)")
    if isinstance(wu, dict):
        wd = _d(wu.get("date"))
        if wd and stop and (wd < stop or wd > stop + timedelta(days=7)):
            errs.append(f"write_up.date {wd} is not within seven days after stop_date {stop} (r-write-up-every-experiment)")
        breached = [g.get("name") for g in wu.get("guardrail_results") or [] if g.get("breached")]
        if wu.get("decision") == "ship" and breached:
            errs.append(f"write_up.decision ship with breached guardrails {breached}; a guardrail breach vetoes a ship (r-one-primary-metric-plus-guardrails)")
        if wu.get("decision") == "ship" and srm.get("status") == "failed":
            errs.append("write_up.decision ship on a failed SRM check; every downstream number is invalid (r-fixed-stop-date-no-peeking-srm-check)")
        if isinstance(pval, (int, float)) and wu.get("srm_p") != pval:
            errs.append(f"write_up.srm_p {wu.get('srm_p')} differs from srm_check.chi_square_p {pval} (r-write-up-every-experiment)")
        gnames = {g.get("name") for g in obj.get("guardrails") or []}
        reported = {g.get("name") for g in wu.get("guardrail_results") or []}
        for g in sorted(gnames - reported):
            errs.append(f"write_up.guardrail_results lacks guardrail {g!r} (r-write-up-every-experiment)")
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
        prog="validate-growth-experiment-design.py",
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
