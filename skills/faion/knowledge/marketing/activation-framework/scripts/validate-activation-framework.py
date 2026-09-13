#!/usr/bin/env python3
"""validate-activation-framework.py

Validate the artefact produced by the activation-framework methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/activation-framework.json',
 'title': 'Activation Framework spec',
 'type': 'object',
 'required': ['activation_event',
              'd30_validation',
              'baseline',
              'funnel',
              'dropoff_priorities',
              'experiments',
              'dashboard'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'event_name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1},
                 'score': {'type': 'integer', 'minimum': 1, 'maximum': 10},
                 'group': {'type': 'object',
                           'required': ['users', 'd30_retention'],
                           'additionalProperties': False,
                           'properties': {'users': {'type': 'integer', 'minimum': 1},
                                          'd30_retention': {'$ref': '#/definitions/rate'}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'activation_event': {'type': 'object',
                                     'required': ['name', 'window_days'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'$ref': '#/definitions/event_name'},
                                                    'window_days': {'type': 'integer',
                                                                    'minimum': 1}}},
                'd30_validation': {'type': 'object',
                                   'required': ['cohort',
                                                'performed',
                                                'not_performed',
                                                'correlational_note'],
                                   'additionalProperties': False,
                                   'properties': {'cohort': {'type': 'string', 'minLength': 4},
                                                  'performed': {'$ref': '#/definitions/group'},
                                                  'not_performed': {'$ref': '#/definitions/group'},
                                                  'correlational_note': {'const': True}}},
                'baseline': {'type': 'object',
                             'required': ['data_cutoff', 'cohorts'],
                             'additionalProperties': False,
                             'properties': {'data_cutoff': {'$ref': '#/definitions/date'},
                                            'cohorts': {'type': 'array',
                                                        'minItems': 4,
                                                        'items': {'type': 'object',
                                                                  'required': ['signup_week_start',
                                                                               'signups',
                                                                               'activated',
                                                                               'activation_rate'],
                                                                  'additionalProperties': False,
                                                                  'properties': {'signup_week_start': {'$ref': '#/definitions/date'},
                                                                                 'signups': {'type': 'integer',
                                                                                             'minimum': 1},
                                                                                 'activated': {'type': 'integer',
                                                                                               'minimum': 0},
                                                                                 'activation_rate': {'$ref': '#/definitions/rate'}}}}}},
                'funnel': {'type': 'array',
                           'minItems': 1,
                           'items': {'type': 'object',
                                     'required': ['name', 'status'],
                                     'properties': {'name': {'type': 'string', 'minLength': 2},
                                                    'status': {'type': 'string',
                                                               'enum': ['instrumented',
                                                                        'uninstrumented']}},
                                     'if': {'properties': {'status': {'const': 'instrumented'}}},
                                     'then': {'required': ['event', 'entered', 'completed'],
                                              'additionalProperties': False,
                                              'properties': {'name': {'type': 'string'},
                                                             'status': {'const': 'instrumented'},
                                                             'event': {'$ref': '#/definitions/event_name'},
                                                             'entered': {'type': 'integer',
                                                                         'minimum': 0},
                                                             'completed': {'type': 'integer',
                                                                           'minimum': 0}}},
                                     'else': {'required': ['instrumentation_task'],
                                              'additionalProperties': False,
                                              'properties': {'name': {'type': 'string'},
                                                             'status': {'const': 'uninstrumented'},
                                                             'instrumentation_task': {'type': 'string',
                                                                                      'minLength': 8}}}}},
                'dropoff_priorities': {'type': 'array',
                                       'minItems': 1,
                                       'items': {'type': 'object',
                                                 'required': ['step',
                                                              'users_lost',
                                                              'relative_drop'],
                                                 'additionalProperties': False,
                                                 'properties': {'step': {'type': 'string',
                                                                         'minLength': 2},
                                                                'users_lost': {'type': 'integer',
                                                                               'minimum': 0},
                                                                'relative_drop': {'$ref': '#/definitions/rate'}}}},
                'experiments': {'type': 'array',
                                'minItems': 1,
                                'items': {'type': 'object',
                                          'required': ['name',
                                                       'funnel_step',
                                                       'hypothesis',
                                                       'primary_metric',
                                                       'baseline_value',
                                                       'ship_threshold_lift',
                                                       'impact',
                                                       'confidence',
                                                       'ease',
                                                       'ice'],
                                          'additionalProperties': False,
                                          'properties': {'name': {'type': 'string', 'minLength': 3},
                                                         'funnel_step': {'type': 'string',
                                                                         'minLength': 2},
                                                         'hypothesis': {'type': 'string',
                                                                        'minLength': 20},
                                                         'primary_metric': {'type': 'string',
                                                                            'enum': ['activation_rate',
                                                                                     'step_conversion']},
                                                         'baseline_value': {'$ref': '#/definitions/rate'},
                                                         'ship_threshold_lift': {'type': 'number',
                                                                                 'exclusiveMinimum': 0,
                                                                                 'maximum': 1},
                                                         'impact': {'$ref': '#/definitions/score'},
                                                         'confidence': {'$ref': '#/definitions/score'},
                                                         'ease': {'$ref': '#/definitions/score'},
                                                         'ice': {'type': 'number',
                                                                 'minimum': 1,
                                                                 'maximum': 10}}}},
                'dashboard': {'type': 'object',
                              'required': ['cadence',
                                           'closed_cohorts_only',
                                           'window_days',
                                           'segment_by',
                                           'series_id'],
                              'additionalProperties': False,
                              'properties': {'cadence': {'const': 'weekly'},
                                             'closed_cohorts_only': {'const': True},
                                             'window_days': {'type': 'integer', 'minimum': 1},
                                             'segment_by': {'type': 'array',
                                                            'minItems': 1,
                                                            'items': {'type': 'string'},
                                                            'contains': {'const': 'acquisition_channel'}},
                                             'series_id': {'type': 'string', 'minLength': 3}}}}}

OK = {'activation_event': {'name': 'project_created', 'window_days': 7},
 'd30_validation': {'cohort': 'signup week 2026-03-02',
                    'performed': {'users': 412, 'd30_retention': 0.46},
                    'not_performed': {'users': 1388, 'd30_retention': 0.11},
                    'correlational_note': True},
 'baseline': {'data_cutoff': '2026-05-04',
              'cohorts': [{'signup_week_start': '2026-03-30',
                           'signups': 1810,
                           'activated': 407,
                           'activation_rate': 0.225},
                          {'signup_week_start': '2026-04-06',
                           'signups': 1742,
                           'activated': 383,
                           'activation_rate': 0.22},
                          {'signup_week_start': '2026-04-13',
                           'signups': 1905,
                           'activated': 438,
                           'activation_rate': 0.23},
                          {'signup_week_start': '2026-04-20',
                           'signups': 1688,
                           'activated': 371,
                           'activation_rate': 0.22}]},
 'funnel': [{'name': 'signup',
             'status': 'instrumented',
             'event': 'signup_completed',
             'entered': 7145,
             'completed': 7145},
            {'name': 'email verified',
             'status': 'instrumented',
             'event': 'email_verified',
             'entered': 7145,
             'completed': 5216},
            {'name': 'workspace named',
             'status': 'instrumented',
             'event': 'workspace_named',
             'entered': 5216,
             'completed': 4903},
            {'name': 'template picked',
             'status': 'uninstrumented',
             'instrumentation_task': 'GROW-118: emit template_picked from the onboarding modal'},
            {'name': 'project created',
             'status': 'instrumented',
             'event': 'project_created',
             'entered': 4903,
             'completed': 1599}],
 'dropoff_priorities': [{'step': 'project created', 'users_lost': 3304, 'relative_drop': 0.674},
                        {'step': 'email verified', 'users_lost': 1929, 'relative_drop': 0.27},
                        {'step': 'workspace named', 'users_lost': 313, 'relative_drop': 0.06}],
 'experiments': [{'name': 'Sample project on first login',
                  'funnel_step': 'project created',
                  'hypothesis': 'Users who land in a pre-filled sample project create their own '
                                'within the window because the empty state is the blocker.',
                  'primary_metric': 'activation_rate',
                  'baseline_value': 0.224,
                  'ship_threshold_lift': 0.03,
                  'impact': 8,
                  'confidence': 7,
                  'ease': 8,
                  'ice': 7.67},
                 {'name': 'Magic-link instead of verification code',
                  'funnel_step': 'email verified',
                  'hypothesis': 'A one-click magic link removes the code-entry step where 27 '
                                'percent of signups stop.',
                  'primary_metric': 'step_conversion',
                  'baseline_value': 0.73,
                  'ship_threshold_lift': 0.05,
                  'impact': 7,
                  'confidence': 8,
                  'ease': 6,
                  'ice': 7.0}],
 'dashboard': {'cadence': 'weekly',
               'closed_cohorts_only': True,
               'window_days': 7,
               'segment_by': ['acquisition_channel'],
               'series_id': 'activation-project_created-7d-v1'}}

BAD = {'activation_event': {'name': 'user sees value or invites a teammate', 'window_days': 7},
 'd30_validation': {'cohort': 'signup week 2026-03-02',
                    'performed': {'users': 412, 'd30_retention': 0.11},
                    'not_performed': {'users': 1388, 'd30_retention': 0.11},
                    'correlational_note': True},
 'baseline': {'data_cutoff': '2026-05-04',
              'cohorts': [{'signup_week_start': '2026-04-20',
                           'signups': 1688,
                           'activated': 371,
                           'activation_rate': 0.22},
                          {'signup_week_start': '2026-04-27',
                           'signups': 1701,
                           'activated': 290,
                           'activation_rate': 0.17}]},
 'funnel': [{'name': 'signup',
             'status': 'instrumented',
             'event': 'signup_completed',
             'entered': 3389,
             'completed': 3389},
            {'name': 'template picked',
             'status': 'uninstrumented',
             'instrumentation_task': 'GROW-118: emit template_picked',
             'entered': 2400,
             'completed': 1800},
            {'name': 'project created',
             'status': 'instrumented',
             'event': 'project_created',
             'entered': 1800,
             'completed': 661}],
 'dropoff_priorities': [{'step': 'template picked', 'users_lost': 600, 'relative_drop': 0.25},
                        {'step': 'project created', 'users_lost': 1139, 'relative_drop': 0.633}],
 'experiments': [{'name': 'Better onboarding',
                  'funnel_step': 'project created',
                  'hypothesis': 'Improving onboarding will raise activation.',
                  'primary_metric': 'activation_rate',
                  'baseline_value': 0.2,
                  'ship_threshold_lift': 0.02,
                  'impact': 7.5,
                  'confidence': 12,
                  'ease': 4,
                  'ice': 9.1}],
 'dashboard': {'cadence': 'weekly',
               'closed_cohorts_only': False,
               'window_days': 14,
               'segment_by': ['plan'],
               'series_id': 'activation-v1'}}


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
    ev = obj.get("activation_event") or {}
    window = ev.get("window_days")
    d30 = obj.get("d30_validation") or {}
    p, n = d30.get("performed") or {}, d30.get("not_performed") or {}
    if p.get("d30_retention") is not None and n.get("d30_retention") is not None and p["d30_retention"] <= n["d30_retention"]:
        errs.append("d30_validation: performed.d30_retention is not above not_performed.d30_retention; the event does not predict retention (r-event-validated-against-d30-retention)")
    base = obj.get("baseline") or {}
    cutoff = _d(base.get("data_cutoff", ""))
    for i, c in enumerate(base.get("cohorts") or []):
        start = _d(c.get("signup_week_start", ""))
        if start and cutoff and window is not None and start + timedelta(days=6 + window) >= cutoff:
            errs.append(f"baseline.cohorts[{i}]: open cohort, week end {start + timedelta(days=6)} + {window} days is not before data_cutoff {cutoff} (r-baseline-before-experiments)")
        if c.get("signups") and c.get("activated") is not None and abs(round(c["activated"] / c["signups"], 3) - c.get("activation_rate", -1)) > 0.0005:
            errs.append(f"baseline.cohorts[{i}]: activation_rate must be activated / signups = {round(c['activated'] / c['signups'], 3)} (r-baseline-before-experiments)")
    steps = {s.get("name"): s for s in obj.get("funnel") or [] if isinstance(s, dict)}
    for i, s in enumerate(obj.get("funnel") or []):
        if s.get("status") == "instrumented" and s.get("completed", 0) > s.get("entered", 0):
            errs.append(f"funnel[{i}]: completed exceeds entered (r-funnel-steps-map-to-events)")
    prev = None
    for i, d in enumerate(obj.get("dropoff_priorities") or []):
        s = steps.get(d.get("step"))
        if not s or s.get("status") != "instrumented":
            errs.append(f"dropoff_priorities[{i}]: step {d.get('step')!r} is not an instrumented funnel step (r-funnel-steps-map-to-events)")
        else:
            lost = s["entered"] - s["completed"]
            if d.get("users_lost") != lost:
                errs.append(f"dropoff_priorities[{i}]: users_lost must be entered - completed = {lost} (r-dropoffs-ranked-by-absolute-loss)")
            if s["entered"] and abs(round(lost / s["entered"], 3) - d.get("relative_drop", -1)) > 0.0005:
                errs.append(f"dropoff_priorities[{i}]: relative_drop must be users_lost / entered = {round(lost / s['entered'], 3)} (r-dropoffs-ranked-by-absolute-loss)")
        if prev is not None and d.get("users_lost", 0) > prev:
            errs.append(f"dropoff_priorities[{i}]: not sorted by users_lost descending (r-dropoffs-ranked-by-absolute-loss)")
        prev = d.get("users_lost", 0)
    prev_ice = None
    for i, x in enumerate(obj.get("experiments") or []):
        want = round((x.get("impact", 0) + x.get("confidence", 0) + x.get("ease", 0)) / 3, 2)
        if abs(x.get("ice", -1) - want) > 0.005:
            errs.append(f"experiments[{i}]: ice must be round((impact + confidence + ease) / 3, 2) = {want} as templates/ice.py computes (r-ice-integer-scale-and-formula)")
        if prev_ice is not None and x.get("ice", 0) > prev_ice:
            errs.append(f"experiments[{i}]: backlog not sorted by ice descending (r-ice-integer-scale-and-formula)")
        prev_ice = x.get("ice", 0)
        if x.get("funnel_step") not in steps:
            errs.append(f"experiments[{i}]: funnel_step {x.get('funnel_step')!r} is not a step in funnel[] (r-experiment-names-step-metric-threshold)")
    dash = obj.get("dashboard") or {}
    if window is not None and dash.get("window_days") != window:
        errs.append(f"dashboard.window_days {dash.get('window_days')} differs from activation_event.window_days {window} (r-dashboard-reports-closed-cohorts-weekly)")
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
        prog="validate-activation-framework.py",
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
