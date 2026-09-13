#!/usr/bin/env python3
"""validate-activation-metrics.py

Validate the artefact produced by the activation-metrics methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/activation-metrics.json',
 'title': 'Activation Metrics report',
 'type': 'object',
 'required': ['activation_event',
              'window_days',
              'period_start',
              'period_end',
              'data_cutoff',
              'signups_total',
              'sample_floor',
              'channel_attribution',
              'metrics',
              'time_to_activation',
              'funnel',
              'findings'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'snake': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1},
                 'period': {'type': 'object',
                            'required': ['start', 'end'],
                            'additionalProperties': False,
                            'properties': {'start': {'$ref': '#/definitions/date'},
                                           'end': {'$ref': '#/definitions/date'}}},
                 'group': {'type': 'object',
                           'required': ['users', 'd30_retention'],
                           'additionalProperties': False,
                           'properties': {'users': {'type': 'integer', 'minimum': 1},
                                          'd30_retention': {'$ref': '#/definitions/rate'}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'activation_event': {'$ref': '#/definitions/snake'},
                'window_days': {'type': 'integer', 'minimum': 1},
                'period_start': {'$ref': '#/definitions/date'},
                'period_end': {'$ref': '#/definitions/date'},
                'data_cutoff': {'$ref': '#/definitions/date'},
                'previous_period': {'$ref': '#/definitions/period'},
                'signups_total': {'type': 'integer', 'minimum': 1},
                'sample_floor': {'type': 'integer', 'minimum': 1},
                'channel_attribution': {'type': 'boolean'},
                'metrics': {'type': 'array',
                            'minItems': 1,
                            'contains': {'properties': {'name': {'const': 'activation_rate'}},
                                         'required': ['numerator', 'denominator']},
                            'items': {'type': 'object',
                                      'required': ['name', 'value', 'unit'],
                                      'additionalProperties': False,
                                      'properties': {'name': {'$ref': '#/definitions/snake'},
                                                     'value': {'type': 'number'},
                                                     'unit': {'type': 'string',
                                                              'enum': ['ratio',
                                                                       'count',
                                                                       'days',
                                                                       'hours',
                                                                       'pp']},
                                                     'numerator': {'type': 'integer', 'minimum': 0},
                                                     'denominator': {'type': 'integer',
                                                                     'minimum': 1},
                                                     'low_sample': {'type': 'boolean'}},
                                      'if': {'properties': {'unit': {'const': 'ratio'}}},
                                      'then': {'properties': {'value': {'$ref': '#/definitions/rate'}}}}},
                'time_to_activation': {'type': 'object',
                                       'required': ['unit', 'median'],
                                       'anyOf': [{'required': ['p75']}, {'required': ['p90']}],
                                       'additionalProperties': False,
                                       'properties': {'unit': {'type': 'string',
                                                               'enum': ['hours', 'days']},
                                                      'median': {'type': 'number', 'minimum': 0},
                                                      'p75': {'type': 'number', 'minimum': 0},
                                                      'p90': {'type': 'number', 'minimum': 0},
                                                      'mean': {'type': 'number', 'minimum': 0}}},
                'd30_lift': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'object',
                                       'required': ['event',
                                                    'cohort_signup_start',
                                                    'cohort_signup_end',
                                                    'performed',
                                                    'not_performed',
                                                    'wording'],
                                       'additionalProperties': False,
                                       'properties': {'event': {'$ref': '#/definitions/snake'},
                                                      'cohort_signup_start': {'$ref': '#/definitions/date'},
                                                      'cohort_signup_end': {'$ref': '#/definitions/date'},
                                                      'performed': {'$ref': '#/definitions/group'},
                                                      'not_performed': {'$ref': '#/definitions/group'},
                                                      'wording': {'const': 'correlation'}}}},
                'funnel': {'type': 'array',
                           'minItems': 2,
                           'items': {'type': 'object',
                                     'required': ['name', 'status'],
                                     'properties': {'name': {'type': 'string', 'minLength': 2},
                                                    'status': {'type': 'string',
                                                               'enum': ['instrumented',
                                                                        'uninstrumented']}},
                                     'if': {'properties': {'status': {'const': 'instrumented'}}},
                                     'then': {'required': ['event',
                                                           'entering',
                                                           'completing',
                                                           'absolute_drop',
                                                           'relative_drop'],
                                              'additionalProperties': False,
                                              'properties': {'name': {'type': 'string'},
                                                             'status': {'const': 'instrumented'},
                                                             'event': {'$ref': '#/definitions/snake'},
                                                             'entering': {'type': 'integer',
                                                                          'minimum': 0},
                                                             'completing': {'type': 'integer',
                                                                            'minimum': 0},
                                                             'absolute_drop': {'type': 'integer',
                                                                               'minimum': 0},
                                                             'relative_drop': {'$ref': '#/definitions/rate'}}},
                                     'else': {'required': ['instrumentation_task'],
                                              'additionalProperties': False,
                                              'properties': {'name': {'type': 'string'},
                                                             'status': {'const': 'uninstrumented'},
                                                             'instrumentation_task': {'type': 'string',
                                                                                      'minLength': 8}}}}},
                'findings': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'object',
                                       'required': ['metric', 'text', 'compared_to', 'causal'],
                                       'additionalProperties': False,
                                       'properties': {'metric': {'$ref': '#/definitions/snake'},
                                                      'text': {'type': 'string', 'minLength': 20},
                                                      'compared_to': {'$ref': '#/definitions/period'},
                                                      'causal': {'type': 'boolean'},
                                                      'product_change': {'type': 'object',
                                                                         'required': ['name',
                                                                                      'released_at'],
                                                                         'additionalProperties': False,
                                                                         'properties': {'name': {'type': 'string',
                                                                                                 'minLength': 3},
                                                                                        'released_at': {'$ref': '#/definitions/date'},
                                                                                        'ab_test_result': {'type': 'string',
                                                                                                           'minLength': 10}}}},
                                       'if': {'properties': {'causal': {'const': True}}},
                                       'then': {'required': ['product_change'],
                                                'properties': {'product_change': {'required': ['ab_test_result']}}}}}}}

OK = {'activation_event': 'project_created',
 'window_days': 7,
 'period_start': '2026-04-06',
 'period_end': '2026-04-26',
 'data_cutoff': '2026-05-04',
 'previous_period': {'start': '2026-03-16', 'end': '2026-04-05'},
 'signups_total': 5335,
 'sample_floor': 100,
 'channel_attribution': True,
 'metrics': [{'name': 'signups', 'value': 5335, 'unit': 'count'},
             {'name': 'activation_rate',
              'value': 0.223,
              'unit': 'ratio',
              'numerator': 1192,
              'denominator': 5335},
             {'name': 'activation_rate__organic',
              'value': 0.269,
              'unit': 'ratio',
              'numerator': 702,
              'denominator': 2610},
             {'name': 'activation_rate__paid_search',
              'value': 0.181,
              'unit': 'ratio',
              'numerator': 401,
              'denominator': 2210},
             {'name': 'activation_rate__partner',
              'value': 0.165,
              'unit': 'ratio',
              'numerator': 75,
              'denominator': 454},
             {'name': 'activation_rate__referral',
              'value': 0.23,
              'unit': 'ratio',
              'numerator': 14,
              'denominator': 61,
              'low_sample': True},
             {'name': 'activation_rate_wow_delta', 'value': -0.4, 'unit': 'pp'},
             {'name': 'activation_rate_partial',
              'value': 0.17,
              'unit': 'ratio',
              'numerator': 290,
              'denominator': 1701}],
 'time_to_activation': {'unit': 'hours', 'median': 1.4, 'p75': 26.0, 'p90': 88.5},
 'd30_lift': [{'event': 'project_created',
               'cohort_signup_start': '2026-03-02',
               'cohort_signup_end': '2026-03-08',
               'performed': {'users': 412, 'd30_retention': 0.46},
               'not_performed': {'users': 1388, 'd30_retention': 0.11},
               'wording': 'correlation'}],
 'funnel': [{'name': 'signup',
             'status': 'instrumented',
             'event': 'signup_completed',
             'entering': 5335,
             'completing': 5335,
             'absolute_drop': 0,
             'relative_drop': 0},
            {'name': 'email verified',
             'status': 'instrumented',
             'event': 'email_verified',
             'entering': 5335,
             'completing': 3895,
             'absolute_drop': 1440,
             'relative_drop': 0.27},
            {'name': 'workspace named',
             'status': 'instrumented',
             'event': 'workspace_named',
             'entering': 3895,
             'completing': 3661,
             'absolute_drop': 234,
             'relative_drop': 0.06},
            {'name': 'template picked',
             'status': 'uninstrumented',
             'instrumentation_task': 'GROW-118: emit template_picked from the onboarding modal'},
            {'name': 'project created',
             'status': 'instrumented',
             'event': 'project_created',
             'entering': 3661,
             'completing': 1192,
             'absolute_drop': 2469,
             'relative_drop': 0.674}],
 'findings': [{'metric': 'activation_rate',
               'text': 'activation_rate 0.223 for signups 2026-04-06 to 2026-04-26 against 0.227 '
                       'for 2026-03-16 to 2026-04-05, a -0.4 pp change inside week-to-week noise.',
               'compared_to': {'start': '2026-03-16', 'end': '2026-04-05'},
               'causal': False},
              {'metric': 'activation_rate__paid_search',
               'text': 'activation_rate__paid_search 0.181 against activation_rate__organic 0.269; '
                       'paid search rose from 33 to 41 percent of signups versus 2026-03-16 to '
                       '2026-04-05, which accounts for the aggregate dip. Onboarding checklist v2 '
                       'released 2026-04-13 shows no separable effect.',
               'compared_to': {'start': '2026-03-16', 'end': '2026-04-05'},
               'causal': False,
               'product_change': {'name': 'onboarding checklist v2', 'released_at': '2026-04-13'}},
              {'metric': 'activation_rate__referral',
               'text': 'activation_rate__referral is low_sample (61 signups against a floor of '
                       '100) and is not compared with 2026-03-16 to 2026-04-05.',
               'compared_to': {'start': '2026-03-16', 'end': '2026-04-05'},
               'causal': False}]}

BAD = {'activation_event': 'project_created',
 'window_days': 7,
 'period_start': '2026-04-06',
 'period_end': '2026-05-03',
 'data_cutoff': '2026-05-04',
 'signups_total': 7036,
 'sample_floor': 100,
 'channel_attribution': True,
 'metrics': [{'name': 'activation_rate',
              'value': 31,
              'unit': 'percent',
              'numerator': 1482,
              'denominator': 4780},
             {'name': 'activation_rate__referral',
              'value': 0.23,
              'unit': 'ratio',
              'numerator': 14,
              'denominator': 61}],
 'time_to_activation': {'unit': 'days', 'mean': 6.4},
 'd30_lift': [{'event': 'invite_sent',
               'cohort_signup_start': '2026-04-20',
               'cohort_signup_end': '2026-04-26',
               'performed': {'users': 120, 'd30_retention': 0.51},
               'not_performed': {'users': 1568, 'd30_retention': 0.17},
               'wording': 'correlation'}],
 'funnel': [{'name': 'signup',
             'status': 'instrumented',
             'event': 'signup_completed',
             'entering': 7036,
             'completing': 7036,
             'absolute_drop': 0,
             'relative_drop': 0},
            {'name': 'template picked',
             'status': 'uninstrumented',
             'instrumentation_task': 'GROW-118: emit template_picked',
             'entering': 4780,
             'completing': 3200},
            {'name': 'project created',
             'status': 'instrumented',
             'event': 'project_created',
             'entering': 3200,
             'completing': 1482,
             'absolute_drop': 1600,
             'relative_drop': 0.5}],
 'findings': [{'metric': 'activation_rate',
               'text': 'Activation improved thanks to the new onboarding checklist.',
               'compared_to': {'start': '2026-03-16', 'end': '2026-04-05'},
               'causal': True,
               'product_change': {'name': 'onboarding checklist v2', 'released_at': '2026-04-13'}}]}


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

from datetime import date, timedelta


def _d(s: str) -> date | None:
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    window = obj.get("window_days") or 0
    cutoff = _d(obj.get("data_cutoff", ""))
    pe, ps = _d(obj.get("period_end", "")), _d(obj.get("period_start", ""))
    if ps and pe and ps > pe:
        errs.append("period_start is after period_end (r-one-fixed-window-closed-cohorts-only)")
    if pe and cutoff and pe + timedelta(days=window) > cutoff:
        errs.append(f"period_end + window_days = {pe + timedelta(days=window)} is after data_cutoff {cutoff}: the period contains an open cohort (r-one-fixed-window-closed-cohorts-only)")
    metrics = [m for m in obj.get("metrics") or [] if isinstance(m, dict)]
    names = {m.get("name") for m in metrics}
    floor = obj.get("sample_floor") or 0
    for i, m in enumerate(metrics):
        if m.get("name") == "activation_rate" and m.get("denominator") != obj.get("signups_total"):
            errs.append(f"metrics[{i}]: activation_rate.denominator {m.get('denominator')} must equal signups_total {obj.get('signups_total')} (r-activation-rate-denominator-is-signups)")
        if m.get("unit") == "ratio" and m.get("denominator") and m.get("numerator") is not None:
            want = round(m["numerator"] / m["denominator"], 3)
            if abs(want - m.get("value", -1)) > 0.0005:
                errs.append(f"metrics[{i}]: {m.get('name')} value must be numerator / denominator = {want} (r-metric-naming-and-units)")
        if str(m.get("name", "")).startswith("activation_rate__") and m.get("denominator") is not None and m["denominator"] < floor and m.get("low_sample") is not True:
            errs.append(f"metrics[{i}]: {m.get('name')} has {m['denominator']} signups, below sample_floor {floor}, and is not flagged low_sample (r-segment-by-acquisition-channel)")
        if m.get("unit") == "pp" and not obj.get("previous_period"):
            errs.append(f"metrics[{i}]: a pp delta requires previous_period (r-metric-naming-and-units)")
    if obj.get("channel_attribution") is True and not any(n.startswith("activation_rate__") for n in names if isinstance(n, str)):
        errs.append("channel_attribution is true but no activation_rate__<channel> metric is present (r-segment-by-acquisition-channel)")
    for i, d in enumerate(obj.get("d30_lift") or []):
        end = _d(d.get("cohort_signup_end", ""))
        if end and cutoff and end + timedelta(days=30) > cutoff:
            errs.append(f"d30_lift[{i}]: cohort_signup_end + 30 days = {end + timedelta(days=30)} is after data_cutoff; the cohort has no D30 yet (r-d30-lift-table-with-sizes)")
    for i, s in enumerate(obj.get("funnel") or []):
        if s.get("status") != "instrumented":
            continue
        ent, comp = s.get("entering", 0), s.get("completing", 0)
        if comp > ent:
            errs.append(f"funnel[{i}]: completing exceeds entering (r-funnel-steps-absolute-and-relative)")
        if s.get("absolute_drop") != ent - comp:
            errs.append(f"funnel[{i}]: absolute_drop must be entering - completing = {ent - comp} (r-funnel-steps-absolute-and-relative)")
        if ent and abs(round((ent - comp) / ent, 3) - s.get("relative_drop", -1)) > 0.0005:
            errs.append(f"funnel[{i}]: relative_drop must be absolute_drop / entering = {round((ent - comp) / ent, 3)} (r-funnel-steps-absolute-and-relative)")
    for i, f in enumerate(obj.get("findings") or []):
        if f.get("metric") not in names:
            errs.append(f"findings[{i}]: metric {f.get('metric')!r} is not a metrics[].name in this report (r-findings-cite-metric-and-period)")
        if f.get("metric") and f.get("metric") not in str(f.get("text", "")):
            errs.append(f"findings[{i}]: text does not mention its metric {f.get('metric')!r} (r-findings-cite-metric-and-period)")
        cmp = f.get("compared_to") or {}
        if cmp.get("start") and cmp["start"] not in str(f.get("text", "")) and cmp.get("end", "") not in str(f.get("text", "")):
            errs.append(f"findings[{i}]: text does not name the comparison period {cmp.get('start')} to {cmp.get('end')} (r-findings-cite-metric-and-period)")
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
        prog="validate-activation-metrics.py",
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
