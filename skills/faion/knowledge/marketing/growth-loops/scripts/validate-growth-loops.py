#!/usr/bin/env python3
"""validate-growth-loops.py

Validate the artefact produced by the growth-loops methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/growth-loops.json',
 'title': 'Growth Loops spec',
 'type': 'object',
 'required': ['loop_name',
              'loop_type',
              'input_source',
              'secondary_loops',
              'stages',
              'stage_metrics',
              'efficiency',
              'projection',
              'friction_map',
              'cac_payback',
              'quality_guardrail'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'loop_type': {'type': 'string',
                               'enum': ['viral',
                                        'ugc_search',
                                        'paid',
                                        'network_effect',
                                        'supply_side']},
                 'transition': {'type': 'string',
                                'enum': ['input-action', 'action-output', 'output-fuel_back']},
                 'stage': {'type': 'object',
                           'required': ['name', 'event', 'unit'],
                           'additionalProperties': False,
                           'properties': {'name': {'type': 'string', 'minLength': 3},
                                          'event': {'$ref': '#/definitions/event_name'},
                                          'unit': {'type': 'string', 'minLength': 3}}},
                 'payback': {'type': 'object',
                             'required': ['blended_cac', 'payback_months'],
                             'additionalProperties': False,
                             'properties': {'blended_cac': {'type': 'number', 'minimum': 0},
                                            'payback_months': {'type': 'number', 'minimum': 0}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'loop_name': {'type': 'string', 'minLength': 3},
                'loop_type': {'$ref': '#/definitions/loop_type'},
                'input_source': {'type': 'string',
                                 'enum': ['user_action', 'content', 'capital', 'supply']},
                'secondary_loops': {'type': 'array',
                                    'items': {'type': 'object',
                                              'required': ['type', 'note'],
                                              'additionalProperties': False,
                                              'properties': {'type': {'$ref': '#/definitions/loop_type'},
                                                             'note': {'type': 'string',
                                                                      'minLength': 10}}}},
                'stages': {'type': 'object',
                           'required': ['input', 'action', 'output', 'fuel_back'],
                           'additionalProperties': False,
                           'properties': {'input': {'$ref': '#/definitions/stage'},
                                          'action': {'$ref': '#/definitions/stage'},
                                          'output': {'$ref': '#/definitions/stage'},
                                          'fuel_back': {'$ref': '#/definitions/stage'}}},
                'stage_metrics': {'type': 'array',
                                  'minItems': 3,
                                  'maxItems': 3,
                                  'items': {'type': 'object',
                                            'required': ['transition',
                                                         'event',
                                                         'numerator',
                                                         'denominator',
                                                         'value',
                                                         'basis',
                                                         'measured_on',
                                                         'sample_size'],
                                            'additionalProperties': False,
                                            'properties': {'transition': {'$ref': '#/definitions/transition'},
                                                           'event': {'$ref': '#/definitions/event_name'},
                                                           'numerator': {'type': 'string',
                                                                         'minLength': 5},
                                                           'denominator': {'type': 'string',
                                                                           'minLength': 5},
                                                           'value': {'type': 'number',
                                                                     'minimum': 0},
                                                           'basis': {'type': 'string',
                                                                     'enum': ['measured',
                                                                              'assumption']},
                                                           'measured_on': {'anyOf': [{'$ref': '#/definitions/date'},
                                                                                     {'type': 'null'}]},
                                                           'sample_size': {'type': ['integer',
                                                                                    'null'],
                                                                           'minimum': 1}},
                                            'if': {'properties': {'basis': {'const': 'measured'}}},
                                            'then': {'properties': {'measured_on': {'type': 'string'},
                                                                    'sample_size': {'type': 'integer'}}}}},
                'efficiency': {'type': 'object',
                               'required': ['k',
                                            'cycle_time_days',
                                            'reading',
                                            'multiplier',
                                            'growth_rate_per_cycle'],
                               'additionalProperties': False,
                               'properties': {'k': {'type': 'number', 'minimum': 0},
                                              'cycle_time_days': {'type': 'number',
                                                                  'exclusiveMinimum': 0},
                                              'reading': {'type': 'string',
                                                          'enum': ['amplifier', 'self_sustaining']},
                                              'multiplier': {'type': ['number', 'null'],
                                                             'minimum': 1},
                                              'growth_rate_per_cycle': {'type': ['number', 'null'],
                                                                        'minimum': 0}},
                               'if': {'properties': {'k': {'exclusiveMaximum': 1}}},
                               'then': {'properties': {'reading': {'const': 'amplifier'},
                                                       'multiplier': {'type': 'number'},
                                                       'growth_rate_per_cycle': {'type': 'null'}}},
                               'else': {'properties': {'reading': {'const': 'self_sustaining'},
                                                       'multiplier': {'type': 'null'},
                                                       'growth_rate_per_cycle': {'type': 'number'}}}},
                'projection': {'type': 'object',
                               'required': ['horizon_days',
                                            'cycles',
                                            'decay',
                                            'rests_on_assumption',
                                            'headline',
                                            'cohorts'],
                               'additionalProperties': False,
                               'properties': {'horizon_days': {'type': 'integer', 'minimum': 90},
                                              'cycles': {'type': 'integer', 'minimum': 3},
                                              'decay': {'type': 'object',
                                                        'required': ['kind', 'rate_per_cycle'],
                                                        'additionalProperties': False,
                                                        'properties': {'kind': {'type': 'string',
                                                                                'enum': ['contributor_churn',
                                                                                         'content_decay',
                                                                                         'audience_saturation',
                                                                                         'rising_cpm']},
                                                                       'rate_per_cycle': {'type': 'number',
                                                                                          'exclusiveMinimum': 0,
                                                                                          'maximum': 1}}},
                                              'rests_on_assumption': {'type': 'boolean'},
                                              'headline': {'type': 'string', 'minLength': 20},
                                              'cohorts': {'type': 'array',
                                                          'minItems': 3,
                                                          'items': {'type': 'object',
                                                                    'required': ['cycle',
                                                                                 'external_inputs',
                                                                                 'loop_inputs',
                                                                                 'total_inputs'],
                                                                    'additionalProperties': False,
                                                                    'properties': {'cycle': {'type': 'integer',
                                                                                             'minimum': 1},
                                                                                   'external_inputs': {'type': 'integer',
                                                                                                       'minimum': 0},
                                                                                   'loop_inputs': {'type': 'integer',
                                                                                                   'minimum': 0},
                                                                                   'total_inputs': {'type': 'integer',
                                                                                                    'minimum': 0}}}}}},
                'friction_map': {'type': 'object',
                                 'required': ['bottleneck_stage',
                                              'bottleneck_value',
                                              'k_if_doubled',
                                              'experiments'],
                                 'additionalProperties': False,
                                 'properties': {'bottleneck_stage': {'$ref': '#/definitions/transition'},
                                                'bottleneck_value': {'type': 'number',
                                                                     'minimum': 0},
                                                'k_if_doubled': {'type': 'number', 'minimum': 0},
                                                'experiments': {'type': 'array',
                                                                'minItems': 1,
                                                                'items': {'type': 'object',
                                                                          'required': ['rank',
                                                                                       'name',
                                                                                       'stage',
                                                                                       'justification'],
                                                                          'additionalProperties': False,
                                                                          'properties': {'rank': {'type': 'integer',
                                                                                                  'minimum': 1},
                                                                                         'name': {'type': 'string',
                                                                                                  'minLength': 5},
                                                                                         'stage': {'$ref': '#/definitions/transition'},
                                                                                         'justification': {'type': ['string',
                                                                                                                    'null'],
                                                                                                           'minLength': 15}}}}}},
                'cac_payback': {'type': 'object',
                                'required': ['period_days',
                                             'attributed_by',
                                             'without_loop',
                                             'with_loop'],
                                'additionalProperties': False,
                                'properties': {'period_days': {'type': 'integer', 'minimum': 30},
                                               'attributed_by': {'$ref': '#/definitions/event_name'},
                                               'without_loop': {'$ref': '#/definitions/payback'},
                                               'with_loop': {'$ref': '#/definitions/payback'}}},
                'quality_guardrail': {'type': 'object',
                                      'required': ['metric',
                                                   'threshold',
                                                   'loop_cohort_value',
                                                   'baseline_value',
                                                   'status'],
                                      'additionalProperties': False,
                                      'properties': {'metric': {'type': 'string',
                                                                'enum': ['activation_rate',
                                                                         'd30_retention',
                                                                         'indexed_and_trafficked_share']},
                                                     'threshold': {'type': 'number',
                                                                   'minimum': 0,
                                                                   'maximum': 1},
                                                     'loop_cohort_value': {'type': 'number',
                                                                           'minimum': 0,
                                                                           'maximum': 1},
                                                     'baseline_value': {'type': ['number', 'null'],
                                                                        'minimum': 0,
                                                                        'maximum': 1},
                                                     'status': {'type': 'string',
                                                                'enum': ['within', 'breached']}}}}}

OK = {'loop_name': 'external document share loop',
 'loop_type': 'viral',
 'input_source': 'user_action',
 'secondary_loops': [{'type': 'ugc_search',
                      'note': 'public templates indexed by search; tracked separately, not in this '
                              'projection'}],
 'stages': {'input': {'name': 'new workspace signup',
                      'event': 'signup_completed',
                      'unit': 'new signups'},
            'action': {'name': 'user shares a document with an external recipient',
                       'event': 'share_sent',
                       'unit': 'shares sent'},
            'output': {'name': 'external recipient opens the shared document',
                       'event': 'share_viewed',
                       'unit': 'recipient views'},
            'fuel_back': {'name': 'recipient signs up from the shared document',
                          'event': 'signup_via_share',
                          'unit': 'new signups'}},
 'stage_metrics': [{'transition': 'input-action',
                    'event': 'share_sent',
                    'numerator': 'signups that sent at least one external share within 14 days',
                    'denominator': 'signups in the cohort',
                    'value': 0.45,
                    'basis': 'measured',
                    'measured_on': '2026-05-04',
                    'sample_size': 8400},
                   {'transition': 'action-output',
                    'event': 'share_viewed',
                    'numerator': 'distinct external recipients who viewed',
                    'denominator': 'sharers',
                    'value': 2.4,
                    'basis': 'measured',
                    'measured_on': '2026-05-04',
                    'sample_size': 3780},
                   {'transition': 'output-fuel_back',
                    'event': 'signup_via_share',
                    'numerator': 'viewers who signed up within 14 days',
                    'denominator': 'distinct viewers',
                    'value': 0.12,
                    'basis': 'measured',
                    'measured_on': '2026-05-04',
                    'sample_size': 9072}],
 'efficiency': {'k': 0.13,
                'cycle_time_days': 9,
                'reading': 'amplifier',
                'multiplier': 1.15,
                'growth_rate_per_cycle': None},
 'projection': {'horizon_days': 120,
                'cycles': 13,
                'decay': {'kind': 'audience_saturation', 'rate_per_cycle': 0.05},
                'rests_on_assumption': False,
                'headline': 'The loop adds about 13 percent on top of external signups and '
                            'saturates toward 1,120 signups per 9-day cycle at 1,000 external '
                            'inputs.',
                'cohorts': [{'cycle': 1,
                             'external_inputs': 1000,
                             'loop_inputs': 0,
                             'total_inputs': 1000},
                            {'cycle': 2,
                             'external_inputs': 1000,
                             'loop_inputs': 124,
                             'total_inputs': 1124},
                            {'cycle': 3,
                             'external_inputs': 1000,
                             'loop_inputs': 132,
                             'total_inputs': 1132},
                            {'cycle': 4,
                             'external_inputs': 1000,
                             'loop_inputs': 126,
                             'total_inputs': 1126}]},
 'friction_map': {'bottleneck_stage': 'output-fuel_back',
                  'bottleneck_value': 0.12,
                  'k_if_doubled': 0.26,
                  'experiments': [{'rank': 1,
                                   'name': 'signup call to action on the shared-document view page',
                                   'stage': 'output-fuel_back',
                                   'justification': None},
                                  {'rank': 2,
                                   'name': 'prompt to share at first document completion',
                                   'stage': 'input-action',
                                   'justification': 'the view page redesign is blocked on the '
                                                    'design system release for two weeks; this '
                                                    'experiment is already built'}]},
 'cac_payback': {'period_days': 90,
                 'attributed_by': 'signup_via_share',
                 'without_loop': {'blended_cac': 310, 'payback_months': 14.2},
                 'with_loop': {'blended_cac': 271, 'payback_months': 12.4}},
 'quality_guardrail': {'metric': 'd30_retention',
                       'threshold': 0.3,
                       'loop_cohort_value': 0.33,
                       'baseline_value': 0.34,
                       'status': 'within'}}

BAD = {'loop_name': 'growth flywheel',
 'loop_type': 'viral and content',
 'input_source': 'user_action',
 'secondary_loops': [],
 'stages': {'input': {'name': 'new workspace signup',
                      'event': 'signup_completed',
                      'unit': 'new signups'},
            'action': {'name': 'user shares a document',
                       'event': 'share_sent',
                       'unit': 'shares sent'},
            'output': {'name': 'recipient opens the document',
                       'event': 'share_viewed',
                       'unit': 'recipient views'},
            'fuel_back': {'name': 'retained user comes back',
                          'event': 'session_started',
                          'unit': 'sessions'}},
 'stage_metrics': [{'transition': 'input-action',
                    'event': 'share_sent',
                    'numerator': 'signups that shared',
                    'denominator': 'signups in the cohort',
                    'value': 0.3,
                    'basis': 'benchmark',
                    'measured_on': None,
                    'sample_size': None},
                   {'transition': 'action-output',
                    'event': 'share_viewed',
                    'numerator': 'recipients who viewed',
                    'denominator': 'sharers',
                    'value': 2.4,
                    'basis': 'measured',
                    'measured_on': None,
                    'sample_size': None},
                   {'transition': 'output-fuel_back',
                    'event': 'session_started',
                    'numerator': 'viewers who signed up',
                    'denominator': 'distinct viewers',
                    'value': 0.12,
                    'basis': 'measured',
                    'measured_on': '2026-05-04',
                    'sample_size': 9072}],
 'efficiency': {'k': 0.6,
                'cycle_time_days': 9,
                'reading': 'self_sustaining',
                'multiplier': None,
                'growth_rate_per_cycle': None},
 'projection': {'horizon_days': 30,
                'cycles': 1,
                'decay': {'kind': 'none', 'rate_per_cycle': 0},
                'rests_on_assumption': False,
                'headline': 'Viral growth: signups double every month.',
                'cohorts': [{'cycle': 1,
                             'external_inputs': 1000,
                             'loop_inputs': 300,
                             'total_inputs': 1300}]},
 'friction_map': {'bottleneck_stage': 'input-action',
                  'bottleneck_value': 0.3,
                  'k_if_doubled': 1.2,
                  'experiments': []},
 'cac_payback': {'period_days': 90,
                 'attributed_by': 'organic',
                 'without_loop': {'blended_cac': 310, 'payback_months': 14.2},
                 'with_loop': {'blended_cac': 180, 'payback_months': 8}},
 'quality_guardrail': {'metric': 'd30_retention',
                       'threshold': 0.3,
                       'loop_cohort_value': 0.19,
                       'baseline_value': 0.34,
                       'status': 'within'}}


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


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    st = obj.get("stages") or {}
    inp, fb = st.get("input") or {}, st.get("fuel_back") or {}
    if inp.get("unit") and fb.get("unit") and inp["unit"] != fb["unit"]:
        errs.append(f"stages.fuel_back.unit {fb['unit']!r} differs from stages.input.unit {inp['unit']!r}; output must feed input in the same unit or the design is a funnel (r-loop-closes-output-into-input)")
    metrics = obj.get("stage_metrics") or []
    order = ["input-action", "action-output", "output-fuel_back"]
    seen = [m.get("transition") for m in metrics]
    if seen and seen != order:
        errs.append(f"stage_metrics transitions must be {order} in order, got {seen} (r-stage-conversion-measured-not-estimated)")
    fb_rows = [m for m in metrics if m.get("transition") == "output-fuel_back"]
    if fb_rows and fb.get("event") and fb_rows[0].get("event") != fb["event"]:
        errs.append(f"stage_metrics output-fuel_back event {fb_rows[0].get('event')!r} is not the fuel-back event {fb['event']!r} (r-loop-closes-output-into-input)")
    eff = obj.get("efficiency") or {}
    if metrics and all(isinstance(m.get("value"), (int, float)) for m in metrics):
        prod = 1.0
        for m in metrics:
            prod *= m["value"]
        if isinstance(eff.get("k"), (int, float)) and abs(round(prod, 2) - eff["k"]) > 0.0051:
            errs.append(f"efficiency.k {eff.get('k')} is not the product of the stage values {round(prod, 2)} (r-loop-efficiency-and-cycle-time)")
    k = eff.get("k")
    if isinstance(k, (int, float)):
        if k < 1 and isinstance(eff.get("multiplier"), (int, float)) and abs(round(1 / (1 - k), 2) - eff["multiplier"]) > 0.0051:
            errs.append(f"efficiency.multiplier must be 1 / (1 - k) = {round(1 / (1 - k), 2)} (r-loop-efficiency-and-cycle-time)")
        if k >= 1 and isinstance(eff.get("growth_rate_per_cycle"), (int, float)) and abs(round(k - 1, 2) - eff["growth_rate_per_cycle"]) > 0.0051:
            errs.append(f"efficiency.growth_rate_per_cycle must be k - 1 = {round(k - 1, 2)} per cycle (r-loop-efficiency-and-cycle-time)")
    pr = obj.get("projection") or {}
    ct = eff.get("cycle_time_days")
    if isinstance(ct, (int, float)) and isinstance(pr.get("horizon_days"), int):
        if pr["horizon_days"] < 3 * ct:
            errs.append(f"projection.horizon_days {pr['horizon_days']} covers fewer than three cycles of {ct} days (r-steady-state-projection-90-days)")
        if isinstance(pr.get("cycles"), int) and pr["cycles"] > pr["horizon_days"] / ct + 1e-9:
            errs.append(f"projection.cycles {pr['cycles']} does not fit in horizon_days {pr['horizon_days']} at {ct} days per cycle (r-steady-state-projection-90-days)")
    assumed = any(m.get("basis") == "assumption" for m in metrics)
    if pr and bool(pr.get("rests_on_assumption")) != assumed:
        errs.append(f"projection.rests_on_assumption must be {assumed}: {'a stage rate is an assumption' if assumed else 'every stage rate is measured'} (r-stage-conversion-measured-not-estimated)")
    if assumed and pr.get("headline") and "assumption" not in pr["headline"].lower():
        errs.append("projection.headline must say the projection rests on an assumption (r-stage-conversion-measured-not-estimated)")
    prev_total = None
    for i, c in enumerate(pr.get("cohorts") or []):
        if c.get("total_inputs") != c.get("external_inputs", 0) + c.get("loop_inputs", 0):
            errs.append(f"projection.cohorts[{i}]: total_inputs must be external_inputs + loop_inputs (r-steady-state-projection-90-days)")
        if i == 0 and c.get("loop_inputs", 0) > 0:
            errs.append("projection.cohorts[0]: the first cycle has no loop inputs yet (r-steady-state-projection-90-days)")
        if prev_total is not None and isinstance(k, (int, float)) and c.get("loop_inputs", 0) > prev_total * k + 1:
            errs.append(f"projection.cohorts[{i}]: loop_inputs {c.get('loop_inputs')} exceed the previous total {prev_total} times k {k}; the projection compounds faster than the loop (r-steady-state-projection-90-days)")
        prev_total = c.get("total_inputs")
    fm = obj.get("friction_map") or {}
    if metrics and all(isinstance(m.get("value"), (int, float)) for m in metrics):
        low = min(metrics, key=lambda m: m["value"])
        if fm.get("bottleneck_stage") != low["transition"]:
            errs.append(f"friction_map.bottleneck_stage must be the lowest-value transition {low['transition']!r} at {low['value']} (r-friction-map-names-the-bottleneck)")
        if fm.get("bottleneck_value") != low["value"]:
            errs.append(f"friction_map.bottleneck_value must be {low['value']} (r-friction-map-names-the-bottleneck)")
        if isinstance(k, (int, float)) and isinstance(fm.get("k_if_doubled"), (int, float)) and abs(round(2 * k, 2) - fm["k_if_doubled"]) > 0.0051:
            errs.append(f"friction_map.k_if_doubled must be 2 x k = {round(2 * k, 2)} (r-friction-map-names-the-bottleneck)")
    exps = sorted(fm.get("experiments") or [], key=lambda e: e.get("rank", 0))
    if exps and exps[0].get("stage") != fm.get("bottleneck_stage"):
        errs.append(f"friction_map.experiments rank 1 targets {exps[0].get('stage')!r}, not the bottleneck {fm.get('bottleneck_stage')!r} (r-friction-map-names-the-bottleneck)")
    for e in exps:
        if e.get("stage") != fm.get("bottleneck_stage") and not e.get("justification"):
            errs.append(f"friction_map.experiments rank {e.get('rank')} is on a non-bottleneck stage with no justification (r-friction-map-names-the-bottleneck)")
    ranks = [e.get("rank") for e in exps]
    if ranks and ranks != list(range(1, len(ranks) + 1)):
        errs.append(f"friction_map.experiments ranks must be 1..n without gaps, got {ranks} (r-friction-map-names-the-bottleneck)")
    cp = obj.get("cac_payback") or {}
    if cp.get("attributed_by") and fb.get("event") and cp["attributed_by"] != fb["event"]:
        errs.append(f"cac_payback.attributed_by {cp['attributed_by']!r} is not the fuel-back event {fb['event']!r}; organic or direct traffic is not loop output (r-cac-payback-with-and-without-loop)")
    qg = obj.get("quality_guardrail") or {}
    if isinstance(qg.get("threshold"), (int, float)) and isinstance(qg.get("loop_cohort_value"), (int, float)):
        want = "within" if qg["loop_cohort_value"] >= qg["threshold"] else "breached"
        if qg.get("status") != want:
            errs.append(f"quality_guardrail.status must be {want!r}: loop_cohort_value {qg['loop_cohort_value']} against threshold {qg['threshold']} (r-loop-quality-guardrail)")
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
        prog="validate-growth-loops.py",
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
